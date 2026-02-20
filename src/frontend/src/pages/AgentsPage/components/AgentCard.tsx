import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { AgentType } from "@/types/agents";

type AgentCardProps = {
  agent: AgentType;
  onEdit: (agent: AgentType) => void;
  onDelete: (agent: AgentType) => void;
};

export default function AgentCard({
  agent,
  onEdit,
  onDelete,
}: AgentCardProps): JSX.Element {
  return (
    <Card
      className="group cursor-pointer hover:shadow-md"
      data-testid={`agent-card-${agent.id}`}
    >
      <CardHeader>
        <div className="flex items-start justify-between">
          <CardTitle className="truncate">{agent.name}</CardTitle>
          <div className="flex gap-1">
            {agent.agent_type && (
              <Badge variant="secondary" size="sm">
                {agent.agent_type}
              </Badge>
            )}
          </div>
        </div>
        <CardDescription className="line-clamp-2">
          {agent.description || "No description"}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="flex flex-wrap gap-1">
          {agent.tools?.map((tool) => (
            <Badge key={tool} variant="outline" size="sm">
              {tool}
            </Badge>
          ))}
          {agent.tags?.map((tag) => (
            <Badge key={tag} variant="gray" size="sm">
              {tag}
            </Badge>
          ))}
        </div>
      </CardContent>
      <CardFooter className="gap-2">
        <button
          className="text-xs text-primary hover:underline"
          onClick={(e) => {
            e.stopPropagation();
            onEdit(agent);
          }}
          data-testid={`agent-edit-${agent.id}`}
        >
          Edit
        </button>
        <button
          className="text-xs text-destructive hover:underline"
          onClick={(e) => {
            e.stopPropagation();
            onDelete(agent);
          }}
          data-testid={`agent-delete-${agent.id}`}
        >
          Delete
        </button>
      </CardFooter>
    </Card>
  );
}
