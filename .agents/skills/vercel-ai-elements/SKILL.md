---
name: vercel-ai-elements
description: Build AI-native chat UIs with Vercel AI Elements — prebuilt, composable React components for conversations, messages, prompt inputs, code blocks, and reasoning displays. Use when implementing chat interfaces, AI streaming UIs, or any AI SDK-powered frontend.
---

# Vercel AI Elements

Build production-ready AI-native interfaces with prebuilt, customizable React components from the Vercel AI Elements library.

## Overview

[AI Elements](https://github.com/vercel/ai-elements) is a component library built on top of [shadcn/ui](https://ui.shadcn.com/) that provides pre-built, composable React components specifically designed for AI applications. Components handle conversations, streaming messages, prompt inputs, code blocks, reasoning displays, and more — all wired to work seamlessly with the Vercel AI SDK.

**Key Strengths:**
- **AI SDK native**: Integrates directly with `useChat`, `useCompletion`, and other AI SDK hooks
- **Streaming-ready**: Handles incremental renders, loading states, and real-time updates out of the box
- **Built on shadcn/ui**: Fully customizable, installed locally into your codebase, styled with Tailwind CSS
- **Composable**: Mix, match, and extend components for any AI workflow

## When to Use This Skill

- Building chat interfaces with streaming AI responses
- Implementing copilot-style UIs or agent interfaces
- Displaying LLM reasoning, tool calls, or chain-of-thought
- Adding prompt input boxes with auto-resize and attachment support
- Rendering AI-generated code with syntax highlighting
- Showing inline citations or RAG sources alongside responses

## Do Not Use This Skill When

- Your project doesn't use the Vercel AI SDK
- You're not using React/Next.js
- You need a backend-only solution (no UI components involved)
- Your project doesn't have shadcn/ui and Tailwind CSS configured

---

## Prerequisites

Before using AI Elements, ensure your project has:

- **Node.js** 18 or later
- **Next.js** project with the [AI SDK](https://ai-sdk.dev/) installed
- **shadcn/ui** initialized (`npx shadcn@latest init`)
- **Tailwind CSS** configured in CSS Variables mode

---

## Installation

### Install All Components at Once

```bash
npx ai-elements@latest
```

This will:
1. Set up shadcn/ui if not already configured
2. Install all AI Elements components to your `components/ai-elements/` directory
3. Add necessary npm dependencies

### Install Specific Components

```bash
npx ai-elements@latest add <component-name>

# Examples
npx ai-elements@latest add message
npx ai-elements@latest add conversation
npx ai-elements@latest add code-block
npx ai-elements@latest add prompt-input
```

### Alternative: Install via shadcn CLI

```bash
# Install all components
npx shadcn@latest add https://elements.ai-sdk.dev/api/registry/all.json

# Install a specific component
npx shadcn@latest add https://elements.ai-sdk.dev/api/registry/message.json
```

---

## Quick Start

After installing components, wire them to the AI SDK `useChat` hook:

```tsx
"use client";

import { useChat } from "@ai-sdk/react";
import {
  Conversation,
  ConversationContent,
} from "@/components/ai-elements/conversation";
import {
  Message,
  MessageContent,
  MessageResponse,
} from "@/components/ai-elements/message";
import {
  PromptInput,
  PromptInputActions,
  PromptInputTextarea,
} from "@/components/ai-elements/prompt-input";

export default function Chat() {
  const { messages, input, handleInputChange, handleSubmit } = useChat();

  return (
    <Conversation>
      <ConversationContent>
        {messages.map((message, index) => (
          <Message key={index} from={message.role}>
            <MessageContent>
              <MessageResponse>{message.content}</MessageResponse>
            </MessageContent>
          </Message>
        ))}
      </ConversationContent>

      <form onSubmit={handleSubmit}>
        <PromptInput value={input} onValueChange={handleInputChange}>
          <PromptInputTextarea placeholder="Ask something..." />
          <PromptInputActions>
            <button type="submit">Send</button>
          </PromptInputActions>
        </PromptInput>
      </form>
    </Conversation>
  );
}
```

---

## Core Components Reference

### `Conversation` / `ConversationContent`

Container for the full chat session with automatic scroll management.

```tsx
import {
  Conversation,
  ConversationContent,
} from "@/components/ai-elements/conversation";

<Conversation>
  <ConversationContent>
    {/* Message list goes here */}
  </ConversationContent>
</Conversation>
```

**Key props:**
- `Conversation` — outer shell, handles sizing and layout
- `ConversationContent` — inner scroll area for the message list

---

### `Message` / `MessageContent` / `MessageResponse`

Display individual messages with role-aware styling (user vs. assistant vs. system).

```tsx
import {
  Message,
  MessageContent,
  MessageResponse,
  MessageAvatar,
} from "@/components/ai-elements/message";

<Message from="assistant">
  <MessageAvatar />
  <MessageContent>
    <MessageResponse>{message.content}</MessageResponse>
  </MessageContent>
</Message>
```

**Key props:**
- `from` — `"user"` | `"assistant"` | `"system"` — controls alignment and styling
- `MessageAvatar` — optional avatar for assistant messages
- `MessageResponse` — renders message text, handles markdown by default

---

### `PromptInput`

Advanced chat input with auto-resize textarea, submit handling, and attachment support.

```tsx
import {
  PromptInput,
  PromptInputActions,
  PromptInputTextarea,
} from "@/components/ai-elements/prompt-input";

<PromptInput value={input} onValueChange={handleInputChange}>
  <PromptInputTextarea
    placeholder="Ask me anything..."
    onKeyDown={(e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        handleSubmit();
      }
    }}
  />
  <PromptInputActions>
    <button type="submit" disabled={isLoading}>
      Send
    </button>
  </PromptInputActions>
</PromptInput>
```

**Key props:**
- `value` — controlled input value
- `onValueChange` — change handler
- `PromptInputTextarea` — auto-resizing textarea
- `PromptInputActions` — slot for buttons (send, stop, attach, etc.)

---

### `CodeBlock`

Renders AI-generated code responses with syntax highlighting and copy button.

```tsx
import { CodeBlock } from "@/components/ai-elements/code-block";

<CodeBlock language="typescript" code={codeString} />
```

**Key props:**
- `language` — syntax highlight language (e.g., `"typescript"`, `"python"`, `"bash"`)
- `code` — the code string to display
- Automatically includes a copy-to-clipboard button

---

### `Reasoning`

Visualize an LLM's chain-of-thought, tool calls, or step-by-step reasoning.

```tsx
import {
  Reasoning,
  ReasoningContent,
  ReasoningTrigger,
} from "@/components/ai-elements/reasoning";

<Reasoning>
  <ReasoningTrigger>Show reasoning</ReasoningTrigger>
  <ReasoningContent>
    {thinkingSteps.map((step, i) => (
      <p key={i}>{step}</p>
    ))}
  </ReasoningContent>
</Reasoning>
```

Use with AI SDK's `experimental_generateText` when `includeReasoning: true` is enabled.

---

## Full Chat Example with Streaming

```tsx
"use client";

import { useChat } from "@ai-sdk/react";
import {
  Conversation,
  ConversationContent,
} from "@/components/ai-elements/conversation";
import {
  Message,
  MessageContent,
  MessageResponse,
} from "@/components/ai-elements/message";
import {
  PromptInput,
  PromptInputActions,
  PromptInputTextarea,
} from "@/components/ai-elements/prompt-input";

export default function StreamingChat() {
  const { messages, input, handleInputChange, handleSubmit, isLoading, stop } =
    useChat({ api: "/api/chat" });

  return (
    <div className="flex flex-col h-screen">
      <Conversation className="flex-1">
        <ConversationContent>
          {messages.map((message) => (
            <Message key={message.id} from={message.role}>
              <MessageContent>
                <MessageResponse>{message.content}</MessageResponse>
              </MessageContent>
            </Message>
          ))}
        </ConversationContent>
      </Conversation>

      <div className="p-4 border-t">
        <form onSubmit={handleSubmit}>
          <PromptInput value={input} onValueChange={handleInputChange}>
            <PromptInputTextarea
              placeholder="Type a message..."
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  handleSubmit();
                }
              }}
            />
            <PromptInputActions>
              {isLoading ? (
                <button type="button" onClick={stop}>
                  Stop
                </button>
              ) : (
                <button type="submit" disabled={!input.trim()}>
                  Send
                </button>
              )}
            </PromptInputActions>
          </PromptInput>
        </form>
      </div>
    </div>
  );
}
```

---

## Next.js API Route (AI SDK Backend)

Pair your UI with an AI SDK streaming route:

```ts
// app/api/chat/route.ts
import { openai } from "@ai-sdk/openai";
import { streamText } from "ai";

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = streamText({
    model: openai("gpt-4o"),
    messages,
  });

  return result.toDataStreamResponse();
}
```

---

## Integration with Reasoning / Tool Calls

For agents that return tool results or reasoning steps, use the structured parts API:

```tsx
{messages.map((message) => (
  <Message key={message.id} from={message.role}>
    <MessageContent>
      {message.parts?.map((part, i) => {
        if (part.type === "text") {
          return <MessageResponse key={i}>{part.text}</MessageResponse>;
        }
        if (part.type === "reasoning") {
          return (
            <Reasoning key={i}>
              <ReasoningTrigger>View reasoning</ReasoningTrigger>
              <ReasoningContent>{part.reasoning}</ReasoningContent>
            </Reasoning>
          );
        }
        if (part.type === "tool-invocation") {
          return (
            <div key={i} className="text-sm text-muted-foreground">
              Called: {part.toolInvocation.toolName}
            </div>
          );
        }
        return null;
      })}
    </MessageContent>
  </Message>
))}
```

---

## Best Practices

1. **Always wrap in a `Conversation`** — provides layout, scroll management, and consistent spacing
2. **Use `from` prop correctly** — `"user"` | `"assistant"` controls alignment and visual treatment
3. **Handle loading states** — show a loading indicator while `isLoading` is true from `useChat`
4. **Use `handleSubmit` from useChat** — never manage messages state manually
5. **Prevent double-submit** — disable the send button while `isLoading`
6. **Use `stop()` for cancellation** — wire it to a Stop button for long-running generations
7. **Install only what you need** — use `npx ai-elements@latest add <component>` to keep bundle small
8. **Customize locally** — since components are copied into your codebase, edit them freely to match your design

---

## Recommended Project Setup

```bash
# 1. Initialize shadcn/ui (if not already done)
npx shadcn@latest init

# 2. Install AI SDK
npm install ai @ai-sdk/react @ai-sdk/openai

# 3. Install AI Elements
npx ai-elements@latest

# 4. Optional: Set up Vercel AI Gateway
# Add to .env.local:
# AI_GATEWAY_API_KEY=your_key_here
```

---

## Resources

- [AI Elements GitHub](https://github.com/vercel/ai-elements)
- [AI Elements Docs](https://elements.ai-sdk.dev/)
- [Vercel AI SDK Docs](https://ai-sdk.dev/)
- [shadcn/ui](https://ui.shadcn.com/)
- [Vercel Announcement](https://vercel.com/changelog/introducing-ai-elements)
