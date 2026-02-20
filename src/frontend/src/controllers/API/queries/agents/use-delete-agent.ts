import { useMutationFunctionType } from "@/types/api";
import { api } from "../../api";
import { getURL } from "../../helpers/constants";
import { UseRequestProcessor } from "../../services/request-processor";

interface IDeleteAgent {
  id: string;
}

export const useDeleteAgent: useMutationFunctionType<
  undefined,
  IDeleteAgent
> = (options?) => {
  const { mutate, queryClient } = UseRequestProcessor();

  const deleteAgentFn = async (payload: IDeleteAgent): Promise<void> => {
    await api.delete(`${getURL("AGENTS")}/${payload.id}`);
  };

  const mutation = mutate(["useDeleteAgent"], deleteAgentFn, {
    ...options,
    onSettled: () => {
      queryClient.refetchQueries({ queryKey: ["useGetAgents"] });
    },
  });

  return mutation;
};
