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

export default function CreateAgentDialog({
  open,
  onClose,
}: CreateAgentDialogProps): JSX.Element {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [agentType, setAgentType] = useState("");
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
    };

    createAgent(payload, {
      onSuccess: () => {
        setSuccessData({ title: "Agent created successfully." });
        setName("");
        setDescription("");
        setAgentType("");
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
