import sys
from types import ModuleType

import pytest

from langflow.processing.orchestrator import run_graph_with_orchestrator


class DummyGraph:
    def __init__(self):
        self._run_calls = 0
        self.session_id = ""

    async def _run(self, **kwargs):
        self._run_calls += 1
        return []


class FakeCompiledGraph:
    def __init__(self, node):
        self._node = node

    async def ainvoke(self, state):
        return await self._node(state)


class FakeStateGraph:
    def __init__(self, _state):
        self._node = None

    def add_node(self, _name, node):
        self._node = node

    def set_entry_point(self, _name):
        return None

    def add_edge(self, _source, _target):
        return None

    def compile(self):
        return FakeCompiledGraph(self._node)


@pytest.mark.asyncio
async def test_langgraph_backend_uses_graph_private_run(monkeypatch):
    graph = DummyGraph()
    fake_langgraph = ModuleType("langgraph")
    fake_langgraph_graph = ModuleType("langgraph.graph")
    fake_langgraph_graph.END = "END"
    fake_langgraph_graph.StateGraph = FakeStateGraph
    fake_langgraph.graph = fake_langgraph_graph
    monkeypatch.setitem(sys.modules, "langgraph", fake_langgraph)
    monkeypatch.setitem(sys.modules, "langgraph.graph", fake_langgraph_graph)

    result = await run_graph_with_orchestrator(
        graph=graph,
        inputs=[{"input_value": "hello"}],
    )

    assert len(result) == 1
    assert result[0].inputs == {"input_value": "hello"}
    assert graph._run_calls == 1
