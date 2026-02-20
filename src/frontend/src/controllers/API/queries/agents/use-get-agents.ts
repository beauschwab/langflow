import { AgentType } from "@/types/agents";
import { useQueryFunctionType } from "@/types/api";
import { api } from "../../api";
import { getURL } from "../../helpers/constants";
import { UseRequestProcessor } from "../../services/request-processor";

interface IGetAgents {
  search?: string;
  agent_type?: string;
}

export const useGetAgents: useQueryFunctionType<IGetAgents, AgentType[]> = (
  params,
  options,
) => {
  const { query } = UseRequestProcessor();

  const getAgentsFn = async (params: IGetAgents): Promise<AgentType[]> => {
    const queryParams = new URLSearchParams();
    if (params?.search) queryParams.set("search", params.search);
    if (params?.agent_type) queryParams.set("agent_type", params.agent_type);
    const url = `${getURL("AGENTS")}/${queryParams.toString() ? `?${queryParams.toString()}` : ""}`;
    const { data } = await api.get<AgentType[]>(url);
    return data;
  };

  return query(
    ["useGetAgents", params],
    () => getAgentsFn(params ?? {}),
    {
      refetchOnWindowFocus: false,
      ...options,
    },
  );
};
