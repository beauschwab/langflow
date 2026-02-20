import {
  Card,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { usePostAddAgent } from "@/controllers/API/queries/agents";
import useAlertStore from "@/stores/alertStore";
import { AgentCreateType } from "@/types/agents";
import { useState } from "react";

type CreateAgentDialogProps = {
  open: boolean;
  onClose: () => void;
};

const AVAILABLE_TOOLS = [
  {
    id: "SharePointFilesLoader",
    name: "SharePoint Files Loader",
    description:
      "Load files from SharePoint document libraries using Microsoft Graph.",
  },
];

export default function CreateAgentDialog({
  open,
  onClose,
}: CreateAgentDialogProps): JSX.Element {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [agentType, setAgentType] = useState("");
  const [selectedTools, setSelectedTools] = useState<string[]>([]);
  const setSuccessData = useAlertStore((state) => state.setSuccessData);
  const setErrorData = useAlertStore((state) => state.setErrorData);

  const { mutate: createAgent } = usePostAddAgent();

  const handleSubmit = () => {
    if (!name.trim()) {
      setErrorData({ title: "Agent name is required." });
      return;
    }

    const payload: AgentCreateType = {
      name: name.trim(),
      description: description.trim() || null,
      agent_type: agentType.trim() || null,
      tools: selectedTools.length ? selectedTools : null,
    };

    createAgent(payload, {
      onSuccess: () => {
        setSuccessData({ title: "Agent created successfully." });
        setName("");
        setDescription("");
        setAgentType("");
        setSelectedTools([]);
        onClose();
      },
      onError: (err: any) => {
        console.error(err);
        setErrorData({ title: "Error creating agent." });
      },
    });
  };

  return (
    <Dialog open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
      <DialogContent data-testid="create-agent-dialog">
        <DialogHeader>
          <DialogTitle>Create Agent</DialogTitle>
          <DialogDescription>
            Create a new agent to manage workflows and tools.
          </DialogDescription>
        </DialogHeader>
        <div className="flex flex-col gap-4 py-4">
          <div className="flex flex-col gap-2">
            <label className="text-sm font-medium" htmlFor="agent-name">
              Name *
            </label>
            <Input
              id="agent-name"
              data-testid="agent-name-input"
              placeholder="My Agent"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          </div>
          <div className="flex flex-col gap-2">
            <label className="text-sm font-medium" htmlFor="agent-description">
              Description
            </label>
            <Input
              id="agent-description"
              data-testid="agent-description-input"
              placeholder="Describe what this agent does..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
          </div>
          <div className="flex flex-col gap-2">
            <label className="text-sm font-medium" htmlFor="agent-type">
              Agent Type
            </label>
            <Input
              id="agent-type"
              data-testid="agent-type-input"
              placeholder="e.g., tool_calling, lc_agent"
              value={agentType}
              onChange={(e) => setAgentType(e.target.value)}
            />
          </div>
          <div className="flex flex-col gap-2">
            <label className="text-sm font-medium">Tools</label>
            <div className="grid gap-2">
              {AVAILABLE_TOOLS.map((tool) => {
                const isSelected = selectedTools.includes(tool.id);
                return (
                  <button
                    key={tool.id}
                    type="button"
                    onClick={() =>
                      setSelectedTools((prev) =>
                        prev.includes(tool.id)
                          ? prev.filter((item) => item !== tool.id)
                          : [...prev, tool.id],
                      )
                    }
                    className="text-left"
                    data-testid={`tool-card-${tool.id}`}
                    aria-label={`${isSelected ? "Deselect" : "Select"} ${tool.name} tool`}
                    aria-pressed={isSelected}
                  >
                    <Card
                      className={
                        isSelected ? "border-primary bg-primary/5" : ""
                      }
                    >
                      <CardHeader className="py-3">
                        <CardTitle className="text-sm">{tool.name}</CardTitle>
                        <CardDescription>{tool.description}</CardDescription>
                      </CardHeader>
                    </Card>
                  </button>
                );
              })}
            </div>
          </div>
        </div>
        <DialogFooter>
          <button
            className="rounded-md border px-4 py-2 text-sm hover:bg-muted"
            onClick={onClose}
          >
            Cancel
          </button>
          <button
            className="rounded-md bg-primary px-4 py-2 text-sm text-primary-foreground hover:bg-primary/90"
            onClick={handleSubmit}
            data-testid="create-agent-submit"
          >
            Create
          </button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
