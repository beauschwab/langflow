"""Tests for the DeepAgentComponent (all 4 phases)."""

from typing import Any
from uuid import uuid4

import pytest
from langflow.components.agents.deep_agent import DeepAgentComponent
from langflow.custom import Component
from langflow.utils.constants import MESSAGE_SENDER_AI, MESSAGE_SENDER_NAME_AI

from tests.base import ComponentTestBaseWithoutClient
from tests.unit.mock_language_model import MockLanguageModel


class TestDeepAgentComponent(ComponentTestBaseWithoutClient):
    @pytest.fixture
    def component_class(self):
        return DeepAgentComponent

    @pytest.fixture
    def file_names_mapping(self):
        return []

    async def component_setup(self, component_class: type[Any], default_kwargs: dict[str, Any]) -> Component:
        component_instance = await super().component_setup(component_class, default_kwargs)
        component_instance._should_process_output = lambda output: False  # noqa: ARG005
        return component_instance

    @pytest.fixture
    def default_kwargs(self):
        return {
            "_type": "DeepAgent",
            "add_current_date_tool": True,
            "agent_description": "A deep agent with planning, context tools, and sub-agents",
            "agent_llm": MockLanguageModel(),
            "handle_parsing_errors": True,
            "input_value": "",
            "max_iterations": 25,
            "system_prompt": "You are a helpful assistant.",
            "tools": [],
            "verbose": True,
            "enable_planning": True,
            "enable_context_tools": True,
            "enable_sub_agents": False,
            "enable_summarization": False,
            "enable_skills": False,
            "skills_directory": "",
            "sub_agent_max_depth": 2,
            "sub_agent_max_iterations": 15,
            "session_id": str(uuid4()),
            "sender": MESSAGE_SENDER_AI,
            "sender_name": MESSAGE_SENDER_NAME_AI,
        }

    async def test_build_config_update(self, component_class, default_kwargs):
        """Test that update_build_config works correctly with model provider switching."""
        component = await self.component_setup(component_class, default_kwargs)
        frontend_node = component.to_frontend_node()
        build_config = frontend_node["data"]["node"]["template"]

        # Test updating build config for OpenAI
        component.set(agent_llm="OpenAI")
        updated_config = await component.update_build_config(build_config, "OpenAI", "agent_llm")
        assert "agent_llm" in updated_config
        assert updated_config["agent_llm"]["value"] == "OpenAI"

        # Verify Deep Agent specific fields are present
        assert "enable_planning" in updated_config
        assert "enable_context_tools" in updated_config
        assert "enable_sub_agents" in updated_config
        assert "enable_summarization" in updated_config

        # Test updating build config for Custom
        updated_config = await component.update_build_config(build_config, "Custom", "agent_llm")
        assert "agent_llm" in updated_config
        assert updated_config["agent_llm"]["value"] == "Custom"
        assert updated_config["agent_llm"]["input_types"] == ["LanguageModel"]

    async def test_planning_tool_creation(self, component_class, default_kwargs):
        """Phase 1: Test that the planning tool is created correctly."""
        component = await self.component_setup(component_class, default_kwargs)
        planning_tool = component._build_planning_tool()
        assert planning_tool.name == "write_todos"
        assert "todo" in planning_tool.description.lower()

        # Test running the planning tool
        from langflow.components.agents.deep_agent import TodoItem

        result = planning_tool.invoke(
            {"todos": [TodoItem(task="Test task 1", status="pending"), TodoItem(task="Test task 2", status="done")]}
        )
        assert "Test task 1" in result
        assert "Test task 2" in result
        assert "⬜" in result  # pending icon
        assert "✅" in result  # done icon

    async def test_context_tools_creation(self, component_class, default_kwargs):
        """Phase 3b: Test that context tools are created correctly."""
        component = await self.component_setup(component_class, default_kwargs)
        context_tools = component._build_context_tools()
        assert len(context_tools) == 2

        write_tool = next(t for t in context_tools if t.name == "write_context")
        read_tool = next(t for t in context_tools if t.name == "read_context")

        # Test write then read
        write_result = write_tool.invoke({"key": "findings", "value": "Some research findings"})
        assert "findings" in write_result
        assert "22" in write_result  # character count

        read_result = read_tool.invoke({"key": "findings"})
        assert read_result == "Some research findings"

        # Test read non-existent key
        read_missing = read_tool.invoke({"key": "nonexistent"})
        assert "No context found" in read_missing

    async def test_delegate_task_tool_creation(self, component_class, default_kwargs):
        """Phase 3a: Test that the delegate_task tool is created correctly."""
        component = await self.component_setup(component_class, default_kwargs)
        component.sub_agent_max_depth = 2
        component.sub_agent_max_iterations = 15

        mock_llm = MockLanguageModel()
        delegate_tool = component._build_delegate_task_tool(mock_llm, [], current_depth=0)
        assert delegate_tool.name == "delegate_task"
        assert "sub-agent" in delegate_tool.description.lower()

    async def test_delegate_task_depth_limit(self, component_class, default_kwargs):
        """Phase 3a: Test that sub-agent depth limits are enforced."""
        component = await self.component_setup(component_class, default_kwargs)
        component.sub_agent_max_depth = 2
        component.sub_agent_max_iterations = 15

        mock_llm = MockLanguageModel()
        # Create a tool at depth 2 (max_depth=2, so next would be 3 > 2)
        delegate_tool = component._build_delegate_task_tool(mock_llm, [], current_depth=2)

        # Should return depth limit message without executing
        result = await delegate_tool.coroutine(task="test task", context=None)
        assert "Cannot delegate" in result
        assert "maximum sub-agent depth" in result

    async def test_summarize_tool_creation(self, component_class, default_kwargs):
        """Phase 2: Test that the summarize tool is created correctly."""
        component = await self.component_setup(component_class, default_kwargs)
        mock_llm = MockLanguageModel()
        summarize_tool = component._build_summarize_tool(mock_llm)
        assert summarize_tool.name == "summarize"
        assert "summarize" in summarize_tool.description.lower()

    async def test_component_metadata(self, component_class, default_kwargs):
        """Phase 4: Test component metadata is set correctly."""
        component = await self.component_setup(component_class, default_kwargs)
        assert component.display_name == "Deep Agent"
        assert component.name == "DeepAgent"
        assert component.beta is True

        # Check that capability toggles exist as inputs
        input_names = [i.name for i in component.inputs if hasattr(i, "name")]
        assert "enable_planning" in input_names
        assert "enable_context_tools" in input_names
        assert "enable_sub_agents" in input_names
        assert "enable_summarization" in input_names
        assert "enable_skills" in input_names
        assert "skills_directory" in input_names
        assert "sub_agent_max_depth" in input_names
        assert "sub_agent_max_iterations" in input_names

    async def test_sub_agent_toggle_visibility(self, component_class, default_kwargs):
        """Test that sub-agent config fields become visible when toggle is enabled."""
        component = await self.component_setup(component_class, default_kwargs)
        frontend_node = component.to_frontend_node()
        build_config = frontend_node["data"]["node"]["template"]

        # Toggle sub-agents ON
        component.set(enable_sub_agents=True)
        updated_config = await component.update_build_config(build_config, True, "enable_sub_agents")

        # sub_agent fields should NOT be advanced (= visible) when toggle is on
        if "sub_agent_max_depth" in updated_config:
            assert updated_config["sub_agent_max_depth"]["advanced"] is False
        if "sub_agent_max_iterations" in updated_config:
            assert updated_config["sub_agent_max_iterations"]["advanced"] is False

    async def test_skills_tool_creation(self, component_class, default_kwargs, tmp_path):
        """Phase 5: Test that skill tools are created correctly with valid directory."""
        # Create a test skill directory
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            "---\nname: test-skill\ndescription: A test skill\n---\n\n# Test\n\n1. Do the thing\n"
        )
        (skill_dir / "ref.md").write_text("# Reference\n\nSome reference content.")

        component = await self.component_setup(component_class, default_kwargs)
        component.skills_directory = str(tmp_path)
        skills_tools = component._build_skills_tools()

        assert len(skills_tools) == 2
        tool_names = [t.name for t in skills_tools]
        assert "load_skill" in tool_names
        assert "read_skill_file" in tool_names

        # Verify catalog was injected into system prompt
        assert "Skills system" in component.system_prompt
        assert "test-skill" in component.system_prompt

    async def test_skills_tool_empty_directory(self, component_class, default_kwargs, tmp_path):
        """Phase 5: Test skills tool returns empty list for empty directory."""
        empty_dir = tmp_path / "empty-skills"
        empty_dir.mkdir()

        component = await self.component_setup(component_class, default_kwargs)
        component.skills_directory = str(empty_dir)
        skills_tools = component._build_skills_tools()
        assert skills_tools == []

    async def test_skills_tool_no_directory(self, component_class, default_kwargs):
        """Phase 5: Test skills tool returns empty list with no directory configured."""
        component = await self.component_setup(component_class, default_kwargs)
        component.skills_directory = ""
        skills_tools = component._build_skills_tools()
        assert skills_tools == []

    async def test_skills_toggle_visibility(self, component_class, default_kwargs):
        """Test that skills_directory becomes visible when enable_skills is toggled ON."""
        component = await self.component_setup(component_class, default_kwargs)
        frontend_node = component.to_frontend_node()
        build_config = frontend_node["data"]["node"]["template"]

        # Toggle skills ON
        component.set(enable_skills=True)
        updated_config = await component.update_build_config(build_config, True, "enable_skills")

        if "skills_directory" in updated_config:
            assert updated_config["skills_directory"]["advanced"] is False

    async def test_component_metadata_includes_skills(self, component_class, default_kwargs):
        """Test that skills inputs are registered on the component."""
        component = await self.component_setup(component_class, default_kwargs)
        input_names = [i.name for i in component.inputs if hasattr(i, "name")]
        assert "enable_skills" in input_names
        assert "skills_directory" in input_names
