import { AgentType } from "@/types/agents";
import { create } from "zustand";

type AgentStoreType = {
  agents: AgentType[];
  selectedAgent: AgentType | null;
  searchQuery: string;
  setAgents: (agents: AgentType[]) => void;
  setSelectedAgent: (agent: AgentType | null) => void;
  setSearchQuery: (query: string) => void;
  addAgent: (agent: AgentType) => void;
  updateAgent: (agent: AgentType) => void;
  removeAgent: (id: string) => void;
};

const useAgentStore = create<AgentStoreType>((set, get) => ({
  agents: [],
  selectedAgent: null,
  searchQuery: "",

  setAgents: (agents) => set({ agents }),
  setSelectedAgent: (agent) => set({ selectedAgent: agent }),
  setSearchQuery: (query) => set({ searchQuery: query }),

  addAgent: (agent) =>
    set({ agents: [...get().agents, agent] }),

  updateAgent: (agent) =>
    set({
      agents: get().agents.map((a) => (a.id === agent.id ? agent : a)),
    }),

  removeAgent: (id) =>
    set({
      agents: get().agents.filter((a) => a.id !== id),
    }),
}));

export default useAgentStore;
