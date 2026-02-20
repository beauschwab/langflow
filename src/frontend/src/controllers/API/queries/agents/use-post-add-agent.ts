import { AgentCreateType, AgentType } from "@/types/agents";
import { useMutationFunctionType } from "@/types/api";
import { api } from "../../api";
import { getURL } from "../../helpers/constants";
import { UseRequestProcessor } from "../../services/request-processor";

export const usePostAddAgent: useMutationFunctionType<
  undefined,
  AgentCreateType
> = (options?) => {
  const { mutate, queryClient } = UseRequestProcessor();

  const postAddAgentFn = async (
    payload: AgentCreateType,
  ): Promise<AgentType> => {
    const response = await api.post<AgentType>(`${getURL("AGENTS")}/`, {
      name: payload.name,
      description: payload.description || null,
      agent_type: payload.agent_type || null,
      config: payload.config || null,
      tools: payload.tools || null,
      tags: payload.tags || null,
      flow_id: payload.flow_id || null,
    });
    return response.data;
  };

  const mutation = mutate(["usePostAddAgent"], postAddAgentFn, {
    ...options,
    onSettled: () => {
      queryClient.refetchQueries({ queryKey: ["useGetAgents"] });
    },
  });

  return mutation;
};
