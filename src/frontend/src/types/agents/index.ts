export type AgentType = {
  id: string;
  name: string;
  description: string | null;
  agent_type: string | null;
  config: Record<string, unknown> | null;
  tools: string[] | null;
  tags: string[] | null;
  user_id: string | null;
  flow_id: string | null;
  created_at: string | null;
  updated_at: string | null;
};

export type AgentCreateType = {
  name: string;
  description?: string | null;
  agent_type?: string | null;
  config?: Record<string, unknown> | null;
  tools?: string[] | null;
  tags?: string[] | null;
  flow_id?: string | null;
};

export type AgentUpdateType = {
  name?: string | null;
  description?: string | null;
  agent_type?: string | null;
  config?: Record<string, unknown> | null;
  tools?: string[] | null;
  tags?: string[] | null;
  flow_id?: string | null;
};
