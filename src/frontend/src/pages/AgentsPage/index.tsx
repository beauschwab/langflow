import { Input } from "@/components/ui/input";
import { useGetAgents } from "@/controllers/API/queries/agents";
import { useDeleteAgent } from "@/controllers/API/queries/agents";
import useAlertStore from "@/stores/alertStore";
import { AgentType } from "@/types/agents";
import { useState } from "react";
import AgentCard from "./components/AgentCard";
import CreateAgentDialog from "./components/CreateAgentDialog";

export default function AgentsPage(): JSX.Element {
  const [search, setSearch] = useState("");
  const [createDialogOpen, setCreateDialogOpen] = useState(false);

  const setSuccessData = useAlertStore((state) => state.setSuccessData);
  const setErrorData = useAlertStore((state) => state.setErrorData);

  const { data: agents, isLoading } = useGetAgents(
    { search: search || undefined },
    { refetchOnWindowFocus: false },
  );

  const { mutate: deleteAgent } = useDeleteAgent();

  const handleEdit = (agent: AgentType) => {
    // Edit functionality will use the edit dialog
    // For now, this is a placeholder
  };

  const handleDelete = (agent: AgentType) => {
    deleteAgent(
      { id: agent.id },
      {
        onSuccess: () => {
          setSuccessData({ title: "Agent deleted successfully." });
        },
        onError: (err: any) => {
          console.error(err);
          setErrorData({ title: "Error deleting agent." });
        },
      },
    );
  };

  return (
    <div className="flex h-full w-full flex-col gap-4 overflow-auto p-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Agents</h1>
          <p className="text-sm text-muted-foreground">
            Create and manage your AI agents.
          </p>
        </div>
        <button
          className="rounded-md bg-primary px-4 py-2 text-sm text-primary-foreground hover:bg-primary/90"
          onClick={() => setCreateDialogOpen(true)}
          data-testid="create-agent-button"
        >
          Create Agent
        </button>
      </div>
      <div className="flex items-center gap-2">
        <Input
          icon="Search"
          placeholder="Search agents..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="max-w-sm"
          data-testid="agent-search-input"
        />
        {agents && (
          <span className="text-sm text-muted-foreground">
            {agents.length} Agent{agents.length !== 1 ? "s" : ""}
          </span>
        )}
      </div>
      <div className="flex-1">
        {isLoading ? (
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
            {Array.from({ length: 6 }).map((_, i) => (
              <div
                key={i}
                className="h-40 animate-pulse rounded-lg border bg-muted"
              />
            ))}
          </div>
        ) : agents && agents.length > 0 ? (
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
            {agents.map((agent) => (
              <AgentCard
                key={agent.id}
                agent={agent}
                onEdit={handleEdit}
                onDelete={handleDelete}
              />
            ))}
          </div>
        ) : (
          <div className="flex h-64 flex-col items-center justify-center rounded-lg border border-dashed">
            <p className="text-sm text-muted-foreground">
              {search
                ? "No agents found matching your search."
                : "No agents yet. Create your first agent to get started."}
            </p>
            {!search && (
              <button
                className="mt-4 rounded-md bg-primary px-4 py-2 text-sm text-primary-foreground hover:bg-primary/90"
                onClick={() => setCreateDialogOpen(true)}
              >
                Create Agent
              </button>
            )}
          </div>
        )}
      </div>
      <CreateAgentDialog
        open={createDialogOpen}
        onClose={() => setCreateDialogOpen(false)}
      />
    </div>
  );
}
