"""Deep Agent component with planning, context management, sub-agent delegation, and summarization."""

from __future__ import annotations

from typing import Any

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.agents.agent import RunnableAgent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from langflow.base.agents.agent import LCToolsAgentComponent
from langflow.base.agents.events import ExceptionWithMessageError
from langflow.base.models.model_input_constants import (
    ALL_PROVIDER_FIELDS,
    MODEL_DYNAMIC_UPDATE_FIELDS,
    MODEL_PROVIDERS_DICT,
    MODELS_METADATA,
)
from langflow.base.models.model_utils import get_model_name
from langflow.components.helpers import CurrentDateComponent
from langflow.components.helpers.memory import MemoryComponent
from langflow.custom.custom_component.component import _get_component_toolkit
from langflow.custom.utils import update_component_build_config
from langflow.field_typing import Tool
from langflow.io import BoolInput, DropdownInput, IntInput, MultilineInput, Output
from langflow.logging import logger
from langflow.schema.dotdict import dotdict
from langflow.schema.message import Message

# ---------------------------------------------------------------------------
# Phase 1: Enhanced system prompt with behavioral scaffolding
# ---------------------------------------------------------------------------

DEEP_AGENT_PROMPT = """\
You are an intelligent assistant with access to tools for completing tasks.

## How to work

1. **Understand first** — Read the user's request carefully. If ambiguous, ask for clarification.
2. **Plan** — For complex tasks, use the write_todos tool to break the work into steps.
3. **Act** — Execute each step using available tools. Work accurately and efficiently.
4. **Verify** — Check your work against what was asked. Iterate if needed.

## Communication style

- Be concise and direct. Avoid unnecessary preamble.
- Don't say "I'll now do X" — just do it.
- For longer tasks, provide brief progress updates.

## Tool usage

- Use tools when they can help. Don't guess when a tool can provide the answer.
- If a tool fails, analyze why before retrying with a different approach.
- Save intermediate results with write_context if they'll be needed later.
"""


# ---------------------------------------------------------------------------
# Phase 1: Planning tool (write_todos) — Pydantic schemas
# ---------------------------------------------------------------------------


class TodoItem(BaseModel):
    """A single todo item."""

    task: str = Field(description="Description of the task")
    status: str = Field(
        default="pending",
        description="Status of the task: pending, in_progress, or done",
    )


class WriteTodosInput(BaseModel):
    """Input schema for the write_todos tool."""

    todos: list[TodoItem] = Field(description="List of todo items with task descriptions and statuses")


# ---------------------------------------------------------------------------
# Phase 3a: Sub-agent delegation — Pydantic schemas
# ---------------------------------------------------------------------------


class DelegateTaskInput(BaseModel):
    """Input schema for the delegate_task tool."""

    task: str = Field(description="The task to delegate to a sub-agent")
    context: str | None = Field(default=None, description="Optional context to provide to the sub-agent")


# ---------------------------------------------------------------------------
# Phase 3b: Context tools — Pydantic schemas
# ---------------------------------------------------------------------------


class WriteContextInput(BaseModel):
    """Input schema for the write_context tool."""

    key: str = Field(description="A unique key to store the context under")
    value: str = Field(description="The value to store")


class ReadContextInput(BaseModel):
    """Input schema for the read_context tool."""

    key: str = Field(description="The key of the context to retrieve")


# ---------------------------------------------------------------------------
# Phase 2: Summarization input schema
# ---------------------------------------------------------------------------


class SummarizeInput(BaseModel):
    """Input for context summarization."""

    text: str = Field(description="Text to summarize")
    max_length: int = Field(default=500, description="Approximate max length of the summary in characters")


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------


def set_advanced_true(component_input):
    component_input.advanced = True
    return component_input


# ---------------------------------------------------------------------------
# DeepAgentComponent — integrates all 4 phases
# ---------------------------------------------------------------------------


class DeepAgentComponent(LCToolsAgentComponent):
    """Advanced agent with planning, context management, sub-agent delegation, and summarization.

    Implements all 4 phases of the Deep Agents adaptation plan:
    - Phase 1: Planning tool (write_todos) + enhanced system prompt
    - Phase 2: Context summarization
    - Phase 3: Sub-agent delegation + context read/write tools
    - Phase 4: Full integration as a unified DeepAgentComponent
    """

    display_name: str = "Deep Agent"
    description: str = (
        "Advanced agent with planning, context tools, sub-agent delegation, and summarization. "
        "Inspired by LangChain Deep Agents patterns."
    )
    icon = "bot"
    beta = True
    name = "DeepAgent"

    memory_inputs = [set_advanced_true(component_input) for component_input in MemoryComponent().inputs]

    inputs = [
        # ---- Core: model provider ----
        DropdownInput(
            name="agent_llm",
            display_name="Model Provider",
            info="The provider of the language model that the agent will use to generate responses.",
            options=[*sorted(MODEL_PROVIDERS_DICT.keys()), "Custom"],
            value="OpenAI",
            real_time_refresh=True,
            input_types=[],
            options_metadata=[MODELS_METADATA[key] for key in sorted(MODELS_METADATA.keys())] + [{"icon": "brain"}],
        ),
        *MODEL_PROVIDERS_DICT["OpenAI"]["inputs"],
        # ---- Core: system prompt (Phase 1 enhanced) ----
        MultilineInput(
            name="system_prompt",
            display_name="Agent Instructions",
            info="System prompt with behavioral scaffolding for planning, acting, and verifying.",
            value=DEEP_AGENT_PROMPT,
            advanced=False,
        ),
        # ---- Base agent inputs (tools, input_value, etc.) ----
        *LCToolsAgentComponent._base_inputs,
        # ---- Phase 1: Planning toggle ----
        BoolInput(
            name="enable_planning",
            display_name="Planning",
            value=True,
            advanced=False,
            info="Adds a write_todos tool for task breakdown and progress tracking.",
        ),
        # ---- Phase 3b: Context tools toggle ----
        BoolInput(
            name="enable_context_tools",
            display_name="Context Tools",
            value=True,
            advanced=False,
            info="Adds write_context / read_context tools for saving and retrieving intermediate results.",
        ),
        # ---- Phase 3a: Sub-agent delegation toggle ----
        BoolInput(
            name="enable_sub_agents",
            display_name="Sub-Agents",
            value=False,
            advanced=False,
            info="Adds a delegate_task tool for spawning isolated sub-agent workers.",
            real_time_refresh=True,
        ),
        # ---- Phase 2: Summarization toggle ----
        BoolInput(
            name="enable_summarization",
            display_name="Summarization",
            value=False,
            advanced=False,
            info="Adds a summarize tool that condenses long text to manage context window limits.",
            real_time_refresh=True,
        ),
        # ---- Advanced: sub-agent config ----
        IntInput(
            name="sub_agent_max_depth",
            display_name="Sub-Agent Max Depth",
            value=2,
            advanced=True,
            info="Maximum nesting depth for sub-agent delegation.",
        ),
        IntInput(
            name="sub_agent_max_iterations",
            display_name="Sub-Agent Max Iterations",
            value=15,
            advanced=True,
            info="Maximum iterations per sub-agent.",
        ),
        # ---- Memory inputs (advanced) ----
        *memory_inputs,
        # ---- Existing agent toggles ----
        BoolInput(
            name="add_current_date_tool",
            display_name="Current Date",
            advanced=True,
            info="If true, will add a tool to the agent that returns the current date.",
            value=True,
        ),
    ]
    outputs = [Output(name="response", display_name="Response", method="message_response")]

    # -----------------------------------------------------------------------
    # Phase 1: Planning tool builder
    # -----------------------------------------------------------------------

    def _build_planning_tool(self) -> StructuredTool:
        """Build the write_todos planning tool (Phase 1)."""
        todo_state: list[dict[str, str]] = []

        def write_todos(todos: list[TodoItem]) -> str:
            """Create or update a todo list for task planning and progress tracking."""
            todo_state.clear()
            lines: list[str] = []
            for item in todos:
                status_icon = {"pending": "⬜", "in_progress": "🔄", "done": "✅"}.get(item.status, "⬜")
                todo_state.append({"task": item.task, "status": item.status})
                lines.append(f"{status_icon} {item.task}")
            result = "Todo List:\n" + "\n".join(lines)
            return result

        return StructuredTool.from_function(
            func=write_todos,
            name="write_todos",
            description=(
                "Create or update a todo list for task planning. "
                "Each item has a task description and status (pending, in_progress, done). "
                "Use this to break complex work into trackable steps."
            ),
            args_schema=WriteTodosInput,
        )

    # -----------------------------------------------------------------------
    # Phase 3b: Context tools builder
    # -----------------------------------------------------------------------

    def _build_context_tools(self) -> list[StructuredTool]:
        """Build write_context and read_context tools (Phase 3b).

        Uses an in-memory dict scoped to the current execution.
        """
        context_store: dict[str, str] = {}

        def write_context(key: str, value: str) -> str:
            """Save an intermediate result or note under a named key for later retrieval."""
            context_store[key] = value
            return f"Saved context '{key}' ({len(value)} chars)."

        def read_context(key: str) -> str:
            """Retrieve a previously saved context value by its key."""
            value = context_store.get(key)
            if value is None:
                return f"No context found for key '{key}'. Available keys: {list(context_store.keys())}"
            return value

        write_tool = StructuredTool.from_function(
            func=write_context,
            name="write_context",
            description=(
                "Save intermediate results, notes, or data under a named key for later retrieval. "
                "Use this to avoid losing important information as the conversation grows."
            ),
            args_schema=WriteContextInput,
        )
        read_tool = StructuredTool.from_function(
            func=read_context,
            name="read_context",
            description="Retrieve previously saved context by key name.",
            args_schema=ReadContextInput,
        )
        return [write_tool, read_tool]

    # -----------------------------------------------------------------------
    # Phase 3a: Sub-agent delegation tool builder
    # -----------------------------------------------------------------------

    def _build_delegate_task_tool(
        self,
        llm: Any,
        external_tools: list,
        *,
        current_depth: int = 0,
    ) -> StructuredTool:
        """Build the delegate_task sub-agent tool (Phase 3a).

        The sub-agent inherits the parent's LLM and external tools but operates
        in a fresh context window. The delegate_task tool is excluded from the
        child's tool list to prevent infinite recursion.
        """
        max_depth = self.sub_agent_max_depth
        max_iters = self.sub_agent_max_iterations

        async def delegate_task(task: str, context: str | None = None) -> str:
            """Delegate a focused subtask to an isolated sub-agent with its own context window."""
            next_depth = current_depth + 1
            if next_depth > max_depth:
                return f"Cannot delegate: maximum sub-agent depth ({max_depth}) reached."

            sub_prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a focused sub-agent. Complete the assigned task using available tools."),
                ("placeholder", "{chat_history}"),
                ("human", "Context: {context}\n\nTask: {task}"),
                ("placeholder", "{agent_scratchpad}"),
            ])

            sub_agent = create_tool_calling_agent(llm, external_tools, sub_prompt)
            sub_executor = AgentExecutor(
                agent=RunnableAgent(runnable=sub_agent, input_keys_arg=["input"], return_keys_arg=["output"]),
                tools=external_tools,
                max_iterations=max_iters,
                handle_parsing_errors=True,
            )

            result = await sub_executor.ainvoke({
                "input": task,
                "context": context or "None",
                "task": task,
            })
            return result.get("output", "Sub-agent completed without output.")

        return StructuredTool.from_function(
            coroutine=delegate_task,
            name="delegate_task",
            description=(
                "Delegate a focused subtask to an isolated sub-agent with its own context window. "
                "Use for independent work that doesn't need the full conversation context. "
                "The sub-agent has access to the same tools as the parent."
            ),
            args_schema=DelegateTaskInput,
        )

    # -----------------------------------------------------------------------
    # Phase 2: Summarization tool builder
    # -----------------------------------------------------------------------

    def _build_summarize_tool(self, llm: Any) -> StructuredTool:
        """Build a summarization tool that uses the agent's LLM (Phase 2)."""

        async def summarize(text: str, max_length: int = 500) -> str:
            """Summarize a long piece of text to a shorter version, preserving key information."""
            prompt = ChatPromptTemplate.from_messages([
                (
                    "system",
                    (
                        "You are a summarization assistant. Summarize the following text concisely, "
                        f"keeping the most important information. Target approximately {max_length} characters."
                    ),
                ),
                ("human", "{text}"),
            ])
            chain = prompt | llm
            result = await chain.ainvoke({"text": text})
            if hasattr(result, "content"):
                return result.content
            return str(result)

        return StructuredTool.from_function(
            coroutine=summarize,
            name="summarize",
            description=(
                "Summarize a long piece of text to a shorter version, preserving key information. "
                "Use this when you have gathered a lot of information and need to condense it, "
                "or when context is getting too long."
            ),
            args_schema=SummarizeInput,
        )

    # -----------------------------------------------------------------------
    # Phase 4: Unified message_response integrating all phases
    # -----------------------------------------------------------------------

    async def message_response(self) -> Message:
        """Run the Deep Agent with all enabled capabilities."""
        try:
            # Get LLM model and validate
            llm_model, display_name = self.get_llm()
            if llm_model is None:
                msg = "No language model selected. Please choose a model to proceed."
                raise ValueError(msg)
            self.model_name = get_model_name(llm_model, display_name=display_name)

            # Get memory data
            self.chat_history = await self.get_memory_data()

            # Ensure tools list exists
            if not isinstance(self.tools, list):  # type: ignore[has-type]
                self.tools = []

            # ---- Phase 1: Inject planning tool ----
            if self.enable_planning:
                self.tools.append(self._build_planning_tool())

            # ---- Phase 3b: Inject context tools ----
            if self.enable_context_tools:
                self.tools.extend(self._build_context_tools())

            # ---- Phase 2: Inject summarization tool ----
            if self.enable_summarization:
                self.tools.append(self._build_summarize_tool(llm_model))

            # ---- Phase 3a: Inject sub-agent delegation tool ----
            if self.enable_sub_agents:
                # External tools = everything except delegate_task itself
                external_tools = [t for t in self.tools if t.name != "delegate_task"]
                self.tools.append(
                    self._build_delegate_task_tool(llm_model, external_tools, current_depth=0)
                )

            # Add current date tool if enabled
            if self.add_current_date_tool:
                current_date_tool = (await CurrentDateComponent(**self.get_base_args()).to_toolkit()).pop(0)
                if not isinstance(current_date_tool, StructuredTool):
                    msg = "CurrentDateComponent must be converted to a StructuredTool"
                    raise TypeError(msg)
                self.tools.append(current_date_tool)

            # Validate tools
            if not self.tools:
                msg = "Tools are required to run the agent. Please add at least one tool."
                raise ValueError(msg)

            # Set up and run agent
            self.set(
                llm=llm_model,
                tools=self.tools,
                chat_history=self.chat_history,
                input_value=self.input_value,
                system_prompt=self.system_prompt,
            )
            agent = self.create_agent_runnable()
            return await self.run_agent(agent)

        except (ValueError, TypeError, KeyError) as e:
            logger.error(f"{type(e).__name__}: {e!s}")
            raise
        except ExceptionWithMessageError as e:
            logger.error(f"ExceptionWithMessageError occurred: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e!s}")
            raise

    # -----------------------------------------------------------------------
    # LLM model building (same pattern as AgentComponent)
    # -----------------------------------------------------------------------

    async def get_memory_data(self):
        memory_kwargs = {
            component_input.name: getattr(self, component_input.name) for component_input in self.memory_inputs
        }
        memory_kwargs = {k: v for k, v in memory_kwargs.items() if v}
        return await MemoryComponent(**self.get_base_args()).set(**memory_kwargs).retrieve_messages()

    def get_llm(self):
        if not isinstance(self.agent_llm, str):
            return self.agent_llm, None

        try:
            provider_info = MODEL_PROVIDERS_DICT.get(self.agent_llm)
            if not provider_info:
                msg = f"Invalid model provider: {self.agent_llm}"
                raise ValueError(msg)

            component_class = provider_info.get("component_class")
            display_name = component_class.display_name
            inputs = provider_info.get("inputs")
            prefix = provider_info.get("prefix", "")

            return self._build_llm_model(component_class, inputs, prefix), display_name

        except Exception as e:
            logger.error(f"Error building {self.agent_llm} language model: {e!s}")
            msg = f"Failed to initialize language model: {e!s}"
            raise ValueError(msg) from e

    def _build_llm_model(self, component, inputs, prefix=""):
        model_kwargs = {input_.name: getattr(self, f"{prefix}{input_.name}") for input_ in inputs}
        return component.set(**model_kwargs).build_model()

    def set_component_params(self, component):
        provider_info = MODEL_PROVIDERS_DICT.get(self.agent_llm)
        if provider_info:
            inputs = provider_info.get("inputs")
            prefix = provider_info.get("prefix")
            model_kwargs = {input_.name: getattr(self, f"{prefix}{input_.name}") for input_ in inputs}
            return component.set(**model_kwargs)
        return component

    # -----------------------------------------------------------------------
    # Dynamic build config (model provider switching + capability toggles)
    # -----------------------------------------------------------------------

    def delete_fields(self, build_config: dotdict, fields: dict | list[str]) -> None:
        for field in fields:
            build_config.pop(field, None)

    def update_input_types(self, build_config: dotdict) -> dotdict:
        for key, value in build_config.items():
            if isinstance(value, dict):
                if value.get("input_types") is None:
                    build_config[key]["input_types"] = []
            elif hasattr(value, "input_types") and value.input_types is None:
                value.input_types = []
        return build_config

    async def update_build_config(
        self, build_config: dotdict, field_value: str, field_name: str | None = None
    ) -> dotdict:
        # --- Model provider switching (same as AgentComponent) ---
        if field_name in ("agent_llm",):
            build_config["agent_llm"]["value"] = field_value
            provider_info = MODEL_PROVIDERS_DICT.get(field_value)
            if provider_info:
                component_class = provider_info.get("component_class")
                if component_class and hasattr(component_class, "update_build_config"):
                    build_config = await update_component_build_config(
                        component_class, build_config, field_value, "model_name"
                    )

            provider_configs: dict[str, tuple[dict, list[dict]]] = {
                provider: (
                    MODEL_PROVIDERS_DICT[provider]["fields"],
                    [
                        MODEL_PROVIDERS_DICT[other_provider]["fields"]
                        for other_provider in MODEL_PROVIDERS_DICT
                        if other_provider != provider
                    ],
                )
                for provider in MODEL_PROVIDERS_DICT
            }
            if field_value in provider_configs:
                fields_to_add, fields_to_delete = provider_configs[field_value]
                for fields in fields_to_delete:
                    self.delete_fields(build_config, fields)
                if field_value == "OpenAI" and not any(field in build_config for field in fields_to_add):
                    build_config.update(fields_to_add)
                else:
                    build_config.update(fields_to_add)
                build_config["agent_llm"]["input_types"] = []
            elif field_value == "Custom":
                self.delete_fields(build_config, ALL_PROVIDER_FIELDS)
                custom_component = DropdownInput(
                    name="agent_llm",
                    display_name="Language Model",
                    options=[*sorted(MODEL_PROVIDERS_DICT.keys()), "Custom"],
                    value="Custom",
                    real_time_refresh=True,
                    input_types=["LanguageModel"],
                    options_metadata=[MODELS_METADATA[key] for key in sorted(MODELS_METADATA.keys())]
                    + [{"icon": "brain"}],
                )
                build_config.update({"agent_llm": custom_component.to_dict()})
            build_config = self.update_input_types(build_config)

            default_keys = [
                "code",
                "_type",
                "agent_llm",
                "tools",
                "input_value",
                "add_current_date_tool",
                "system_prompt",
                "agent_description",
                "max_iterations",
                "handle_parsing_errors",
                "verbose",
                "enable_planning",
                "enable_context_tools",
                "enable_sub_agents",
                "enable_summarization",
            ]
            missing_keys = [key for key in default_keys if key not in build_config]
            if missing_keys:
                msg = f"Missing required keys in build_config: {missing_keys}"
                raise ValueError(msg)

        # --- Dynamic visibility for capability toggles ---
        if field_name == "enable_sub_agents":
            is_enabled = field_value in (True, "true", "True")
            if "sub_agent_max_depth" in build_config:
                build_config["sub_agent_max_depth"]["advanced"] = not is_enabled
            if "sub_agent_max_iterations" in build_config:
                build_config["sub_agent_max_iterations"]["advanced"] = not is_enabled

        if (
            isinstance(self.agent_llm, str)
            and self.agent_llm in MODEL_PROVIDERS_DICT
            and field_name in MODEL_DYNAMIC_UPDATE_FIELDS
        ):
            provider_info = MODEL_PROVIDERS_DICT.get(self.agent_llm)
            if provider_info:
                component_class = provider_info.get("component_class")
                component_class = self.set_component_params(component_class)
                prefix = provider_info.get("prefix")
                if component_class and hasattr(component_class, "update_build_config"):
                    if isinstance(field_name, str) and isinstance(prefix, str):
                        field_name = field_name.replace(prefix, "")
                    build_config = await update_component_build_config(
                        component_class, build_config, field_value, "model_name"
                    )
        return dotdict({k: v.to_dict() if hasattr(v, "to_dict") else v for k, v in build_config.items()})

    async def to_toolkit(self) -> list[Tool]:
        component_toolkit = _get_component_toolkit()
        tools_names = self._build_tools_names()
        agent_description = self.get_tool_description()
        description = f"{agent_description}{tools_names}"
        tools = component_toolkit(component=self).get_tools(
            tool_name=self.get_tool_name(), tool_description=description, callbacks=self.get_langchain_callbacks()
        )
        if hasattr(self, "tools_metadata"):
            tools = component_toolkit(component=self, metadata=self.tools_metadata).update_tools_metadata(tools=tools)
        return tools
