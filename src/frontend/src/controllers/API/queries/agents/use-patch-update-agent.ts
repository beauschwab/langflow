import { AgentType, AgentUpdateType } from "@/types/agents";
import { useMutationFunctionType } from "@/types/api";
import { api } from "../../api";
import { getURL } from "../../helpers/constants";
import { UseRequestProcessor } from "../../services/request-processor";

interface IPatchAgent {
  id: string;
  data: AgentUpdateType;
}

export const usePatchUpdateAgent: useMutationFunctionType<
  undefined,
  IPatchAgent
> = (options?) => {
  const { mutate, queryClient } = UseRequestProcessor();

  const patchAgentFn = async (payload: IPatchAgent): Promise<AgentType> => {
    const response = await api.patch<AgentType>(
      `${getURL("AGENTS")}/${payload.id}`,
      payload.data,
    );
    return response.data;
  };

  const mutation = mutate(["usePatchUpdateAgent"], patchAgentFn, {
    ...options,
    onSettled: () => {
      queryClient.refetchQueries({ queryKey: ["useGetAgents"] });
    },
  });

  return mutation;
};
