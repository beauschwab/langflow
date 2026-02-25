import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { useState } from "react";
import { AVAILABLE_TOOLS } from "./constants";

export default function ToolsTab(): JSX.Element {
  const [search, setSearch] = useState("");

  const filteredTools = AVAILABLE_TOOLS.filter(
    (tool) =>
      !search ||
      tool.name.toLowerCase().includes(search.toLowerCase()) ||
      tool.description.toLowerCase().includes(search.toLowerCase()),
  );

  return (
    <div className="flex flex-col gap-4">
      <div className="flex items-center justify-between">
        <p className="text-sm text-muted-foreground">
          Available tools that can be assigned to agents.
        </p>
      </div>
      <div className="flex items-center gap-2">
        <Input
          icon="Search"
          placeholder="Search tools..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="max-w-sm"
          data-testid="tools-search-input"
        />
        <span className="text-sm text-muted-foreground">
          {filteredTools.length} Tool{filteredTools.length !== 1 ? "s" : ""}
        </span>
      </div>
      {filteredTools.length > 0 ? (
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
          {filteredTools.map((tool) => (
            <Card
              key={tool.id}
              className="hover:shadow-md"
              data-testid={`tool-card-${tool.id}`}
            >
              <CardHeader>
                <div className="flex items-start justify-between">
                  <CardTitle className="truncate text-sm">
                    {tool.name}
                  </CardTitle>
                  <Badge variant="secondary" size="sm">
                    Tool
                  </Badge>
                </div>
                <CardDescription>{tool.description}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex items-center gap-2 text-xs text-muted-foreground">
                  <span>ID: {tool.id}</span>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : (
        <div className="flex h-64 flex-col items-center justify-center rounded-lg border border-dashed">
          <p className="text-sm text-muted-foreground">
            {search
              ? "No tools found matching your search."
              : "No tools available."}
          </p>
        </div>
      )}
    </div>
  );
}
