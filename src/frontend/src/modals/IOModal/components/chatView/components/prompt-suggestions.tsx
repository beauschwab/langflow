import ForwardedIconComponent from "@/components/common/genericIconComponent";
import { useUtilityStore } from "@/stores/utilityStore";
import { cn } from "@/utils/utils";

const SUGGESTED_PROMPTS = [
  {
    text: "Hello!",
    icon: "MessageCircle",
  },
  {
    text: "What can you do?",
    icon: "HelpCircle",
  },
  {
    text: "Help me get started",
    icon: "Rocket",
  },
  {
    text: "Summarize this for me",
    icon: "FileText",
  },
];

export default function PromptSuggestions() {
  const setChatValueStore = useUtilityStore(
    (state) => state.setChatValueStore,
  );

  return (
    <div
      className="mt-4 grid grid-cols-2 gap-2"
      data-testid="prompt-suggestions"
    >
      {SUGGESTED_PROMPTS.map((prompt) => (
        <button
          key={prompt.text}
          className={cn(
            "flex items-center gap-2 rounded-lg border border-border bg-background px-4 py-3",
            "text-left text-sm text-muted-foreground",
            "transition-colors hover:border-primary hover:bg-muted hover:text-foreground",
          )}
          onClick={() => setChatValueStore(prompt.text)}
          data-testid={`prompt-suggestion-${prompt.text.toLowerCase().replace(/\s+/g, "-")}`}
        >
          <ForwardedIconComponent
            name={prompt.icon}
            className="h-4 w-4 flex-shrink-0"
          />
          <span className="truncate">{prompt.text}</span>
        </button>
      ))}
    </div>
  );
}
