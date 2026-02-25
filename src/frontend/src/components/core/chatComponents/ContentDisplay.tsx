import { ContentType } from "@/types/chat";
import { ReactNode } from "react";
import Markdown from "react-markdown";
import rehypeMathjax from "rehype-mathjax";
import remarkGfm from "remark-gfm";
import ForwardedIconComponent from "../../common/genericIconComponent";
import SimplifiedCodeTabComponent from "../codeTabsComponent/ChatCodeTabComponent";
import DurationDisplay from "./DurationDisplay";

export default function ContentDisplay({
  content,
  chatId,
  playgroundPage,
}: {
  content: ContentType;
  chatId: string;
  playgroundPage?: boolean;
}) {
  // First render the common BaseContent elements if they exist
  const renderHeader = content.header && (
    <>
      <div className="flex items-center gap-2 pb-[12px]">
        {content.header.icon && (
          <ForwardedIconComponent
            name={content.header.icon}
            className="h-4 w-4"
            strokeWidth={1.5}
          />
        )}
        {content.header.title && (
          <>
            <Markdown
              remarkPlugins={[remarkGfm]}
              rehypePlugins={[rehypeMathjax]}
              className="inline-block w-fit max-w-full text-[14px] font-semibold text-foreground"
            >
              {content.header.title}
            </Markdown>
          </>
        )}
      </div>
    </>
  );
  const renderDuration = content.duration !== undefined && !playgroundPage && (
    <div className="absolute right-2 top-4">
      <DurationDisplay duration={content.duration} chatId={chatId} />
    </div>
  );

  // Then render the specific content based on type
  let contentData: ReactNode | null = null;
  switch (content.type) {
    case "text":
      contentData = (
        <div className="ml-1 pr-20">
          <Markdown
            remarkPlugins={[remarkGfm]}
            linkTarget="_blank"
            rehypePlugins={[rehypeMathjax]}
            className="markdown prose max-w-full text-[14px] font-normal dark:prose-invert"
            components={{
              p({ node, ...props }) {
                return (
                  <span className="block w-fit max-w-full">
                    {props.children}
                  </span>
                );
              },
              pre({ node, ...props }) {
                return <>{props.children}</>;
              },
              code: ({ node, inline, className, children, ...props }) => {
                let content = children as string;
                if (
                  Array.isArray(children) &&
                  children.length === 1 &&
                  typeof children[0] === "string"
                ) {
                  content = children[0] as string;
                }
                if (typeof content === "string") {
                  if (content.length) {
                    if (content[0] === "▍") {
                      return <span className="form-modal-markdown-span"></span>;
                    }
                  }

                  const match = /language-(\w+)/.exec(className || "");

                  return !inline ? (
                    <SimplifiedCodeTabComponent
                      language={(match && match[1]) || ""}
                      code={String(content).replace(/\n$/, "")}
                    />
                  ) : (
                    <code className={className} {...props}>
                      {content}
                    </code>
                  );
                }
              },
            }}
          >
            {String(content.text)}
          </Markdown>
        </div>
      );
      break;

    case "code":
      contentData = (
        <div className="pr-20">
          <SimplifiedCodeTabComponent
            language={content.language}
            code={content.code}
          />
        </div>
      );
      break;

    case "json":
      contentData = (
        <div className="pr-20">
          <SimplifiedCodeTabComponent
            language="json"
            code={JSON.stringify(content.data, null, 2)}
          />
        </div>
      );
      break;

    case "error":
      contentData = (
        <div className="text-red-500">
          {content.reason && <div>Reason: {content.reason}</div>}
          {content.solution && <div>Solution: {content.solution}</div>}
          {content.traceback && (
            <SimplifiedCodeTabComponent
              language="text"
              code={content.traceback}
            />
          )}
        </div>
      );
      break;

    case "tool_use":
      // Deep agent tool-specific renderers
      if (content.name === "write_todos" && content.output) {
        // Parse todo list output into checklist items
        const todoLines = String(content.output)
          .split("\n")
          .filter((line) => line.trim());
        const hasTodoItems = todoLines.some(
          (line) => line.includes("⬜") || line.includes("🔄") || line.includes("✅"),
        );

        if (hasTodoItems) {
          contentData = (
            <div className="flex flex-col gap-1">
              {todoLines
                .filter(
                  (line) =>
                    line.includes("⬜") ||
                    line.includes("🔄") ||
                    line.includes("✅"),
                )
                .map((line, i) => (
                  <div key={i} className="flex items-center gap-2 text-[14px]">
                    <span>{line.trim()}</span>
                  </div>
                ))}
            </div>
          );
          break;
        }
      }

      if (
        (content.name === "write_context" ||
          content.name === "read_context") &&
        content.output
      ) {
        const isWrite = content.name === "write_context";
        const contextKey =
          content.tool_input?.key || (isWrite ? "unknown" : "unknown");
        contentData = (
          <div className="flex flex-col gap-1">
            <span className="text-[14px] text-muted-foreground">
              {isWrite ? "Key" : "Key"}: <strong>{contextKey}</strong>
              {isWrite &&
                content.tool_input?.value &&
                ` · ${String(content.tool_input.value).length} chars`}
            </span>
            {content.output && (
              <details className="mt-1">
                <summary className="cursor-pointer text-[13px] text-muted-foreground hover:text-foreground">
                  View value
                </summary>
                <div className="mt-1">
                  <Markdown
                    remarkPlugins={[remarkGfm]}
                    rehypePlugins={[rehypeMathjax]}
                    className="markdown prose max-w-full text-[14px] font-normal dark:prose-invert"
                  >
                    {String(content.output)}
                  </Markdown>
                </div>
              </details>
            )}
          </div>
        );
        break;
      }

      if (content.name === "delegate_task") {
        contentData = (
          <div className="flex flex-col gap-2">
            {content.tool_input?.task && (
              <div className="text-[14px]">
                <strong>Task:</strong> {String(content.tool_input.task)}
              </div>
            )}
            {content.tool_input?.context && (
              <details>
                <summary className="cursor-pointer text-[13px] text-muted-foreground hover:text-foreground">
                  Context provided
                </summary>
                <div className="mt-1 text-[14px] text-muted-foreground">
                  {String(content.tool_input.context)}
                </div>
              </details>
            )}
            {content.output && (
              <div className="mt-1 rounded-md border border-border bg-muted/50 p-3">
                <div className="mb-1 text-[12px] font-medium text-muted-foreground">
                  Sub-Agent Result
                </div>
                <Markdown
                  remarkPlugins={[remarkGfm]}
                  rehypePlugins={[rehypeMathjax]}
                  className="markdown prose max-w-full text-[14px] font-normal dark:prose-invert"
                >
                  {String(content.output)}
                </Markdown>
              </div>
            )}
            {content.error && (
              <div className="text-red-500">
                <strong>Error:</strong> {String(content.error)}
              </div>
            )}
          </div>
        );
        break;
      }

      if (content.name === "load_skill") {
        // Parse JSON output for skill loading
        let skillData: {
          skill_name?: string;
          description?: string;
          instructions?: string;
          available_files?: string[];
          error?: string;
        } | null = null;
        if (content.output && typeof content.output === "string") {
          try {
            skillData = JSON.parse(content.output);
          } catch {
            skillData = null;
          }
        }

        contentData = (
          <div className="flex flex-col gap-2">
            {content.tool_input?.skill_name && (
              <div className="flex items-center gap-2">
                <span className="inline-flex items-center rounded-md border border-border bg-muted/50 px-2 py-0.5 text-[13px] font-medium">
                  {String(content.tool_input.skill_name)}
                </span>
              </div>
            )}
            {skillData?.error && (
              <div className="text-[14px] text-red-500">
                {skillData.error}
              </div>
            )}
            {skillData?.description && (
              <div className="text-[13px] text-muted-foreground">
                {skillData.description}
              </div>
            )}
            {skillData?.instructions && (
              <details className="mt-1">
                <summary className="cursor-pointer text-[13px] text-muted-foreground hover:text-foreground">
                  View instructions ({skillData.instructions.length.toLocaleString()} chars)
                </summary>
                <div className="mt-1">
                  <Markdown
                    remarkPlugins={[remarkGfm]}
                    rehypePlugins={[rehypeMathjax]}
                    className="markdown prose max-w-full text-[14px] font-normal dark:prose-invert"
                  >
                    {skillData.instructions}
                  </Markdown>
                </div>
              </details>
            )}
            {skillData?.available_files &&
              skillData.available_files.length > 0 && (
                <div className="text-[13px] text-muted-foreground">
                  Supporting files: {skillData.available_files.join(", ")}
                </div>
              )}
          </div>
        );
        break;
      }

      if (content.name === "read_skill_file") {
        // Parse JSON output for skill file reading
        let fileData: {
          skill_name?: string;
          filename?: string;
          content?: string;
          error?: string;
        } | null = null;
        if (content.output && typeof content.output === "string") {
          try {
            fileData = JSON.parse(content.output);
          } catch {
            fileData = null;
          }
        }

        contentData = (
          <div className="flex flex-col gap-2">
            <div className="flex items-center gap-2 text-[14px]">
              {content.tool_input?.skill_name && (
                <span className="inline-flex items-center rounded-md border border-border bg-muted/50 px-2 py-0.5 text-[13px] font-medium">
                  {String(content.tool_input.skill_name)}
                </span>
              )}
              {content.tool_input?.filename && (
                <span className="text-muted-foreground">
                  / {String(content.tool_input.filename)}
                </span>
              )}
            </div>
            {fileData?.error && (
              <div className="text-[14px] text-red-500">
                {fileData.error}
              </div>
            )}
            {fileData?.content && (
              <details className="mt-1">
                <summary className="cursor-pointer text-[13px] text-muted-foreground hover:text-foreground">
                  View content ({fileData.content.length.toLocaleString()} chars)
                </summary>
                <div className="mt-1">
                  <Markdown
                    remarkPlugins={[remarkGfm]}
                    rehypePlugins={[rehypeMathjax]}
                    className="markdown prose max-w-full text-[14px] font-normal dark:prose-invert"
                  >
                    {fileData.content}
                  </Markdown>
                </div>
              </details>
            )}
          </div>
        );
        break;
      }

      if (content.name === "summarize" && content.output) {
        const inputLength = content.tool_input?.text
          ? String(content.tool_input.text).length
          : 0;
        const outputLength = String(content.output).length;
        const reduction =
          inputLength > 0
            ? Math.round((1 - outputLength / inputLength) * 100)
            : 0;

        contentData = (
          <div className="flex flex-col gap-1">
            {inputLength > 0 && (
              <span className="text-[13px] text-muted-foreground">
                {inputLength.toLocaleString()} chars → {outputLength.toLocaleString()} chars
                {reduction > 0 && ` (${reduction}% reduction)`}
              </span>
            )}
            <details className="mt-1">
              <summary className="cursor-pointer text-[13px] text-muted-foreground hover:text-foreground">
                View summary
              </summary>
              <div className="mt-1">
                <Markdown
                  remarkPlugins={[remarkGfm]}
                  rehypePlugins={[rehypeMathjax]}
                  className="markdown prose max-w-full text-[14px] font-normal dark:prose-invert"
                >
                  {String(content.output)}
                </Markdown>
              </div>
            </details>
          </div>
        );
        break;
      }

      // Default: generic tool_use rendering
      const formatToolOutput = (output: any) => {
        if (output === null || output === undefined) return "";

        // If it's a string, render as markdown
        if (typeof output === "string") {
          return (
            <Markdown
              remarkPlugins={[remarkGfm]}
              rehypePlugins={[rehypeMathjax]}
              className="markdown prose max-w-full text-[14px] font-normal dark:prose-invert"
              components={{
                pre({ node, ...props }) {
                  return <>{props.children}</>;
                },
                ol({ node, ...props }) {
                  return <ol className="max-w-full">{props.children}</ol>;
                },
                ul({ node, ...props }) {
                  return <ul className="max-w-full">{props.children}</ul>;
                },
                code: ({ node, inline, className, children, ...props }) => {
                  const match = /language-(\w+)/.exec(className || "");
                  return !inline ? (
                    <SimplifiedCodeTabComponent
                      language={(match && match[1]) || ""}
                      code={String(children).replace(/\n$/, "")}
                    />
                  ) : (
                    <code className={className} {...props}>
                      {children}
                    </code>
                  );
                },
              }}
            >
              {output}
            </Markdown>
          );
        }

        // For objects/arrays, format as JSON
        try {
          return (
            <SimplifiedCodeTabComponent
              language="json"
              code={JSON.stringify(output, null, 2)}
            />
          );
        } catch {
          return String(output);
        }
      };

      contentData = (
        <div className="flex flex-col gap-2">
          <Markdown
            remarkPlugins={[remarkGfm]}
            rehypePlugins={[rehypeMathjax]}
            className="markdown prose max-w-full text-[14px] font-normal dark:prose-invert"
          >
            **Input:**
          </Markdown>
          <SimplifiedCodeTabComponent
            language="json"
            code={JSON.stringify(content.tool_input, null, 2)}
          />
          {content.output && (
            <>
              <Markdown
                remarkPlugins={[remarkGfm]}
                rehypePlugins={[rehypeMathjax]}
                className="markdown prose max-w-full text-[14px] font-normal dark:prose-invert"
              >
                **Output:**
              </Markdown>
              <div className="mt-1">{formatToolOutput(content.output)}</div>
            </>
          )}
          {content.error && (
            <div className="text-red-500">
              <Markdown
                remarkPlugins={[remarkGfm]}
                rehypePlugins={[rehypeMathjax]}
                className="markdown prose max-w-full text-[14px] font-normal dark:prose-invert"
              >
                **Error:**
              </Markdown>
              <SimplifiedCodeTabComponent
                language="json"
                code={JSON.stringify(content.error, null, 2)}
              />
            </div>
          )}
        </div>
      );
      break;

    case "media":
      contentData = (
        <div>
          {content.urls.map((url, index) => (
            <img
              key={index}
              src={url}
              alt={content.caption || `Media ${index}`}
            />
          ))}
          {content.caption && <div>{content.caption}</div>}
        </div>
      );
      break;
  }

  return (
    <div className="relative p-[16px]">
      {renderHeader}
      {renderDuration}
      {contentData}
    </div>
  );
}
