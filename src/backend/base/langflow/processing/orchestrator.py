from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, TypedDict, cast

from loguru import logger

from langflow.graph.schema import RunOutputs

if TYPE_CHECKING:
    from langflow.events.event_manager import EventManager
    from langflow.graph.graph.base import Graph
    from langflow.schema.schema import InputType


@dataclass
class _RunConfig:
    inputs: dict[str, str]
    components: list[str]
    input_type: InputType | None


def _normalize_run_configs(
    inputs: list[dict[str, str]],
    inputs_components: list[list[str]] | None,
    types: list[InputType | None] | None,
) -> list[_RunConfig]:
    normalized_inputs = inputs if isinstance(inputs, list) else [inputs]
    if not normalized_inputs:
        normalized_inputs = [{}]

    normalized_components = list(inputs_components or [])
    for _ in range(len(normalized_inputs) - len(normalized_components)):
        normalized_components.append([])

    normalized_types = list(types or [])
    for _ in range(len(normalized_inputs) - len(normalized_types)):
        normalized_types.append("chat")

    return [
        _RunConfig(inputs=run_inputs, components=components, input_type=input_type)
        for run_inputs, components, input_type in zip(normalized_inputs, normalized_components, normalized_types, strict=True)
    ]


async def run_graph_with_orchestrator(
    graph: Graph,
    inputs: list[dict[str, str]],
    *,
    inputs_components: list[list[str]] | None = None,
    types: list[InputType | None] | None = None,
    outputs: list[str] | None = None,
    session_id: str | None = None,
    stream: bool = False,
    fallback_to_env_vars: bool = False,
    event_manager: EventManager | None = None,
    backend: str = "legacy",
) -> list[RunOutputs]:
    if backend != "langgraph":
        return await graph.arun(
            inputs=inputs,
            inputs_components=inputs_components,
            types=types,
            outputs=outputs,
            session_id=session_id,
            stream=stream,
            fallback_to_env_vars=fallback_to_env_vars,
            event_manager=event_manager,
        )

    return await _run_with_langgraph(
        graph=graph,
        inputs=inputs,
        inputs_components=inputs_components,
        types=types,
        outputs=outputs,
        session_id=session_id,
        stream=stream,
        fallback_to_env_vars=fallback_to_env_vars,
        event_manager=event_manager,
    )


async def _run_with_langgraph(
    graph: Graph,
    inputs: list[dict[str, str]],
    *,
    inputs_components: list[list[str]] | None,
    types: list[InputType | None] | None,
    outputs: list[str] | None,
    session_id: str | None,
    stream: bool,
    fallback_to_env_vars: bool,
    event_manager: EventManager | None,
) -> list[RunOutputs]:
    try:
        from langgraph.graph import END, StateGraph
    except ImportError:
        logger.warning("LangGraph backend selected but langgraph is not installed; falling back to legacy orchestrator.")
        return await graph.arun(
            inputs=inputs,
            inputs_components=inputs_components,
            types=types,
            outputs=outputs,
            session_id=session_id,
            stream=stream,
            fallback_to_env_vars=fallback_to_env_vars,
            event_manager=event_manager,
        )

    run_configs = _normalize_run_configs(inputs=inputs, inputs_components=inputs_components, types=types)
    if session_id:
        graph.session_id = session_id

    class OrchestratorState(TypedDict):
        run_configs: list[_RunConfig]
        run_outputs: list[RunOutputs]

    async def execute_graph(state: OrchestratorState):
        run_outputs: list[RunOutputs] = []
        for run_config in state["run_configs"]:
            vertex_outputs = await graph._run(
                inputs=run_config.inputs,
                input_components=run_config.components,
                input_type=run_config.input_type,
                outputs=outputs or [],
                stream=stream,
                session_id=session_id or "",
                fallback_to_env_vars=fallback_to_env_vars,
                event_manager=event_manager,
            )
            run_output_object = RunOutputs(inputs=run_config.inputs, outputs=vertex_outputs)
            logger.debug(f"Run outputs: {run_output_object}")
            run_outputs.append(run_output_object)
        return {"run_outputs": run_outputs}

    workflow = StateGraph(OrchestratorState)
    workflow.add_node("execute_graph", execute_graph)
    workflow.set_entry_point("execute_graph")
    workflow.add_edge("execute_graph", END)

    app = workflow.compile()
    result = cast("dict[str, Any]", await app.ainvoke({"run_configs": run_configs, "run_outputs": []}))
    return cast("list[RunOutputs]", result.get("run_outputs", []))
