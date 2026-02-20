# Frontend Node Type Inventory (Current Built-in Components)

This inventory documents the node/component types currently available to the frontend sidebar via `GET /api/v1/all`.

- **Source of truth**: `src/backend/base/langflow/components/**` (excluding `deactivated`)
- **Frontend consumption path**: `src/frontend/src/controllers/API/queries/flows/use-get-types.ts` → `typesStore` → Flow sidebar

## Summary

- Total categories: **38**
- Total node types: **244**

## Notion (8 node types)

### AddContentToPage

- **Class**: `AddContentToPage`
- **Source**: `Notion/add_content_to_page.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `markdown_text` (MultilineInput) — display: "Markdown Text"; info: The markdown text to convert to Notion blocks.
  - `block_id` (StrInput) — display: "Page/Block ID"; info: The ID of the page/block to add the content.
  - `notion_secret` (SecretStrInput) — display: "Notion Secret"; required: true; info: The Notion integration token.

- **Output ports**:
  - _No class-level outputs declared._

### List Users

- **Class**: `NotionUserList`
- **Source**: `Notion/list_users.py`
- **Description**: Retrieve users from Notion.

- **Input/configuration ports**:
  - `notion_secret` (SecretStrInput) — display: "Notion Secret"; required: true; info: The Notion integration token.

- **Output ports**:
  - _No class-level outputs declared._

### NotionDatabaseProperties

- **Class**: `NotionDatabaseProperties`
- **Source**: `Notion/list_database_properties.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `database_id` (StrInput) — display: "Database ID"; info: The ID of the Notion database.
  - `notion_secret` (SecretStrInput) — display: "Notion Secret"; required: true; info: The Notion integration token.

- **Output ports**:
  - _No class-level outputs declared._

### NotionListPages

- **Class**: `NotionListPages`
- **Source**: `Notion/list_pages.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `notion_secret` (SecretStrInput) — display: "Notion Secret"; required: true; info: The Notion integration token.
  - `database_id` (StrInput) — display: "Database ID"; info: The ID of the Notion database to query.
  - `query_json` (MultilineInput) — display: "Database query (JSON)"; info: A JSON string containing the filters and sorts that will be used for querying the database. Leave empty for no filters or sorts.

- **Output ports**:
  - _No class-level outputs declared._

### NotionPageCreator

- **Class**: `NotionPageCreator`
- **Source**: `Notion/create_page.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `database_id` (StrInput) — display: "Database ID"; info: The ID of the Notion database.
  - `notion_secret` (SecretStrInput) — display: "Notion Secret"; required: true; info: The Notion integration token.
  - `properties_json` (MultilineInput) — display: "Properties (JSON)"; info: The properties of the new page as a JSON string.

- **Output ports**:
  - _No class-level outputs declared._

### NotionPageUpdate

- **Class**: `NotionPageUpdate`
- **Source**: `Notion/update_page_property.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `page_id` (StrInput) — display: "Page ID"; info: The ID of the Notion page to update.
  - `properties` (MultilineInput) — display: "Properties"; info: The properties to update on the page (as a JSON string or a dictionary).
  - `notion_secret` (SecretStrInput) — display: "Notion Secret"; required: true; info: The Notion integration token.

- **Output ports**:
  - _No class-level outputs declared._

### NotionSearch

- **Class**: `NotionSearch`
- **Source**: `Notion/search.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `notion_secret` (SecretStrInput) — display: "Notion Secret"; required: true; info: The Notion integration token.
  - `query` (StrInput) — display: "Search Query"; info: The text that the API compares page and database titles against.
  - `filter_value` (DropdownInput) — display: "Filter Type"; options: ['page', 'database']; default: 'page'; info: Limits the results to either only pages or only databases.
  - `sort_direction` (DropdownInput) — display: "Sort Direction"; options: ['ascending', 'descending']; default: 'descending'; info: The direction to sort the results.

- **Output ports**:
  - _No class-level outputs declared._

### Page Content Viewer

- **Class**: `NotionPageContent`
- **Source**: `Notion/page_content_viewer.py`
- **Description**: Retrieve the content of a Notion page as plain text.

- **Input/configuration ports**:
  - `page_id` (StrInput) — display: "Page ID"; info: The ID of the Notion page to retrieve.
  - `notion_secret` (SecretStrInput) — display: "Notion Secret"; required: true; info: The Notion integration token.

- **Output ports**:
  - _No class-level outputs declared._

## agentql (1 node types)

### Extract Web Data

- **Class**: `AgentQL`
- **Source**: `agentql/agentql_api.py`
- **Description**: Extracts structured data from a web page using an AgentQL query or a Natural Language description.

- **Input/configuration ports**:
  - `api_key` (SecretStrInput) — display: "API Key"; required: true; info: Your AgentQL API key from dev.agentql.com
  - `url` (MessageTextInput) — display: "URL"; required: true; info: The URL of the public web page you want to extract data from.
  - `query` (MultilineInput) — display: "AgentQL Query"; required: false; info: The AgentQL query to execute. Learn more at https://docs.agentql.com/agentql-query or use a prompt.
  - `prompt` (MultilineInput) — display: "Prompt"; required: false; info: A Natural Language description of the data to extract from the page. Alternative to AgentQL query.
  - `is_stealth_mode_enabled` (BoolInput) — display: "Enable Stealth Mode (Beta)"; default: False; info: Enable experimental anti-bot evasion strategies. May not work for all websites at all times.
  - `timeout` (IntInput) — display: "Timeout"; default: 900; info: Seconds to wait for a request.
  - `mode` (DropdownInput) — display: "Request Mode"; options: ['fast', 'standard']; default: 'fast'; info: 'standard' uses deep data analysis, while 'fast' trades some depth of analysis for speed.
  - `wait_for` (IntInput) — display: "Wait For"; default: 0; info: Seconds to wait for the page to load before extracting data.
  - `is_scroll_to_bottom_enabled` (BoolInput) — display: "Enable scroll to bottom"; default: False; info: Scroll to bottom of the page before extracting data.
  - `is_screenshot_enabled` (BoolInput) — display: "Enable screenshot"; default: False; info: Take a screenshot before extracting data. Returned in 'metadata' as a Base64 string.

- **Output ports**:
  - `data` (Output) — display: "Data"; method: `build_output`

## agents (1 node types)

### AgentComponent

- **Class**: `AgentComponent`
- **Source**: `agents/agent.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `agent_llm` (DropdownInput) — display: "Model Provider"; input_types: []; options: [*sorted(MODEL_PROVIDERS_DICT.keys()), 'Custom']; default: 'OpenAI'; info: The provider of the language model that the agent will use to generate responses.
  - `system_prompt` (MultilineInput) — display: "Agent Instructions"; default: 'You are a helpful assistant that can use tools to answer questions and perform tasks.'; info: System Prompt: Initial instructions and context provided to guide the agent's behavior.
  - `add_current_date_tool` (BoolInput) — display: "Current Date"; default: True; info: If true, will add a tool to the agent that returns the current date.

- **Output ports**:
  - `response` (Output) — display: "Response"; method: `message_response`

## apify (1 node types)

### Apify Actors

- **Class**: `ApifyActorsComponent`
- **Source**: `apify/apify_actor.py`
- **Description**: Use Apify Actors to extract data from hundreds of places fast. This component can be used in a flow to retrieve data or as a tool with an agent.

- **Input/configuration ports**:
  - `apify_token` (SecretStrInput) — display: "Apify Token"; required: true; info: The API token for the Apify account.
  - `actor_id` (StrInput) — display: "Actor"; required: true; default: 'apify/website-content-crawler'; info: Actor name from Apify store to run. For example 'apify/website-content-crawler' to use the Website Content Crawler Actor.
  - `run_input` (MultilineInput) — display: "Run input"; required: true; default: '{"startUrls":[{"url":"https://docs.apify.com/academy/web-scraping-for-beginners"}],"maxCrawlDepth":0}'; info: The JSON input for the Actor run. For example for the "apify/website-content-crawler" Actor: {"startUrls":[{"url":"https://docs.apify.com/academy/web-scraping-for-beginners"}],"maxCrawlDepth":0}
  - `dataset_fields` (MultilineInput) — display: "Output fields"; info: Fields to extract from the dataset, split by commas. Other fields will be ignored. Dots in nested structures will be replaced by underscores. Sample input: 'text, metadata.title'. Sample output: {'text': 'page content here', 'metadata_title': 'page title here'}. For example, for the 'apify/website-content-crawler' Actor, you can extract the 'markdown' field, which is the content of the website in markdown format.
  - `flatten_dataset` (BoolInput) — display: "Flatten output"; info: The output dataset will be converted from a nested format to a flat structure. Dots in nested structure will be replaced by underscores. This is useful for further processing of the Data object. For example, {'a': {'b': 1}} will be flattened to {'a_b': 1}.

- **Output ports**:
  - `output` (Output) — display: "Output"; method: `run_model`
  - `tool` (Output) — display: "Tool"; method: `build_tool`

## assemblyai (5 node types)

### AssemblyAI Get Subtitles

- **Class**: `AssemblyAIGetSubtitles`
- **Source**: `assemblyai/assemblyai_get_subtitles.py`
- **Description**: Export your transcript in SRT or VTT format for subtitles and closed captions

- **Input/configuration ports**:
  - `api_key` (SecretStrInput) — display: "Assembly API Key"; required: true; info: Your AssemblyAI API key. You can get one from https://www.assemblyai.com/
  - `transcription_result` (DataInput) — display: "Transcription Result"; required: true; info: The transcription result from AssemblyAI
  - `subtitle_format` (DropdownInput) — display: "Subtitle Format"; options: ['srt', 'vtt']; default: 'srt'; info: The format of the captions (SRT or VTT)
  - `chars_per_caption` (IntInput) — display: "Characters per Caption"; default: 0; info: The maximum number of characters per caption (0 for no limit)

- **Output ports**:
  - `subtitles` (Output) — display: "Subtitles"; method: `get_subtitles`

### AssemblyAI LeMUR

- **Class**: `AssemblyAILeMUR`
- **Source**: `assemblyai/assemblyai_lemur.py`
- **Description**: Apply Large Language Models to spoken data using the AssemblyAI LeMUR framework

- **Input/configuration ports**:
  - `api_key` (SecretStrInput) — display: "Assembly API Key"; required: true; info: Your AssemblyAI API key. You can get one from https://www.assemblyai.com/
  - `transcription_result` (DataInput) — display: "Transcription Result"; required: true; info: The transcription result from AssemblyAI
  - `prompt` (MultilineInput) — display: "Input Prompt"; required: true; info: The text to prompt the model
  - `final_model` (DropdownInput) — display: "Final Model"; options: ['claude3_5_sonnet', 'claude3_opus', 'claude3_haiku', 'claude3_sonnet']; default: 'claude3_5_sonnet'; info: The model that is used for the final prompt after compression is performed
  - `temperature` (FloatInput) — display: "Temperature"; default: 0.0; info: The temperature to use for the model
  - `max_output_size` (IntInput) — display: "Max Output Size"; default: 2000; info: Max output size in tokens, up to 4000
  - `endpoint` (DropdownInput) — display: "Endpoint"; options: ['task', 'summary', 'question-answer']; default: 'task'; info: The LeMUR endpoint to use. For 'summary' and 'question-answer', no prompt input is needed. See https://www.assemblyai.com/docs/api-reference/lemur/ for more info.
  - `questions` (MultilineInput) — display: "Questions"; info: Comma-separated list of your questions. Only used if Endpoint is 'question-answer'
  - `transcript_ids` (MultilineInput) — display: "Transcript IDs"; info: Comma-separated list of transcript IDs. LeMUR can perform actions over multiple transcripts. If provided, the Transcription Result is ignored.

- **Output ports**:
  - `lemur_response` (Output) — display: "LeMUR Response"; method: `run_lemur`

### AssemblyAI List Transcripts

- **Class**: `AssemblyAIListTranscripts`
- **Source**: `assemblyai/assemblyai_list_transcripts.py`
- **Description**: Retrieve a list of transcripts from AssemblyAI with filtering options

- **Input/configuration ports**:
  - `api_key` (SecretStrInput) — display: "Assembly API Key"; required: true; info: Your AssemblyAI API key. You can get one from https://www.assemblyai.com/
  - `limit` (IntInput) — display: "Limit"; default: 20; info: Maximum number of transcripts to retrieve (default: 20, use 0 for all)
  - `status_filter` (DropdownInput) — display: "Status Filter"; options: ['all', 'queued', 'processing', 'completed', 'error']; default: 'all'; info: Filter by transcript status
  - `created_on` (MessageTextInput) — display: "Created On"; info: Only get transcripts created on this date (YYYY-MM-DD)
  - `throttled_only` (BoolInput) — display: "Throttled Only"; info: Only get throttled transcripts, overrides the status filter

- **Output ports**:
  - `transcript_list` (Output) — display: "Transcript List"; method: `list_transcripts`

### AssemblyAI Poll Transcript

- **Class**: `AssemblyAITranscriptionJobPoller`
- **Source**: `assemblyai/assemblyai_poll_transcript.py`
- **Description**: Poll for the status of a transcription job using AssemblyAI

- **Input/configuration ports**:
  - `api_key` (SecretStrInput) — display: "Assembly API Key"; required: true; info: Your AssemblyAI API key. You can get one from https://www.assemblyai.com/
  - `transcript_id` (DataInput) — display: "Transcript ID"; required: true; info: The ID of the transcription job to poll
  - `polling_interval` (FloatInput) — display: "Polling Interval"; default: 3.0; info: The polling interval in seconds

- **Output ports**:
  - `transcription_result` (Output) — display: "Transcription Result"; method: `poll_transcription_job`

### AssemblyAI Start Transcript

- **Class**: `AssemblyAITranscriptionJobCreator`
- **Source**: `assemblyai/assemblyai_start_transcript.py`
- **Description**: Create a transcription job for an audio file using AssemblyAI with advanced options

- **Input/configuration ports**:
  - `api_key` (SecretStrInput) — display: "Assembly API Key"; required: true; info: Your AssemblyAI API key. You can get one from https://www.assemblyai.com/
  - `audio_file` (FileInput) — display: "Audio File"; required: true; info: The audio file to transcribe
  - `audio_file_url` (MessageTextInput) — display: "Audio File URL"; info: The URL of the audio file to transcribe (Can be used instead of a File)
  - `speech_model` (DropdownInput) — display: "Speech Model"; options: ['best', 'nano']; default: 'best'; info: The speech model to use for the transcription
  - `language_detection` (BoolInput) — display: "Automatic Language Detection"; info: Enable automatic language detection
  - `language_code` (MessageTextInput) — display: "Language"; info: The language of the audio file. Can be set manually if automatic language detection is disabled. See https://www.assemblyai.com/docs/getting-started/supported-languages for a list of supported language codes.
  - `speaker_labels` (BoolInput) — display: "Enable Speaker Labels"; info: Enable speaker diarization
  - `speakers_expected` (MessageTextInput) — display: "Expected Number of Speakers"; info: Set the expected number of speakers (optional, enter a number)
  - `punctuate` (BoolInput) — display: "Punctuate"; default: True; info: Enable automatic punctuation
  - `format_text` (BoolInput) — display: "Format Text"; default: True; info: Enable text formatting

- **Output ports**:
  - `transcript_id` (Output) — display: "Transcript ID"; method: `create_transcription_job`

## astra_assistants (8 node types)

### Astra Assistant Agent

- **Class**: `AstraAssistantManager`
- **Source**: `astra_assistants/astra_assistant_manager.py`
- **Description**: Manages Assistant Interactions

- **Input/configuration ports**:
  - `model_name` (DropdownInput) — display: "Model"; options: litellm_model_names; default: 'gpt-4o-mini'
  - `instructions` (MultilineInput) — display: "Agent Instructions"; info: Instructions for the assistant, think of these as the system prompt.
  - `input_tools` (HandleInput) — display: "Tools"; required: false; input_types: ['Tool']; info: These are the tools that the agent can use to help with tasks.
  - `user_message` (MultilineInput) — display: "User Message"; info: User message to pass to the run.
  - `file` (FileInput) — display: "File(s) for retrieval"; required: false; info: Files to be sent with the message.
  - `input_thread_id` (MultilineInput) — display: "Thread ID (optional)"; info: ID of the thread
  - `input_assistant_id` (MultilineInput) — display: "Assistant ID (optional)"; info: ID of the assistant
  - `env_set` (MultilineInput) — display: "Environment Set"; info: Dummy input to allow chaining with Dotenv Component.

- **Output ports**:
  - `assistant_response` (Output) — display: "Assistant Response"; method: `get_assistant_response`
  - `tool_output` (Output) — display: "Tool output"; method: `get_tool_output`
  - `output_thread_id` (Output) — display: "Thread Id"; method: `get_thread_id`
  - `output_assistant_id` (Output) — display: "Assistant Id"; method: `get_assistant_id`
  - `output_vs_id` (Output) — display: "Vector Store Id"; method: `get_vs_id`

### Create Assistant

- **Class**: `AssistantsCreateAssistant`
- **Source**: `astra_assistants/create_assistant.py`
- **Description**: Creates an Assistant and returns it's id

- **Input/configuration ports**:
  - `assistant_name` (StrInput) — display: "Assistant Name"; info: Name for the assistant being created
  - `instructions` (StrInput) — display: "Instructions"; info: Instructions for the assistant, think of these as the system prompt.
  - `model` (StrInput) — display: "Model name"; info: Model for the assistant. Environment variables for provider credentials can be set with the Dotenv Component. Models are supported via LiteLLM, see (https://docs.litellm.ai/docs/providers) for supported model names and env vars.
  - `env_set` (MultilineInput) — display: "Environment Set"; info: Dummy input to allow chaining with Dotenv Component.

- **Output ports**:
  - `assistant_id` (Output) — display: "Assistant ID"; method: `process_inputs`

### Create Assistant Thread

- **Class**: `AssistantsCreateThread`
- **Source**: `astra_assistants/create_thread.py`
- **Description**: Creates a thread and returns the thread id

- **Input/configuration ports**:
  - `env_set` (MultilineInput) — display: "Environment Set"; info: Dummy input to allow chaining with Dotenv Component.

- **Output ports**:
  - `thread_id` (Output) — display: "Thread ID"; method: `process_inputs`

### Dotenv

- **Class**: `Dotenv`
- **Source**: `astra_assistants/dotenv.py`
- **Description**: Load .env file into env vars

- **Input/configuration ports**:
  - `dotenv_file_content` (MultilineSecretInput) — display: "Dotenv file content"; info: Paste the content of your .env file directly, since contents are sensitive, using a Global variable set as 'password' is recommended

- **Output ports**:
  - `env_set` (Output) — display: "env_set"; method: `process_inputs`

### Get Assistant name

- **Class**: `AssistantsGetAssistantName`
- **Source**: `astra_assistants/get_assistant.py`
- **Description**: Assistant by id

- **Input/configuration ports**:
  - `assistant_id` (StrInput) — display: "Assistant ID"; info: ID of the assistant
  - `env_set` (MultilineInput) — display: "Environment Set"; info: Dummy input to allow chaining with Dotenv Component.

- **Output ports**:
  - `assistant_name` (Output) — display: "Assistant Name"; method: `process_inputs`

### Get env var

- **Class**: `GetEnvVar`
- **Source**: `astra_assistants/getenvvar.py`
- **Description**: Get env var

- **Input/configuration ports**:
  - `env_var_name` (StrInput) — display: "Env var name"; info: Name of the environment variable to get

- **Output ports**:
  - `env_var_value` (Output) — display: "Env var value"; method: `process_inputs`

### List Assistants

- **Class**: `AssistantsListAssistants`
- **Source**: `astra_assistants/list_assistants.py`
- **Description**: Returns a list of assistant id's

- **Input/configuration ports**:
  - _No class-level inputs declared._

- **Output ports**:
  - `assistants` (Output) — display: "Assistants"; method: `process_inputs`

### Run Assistant

- **Class**: `AssistantsRun`
- **Source**: `astra_assistants/run.py`
- **Description**: Executes an Assistant Run against a thread

- **Input/configuration ports**:
  - `assistant_id` (MultilineInput) — display: "Assistant ID"; info: The ID of the assistant to run. Can be retrieved using the List Assistants component or created with the Create Assistant component.
  - `user_message` (MultilineInput) — display: "User Message"; info: User message to pass to the run.
  - `thread_id` (MultilineInput) — display: "Thread ID"; required: false; info: Thread ID to use with the run. If not provided, a new thread will be created.
  - `env_set` (MultilineInput) — display: "Environment Set"; info: Dummy input to allow chaining with Dotenv Component.

- **Output ports**:
  - `assistant_response` (Output) — display: "Assistant Response"; method: `process_inputs`

## cohere (1 node types)

### Cohere Rerank

- **Class**: `CohereRerankComponent`
- **Source**: `cohere/cohere_rerank.py`
- **Description**: Rerank documents using the Cohere API.

- **Input/configuration ports**:
  - `api_key` (SecretStrInput) — display: "Cohere API Key"
  - `model` (DropdownInput) — display: "Model"; options: ['rerank-english-v3.0', 'rerank-multilingual-v3.0', 'rerank-english-v2.0', 'rerank-multilingual-v2.0']; default: 'rerank-english-v3.0'

- **Output ports**:
  - `reranked_documents` (Output) — display: "Reranked Documents"; method: `compress_documents`

## composio (2 node types)

### ComposioAPIComponent

- **Class**: `ComposioAPIComponent`
- **Source**: `composio/composio_api.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `entity_id` (MessageTextInput) — display: "Entity ID"; default: 'default'
  - `api_key` (SecretStrInput) — display: "Composio API Key"; required: true; info: Refer to https://docs.composio.dev/faq/api_key/api_key
  - `app_names` (DropdownInput) — display: "App Name"; required: true; options: []; default: ''; info: The app name to use. Please refresh after selecting app name
  - `app_credentials` (SecretStrInput) — display: "App Credentials"; required: false; info: Credentials for app authentication (API Key, Password, etc)
  - `username` (MessageTextInput) — display: "Username"; required: false; info: Username for Basic authentication
  - `auth_link` (LinkInput) — display: "Authentication Link"; default: ''; info: Click to authenticate with OAuth2
  - `auth_status` (StrInput) — display: "Auth Status"; default: 'Not Connected'; info: Current authentication status
  - `action_names` (MultiselectInput) — display: "Actions to use"; required: true; options: []; default: []; info: The actions to pass to agent to execute

- **Output ports**:
  - `tools` (Output) — display: "Tools"; method: `build_tool`

### GmailAPIComponent

- **Class**: `GmailAPIComponent`
- **Source**: `composio/gmail_api.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `entity_id` (MessageTextInput) — display: "Entity ID"; default: 'default'
  - `api_key` (SecretStrInput) — display: "Composio API Key"; required: true; info: Refer to https://docs.composio.dev/faq/api_key/api_key
  - `auth_link` (LinkInput) — display: "Authentication Link"; default: ''; info: Click to authenticate with OAuth2
  - `auth_status` (StrInput) — display: "Auth Status"; default: 'Not Connected'; info: Current authentication status
  - `action` (DropdownInput) — display: "Action"; required: true; options: []; default: ''; info: Select Gmail action to pass to the agent
  - `recipient_email` (MessageTextInput) — display: "Recipient Email"; required: true; info: Email address of the recipient
  - `subject` (MessageTextInput) — display: "Subject"; required: true; info: Subject of the email
  - `body` (MessageTextInput) — display: "Body"; required: true; info: Content of the email
  - `max_results` (IntInput) — display: "Max Results"; required: true; info: Maximum number of emails to be returned
  - `message_id` (MessageTextInput) — display: "Message ID"; required: true; info: The ID of the specific email message
  - `thread_id` (StrInput) — display: "Thread ID"; required: true; info: The ID of the email thread
  - `query` (MessageTextInput) — display: "Query"; info: Search query to filter emails (e.g., 'from:someone@email.com' or 'subject:hello')
  - `message_body` (MessageTextInput) — display: "Message Body"; info: The body content of the message to be sent
  - `label_name` (MessageTextInput) — display: "Label Name"; info: Name of the Gmail label to create, modify, or filter by
  - `label_id` (MessageTextInput) — display: "Label ID"; info: The ID of the Gmail label
  - `cc` (MessageTextInput) — display: "CC"; info: Email addresses to CC (Carbon Copy) in the email, separated by commas
  - `bcc` (MessageTextInput) — display: "BCC"; info: Email addresses to BCC (Blid Carbon Copy) in the email, separated by commas
  - `is_html` (BoolInput) — display: "Is HTML"; default: False; info: Specify whether the email body contains HTML content (true/false)
  - `page_token` (MessageTextInput) — display: "Page Token"; info: Token for retrieving the next page of results
  - `label_ids` (MessageTextInput) — display: "Label Ids"; info: Comma-separated list of label IDs to filter messages
  - `include_spam_trash` (BoolInput) — display: "Include messages from Spam/Trash"; default: False; info: Include messages from SPAM and TRASH in the results
  - `format` (MessageTextInput) — display: "Format"; info: The format to return the message in. Possible values: minimal, full, raw, metadata
  - `label_list_visibility` (MessageTextInput) — display: "Label List Visibility"; info: The visibility of the label in the label list in the Gmail web interface. Possible values: 'labelShow' to show the label in the label list, 'labelShowIfUnread' to show the label if there are any unread messages with that label, 'labelHide' to not show the label in the label list
  - `message_list_visibility` (MessageTextInput) — display: "Message List Visibility"; info: The visibility of the label in the message list in the Gmail web interface. Possible values: 'show' to show the label in the message list, 'hide' to not show the label in the message list
  - `resource_name` (MessageTextInput) — display: "Resource Name"; info: The resource name of the person to provide information about. To get information about a google account, specify 'people/account_id'
  - `person_fields` (MessageTextInput) — display: "Person fields"; info: A field mask to restrict which fields on the person are returned. Multiple fields can be specified by separating them with commas.Valid values are: addresses, ageRanges, biographies, birthdays, calendarUrls, clientData, coverPhotos, email Addresses etc
  - `attachment_id` (MessageTextInput) — display: "Attachment ID"; required: true; info: Id of the attachment
  - `file_name` (MessageTextInput) — display: "File name"; required: true; info: File name of the attachment file
  - `attachment` (FileInput) — display: "Add Attachment"; info: Add an attachment

- **Output ports**:
  - `text` (Output) — display: "Response"; method: `execute_action`

## confluence (2 node types)

### Confluence

- **Class**: `ConfluenceComponent`
- **Source**: `confluence/confluence.py`
- **Description**: Confluence wiki collaboration platform

- **Input/configuration ports**:
  - `url` (StrInput) — display: "Site URL"; required: true; info: The base URL of the Confluence Space. Example: https://<company>.atlassian.net/wiki.
  - `username` (StrInput) — display: "Username"; required: true; info: Atlassian User E-mail. Example: email@example.com
  - `api_key` (SecretStrInput) — display: "API Key"; required: true; info: Atlassian Key. Create at: https://id.atlassian.com/manage-profile/security/api-tokens
  - `space_key` (StrInput) — display: "Space Key"; required: true
  - `cloud` (BoolInput) — display: "Use Cloud?"; required: true; default: True
  - `content_format` (DropdownInput) — display: "Content Format"; required: true; options: [ContentFormat.EDITOR.value, ContentFormat.EXPORT_VIEW.value, ContentFormat.ANONYMOUS_EXPORT_VIEW.value, ContentFormat.STORAGE.value, ContentFormat.VIEW.value]; default: ContentFormat.STORAGE.value; info: Specify content format, defaults to ContentFormat.STORAGE
  - `max_pages` (IntInput) — display: "Max Pages"; required: false; default: 1000; info: Maximum number of pages to retrieve in total, defaults 1000

- **Output ports**:
  - `data` (Output) — display: "Data"; method: `load_documents`

### Confluence Knowledge Base

- **Class**: `ConfluenceKnowledgeBaseComponent`
- **Source**: `confluence/confluence_knowledge_base.py`
- **Description**: Confluence-based knowledge base loader supporting cloud and on-prem deployments.

- **Input/configuration ports**:
  - `url` (StrInput) — display: "Site URL"; required: true; info: The base URL of the Confluence Space. Example: https://<company>.atlassian.net/wiki.
  - `username` (StrInput) — display: "Username"; required: true; info: Atlassian User E-mail. Example: email@example.com
  - `api_key` (SecretStrInput) — display: "API Key"; required: true; info: Atlassian Key. Create at: https://id.atlassian.com/manage-profile/security/api-tokens
  - `space_key` (StrInput) — display: "Space Key"; required: true
  - `cloud` (BoolInput) — display: "Use Cloud?"; required: true; default: True
  - `content_format` (DropdownInput) — display: "Content Format"; required: true; options: [ContentFormat.EDITOR.value, ContentFormat.EXPORT_VIEW.value, ContentFormat.ANONYMOUS_EXPORT_VIEW.value, ContentFormat.STORAGE.value, ContentFormat.VIEW.value]; default: ContentFormat.STORAGE.value; info: Specify content format, defaults to ContentFormat.STORAGE
  - `max_pages` (IntInput) — display: "Max Pages"; required: false; default: 1000; info: Maximum number of pages to retrieve in total, defaults 1000

- **Output ports**:
  - `data` (Output) — display: "Data"; method: `load_documents`

## crewai (6 node types)

### CrewAI Agent

- **Class**: `CrewAIAgentComponent`
- **Source**: `crewai/crewai.py`
- **Description**: Represents an agent of CrewAI.

- **Input/configuration ports**:
  - `role` (MultilineInput) — display: "Role"; info: The role of the agent.
  - `goal` (MultilineInput) — display: "Goal"; info: The objective of the agent.
  - `backstory` (MultilineInput) — display: "Backstory"; info: The backstory of the agent.
  - `tools` (HandleInput) — display: "Tools"; input_types: ['Tool']; default: []; info: Tools at agents disposal
  - `llm` (HandleInput) — display: "Language Model"; input_types: ['LanguageModel']; info: Language model that will run the agent.
  - `memory` (BoolInput) — display: "Memory"; default: True; info: Whether the agent should have memory or not
  - `verbose` (BoolInput) — display: "Verbose"; default: False
  - `allow_delegation` (BoolInput) — display: "Allow Delegation"; default: True; info: Whether the agent is allowed to delegate tasks to other agents.
  - `allow_code_execution` (BoolInput) — display: "Allow Code Execution"; default: False; info: Whether the agent is allowed to execute code.
  - `kwargs` (DictInput) — display: "kwargs"; info: kwargs of agent.

- **Output ports**:
  - `output` (Output) — display: "Agent"; method: `build_output`

### HierarchicalCrewComponent

- **Class**: `HierarchicalCrewComponent`
- **Source**: `crewai/hierarchical_crew.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `agents` (HandleInput) — display: "Agents"; input_types: ['Agent']
  - `tasks` (HandleInput) — display: "Tasks"; input_types: ['HierarchicalTask']
  - `manager_llm` (HandleInput) — display: "Manager LLM"; required: false; input_types: ['LanguageModel']
  - `manager_agent` (HandleInput) — display: "Manager Agent"; required: false; input_types: ['Agent']

- **Output ports**:
  - _No class-level outputs declared._

### HierarchicalTaskComponent

- **Class**: `HierarchicalTaskComponent`
- **Source**: `crewai/hierarchical_task.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `task_description` (MultilineInput) — display: "Description"; info: Descriptive text detailing task's purpose and execution.
  - `expected_output` (MultilineInput) — display: "Expected Output"; info: Clear definition of expected task outcome.
  - `tools` (HandleInput) — display: "Tools"; required: false; input_types: ['Tool']; info: List of tools/resources limited for task execution. Uses the Agent tools by default.

- **Output ports**:
  - `task_output` (Output) — display: "Task"; method: `build_task`

### Sequential Task Agent

- **Class**: `SequentialTaskAgentComponent`
- **Source**: `crewai/sequential_task_agent.py`
- **Description**: Creates a CrewAI Task and its associated Agent.

- **Input/configuration ports**:
  - `role` (MultilineInput) — display: "Role"; info: The role of the agent.
  - `goal` (MultilineInput) — display: "Goal"; info: The objective of the agent.
  - `backstory` (MultilineInput) — display: "Backstory"; info: The backstory of the agent.
  - `tools` (HandleInput) — display: "Tools"; input_types: ['Tool']; default: []; info: Tools at agent's disposal
  - `llm` (HandleInput) — display: "Language Model"; input_types: ['LanguageModel']; info: Language model that will run the agent.
  - `memory` (BoolInput) — display: "Memory"; default: True; info: Whether the agent should have memory or not
  - `verbose` (BoolInput) — display: "Verbose"; default: True
  - `allow_delegation` (BoolInput) — display: "Allow Delegation"; default: False; info: Whether the agent is allowed to delegate tasks to other agents.
  - `allow_code_execution` (BoolInput) — display: "Allow Code Execution"; default: False; info: Whether the agent is allowed to execute code.
  - `agent_kwargs` (DictInput) — display: "Agent kwargs"; info: Additional kwargs for the agent.
  - `task_description` (MultilineInput) — display: "Task Description"; info: Descriptive text detailing task's purpose and execution.
  - `expected_output` (MultilineInput) — display: "Expected Task Output"; info: Clear definition of expected task outcome.
  - `async_execution` (BoolInput) — display: "Async Execution"; default: False; info: Boolean flag indicating asynchronous task execution.
  - `previous_task` (HandleInput) — display: "Previous Task"; required: false; input_types: ['SequentialTask']; info: The previous task in the sequence (for chaining).

- **Output ports**:
  - `task_output` (Output) — display: "Sequential Task"; method: `build_agent_and_task`

### SequentialCrewComponent

- **Class**: `SequentialCrewComponent`
- **Source**: `crewai/sequential_crew.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `tasks` (HandleInput) — display: "Tasks"; input_types: ['SequentialTask']

- **Output ports**:
  - _No class-level outputs declared._

### SequentialTaskComponent

- **Class**: `SequentialTaskComponent`
- **Source**: `crewai/sequential_task.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `task_description` (MultilineInput) — display: "Description"; info: Descriptive text detailing task's purpose and execution.
  - `expected_output` (MultilineInput) — display: "Expected Output"; info: Clear definition of expected task outcome.
  - `tools` (HandleInput) — display: "Tools"; required: false; input_types: ['Tool']; info: List of tools/resources limited for task execution. Uses the Agent tools by default.
  - `agent` (HandleInput) — display: "Agent"; required: true; input_types: ['Agent']; info: CrewAI Agent that will perform the task
  - `task` (HandleInput) — display: "Task"; input_types: ['SequentialTask']; info: CrewAI Task that will perform the task
  - `async_execution` (BoolInput) — display: "Async Execution"; default: True; info: Boolean flag indicating asynchronous task execution.

- **Output ports**:
  - `task_output` (Output) — display: "Task"; method: `build_task`

## custom_component (1 node types)

### Custom Component

- **Class**: `CustomComponent`
- **Source**: `custom_component/custom_component.py`
- **Description**: Use as a template to create your own component.

- **Input/configuration ports**:
  - `input_value` (MessageTextInput) — display: "Input Value"; default: 'Hello, World!'; info: This is a custom component Input

- **Output ports**:
  - `output` (Output) — display: "Output"; method: `build_output`

## data (9 node types)

### API Request

- **Class**: `APIRequestComponent`
- **Source**: `data/api_request.py`
- **Description**: Make HTTP requests using URLs or cURL commands.

- **Input/configuration ports**:
  - `urls` (MessageTextInput) — display: "URLs"; info: Enter one or more URLs, separated by commas.
  - `curl` (MultilineInput) — display: "cURL"; info: Paste a curl command to populate the fields. This will fill in the dictionary fields for headers and body.
  - `method` (DropdownInput) — display: "Method"; options: ['GET', 'POST', 'PATCH', 'PUT', 'DELETE']; info: The HTTP method to use.
  - `use_curl` (BoolInput) — display: "Use cURL"; default: False; info: Enable cURL mode to populate fields from a cURL command.
  - `query_params` (DataInput) — display: "Query Parameters"; info: The query parameters to append to the URL.
  - `body` (TableInput) — display: "Body"; input_types: ['Data']; default: []; info: The body to send with the request as a dictionary (for POST, PATCH, PUT).
  - `headers` (TableInput) — display: "Headers"; input_types: ['Data']; default: []; info: The headers to send with the request as a dictionary.
  - `timeout` (IntInput) — display: "Timeout"; default: 5; info: The timeout to use for the request.
  - `follow_redirects` (BoolInput) — display: "Follow Redirects"; default: True; info: Whether to follow http redirects.
  - `save_to_file` (BoolInput) — display: "Save to File"; default: False; info: Save the API response to a temporary file
  - `include_httpx_metadata` (BoolInput) — display: "Include HTTPx Metadata"; default: False; info: Include properties such as headers, status_code, response_headers, and redirection_history in the output.

- **Output ports**:
  - `data` (Output) — display: "Data"; method: `make_requests`
  - `dataframe` (Output) — display: "DataFrame"; method: `as_dataframe`

### Directory

- **Class**: `DirectoryComponent`
- **Source**: `data/directory.py`
- **Description**: Recursively load files from a directory.

- **Input/configuration ports**:
  - `path` (MessageTextInput) — display: "Path"; default: '.'; info: Path to the directory to load files from. Defaults to current directory ('.')
  - `types` (MultiselectInput) — display: "File Types"; options: TEXT_FILE_TYPES; default: []; info: File types to load. Select one or more types or leave empty to load all supported types.
  - `depth` (IntInput) — display: "Depth"; default: 0; info: Depth to search for files.
  - `max_concurrency` (IntInput) — display: "Max Concurrency"; default: 2; info: Maximum concurrency for loading files.
  - `load_hidden` (BoolInput) — display: "Load Hidden"; info: If true, hidden files will be loaded.
  - `recursive` (BoolInput) — display: "Recursive"; info: If true, the search will be recursive.
  - `silent_errors` (BoolInput) — display: "Silent Errors"; info: If true, errors will not raise an exception.
  - `use_multithreading` (BoolInput) — display: "Use Multithreading"; info: If true, multithreading will be used.

- **Output ports**:
  - `data` (Output) — display: "Data"; method: `load_directory`
  - `dataframe` (Output) — display: "DataFrame"; method: `as_dataframe`

### File

- **Class**: `FileComponent`
- **Source**: `data/file.py`
- **Description**: Load a file to be used in your project.

- **Input/configuration ports**:
  - `use_multithreading` (BoolInput) — display: "[Deprecated] Use Multithreading"; default: True; info: Set 'Processing Concurrency' greater than 1 to enable multithreading.
  - `concurrency_multithreading` (IntInput) — display: "Processing Concurrency"; default: 1; info: When multiple files are being processed, the number of files to process concurrently.

- **Output ports**:
  - _No class-level outputs declared._

### Load CSV

- **Class**: `CSVToDataComponent`
- **Source**: `data/csv_to_data.py`
- **Description**: Load a CSV file, CSV from a file path, or a valid CSV string and convert it to a list of Data

- **Input/configuration ports**:
  - `csv_file` (FileInput) — display: "CSV File"; info: Upload a CSV file to convert to a list of Data objects
  - `csv_path` (MessageTextInput) — display: "CSV File Path"; info: Provide the path to the CSV file as pure text
  - `csv_string` (MultilineInput) — display: "CSV String"; info: Paste a CSV string directly to convert to a list of Data objects
  - `text_key` (MessageTextInput) — display: "Text Key"; default: 'text'; info: The key to use for the text column. Defaults to 'text'.

- **Output ports**:
  - `data_list` (Output) — display: "Data List"; method: `load_csv_to_data`

### Load JSON

- **Class**: `JSONToDataComponent`
- **Source**: `data/json_to_data.py`
- **Description**: Convert a JSON file, JSON from a file path, or a JSON string to a Data object or a list of Data objects

- **Input/configuration ports**:
  - `json_file` (FileInput) — display: "JSON File"; info: Upload a JSON file to convert to a Data object or list of Data objects
  - `json_path` (MessageTextInput) — display: "JSON File Path"; info: Provide the path to the JSON file as pure text
  - `json_string` (MultilineInput) — display: "JSON String"; info: Enter a valid JSON string (object or array) to convert to a Data object or list of Data objects

- **Output ports**:
  - `data` (Output) — display: "Data"; method: `convert_json_to_data`

### S3 Bucket Uploader

- **Class**: `S3BucketUploaderComponent`
- **Source**: `data/s3_bucket_uploader.py`
- **Description**: Uploads files to S3 bucket.

- **Input/configuration ports**:
  - `aws_access_key_id` (SecretStrInput) — display: "AWS Access Key ID"; required: true; info: AWS Access key ID.
  - `aws_secret_access_key` (SecretStrInput) — display: "AWS Secret Key"; required: true; info: AWS Secret Key.
  - `bucket_name` (StrInput) — display: "Bucket Name"; info: Enter the name of the bucket.
  - `strategy` (DropdownInput) — display: "Strategy for file upload"; options: ['Store Data', 'Store Original File']; default: 'By Data'; info: Choose the strategy to upload the file. By Data means that the source file is parsed and stored as LangFlow data. By File Name means that the source file is uploaded as is.
  - `data_inputs` (HandleInput) — display: "Data Inputs"; required: true; input_types: ['Data']; info: The data to split.
  - `s3_prefix` (StrInput) — display: "S3 Prefix"; info: Prefix for all files.
  - `strip_path` (BoolInput) — display: "Strip Path"; required: true; info: Removes path from file path.

- **Output ports**:
  - `data` (Output) — display: "Writes to AWS Bucket"; method: `process_files`

### SQL Query

- **Class**: `SQLExecutorComponent`
- **Source**: `data/sql_executor.py`
- **Description**: Execute SQL query.

- **Input/configuration ports**:
  - _No class-level inputs declared._

- **Output ports**:
  - _No class-level outputs declared._

### URL

- **Class**: `URLComponent`
- **Source**: `data/url.py`
- **Description**: Load and parse child links from a root URL recursively

- **Input/configuration ports**:
  - `urls` (MessageTextInput) — display: "URLs"; info: Enter one or more URLs to crawl recursively, by clicking the '+' button.
  - `max_depth` (IntInput) — display: "Max Depth"; required: false; default: 1; info: Controls how many 'clicks' away from the initial page the crawler will go: - depth 1: only the initial page - depth 2: initial page + all pages linked directly from it - depth 3: initial page + direct links + links found on those direct link pages Note: This is about link traversal, not URL path depth.
  - `prevent_outside` (BoolInput) — display: "Prevent Outside"; required: false; default: True; info: If enabled, only crawls URLs within the same domain as the root URL. This helps prevent the crawler from going to external websites.
  - `use_async` (BoolInput) — display: "Use Async"; required: false; default: True; info: If enabled, uses asynchronous loading which can be significantly faster but might use more system resources.
  - `format` (DropdownInput) — display: "Output Format"; options: ['Text', 'HTML']; default: 'Text'; info: Output Format. Use 'Text' to extract the text from the HTML or 'HTML' for the raw HTML content.

- **Output ports**:
  - `data` (Output) — display: "Data"; method: `fetch_content`
  - `text` (Output) — display: "Message"; method: `fetch_content_text`
  - `dataframe` (Output) — display: "DataFrame"; method: `as_dataframe`

### Webhook

- **Class**: `WebhookComponent`
- **Source**: `data/webhook.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `data` (MultilineInput) — display: "Payload"; info: Receives a payload from external systems via HTTP POST.
  - `curl` (MultilineInput) — display: "cURL"; input_types: []; default: 'CURL_WEBHOOK'
  - `endpoint` (MultilineInput) — display: "Endpoint"; input_types: []; default: 'BACKEND_URL'

- **Output ports**:
  - `output_data` (Output) — display: "Data"; method: `build_data`

## embeddings (16 node types)

### AI/ML Embeddings

- **Class**: `AIMLEmbeddingsComponent`
- **Source**: `embeddings/aiml.py`
- **Description**: Generate embeddings using the AI/ML API.

- **Input/configuration ports**:
  - `model_name` (DropdownInput) — display: "Model Name"; required: true; options: ['text-embedding-3-small', 'text-embedding-3-large', 'text-embedding-ada-002']
  - `aiml_api_key` (SecretStrInput) — display: "AI/ML API Key"; required: true; default: 'AIML_API_KEY'

- **Output ports**:
  - _No class-level outputs declared._

### AmazonBedrockEmbeddingsComponent

- **Class**: `AmazonBedrockEmbeddingsComponent`
- **Source**: `embeddings/amazon_bedrock.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `model_id` (DropdownInput) — display: "Model Id"; options: AWS_EMBEDDING_MODEL_IDS; default: 'amazon.titan-embed-text-v1'
  - `aws_access_key_id` (SecretStrInput) — display: "AWS Access Key ID"; required: true; default: 'AWS_ACCESS_KEY_ID'; info: The access key for your AWS account.Usually set in Python code as the environment variable 'AWS_ACCESS_KEY_ID'.
  - `aws_secret_access_key` (SecretStrInput) — display: "AWS Secret Access Key"; required: true; default: 'AWS_SECRET_ACCESS_KEY'; info: The secret key for your AWS account. Usually set in Python code as the environment variable 'AWS_SECRET_ACCESS_KEY'.
  - `aws_session_token` (SecretStrInput) — display: "AWS Session Token"; default: 'AWS_SESSION_TOKEN'; info: The session key for your AWS account. Only needed for temporary credentials. Usually set in Python code as the environment variable 'AWS_SESSION_TOKEN'.
  - `credentials_profile_name` (SecretStrInput) — display: "Credentials Profile Name"; default: 'AWS_CREDENTIALS_PROFILE_NAME'; info: The name of the profile to use from your ~/.aws/credentials file. If not provided, the default profile will be used.
  - `region_name` (DropdownInput) — display: "Region Name"; options: AWS_REGIONS; default: 'us-east-1'; info: The AWS region where your Bedrock resources are located.
  - `endpoint_url` (MessageTextInput) — display: "Endpoint URL"; info: The URL of the AWS Bedrock endpoint to use.

- **Output ports**:
  - `embeddings` (Output) — display: "Embeddings"; method: `build_embeddings`

### AstraVectorizeComponent

- **Class**: `AstraVectorizeComponent`
- **Source**: `embeddings/astra_vectorize.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `provider` (DropdownInput) — display: "Provider"; required: true; options: VECTORIZE_PROVIDERS_MAPPING.keys(); default: ''
  - `model_name` (MessageTextInput) — display: "Model Name"; required: true
  - `api_key_name` (MessageTextInput) — display: "API Key name"; info: The name of the embeddings provider API key stored on Astra. If set, it will override the 'ProviderKey' in the authentication parameters.
  - `authentication` (DictInput) — display: "Authentication parameters"
  - `provider_api_key` (SecretStrInput) — display: "Provider API Key"; info: An alternative to the Astra Authentication that passes an API key for the provider with each request to Astra DB. This may be used when Vectorize is configured for the collection, but no corresponding provider secret is stored within Astra's key management system.
  - `authentication` (DictInput) — display: "Authentication Parameters"
  - `model_parameters` (DictInput) — display: "Model Parameters"

- **Output ports**:
  - `config` (Output) — display: "Vectorize"; method: `build_options`; types: ['dict']

### AzureOpenAIEmbeddingsComponent

- **Class**: `AzureOpenAIEmbeddingsComponent`
- **Source**: `embeddings/azure_openai.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `model` (DropdownInput) — display: "Model"; options: OPENAI_EMBEDDING_MODEL_NAMES; default: OPENAI_EMBEDDING_MODEL_NAMES[0]
  - `azure_endpoint` (MessageTextInput) — display: "Azure Endpoint"; required: true; info: Your Azure endpoint, including the resource. Example: `https://example-resource.azure.openai.com/`
  - `azure_deployment` (MessageTextInput) — display: "Deployment Name"; required: true
  - `api_version` (DropdownInput) — display: "API Version"; options: API_VERSION_OPTIONS; default: API_VERSION_OPTIONS[-1]
  - `api_key` (SecretStrInput) — display: "API Key"; required: true
  - `dimensions` (IntInput) — display: "Dimensions"; info: The number of dimensions the resulting output embeddings should have. Only supported by certain models.

- **Output ports**:
  - `embeddings` (Output) — display: "Embeddings"; method: `build_embeddings`

### CloudflareWorkersAIEmbeddingsComponent

- **Class**: `CloudflareWorkersAIEmbeddingsComponent`
- **Source**: `embeddings/cloudflare.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `account_id` (MessageTextInput) — display: "Cloudflare account ID"; required: true; info: Find your account ID https://developers.cloudflare.com/fundamentals/setup/find-account-and-zone-ids/#find-account-id-workers-and-pages
  - `api_token` (SecretStrInput) — display: "Cloudflare API token"; required: true; info: Create an API token https://developers.cloudflare.com/fundamentals/api/get-started/create-token/
  - `model_name` (MessageTextInput) — display: "Model Name"; required: true; default: '@cf/baai/bge-base-en-v1.5'; info: List of supported models https://developers.cloudflare.com/workers-ai/models/#text-embeddings
  - `strip_new_lines` (BoolInput) — display: "Strip New Lines"; default: True
  - `batch_size` (IntInput) — display: "Batch Size"; default: 50
  - `api_base_url` (MessageTextInput) — display: "Cloudflare API base URL"; default: 'https://api.cloudflare.com/client/v4/accounts'
  - `headers` (DictInput) — display: "Headers"; info: Additional request headers

- **Output ports**:
  - `embeddings` (Output) — display: "Embeddings"; method: `build_embeddings`

### Cohere Embeddings

- **Class**: `CohereEmbeddingsComponent`
- **Source**: `embeddings/cohere.py`
- **Description**: Generate embeddings using Cohere models.

- **Input/configuration ports**:
  - `api_key` (SecretStrInput) — display: "Cohere API Key"; required: true
  - `model_name` (DropdownInput) — display: "Model"; options: ['embed-english-v2.0', 'embed-multilingual-v2.0', 'embed-english-light-v2.0', 'embed-multilingual-light-v2.0']; default: 'embed-english-v2.0'
  - `truncate` (MessageTextInput) — display: "Truncate"
  - `max_retries` (IntInput) — display: "Max Retries"; default: 3
  - `user_agent` (MessageTextInput) — display: "User Agent"; default: 'langchain'
  - `request_timeout` (FloatInput) — display: "Request Timeout"

- **Output ports**:
  - `embeddings` (Output) — display: "Embeddings"; method: `build_embeddings`

### EmbeddingSimilarityComponent

- **Class**: `EmbeddingSimilarityComponent`
- **Source**: `embeddings/similarity.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `embedding_vectors` (DataInput) — display: "Embedding Vectors"; required: true; info: A list containing exactly two data objects with embedding vectors to compare.
  - `similarity_metric` (DropdownInput) — display: "Similarity Metric"; options: ['Cosine Similarity', 'Euclidean Distance', 'Manhattan Distance']; default: 'Cosine Similarity'; info: Select the similarity metric to use.

- **Output ports**:
  - `similarity_data` (Output) — display: "Similarity Data"; method: `compute_similarity`

### Google Generative AI Embeddings

- **Class**: `GoogleGenerativeAIEmbeddingsComponent`
- **Source**: `embeddings/google_generative_ai.py`
- **Description**: Connect to Google's generative AI embeddings service using the GoogleGenerativeAIEmbeddings class, found in the langchain-google-genai package.

- **Input/configuration ports**:
  - `api_key` (SecretStrInput) — display: "API Key"; required: true
  - `model_name` (MessageTextInput) — display: "Model Name"; default: 'models/text-embedding-004'

- **Output ports**:
  - `embeddings` (Output) — display: "Embeddings"; method: `build_embeddings`

### HuggingFace Embeddings Inference

- **Class**: `HuggingFaceInferenceAPIEmbeddingsComponent`
- **Source**: `embeddings/huggingface_inference_api.py`
- **Description**: Generate embeddings using HuggingFace Text Embeddings Inference (TEI)

- **Input/configuration ports**:
  - `api_key` (SecretStrInput) — display: "API Key"; info: Required for non-local inference endpoints. Local inference does not require an API Key.
  - `inference_endpoint` (MessageTextInput) — display: "Inference Endpoint"; required: true; default: 'https://api-inference.huggingface.co/models/'; info: Custom inference endpoint URL.
  - `model_name` (MessageTextInput) — display: "Model Name"; required: true; default: 'BAAI/bge-large-en-v1.5'; info: The name of the model to use for text embeddings.

- **Output ports**:
  - `embeddings` (Output) — display: "Embeddings"; method: `build_embeddings`

### LMStudioEmbeddingsComponent

- **Class**: `LMStudioEmbeddingsComponent`
- **Source**: `embeddings/lmstudioembeddings.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `model` (DropdownInput) — display: "Model"; required: true
  - `base_url` (MessageTextInput) — display: "LM Studio Base URL"; required: true; default: 'http://localhost:1234/v1'
  - `api_key` (SecretStrInput) — display: "LM Studio API Key"; default: 'LMSTUDIO_API_KEY'
  - `temperature` (FloatInput) — display: "Model Temperature"; default: 0.1

- **Output ports**:
  - _No class-level outputs declared._

### MistralAI Embeddings

- **Class**: `MistralAIEmbeddingsComponent`
- **Source**: `embeddings/mistral.py`
- **Description**: Generate embeddings using MistralAI models.

- **Input/configuration ports**:
  - `model` (DropdownInput) — display: "Model"; options: ['mistral-embed']; default: 'mistral-embed'
  - `mistral_api_key` (SecretStrInput) — display: "Mistral API Key"; required: true
  - `max_concurrent_requests` (IntInput) — display: "Max Concurrent Requests"; default: 64
  - `max_retries` (IntInput) — display: "Max Retries"; default: 5
  - `timeout` (IntInput) — display: "Request Timeout"; default: 120
  - `endpoint` (MessageTextInput) — display: "API Endpoint"; default: 'https://api.mistral.ai/v1/'

- **Output ports**:
  - `embeddings` (Output) — display: "Embeddings"; method: `build_embeddings`

### NVIDIAEmbeddingsComponent

- **Class**: `NVIDIAEmbeddingsComponent`
- **Source**: `embeddings/nvidia.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `model` (DropdownInput) — display: "Model"; required: true; options: ['nvidia/nv-embed-v1', 'snowflake/arctic-embed-I']; default: 'nvidia/nv-embed-v1'
  - `base_url` (MessageTextInput) — display: "NVIDIA Base URL"; required: true; default: 'https://integrate.api.nvidia.com/v1'
  - `nvidia_api_key` (SecretStrInput) — display: "NVIDIA API Key"; required: true; default: 'NVIDIA_API_KEY'; info: The NVIDIA API Key.
  - `temperature` (FloatInput) — display: "Model Temperature"; default: 0.1

- **Output ports**:
  - _No class-level outputs declared._

### OllamaEmbeddingsComponent

- **Class**: `OllamaEmbeddingsComponent`
- **Source**: `embeddings/ollama.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `model_name` (DropdownInput) — display: "Ollama Model"; required: true; options: []; default: ''
  - `base_url` (MessageTextInput) — display: "Ollama Base URL"; required: true; default: ''

- **Output ports**:
  - `embeddings` (Output) — display: "Embeddings"; method: `build_embeddings`

### OpenAI Embeddings

- **Class**: `OpenAIEmbeddingsComponent`
- **Source**: `embeddings/openai.py`
- **Description**: Generate embeddings using OpenAI models.

- **Input/configuration ports**:
  - `default_headers` (DictInput) — display: "Default Headers"; info: Default headers to use for the API request.
  - `default_query` (DictInput) — display: "Default Query"; info: Default query parameters to use for the API request.
  - `chunk_size` (IntInput) — display: "Chunk Size"; default: 1000
  - `client` (MessageTextInput) — display: "Client"
  - `deployment` (MessageTextInput) — display: "Deployment"
  - `embedding_ctx_length` (IntInput) — display: "Embedding Context Length"; default: 1536
  - `max_retries` (IntInput) — display: "Max Retries"; default: 3
  - `model` (DropdownInput) — display: "Model"; options: OPENAI_EMBEDDING_MODEL_NAMES; default: 'text-embedding-3-small'
  - `model_kwargs` (DictInput) — display: "Model Kwargs"
  - `openai_api_key` (SecretStrInput) — display: "OpenAI API Key"; required: true; default: 'OPENAI_API_KEY'
  - `openai_api_base` (MessageTextInput) — display: "OpenAI API Base"
  - `openai_api_type` (MessageTextInput) — display: "OpenAI API Type"
  - `openai_api_version` (MessageTextInput) — display: "OpenAI API Version"
  - `openai_organization` (MessageTextInput) — display: "OpenAI Organization"
  - `openai_proxy` (MessageTextInput) — display: "OpenAI Proxy"
  - `request_timeout` (FloatInput) — display: "Request Timeout"
  - `show_progress_bar` (BoolInput) — display: "Show Progress Bar"
  - `skip_empty` (BoolInput) — display: "Skip Empty"
  - `tiktoken_model_name` (MessageTextInput) — display: "TikToken Model Name"
  - `tiktoken_enable` (BoolInput) — display: "TikToken Enable"; default: True; info: If False, you must have transformers installed.
  - `dimensions` (IntInput) — display: "Dimensions"; info: The number of dimensions the resulting output embeddings should have. Only supported by certain models.

- **Output ports**:
  - _No class-level outputs declared._

### TextEmbedderComponent

- **Class**: `TextEmbedderComponent`
- **Source**: `embeddings/text_embedder.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `embedding_model` (HandleInput) — display: "Embedding Model"; required: true; input_types: ['Embeddings']; info: The embedding model to use for generating embeddings.
  - `message` (MessageInput) — display: "Message"; required: true; info: The message to generate embeddings for.

- **Output ports**:
  - `embeddings` (Output) — display: "Embedding Data"; method: `generate_embeddings`

### VertexAI Embeddings

- **Class**: `VertexAIEmbeddingsComponent`
- **Source**: `embeddings/vertexai.py`
- **Description**: Generate embeddings using Google Cloud VertexAI models.

- **Input/configuration ports**:
  - `credentials` (FileInput) — display: "Credentials"; required: true; default: ''; info: JSON credentials file. Leave empty to fallback to environment variables
  - `location` (MessageTextInput) — display: "Location"; default: 'us-central1'
  - `project` (MessageTextInput) — display: "Project"; info: The project ID.
  - `max_output_tokens` (IntInput) — display: "Max Output Tokens"
  - `max_retries` (IntInput) — display: "Max Retries"; default: 1
  - `model_name` (MessageTextInput) — display: "Model Name"; required: true; default: 'textembedding-gecko'
  - `n` (IntInput) — display: "N"; default: 1
  - `request_parallelism` (IntInput) — display: "Request Parallelism"; default: 5
  - `stop_sequences` (MessageTextInput) — display: "Stop"
  - `streaming` (BoolInput) — display: "Streaming"; default: False
  - `temperature` (FloatInput) — display: "Temperature"; default: 0.0
  - `top_k` (IntInput) — display: "Top K"
  - `top_p` (FloatInput) — display: "Top P"; default: 0.95

- **Output ports**:
  - `embeddings` (Output) — display: "Embeddings"; method: `build_embeddings`

## firecrawl (4 node types)

### FirecrawlCrawlApi

- **Class**: `FirecrawlCrawlApi`
- **Source**: `firecrawl/firecrawl_crawl_api.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `api_key` (SecretStrInput) — display: "API Key"; required: true; info: The API key to use Firecrawl API.
  - `url` (MultilineInput) — display: "URL"; required: true; info: The URL to scrape.
  - `timeout` (IntInput) — display: "Timeout"; info: Timeout in milliseconds for the request.
  - `idempotency_key` (StrInput) — display: "Idempotency Key"; info: Optional idempotency key to ensure unique requests.
  - `crawlerOptions` (DataInput) — display: "Crawler Options"; info: The crawler options to send with the request.
  - `scrapeOptions` (DataInput) — display: "Scrape Options"; info: The page options to send with the request.

- **Output ports**:
  - `data` (Output) — display: "Data"; method: `crawl`

### FirecrawlExtractApi

- **Class**: `FirecrawlExtractApi`
- **Source**: `firecrawl/firecrawl_extract_api.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `api_key` (SecretStrInput) — display: "API Key"; required: true; info: The API key to use Firecrawl API.
  - `urls` (MultilineInput) — display: "URLs"; required: true; info: List of URLs to extract data from (separated by commas or new lines).
  - `prompt` (MultilineInput) — display: "Prompt"; required: true; info: Prompt to guide the extraction process.
  - `schema` (DataInput) — display: "Schema"; required: false; info: Schema to define the structure of the extracted data.
  - `enable_web_search` (BoolInput) — display: "Enable Web Search"; info: When true, the extraction will use web search to find additional data.

- **Output ports**:
  - `data` (Output) — display: "Data"; method: `extract`

### FirecrawlMapApi

- **Class**: `FirecrawlMapApi`
- **Source**: `firecrawl/firecrawl_map_api.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `api_key` (SecretStrInput) — display: "API Key"; required: true; info: The API key to use Firecrawl API.
  - `urls` (MultilineInput) — display: "URLs"; required: true; info: List of URLs to create maps from (separated by commas or new lines).
  - `ignore_sitemap` (BoolInput) — display: "Ignore Sitemap"; info: When true, the sitemap.xml file will be ignored during crawling.
  - `sitemap_only` (BoolInput) — display: "Sitemap Only"; info: When true, only links found in the sitemap will be returned.
  - `include_subdomains` (BoolInput) — display: "Include Subdomains"; info: When true, subdomains of the provided URL will also be scanned.

- **Output ports**:
  - `data` (Output) — display: "Data"; method: `map`

### FirecrawlScrapeApi

- **Class**: `FirecrawlScrapeApi`
- **Source**: `firecrawl/firecrawl_scrape_api.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `api_key` (SecretStrInput) — display: "API Key"; required: true; info: The API key to use Firecrawl API.
  - `url` (MultilineInput) — display: "URL"; required: true; info: The URL to scrape.
  - `timeout` (IntInput) — display: "Timeout"; info: Timeout in milliseconds for the request.
  - `scrapeOptions` (DataInput) — display: "Scrape Options"; info: The page options to send with the request.
  - `extractorOptions` (DataInput) — display: "Extractor Options"; info: The extractor options to send with the request.

- **Output ports**:
  - `data` (Output) — display: "Data"; method: `scrape`

## git (2 node types)

### Git

- **Class**: `GitLoaderComponent`
- **Source**: `git/git.py`
- **Description**: Load and filter documents from a local or remote Git repository. Use a local repo path or clone from a remote URL.

- **Input/configuration ports**:
  - `repo_source` (DropdownInput) — display: "Repository Source"; required: true; options: ['Local', 'Remote']; info: Select whether to use a local repo path or clone from a remote URL.
  - `repo_path` (MessageTextInput) — display: "Local Repository Path"; required: false; info: The local path to the existing Git repository (used if 'Local' is selected).
  - `clone_url` (MessageTextInput) — display: "Clone URL"; required: false; info: The URL of the Git repository to clone (used if 'Clone' is selected).
  - `branch` (MessageTextInput) — display: "Branch"; required: false; default: 'main'; info: The branch to load files from. Defaults to 'main'.
  - `file_filter` (MessageTextInput) — display: "File Filter"; required: false; info: Patterns to filter files. For example: Include only .py files: '*.py' Exclude .py files: '!*.py' Multiple patterns can be separated by commas.
  - `content_filter` (MessageTextInput) — display: "Content Filter"; required: false; info: A regex pattern to filter files based on their content.

- **Output ports**:
  - `data` (Output) — display: "Data"; method: `load_documents`

### GitExtractor

- **Class**: `GitExtractorComponent`
- **Source**: `git/gitextractor.py`
- **Description**: Analyzes a Git repository and returns file contents and complete repository information

- **Input/configuration ports**:
  - `repository_url` (MessageTextInput) — display: "Repository URL"; default: ''; info: URL of the Git repository (e.g., https://github.com/username/repo)

- **Output ports**:
  - `text_based_file_contents` (Output) — display: "Text-Based File Contents"; method: `get_text_based_file_contents`
  - `directory_structure` (Output) — display: "Directory Structure"; method: `get_directory_structure`
  - `repository_info` (Output) — display: "Repository Info"; method: `get_repository_info`
  - `statistics` (Output) — display: "Statistics"; method: `get_statistics`
  - `files_content` (Output) — display: "Files Content"; method: `get_files_content`

## google (4 node types)

### Gmail Loader

- **Class**: `GmailLoaderComponent`
- **Source**: `google/gmail.py`
- **Description**: Loads emails from Gmail using provided credentials.

- **Input/configuration ports**:
  - `json_string` (SecretStrInput) — display: "JSON String of the Service Account Token"; required: true; default: '{\n "account": "",\n "client_id": "",\n "client_secret": "",\n "expiry": "",\n "refresh_token": "",\n "scopes": [\n "https://www.googleapis.com/auth/gmail.readonly",\n ],\n "token": "",\n "token_uri": "https://oauth2.googleapis.com/token",\n "universe_domain": "googleapis.com"\n }'; info: JSON string containing OAuth 2.0 access token information for service account access
  - `label_ids` (MessageTextInput) — display: "Label IDs"; required: true; default: 'INBOX,SENT,UNREAD,IMPORTANT'; info: Comma-separated list of label IDs to filter emails.
  - `max_results` (MessageTextInput) — display: "Max Results"; required: true; default: '10'; info: Maximum number of emails to load.

- **Output ports**:
  - `data` (Output) — display: "Data"; method: `load_emails`

### Google Drive Loader

- **Class**: `GoogleDriveComponent`
- **Source**: `google/google_drive.py`
- **Description**: Loads documents from Google Drive using provided credentials.

- **Input/configuration ports**:
  - `json_string` (SecretStrInput) — display: "JSON String of the Service Account Token"; required: true; info: JSON string containing OAuth 2.0 access token information for service account access
  - `document_id` (MessageTextInput) — display: "Document ID"; required: true; info: Single Google Drive document ID

- **Output ports**:
  - `docs` (Output) — display: "Loaded Documents"; method: `load_documents`

### Google Drive Search

- **Class**: `GoogleDriveSearchComponent`
- **Source**: `google/google_drive_search.py`
- **Description**: Searches Google Drive files using provided credentials and query parameters.

- **Input/configuration ports**:
  - `token_string` (SecretStrInput) — display: "Token String"; required: true; info: JSON string containing OAuth 2.0 access token information for service account access
  - `query_item` (DropdownInput) — display: "Query Item"; required: true; options: ['name', 'fullText', 'mimeType', 'modifiedTime', 'viewedByMeTime', 'trashed', 'starred', 'parents', 'owners', 'writers', 'readers', 'sharedWithMe', 'createdTime', 'properties', 'appProperties', 'visibility', 'shortcutDetails.targetId']; info: The field to query.
  - `valid_operator` (DropdownInput) — display: "Valid Operator"; required: true; options: ['contains', '=', '!=', '<=', '<', '>', '>=', 'in', 'has']; info: Operator to use in the query.
  - `search_term` (MessageTextInput) — display: "Search Term"; required: true; info: The value to search for in the specified query item.
  - `query_string` (MessageTextInput) — display: "Query String"; default: ''; info: The query string used for searching. You can edit this manually.

- **Output ports**:
  - `doc_urls` (Output) — display: "Document URLs"; method: `search_doc_urls`
  - `doc_ids` (Output) — display: "Document IDs"; method: `search_doc_ids`
  - `doc_titles` (Output) — display: "Document Titles"; method: `search_doc_titles`
  - `Data` (Output) — display: "Data"; method: `search_data`

### Google OAuth Token

- **Class**: `GoogleOAuthToken`
- **Source**: `google/google_oauth_token.py`
- **Description**: Generates a JSON string with your Google OAuth token.

- **Input/configuration ports**:
  - `scopes` (MultilineInput) — display: "Scopes"; required: true; info: Input scopes for your application.
  - `oauth_credentials` (FileInput) — display: "Credentials File"; required: true; info: Input OAuth Credentials file (e.g. credentials.json).

- **Output ports**:
  - `output` (Output) — display: "Output"; method: `build_output`

## helpers (8 node types)

### Batch Run

- **Class**: `BatchRunComponent`
- **Source**: `helpers/batch_run.py`
- **Description**: Runs a language model over each row of a DataFrame's text column and returns a new DataFrame with three columns: '**text_input**' (the original text), '**model_response**' (the model's response),and '**batch_index**' (the processing order).

- **Input/configuration ports**:
  - `model` (HandleInput) — display: "Language Model"; required: true; input_types: ['LanguageModel']; info: Connect the 'Language Model' output from your LLM component here.
  - `system_message` (MultilineInput) — display: "System Message"; required: false; info: Multi-line system instruction for all rows in the DataFrame.
  - `df` (DataFrameInput) — display: "DataFrame"; required: true; info: The DataFrame whose column (specified by 'column_name') we'll treat as text messages.
  - `column_name` (MessageTextInput) — display: "Column Name"; required: true; default: 'text'; info: The name of the DataFrame column to treat as text messages. Default='text'.
  - `enable_metadata` (BoolInput) — display: "Enable Metadata"; required: false; default: True; info: If True, add metadata to the output DataFrame.

- **Output ports**:
  - `batch_results` (Output) — display: "Batch Results"; method: `run_batch`

### Create List

- **Class**: `CreateListComponent`
- **Source**: `helpers/create_list.py`
- **Description**: Creates a list of texts.

- **Input/configuration ports**:
  - `texts` (StrInput) — display: "Texts"; info: Enter one or more texts.

- **Output ports**:
  - `list` (Output) — display: "Data List"; method: `create_list`
  - `dataframe` (Output) — display: "DataFrame"; method: `as_dataframe`

### Current Date

- **Class**: `CurrentDateComponent`
- **Source**: `helpers/current_date.py`
- **Description**: Returns the current date and time in the selected timezone.

- **Input/configuration ports**:
  - `timezone` (DropdownInput) — display: "Timezone"; options: list(available_timezones()); default: 'UTC'; info: Select the timezone for the current date and time.

- **Output ports**:
  - `current_date` (Output) — display: "Current Date"; method: `get_current_date`

### ID Generator

- **Class**: `IDGeneratorComponent`
- **Source**: `helpers/id_generator.py`
- **Description**: Generates a unique ID.

- **Input/configuration ports**:
  - `unique_id` (MessageTextInput) — display: "Value"; info: The generated unique ID.

- **Output ports**:
  - `id` (Output) — display: "ID"; method: `generate_id`

### Message History

- **Class**: `MemoryComponent`
- **Source**: `helpers/memory.py`
- **Description**: Retrieves stored chat messages from Langflow tables or an external memory.

- **Input/configuration ports**:
  - `memory` (HandleInput) — display: "External Memory"; input_types: ['Memory']; info: Retrieve messages from an external memory. If empty, it will use the Langflow tables.
  - `sender` (DropdownInput) — display: "Sender Type"; options: [MESSAGE_SENDER_AI, MESSAGE_SENDER_USER, 'Machine and User']; default: 'Machine and User'; info: Filter by sender type.
  - `sender_name` (MessageTextInput) — display: "Sender Name"; info: Filter by sender name.
  - `n_messages` (IntInput) — display: "Number of Messages"; default: 100; info: Number of messages to retrieve.
  - `session_id` (MessageTextInput) — display: "Session ID"; info: The session ID of the chat. If empty, the current session ID parameter will be used.
  - `order` (DropdownInput) — display: "Order"; options: ['Ascending', 'Descending']; default: 'Ascending'; info: Order of the messages.
  - `template` (MultilineInput) — display: "Template"; default: '{sender_name}: {text}'; info: The template to use for formatting the data. It can contain the keys {text}, {sender} or any other key in the message data.

- **Output ports**:
  - `messages` (Output) — display: "Data"; method: `retrieve_messages`
  - `messages_text` (Output) — display: "Message"; method: `retrieve_messages_as_text`
  - `dataframe` (Output) — display: "DataFrame"; method: `as_dataframe`

### Message Store

- **Class**: `MessageStoreComponent`
- **Source**: `helpers/store_message.py`
- **Description**: Stores a chat message or text into Langflow tables or an external memory.

- **Input/configuration ports**:
  - `message` (MessageTextInput) — display: "Message"; required: true; info: The chat message to be stored.
  - `memory` (HandleInput) — display: "External Memory"; input_types: ['Memory']; info: The external memory to store the message. If empty, it will use the Langflow tables.
  - `sender` (MessageTextInput) — display: "Sender"; info: The sender of the message. Might be Machine or User. If empty, the current sender parameter will be used.
  - `sender_name` (MessageTextInput) — display: "Sender Name"; info: The name of the sender. Might be AI or User. If empty, the current sender parameter will be used.
  - `session_id` (MessageTextInput) — display: "Session ID"; default: ''; info: The session ID of the chat. If empty, the current session ID parameter will be used.

- **Output ports**:
  - `stored_messages` (Output) — display: "Stored Messages"; method: `store_message`

### Output Parser

- **Class**: `OutputParserComponent`
- **Source**: `helpers/output_parser.py`
- **Description**: Transforms the output of an LLM into a specified format.

- **Input/configuration ports**:
  - `parser_type` (DropdownInput) — display: "Parser"; options: ['CSV']; default: 'CSV'

- **Output ports**:
  - `format_instructions` (Output) — display: "Format Instructions"; method: `format_instructions`
  - `output_parser` (Output) — display: "Output Parser"; method: `build_parser`

### Structured Output

- **Class**: `StructuredOutputComponent`
- **Source**: `helpers/structured_output.py`
- **Description**: Transforms LLM responses into **structured data formats**. Ideal for extracting specific information or creating consistent outputs.

- **Input/configuration ports**:
  - `llm` (HandleInput) — display: "Language Model"; required: true; input_types: ['LanguageModel']; info: The language model to use to generate the structured output.
  - `input_value` (MessageTextInput) — display: "Input Message"; required: true; info: The input message to the language model.
  - `system_prompt` (MultilineInput) — display: "Format Instructions"; required: true; default: "You are an AI system designed to extract structured information from unstructured text.Given the input_text, return a JSON object with predefined keys based on the expected structure.Extract values accurately and format them according to the specified type (e.g., string, integer, float, date).If a value is missing or cannot be determined, return a default (e.g., null, 0, or 'N/A').If multiple instances of the expected structure exist within the input_text, stream each as a separate JSON object."; info: The instructions to the language model for formatting the output.
  - `schema_name` (MessageTextInput) — display: "Schema Name"; info: Provide a name for the output data schema.
  - `output_schema` (TableInput) — display: "Output Schema"; required: true; default: [{'name': 'field', 'description': 'description of field', 'type': 'str', 'multiple': 'False'}]; info: Define the structure and data types for the model's output.
  - `multiple` (BoolInput) — display: "Generate Multiple"; default: True; info: [Deplrecated] Always set to True

- **Output ports**:
  - `structured_output` (Output) — display: "Structured Output"; method: `build_structured_output`
  - `structured_output_dataframe` (Output) — display: "DataFrame"; method: `as_dataframe`

## icosacomputing (1 node types)

### Combinatorial Reasoner

- **Class**: `CombinatorialReasonerComponent`
- **Source**: `icosacomputing/combinatorial_reasoner.py`
- **Description**: Uses Combinatorial Optimization to construct an optimal prompt with embedded reasons. Sign up here: https://forms.gle/oWNv2NKjBNaqqvCx6

- **Input/configuration ports**:
  - `prompt` (MessageTextInput) — display: "Prompt"; required: true
  - `openai_api_key` (SecretStrInput) — display: "OpenAI API Key"; required: true; default: 'OPENAI_API_KEY'; info: The OpenAI API Key to use for the OpenAI model.
  - `username` (StrInput) — display: "Username"; required: true; info: Username to authenticate access to Icosa CR API
  - `password` (SecretStrInput) — display: "Password"; required: true; info: Password to authenticate access to Icosa CR API.
  - `model_name` (DropdownInput) — display: "Model Name"; options: OPENAI_MODEL_NAMES; default: OPENAI_MODEL_NAMES[0]

- **Output ports**:
  - `optimized_prompt` (Output) — display: "Optimized Prompt"; method: `build_prompt`
  - `reasons` (Output) — display: "Selected Reasons"; method: `build_reasons`

## inputs (2 node types)

### Chat Input

- **Class**: `ChatInput`
- **Source**: `inputs/chat.py`
- **Description**: Get chat inputs from the Playground.

- **Input/configuration ports**:
  - `input_value` (MultilineInput) — display: "Text"; input_types: []; default: ''; info: Message to be passed as input.
  - `should_store_message` (BoolInput) — display: "Store Messages"; default: True; info: Store the message in the history.
  - `sender` (DropdownInput) — display: "Sender Type"; options: [MESSAGE_SENDER_AI, MESSAGE_SENDER_USER]; default: MESSAGE_SENDER_USER; info: Type of sender.
  - `sender_name` (MessageTextInput) — display: "Sender Name"; default: MESSAGE_SENDER_NAME_USER; info: Name of the sender.
  - `session_id` (MessageTextInput) — display: "Session ID"; info: The session ID of the chat. If empty, the current session ID parameter will be used.
  - `files` (FileInput) — display: "Files"; info: Files to be sent with the message.
  - `background_color` (MessageTextInput) — display: "Background Color"; info: The background color of the icon.
  - `chat_icon` (MessageTextInput) — display: "Icon"; info: The icon of the message.
  - `text_color` (MessageTextInput) — display: "Text Color"; info: The text color of the name

- **Output ports**:
  - `message` (Output) — display: "Message"; method: `message_response`

### Text Input

- **Class**: `TextInputComponent`
- **Source**: `inputs/text.py`
- **Description**: Get text inputs from the Playground.

- **Input/configuration ports**:
  - `input_value` (MultilineInput) — display: "Text"; info: Text to be passed as input.

- **Output ports**:
  - `text` (Output) — display: "Message"; method: `text_response`

## langchain_utilities (28 node types)

### CharacterTextSplitter

- **Class**: `CharacterTextSplitterComponent`
- **Source**: `langchain_utilities/character.py`
- **Description**: Split text by number of characters.

- **Input/configuration ports**:
  - `chunk_size` (IntInput) — display: "Chunk Size"; default: 1000; info: The maximum length of each chunk.
  - `chunk_overlap` (IntInput) — display: "Chunk Overlap"; default: 200; info: The amount of overlap between chunks.
  - `data_input` (DataInput) — display: "Input"; required: true; input_types: ['Document', 'Data']; info: The texts to split.
  - `separator` (MessageTextInput) — display: "Separator"; info: The characters to split on. If left empty defaults to "\n\n".

- **Output ports**:
  - _No class-level outputs declared._

### ConversationChain

- **Class**: `ConversationChainComponent`
- **Source**: `langchain_utilities/conversation.py`
- **Description**: Chain to have a conversation and load context from memory.

- **Input/configuration ports**:
  - `input_value` (MultilineInput) — display: "Input"; required: true; info: The input value to pass to the chain.
  - `llm` (HandleInput) — display: "Language Model"; required: true; input_types: ['LanguageModel']
  - `memory` (HandleInput) — display: "Memory"; input_types: ['BaseChatMemory']

- **Output ports**:
  - _No class-level outputs declared._

### CSVAgent

- **Class**: `CSVAgentComponent`
- **Source**: `langchain_utilities/csv_agent.py`
- **Description**: Construct a CSV agent from a CSV and tools.

- **Input/configuration ports**:
  - `llm` (HandleInput) — display: "Language Model"; required: true; input_types: ['LanguageModel']; info: An LLM Model Object (It can be found in any LLM Component).
  - `path` (FileInput) — display: "File Path"; required: true; input_types: ['str', 'Message']; info: A CSV File or File Path.
  - `agent_type` (DropdownInput) — display: "Agent Type"; options: ['zero-shot-react-description', 'openai-functions', 'openai-tools']; default: 'openai-tools'
  - `input_value` (MessageTextInput) — display: "Text"; required: true; info: Text to be passed as input and extract info from the CSV File.
  - `pandas_kwargs` (DictInput) — display: "Pandas Kwargs"; info: Pandas Kwargs to be passed to the agent.

- **Output ports**:
  - `response` (Output) — display: "Response"; method: `build_agent_response`
  - `agent` (Output) — display: "Agent"; method: `build_agent`

### Fake Embeddings

- **Class**: `FakeEmbeddingsComponent`
- **Source**: `langchain_utilities/fake_embeddings.py`
- **Description**: Generate fake embeddings, useful for initial testing and connecting components.

- **Input/configuration ports**:
  - `dimensions` (IntInput) — display: "Dimensions"; default: 5; info: The number of dimensions the resulting output embeddings should have.

- **Output ports**:
  - _No class-level outputs declared._

### HTML Link Extractor

- **Class**: `HtmlLinkExtractorComponent`
- **Source**: `langchain_utilities/html_link_extractor.py`
- **Description**: Extract hyperlinks from HTML content.

- **Input/configuration ports**:
  - `kind` (StrInput) — display: "Kind of edge"; required: false; default: 'hyperlink'
  - `drop_fragments` (BoolInput) — display: "Drop URL fragments"; required: false; default: True
  - `data_input` (DataInput) — display: "Input"; required: true; input_types: ['Document', 'Data']; info: The texts from which to extract links.

- **Output ports**:
  - _No class-level outputs declared._

### JsonAgent

- **Class**: `JsonAgentComponent`
- **Source**: `langchain_utilities/json_agent.py`
- **Description**: Construct a json agent from an LLM and tools.

- **Input/configuration ports**:
  - `llm` (HandleInput) — display: "Language Model"; required: true; input_types: ['LanguageModel']
  - `path` (FileInput) — display: "File Path"; required: true

- **Output ports**:
  - _No class-level outputs declared._

### LangChainHubPromptComponent

- **Class**: `LangChainHubPromptComponent`
- **Source**: `langchain_utilities/langchain_hub.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `langchain_api_key` (SecretStrInput) — display: "Your LangChain API Key"; required: true; info: The LangChain API Key to use.
  - `langchain_hub_prompt` (StrInput) — display: "LangChain Hub Prompt"; required: true; info: The LangChain Hub prompt to use, i.e., 'efriis/my-first-prompt'

- **Output ports**:
  - `prompt` (Output) — display: "Build Prompt"; method: `build_prompt`

### LanguageRecursiveTextSplitterComponent

- **Class**: `LanguageRecursiveTextSplitterComponent`
- **Source**: `langchain_utilities/language_recursive.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `chunk_size` (IntInput) — display: "Chunk Size"; default: 1000; info: The maximum length of each chunk.
  - `chunk_overlap` (IntInput) — display: "Chunk Overlap"; default: 200; info: The amount of overlap between chunks.
  - `data_input` (DataInput) — display: "Input"; required: true; input_types: ['Document', 'Data']; info: The texts to split.
  - `code_language` (DropdownInput) — display: "Code Language"; options: [x.value for x in Language]; default: 'python'

- **Output ports**:
  - _No class-level outputs declared._

### LLMCheckerChain

- **Class**: `LLMCheckerChainComponent`
- **Source**: `langchain_utilities/llm_checker.py`
- **Description**: Chain for question-answering with self-verification.

- **Input/configuration ports**:
  - `input_value` (MultilineInput) — display: "Input"; required: true; info: The input value to pass to the chain.
  - `llm` (HandleInput) — display: "Language Model"; required: true; input_types: ['LanguageModel']

- **Output ports**:
  - _No class-level outputs declared._

### LLMMathChain

- **Class**: `LLMMathChainComponent`
- **Source**: `langchain_utilities/llm_math.py`
- **Description**: Chain that interprets a prompt and executes python code to do math.

- **Input/configuration ports**:
  - `input_value` (MultilineInput) — display: "Input"; required: true; info: The input value to pass to the chain.
  - `llm` (HandleInput) — display: "Language Model"; required: true; input_types: ['LanguageModel']

- **Output ports**:
  - `text` (Output) — display: "Message"; method: `invoke_chain`

### Natural Language Text Splitter

- **Class**: `NaturalLanguageTextSplitterComponent`
- **Source**: `langchain_utilities/natural_language.py`
- **Description**: Split text based on natural language boundaries, optimized for a specified language.

- **Input/configuration ports**:
  - `chunk_size` (IntInput) — display: "Chunk Size"; default: 1000; info: The maximum number of characters in each chunk after splitting.
  - `chunk_overlap` (IntInput) — display: "Chunk Overlap"; default: 200; info: The number of characters that overlap between consecutive chunks.
  - `data_input` (DataInput) — display: "Input"; required: true; input_types: ['Document', 'Data']; info: The text data to be split.
  - `separator` (MessageTextInput) — display: "Separator"; info: The character(s) to use as a delimiter when splitting text. Defaults to "\n\n" if left empty.
  - `language` (MessageTextInput) — display: "Language"; info: The language of the text. Default is "English". Supports multiple languages for better text boundary recognition.

- **Output ports**:
  - _No class-level outputs declared._

### Natural Language to SQL

- **Class**: `SQLGeneratorComponent`
- **Source**: `langchain_utilities/sql_generator.py`
- **Description**: Generate SQL from natural language.

- **Input/configuration ports**:
  - `input_value` (MultilineInput) — display: "Input"; required: true; info: The input value to pass to the chain.
  - `llm` (HandleInput) — display: "Language Model"; required: true; input_types: ['LanguageModel']
  - `db` (HandleInput) — display: "SQLDatabase"; required: true; input_types: ['SQLDatabase']
  - `top_k` (IntInput) — display: "Top K"; default: 5; info: The number of results per select statement to return.
  - `prompt` (MultilineInput) — display: "Prompt"; info: The prompt must contain `{question}`.

- **Output ports**:
  - `text` (Output) — display: "Message"; method: `invoke_chain`

### OpenAIToolsAgentComponent

- **Class**: `OpenAIToolsAgentComponent`
- **Source**: `langchain_utilities/openai_tools.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `llm` (HandleInput) — display: "Language Model"; required: true; input_types: ['LanguageModel', 'ToolEnabledLanguageModel']
  - `system_prompt` (MultilineInput) — display: "System Prompt"; default: 'You are a helpful assistant'; info: System prompt for the agent.
  - `user_prompt` (MultilineInput) — display: "Prompt"; default: '{input}'; info: This prompt must contain 'input' key.
  - `chat_history` (DataInput) — display: "Chat History"

- **Output ports**:
  - _No class-level outputs declared._

### OpenAPI Agent

- **Class**: `OpenAPIAgentComponent`
- **Source**: `langchain_utilities/openapi.py`
- **Description**: Agent to interact with OpenAPI API.

- **Input/configuration ports**:
  - `llm` (HandleInput) — display: "Language Model"; required: true; input_types: ['LanguageModel']
  - `path` (FileInput) — display: "File Path"; required: true
  - `allow_dangerous_requests` (BoolInput) — display: "Allow Dangerous Requests"; required: true; default: False

- **Output ports**:
  - _No class-level outputs declared._

### RecursiveCharacterTextSplitterComponent

- **Class**: `RecursiveCharacterTextSplitterComponent`
- **Source**: `langchain_utilities/recursive_character.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `chunk_size` (IntInput) — display: "Chunk Size"; default: 1000; info: The maximum length of each chunk.
  - `chunk_overlap` (IntInput) — display: "Chunk Overlap"; default: 200; info: The amount of overlap between chunks.
  - `data_input` (DataInput) — display: "Input"; required: true; input_types: ['Document', 'Data']; info: The texts to split.
  - `separators` (MessageTextInput) — display: "Separators"; info: The characters to split on. If left empty defaults to ["\n\n", "\n", " ", ""].

- **Output ports**:
  - _No class-level outputs declared._

### Retrieval QA

- **Class**: `RetrievalQAComponent`
- **Source**: `langchain_utilities/retrieval_qa.py`
- **Description**: Chain for question-answering querying sources from a retriever.

- **Input/configuration ports**:
  - `input_value` (MultilineInput) — display: "Input"; required: true; info: The input value to pass to the chain.
  - `chain_type` (DropdownInput) — display: "Chain Type"; options: ['Stuff', 'Map Reduce', 'Refine', 'Map Rerank']; default: 'Stuff'; info: Chain type to use.
  - `llm` (HandleInput) — display: "Language Model"; required: true; input_types: ['LanguageModel']
  - `retriever` (HandleInput) — display: "Retriever"; required: true; input_types: ['Retriever']
  - `memory` (HandleInput) — display: "Memory"; input_types: ['BaseChatMemory']
  - `return_source_documents` (BoolInput) — display: "Return Source Documents"; default: False

- **Output ports**:
  - _No class-level outputs declared._

### RetrieverTool

- **Class**: `RetrieverToolComponent`
- **Source**: `langchain_utilities/retriever.py`
- **Description**: Tool for interacting with retriever

- **Input/configuration ports**:
  - _No class-level inputs declared._

- **Output ports**:
  - _No class-level outputs declared._

### Runnable Executor

- **Class**: `RunnableExecComponent`
- **Source**: `langchain_utilities/runnable_executor.py`
- **Description**: Execute a runnable. It will try to guess the input and output keys.

- **Input/configuration ports**:
  - `input_value` (MessageTextInput) — display: "Input"; required: true
  - `runnable` (HandleInput) — display: "Agent Executor"; required: true; input_types: ['Chain', 'AgentExecutor', 'Agent', 'Runnable']
  - `input_key` (MessageTextInput) — display: "Input Key"; default: 'input'
  - `output_key` (MessageTextInput) — display: "Output Key"; default: 'output'
  - `use_stream` (BoolInput) — display: "Stream"; default: False

- **Output ports**:
  - `text` (Output) — display: "Message"; method: `build_executor`

### Self Query Retriever

- **Class**: `SelfQueryRetrieverComponent`
- **Source**: `langchain_utilities/self_query.py`
- **Description**: Retriever that uses a vector store and an LLM to generate the vector store queries.

- **Input/configuration ports**:
  - `query` (HandleInput) — display: "Query"; input_types: ['Message']; info: Query to be passed as input.
  - `vectorstore` (HandleInput) — display: "Vector Store"; input_types: ['VectorStore']; info: Vector Store to be passed as input.
  - `attribute_infos` (HandleInput) — display: "Metadata Field Info"; input_types: ['Data']; info: Metadata Field Info to be passed as input.
  - `document_content_description` (MessageTextInput) — display: "Document Content Description"; info: Document Content Description to be passed as input.
  - `llm` (HandleInput) — display: "LLM"; input_types: ['LanguageModel']; info: LLM to be passed as input.

- **Output ports**:
  - `documents` (Output) — display: "Retrieved Documents"; method: `retrieve_documents`

### SemanticTextSplitterComponent

- **Class**: `SemanticTextSplitterComponent`
- **Source**: `langchain_utilities/language_semantic.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `data_inputs` (HandleInput) — display: "Data Inputs"; required: true; input_types: ['Data']; info: List of Data objects containing text and metadata to split.
  - `embeddings` (HandleInput) — display: "Embeddings"; required: true; input_types: ['Embeddings']; info: Embeddings model to use for semantic similarity. Required.
  - `breakpoint_threshold_type` (DropdownInput) — display: "Breakpoint Threshold Type"; options: ['percentile', 'standard_deviation', 'interquartile']; default: 'percentile'; info: Method to determine breakpoints. Options: 'percentile', 'standard_deviation', 'interquartile'. Defaults to 'percentile'.
  - `breakpoint_threshold_amount` (FloatInput) — display: "Breakpoint Threshold Amount"; default: 0.5; info: Numerical amount for the breakpoint threshold.
  - `number_of_chunks` (IntInput) — display: "Number of Chunks"; default: 5; info: Number of chunks to split the text into.
  - `sentence_split_regex` (MessageTextInput) — display: "Sentence Split Regex"; default: ''; info: Regular expression to split sentences. Optional.
  - `buffer_size` (IntInput) — display: "Buffer Size"; default: 0; info: Size of the buffer.

- **Output ports**:
  - `chunks` (Output) — display: "Chunks"; method: `split_text`

### SpiderTool

- **Class**: `SpiderTool`
- **Source**: `langchain_utilities/spider.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `spider_api_key` (SecretStrInput) — display: "Spider API Key"; required: true; info: The Spider API Key, get it from https://spider.cloud
  - `url` (StrInput) — display: "URL"; required: true; info: The URL to scrape or crawl
  - `mode` (DropdownInput) — display: "Mode"; required: true; options: MODES; default: MODES[0]; info: The mode of operation: scrape or crawl
  - `limit` (IntInput) — display: "Limit"; info: The maximum amount of pages allowed to crawl per website. Set to 0 to crawl all pages.
  - `depth` (IntInput) — display: "Depth"; info: The crawl limit for maximum depth. If 0, no limit will be applied.
  - `blacklist` (StrInput) — display: "Blacklist"; info: Blacklist paths that you do not want to crawl. Use Regex patterns.
  - `whitelist` (StrInput) — display: "Whitelist"; info: Whitelist paths that you want to crawl, ignoring all other routes. Use Regex patterns.
  - `readability` (BoolInput) — display: "Use Readability"; info: Use readability to pre-process the content for reading.
  - `request_timeout` (IntInput) — display: "Request Timeout"; info: Timeout for the request in seconds.
  - `metadata` (BoolInput) — display: "Metadata"; info: Include metadata in the response.
  - `params` (DictInput) — display: "Additional Parameters"; info: Additional parameters to pass to the API. If provided, other inputs will be ignored.

- **Output ports**:
  - `content` (Output) — display: "Markdown"; method: `crawl`

### SQLAgent

- **Class**: `SQLAgentComponent`
- **Source**: `langchain_utilities/sql.py`
- **Description**: Construct an SQL agent from an LLM and tools.

- **Input/configuration ports**:
  - `llm` (HandleInput) — display: "Language Model"; required: true; input_types: ['LanguageModel']
  - `database_uri` (MessageTextInput) — display: "Database URI"; required: true
  - `extra_tools` (HandleInput) — display: "Extra Tools"; input_types: ['Tool']

- **Output ports**:
  - _No class-level outputs declared._

### SQLDatabase

- **Class**: `SQLDatabaseComponent`
- **Source**: `langchain_utilities/sql_database.py`
- **Description**: SQL Database

- **Input/configuration ports**:
  - `uri` (StrInput) — display: "URI"; required: true; info: URI to the database.

- **Output ports**:
  - `SQLDatabase` (Output) — display: "SQLDatabase"; method: `build_sqldatabase`

### ToolCallingAgentComponent

- **Class**: `ToolCallingAgentComponent`
- **Source**: `langchain_utilities/tool_calling.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `llm` (HandleInput) — display: "Language Model"; required: true; input_types: ['LanguageModel']; info: Language model that the agent utilizes to perform tasks effectively.
  - `system_prompt` (MessageTextInput) — display: "System Prompt"; default: 'You are a helpful assistant that can use tools to answer questions and perform tasks.'; info: System prompt to guide the agent's behavior.
  - `chat_history` (DataInput) — display: "Chat Memory"; info: This input stores the chat history, allowing the agent to remember previous conversations.

- **Output ports**:
  - _No class-level outputs declared._

### VectorStore Retriever

- **Class**: `VectoStoreRetrieverComponent`
- **Source**: `langchain_utilities/vector_store.py`
- **Description**: A vector store retriever

- **Input/configuration ports**:
  - _No class-level inputs declared._

- **Output ports**:
  - _No class-level outputs declared._

### VectorStoreInfo

- **Class**: `VectorStoreInfoComponent`
- **Source**: `langchain_utilities/vector_store_info.py`
- **Description**: Information about a VectorStore

- **Input/configuration ports**:
  - `vectorstore_name` (MessageTextInput) — display: "Name"; required: true; info: Name of the VectorStore
  - `vectorstore_description` (MultilineInput) — display: "Description"; required: true; info: Description of the VectorStore
  - `input_vectorstore` (HandleInput) — display: "Vector Store"; required: true; input_types: ['VectorStore']

- **Output ports**:
  - `info` (Output) — display: "Vector Store Info"; method: `build_info`

### VectorStoreRouterAgent

- **Class**: `VectorStoreRouterAgentComponent`
- **Source**: `langchain_utilities/vector_store_router.py`
- **Description**: Construct an agent from a Vector Store Router.

- **Input/configuration ports**:
  - `llm` (HandleInput) — display: "Language Model"; required: true; input_types: ['LanguageModel']
  - `vectorstores` (HandleInput) — display: "Vector Stores"; required: true; input_types: ['VectorStoreInfo']

- **Output ports**:
  - _No class-level outputs declared._

### XMLAgentComponent

- **Class**: `XMLAgentComponent`
- **Source**: `langchain_utilities/xml_agent.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `llm` (HandleInput) — display: "Language Model"; required: true; input_types: ['LanguageModel']
  - `chat_history` (DataInput) — display: "Chat History"
  - `system_prompt` (MultilineInput) — display: "System Prompt"; default: "You are a helpful assistant. Help the user answer any questions.\n\nYou have access to the following tools:\n\n{tools}\n\nIn order to use a tool, you can use <tool></tool> and <tool_input></tool_input> tags. You will then get back a response in the form <observation></observation>\n\nFor example, if you have a tool called 'search' that could run a google search, in order to search for the weather in SF you would respond:\n\n<tool>search</tool><tool_input>weather in SF</tool_input>\n\n<observation>64 degrees</observation>\n\nWhen you are done, respond with a final answer between <final_answer></final_answer>. For example:\n\n<final_answer>The weather in SF is 64 degrees</final_answer>\n\nBegin!\n\nQuestion: {input}\n\n{agent_scratchpad}\n "; info: System prompt for the agent.
  - `user_prompt` (MultilineInput) — display: "Prompt"; default: '{input}'; info: This prompt must contain 'input' key.

- **Output ports**:
  - _No class-level outputs declared._

## langwatch (1 node types)

### LangWatchComponent

- **Class**: `LangWatchComponent`
- **Source**: `langwatch/langwatch.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `evaluator_name` (DropdownInput) — display: "Evaluator Name"; required: true; options: []; info: Select an evaluator.
  - `api_key` (SecretStrInput) — display: "API Key"; required: true; info: Enter your LangWatch API key.
  - `input` (MessageTextInput) — display: "Input"; required: false; info: The input text for evaluation.
  - `output` (MessageTextInput) — display: "Output"; required: false; info: The output text for evaluation.
  - `expected_output` (MessageTextInput) — display: "Expected Output"; required: false; info: The expected output for evaluation.
  - `contexts` (MessageTextInput) — display: "Contexts"; required: false; info: The contexts for evaluation (comma-separated).
  - `timeout` (IntInput) — display: "Timeout"; default: 30; info: The maximum time (in seconds) allowed for the server to respond before timing out.

- **Output ports**:
  - `evaluation_result` (Output) — display: "Evaluation Result"; method: `evaluate`

## logic (9 node types)

### Condition

- **Class**: `DataConditionalRouterComponent`
- **Source**: `logic/data_conditional_router.py`
- **Description**: Route Data object(s) based on a condition applied to a specified key, including boolean validation.

- **Input/configuration ports**:
  - `data_input` (DataInput) — display: "Data Input"; info: The Data object or list of Data objects to process
  - `key_name` (MessageTextInput) — display: "Key Name"; info: The name of the key in the Data object(s) to check
  - `operator` (DropdownInput) — display: "Operator"; options: ['equals', 'not equals', 'contains', 'starts with', 'ends with', 'boolean validator']; default: 'equals'; info: The operator to apply for comparing the values. 'boolean validator' treats the value as a boolean.
  - `compare_value` (MessageTextInput) — display: "Match Text"; info: The value to compare against (not used for boolean validator)

- **Output ports**:
  - `true_output` (Output) — display: "True Output"; method: `process_data`
  - `false_output` (Output) — display: "False Output"; method: `process_data`

### Flow as Tool [Deprecated]

- **Class**: `FlowToolComponent`
- **Source**: `logic/flow_tool.py`
- **Description**: Construct a Tool from a function that runs the loaded Flow.

- **Input/configuration ports**:
  - `flow_name` (DropdownInput) — display: "Flow Name"; info: The name of the flow to run.
  - `tool_name` (StrInput) — display: "Name"; info: The name of the tool.
  - `tool_description` (StrInput) — display: "Description"; info: The description of the tool; defaults to the Flow's description.
  - `return_direct` (BoolInput) — display: "Return Direct"; info: Return the result directly from the Tool.

- **Output ports**:
  - `api_build_tool` (Output) — display: "Tool"; method: `build_tool`

### If-Else

- **Class**: `ConditionalRouterComponent`
- **Source**: `logic/conditional_router.py`
- **Description**: Routes an input message to a corresponding output based on text comparison.

- **Input/configuration ports**:
  - `input_text` (MessageTextInput) — display: "Text Input"; required: true; info: The primary text input for the operation.
  - `match_text` (MessageTextInput) — display: "Match Text"; required: true; info: The text input to compare against.
  - `operator` (DropdownInput) — display: "Operator"; options: ['equals', 'not equals', 'contains', 'starts with', 'ends with', 'regex']; default: 'equals'; info: The operator to apply for comparing the texts.
  - `case_sensitive` (BoolInput) — display: "Case Sensitive"; default: False; info: If true, the comparison will be case sensitive.
  - `message` (MessageInput) — display: "Message"; info: The message to pass through either route.
  - `max_iterations` (IntInput) — display: "Max Iterations"; default: 10; info: The maximum number of iterations for the conditional router.
  - `default_route` (DropdownInput) — display: "Default Route"; options: ['true_result', 'false_result']; default: 'false_result'; info: The default route to take when max iterations are reached.

- **Output ports**:
  - `true_result` (Output) — display: "True"; method: `true_response`
  - `false_result` (Output) — display: "False"; method: `false_response`

### Listen

- **Class**: `ListenComponent`
- **Source**: `logic/listen.py`
- **Description**: A component to listen for a notification.

- **Input/configuration ports**:
  - _No class-level inputs declared._

- **Output ports**:
  - _No class-level outputs declared._

### Loop

- **Class**: `LoopComponent`
- **Source**: `logic/loop.py`
- **Description**: Iterates over a list of Data objects, outputting one item at a time and aggregating results from loop inputs.

- **Input/configuration ports**:
  - `data` (DataInput) — display: "Data"; info: The initial list of Data objects to iterate over.

- **Output ports**:
  - `item` (Output) — display: "Item"; method: `item_output`
  - `done` (Output) — display: "Done"; method: `done_output`

### Notify

- **Class**: `NotifyComponent`
- **Source**: `logic/notify.py`
- **Description**: A component to generate a notification to Get Notified component.

- **Input/configuration ports**:
  - _No class-level inputs declared._

- **Output ports**:
  - _No class-level outputs declared._

### Pass

- **Class**: `PassMessageComponent`
- **Source**: `logic/pass_message.py`
- **Description**: Forwards the input message, unchanged.

- **Input/configuration ports**:
  - `input_message` (MessageInput) — display: "Input Message"; required: true; info: The message to be passed forward.
  - `ignored_message` (MessageInput) — display: "Ignored Message"; info: A second message to be ignored. Used as a workaround for continuity.

- **Output ports**:
  - `output_message` (Output) — display: "Output Message"; method: `pass_message`

### Run Flow

- **Class**: `RunFlowComponent`
- **Source**: `logic/run_flow.py`
- **Description**: Creates a tool component from a Flow that takes all its inputs and runs it. **Select a Flow to use the tool mode**

- **Input/configuration ports**:
  - _No class-level inputs declared._

- **Output ports**:
  - _No class-level outputs declared._

### Sub Flow [Deprecated]

- **Class**: `SubFlowComponent`
- **Source**: `logic/sub_flow.py`
- **Description**: Generates a Component from a Flow, with all of its inputs, and

- **Input/configuration ports**:
  - `flow_name` (DropdownInput) — display: "Flow Name"; options: []; info: The name of the flow to run.

- **Output ports**:
  - `flow_outputs` (Output) — display: "Flow Outputs"; method: `generate_results`

## memories (5 node types)

### Astra DB Chat Memory

- **Class**: `AstraDBChatMemory`
- **Source**: `memories/astra_db.py`
- **Description**: Retrieves and store chat messages from Astra DB.

- **Input/configuration ports**:
  - `token` (SecretStrInput) — display: "Astra DB Application Token"; required: true; default: 'ASTRA_DB_APPLICATION_TOKEN'; info: Authentication token for accessing Astra DB.
  - `api_endpoint` (SecretStrInput) — display: "API Endpoint"; required: true; default: 'ASTRA_DB_API_ENDPOINT'; info: API endpoint URL for the Astra DB service.
  - `collection_name` (StrInput) — display: "Collection Name"; required: true; info: The name of the collection within Astra DB where the vectors will be stored.
  - `namespace` (StrInput) — display: "Namespace"; info: Optional namespace within Astra DB to use for the collection.
  - `session_id` (MessageTextInput) — display: "Session ID"; info: The session ID of the chat. If empty, the current session ID parameter will be used.

- **Output ports**:
  - _No class-level outputs declared._

### Cassandra Chat Memory

- **Class**: `CassandraChatMemory`
- **Source**: `memories/cassandra.py`
- **Description**: Retrieves and store chat messages from Apache Cassandra.

- **Input/configuration ports**:
  - `database_ref` (MessageTextInput) — display: "Contact Points / Astra Database ID"; required: true; info: Contact points for the database (or AstraDB database ID)
  - `username` (MessageTextInput) — display: "Username"; info: Username for the database (leave empty for AstraDB).
  - `token` (SecretStrInput) — display: "Password / AstraDB Token"; required: true; info: User password for the database (or AstraDB token).
  - `keyspace` (MessageTextInput) — display: "Keyspace"; required: true; info: Table Keyspace (or AstraDB namespace).
  - `table_name` (MessageTextInput) — display: "Table Name"; required: true; info: The name of the table (or AstraDB collection) where vectors will be stored.
  - `session_id` (MessageTextInput) — display: "Session ID"; info: Session ID for the message.
  - `cluster_kwargs` (DictInput) — display: "Cluster arguments"; info: Optional dictionary of additional keyword arguments for the Cassandra cluster.

- **Output ports**:
  - _No class-level outputs declared._

### Mem0 Chat Memory

- **Class**: `Mem0MemoryComponent`
- **Source**: `memories/mem0_chat_memory.py`
- **Description**: Retrieves and stores chat messages using Mem0 memory storage.

- **Input/configuration ports**:
  - `mem0_config` (NestedDictInput) — display: "Mem0 Configuration"; input_types: ['Data']; info: Configuration dictionary for initializing Mem0 memory instance. Example: { "graph_store": { "provider": "neo4j", "config": { "url": "neo4j+s://your-neo4j-url", "username": "neo4j", "password": "your-password" } }, "version": "v1.1" }
  - `ingest_message` (MessageTextInput) — display: "Message to Ingest"; info: The message content to be ingested into Mem0 memory.
  - `existing_memory` (HandleInput) — display: "Existing Memory Instance"; input_types: ['Memory']; info: Optional existing Mem0 memory instance. If not provided, a new instance will be created.
  - `user_id` (MessageTextInput) — display: "User ID"; info: Identifier for the user associated with the messages.
  - `search_query` (MessageTextInput) — display: "Search Query"; info: Input text for searching related memories in Mem0.
  - `mem0_api_key` (SecretStrInput) — display: "Mem0 API Key"; info: API key for Mem0 platform. Leave empty to use the local version.
  - `metadata` (DictInput) — display: "Metadata"; info: Additional metadata to associate with the ingested message.
  - `openai_api_key` (SecretStrInput) — display: "OpenAI API Key"; required: false; info: API key for OpenAI. Required if using OpenAI Embeddings without a provided configuration.

- **Output ports**:
  - `memory` (Output) — display: "Mem0 Memory"; method: `ingest_data`
  - `search_results` (Output) — display: "Search Results"; method: `build_search_results`

### Redis Chat Memory

- **Class**: `RedisIndexChatMemory`
- **Source**: `memories/redis.py`
- **Description**: Retrieves and store chat messages from Redis.

- **Input/configuration ports**:
  - `host` (StrInput) — display: "hostname"; required: true; default: 'localhost'; info: IP address or hostname.
  - `port` (IntInput) — display: "port"; required: true; default: 6379; info: Redis Port Number.
  - `database` (StrInput) — display: "database"; required: true; default: '0'; info: Redis database.
  - `username` (MessageTextInput) — display: "Username"; default: ''; info: The Redis user name.
  - `password` (SecretStrInput) — display: "Password"; default: ''; info: The password for username.
  - `key_prefix` (StrInput) — display: "Key prefix"; info: Key prefix.
  - `session_id` (MessageTextInput) — display: "Session ID"; info: Session ID for the message.

- **Output ports**:
  - _No class-level outputs declared._

### Zep Chat Memory

- **Class**: `ZepChatMemory`
- **Source**: `memories/zep.py`
- **Description**: Retrieves and store chat messages from Zep.

- **Input/configuration ports**:
  - `url` (MessageTextInput) — display: "Zep URL"; info: URL of the Zep instance.
  - `api_key` (SecretStrInput) — display: "API Key"; info: API Key for the Zep instance.
  - `api_base_path` (DropdownInput) — display: "API Base Path"; options: ['api/v1', 'api/v2']; default: 'api/v1'
  - `session_id` (MessageTextInput) — display: "Session ID"; info: Session ID for the message.

- **Output ports**:
  - _No class-level outputs declared._

## models (23 node types)

### AIML

- **Class**: `AIMLModelComponent`
- **Source**: `models/aiml.py`
- **Description**: Generates text using AIML LLMs.

- **Input/configuration ports**:
  - `max_tokens` (IntInput) — display: "Max Tokens"; info: The maximum number of tokens to generate. Set to 0 for unlimited tokens.
  - `model_kwargs` (DictInput) — display: "Model Kwargs"
  - `model_name` (DropdownInput) — display: "Model Name"; options: []
  - `aiml_api_base` (StrInput) — display: "AIML API Base"; info: The base URL of the OpenAI API. Defaults to https://api.aimlapi.com . You can change this to use other APIs like JinaChat, LocalAI and Prem.
  - `api_key` (SecretStrInput) — display: "AIML API Key"; required: true; default: 'AIML_API_KEY'; info: The AIML API Key to use for the OpenAI model.
  - `temperature` (SliderInput) — display: "Temperature"; default: 0.1

- **Output ports**:
  - _No class-level outputs declared._

### AmazonBedrockComponent

- **Class**: `AmazonBedrockComponent`
- **Source**: `models/amazon_bedrock.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `model_id` (DropdownInput) — display: "Model ID"; options: AWS_MODEL_IDs; default: 'anthropic.claude-3-haiku-20240307-v1:0'; info: List of available model IDs to choose from.
  - `aws_access_key_id` (SecretStrInput) — display: "AWS Access Key ID"; required: true; default: 'AWS_ACCESS_KEY_ID'; info: The access key for your AWS account.Usually set in Python code as the environment variable 'AWS_ACCESS_KEY_ID'.
  - `aws_secret_access_key` (SecretStrInput) — display: "AWS Secret Access Key"; required: true; default: 'AWS_SECRET_ACCESS_KEY'; info: The secret key for your AWS account. Usually set in Python code as the environment variable 'AWS_SECRET_ACCESS_KEY'.
  - `aws_session_token` (SecretStrInput) — display: "AWS Session Token"; info: The session key for your AWS account. Only needed for temporary credentials. Usually set in Python code as the environment variable 'AWS_SESSION_TOKEN'.
  - `credentials_profile_name` (SecretStrInput) — display: "Credentials Profile Name"; info: The name of the profile to use from your ~/.aws/credentials file. If not provided, the default profile will be used.
  - `region_name` (DropdownInput) — display: "Region Name"; options: AWS_REGIONS; default: 'us-east-1'; info: The AWS region where your Bedrock resources are located.
  - `model_kwargs` (DictInput) — display: "Model Kwargs"; info: Additional keyword arguments to pass to the model.
  - `endpoint_url` (MessageTextInput) — display: "Endpoint URL"; info: The URL of the Bedrock endpoint to use.

- **Output ports**:
  - _No class-level outputs declared._

### Anthropic

- **Class**: `AnthropicModelComponent`
- **Source**: `models/anthropic.py`
- **Description**: Generate text using Anthropic Chat&Completion LLMs with prefill support.

- **Input/configuration ports**:
  - `max_tokens` (IntInput) — display: "Max Tokens"; default: 4096; info: The maximum number of tokens to generate. Set to 0 for unlimited tokens.
  - `model_name` (DropdownInput) — display: "Model Name"; options: ANTHROPIC_MODELS; default: ANTHROPIC_MODELS[0]
  - `api_key` (SecretStrInput) — display: "Anthropic API Key"; required: true; default: None; info: Your Anthropic API key.
  - `temperature` (SliderInput) — display: "Temperature"; default: 0.1; info: Run inference with this temperature. Must by in the closed interval [0.0, 1.0].
  - `base_url` (MessageTextInput) — display: "Anthropic API URL"; default: 'https://api.anthropic.com'; info: Endpoint of the Anthropic API. Defaults to 'https://api.anthropic.com' if not specified.
  - `tool_model_enabled` (BoolInput) — display: "Enable Tool Models"; default: False; info: Select if you want to use models that can work with tools. If yes, only those models will be shown.
  - `prefill` (MessageTextInput) — display: "Prefill"; info: Prefill text to guide the model's response.

- **Output ports**:
  - _No class-level outputs declared._

### AzureChatOpenAIComponent

- **Class**: `AzureChatOpenAIComponent`
- **Source**: `models/azure_openai.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `azure_endpoint` (MessageTextInput) — display: "Azure Endpoint"; required: true; info: Your Azure endpoint, including the resource. Example: `https://example-resource.azure.openai.com/`
  - `azure_deployment` (MessageTextInput) — display: "Deployment Name"; required: true
  - `api_key` (SecretStrInput) — display: "API Key"; required: true
  - `api_version` (DropdownInput) — display: "API Version"; options: sorted(AZURE_OPENAI_API_VERSIONS, reverse=True); default: next((version for version in sorted(AZURE_OPENAI_API_VERSIONS, reverse=True) if not version.endswith('-preview')), AZURE_OPENAI_API_VERSIONS[0])
  - `temperature` (SliderInput) — display: "Temperature"; default: 0.7; info: Controls randomness. Lower values are more deterministic, higher values are more creative.
  - `max_tokens` (IntInput) — display: "Max Tokens"; info: The maximum number of tokens to generate. Set to 0 for unlimited tokens.

- **Output ports**:
  - _No class-level outputs declared._

### Cohere

- **Class**: `CohereComponent`
- **Source**: `models/cohere.py`
- **Description**: Generate text using Cohere LLMs.

- **Input/configuration ports**:
  - `cohere_api_key` (SecretStrInput) — display: "Cohere API Key"; required: true; default: 'COHERE_API_KEY'; info: The Cohere API Key to use for the Cohere model.
  - `temperature` (SliderInput) — display: "Temperature"; default: 0.75; info: Controls randomness. Lower values are more deterministic, higher values are more creative.

- **Output ports**:
  - _No class-level outputs declared._

### DeepSeek

- **Class**: `DeepSeekModelComponent`
- **Source**: `models/deepseek.py`
- **Description**: Generate text using DeepSeek LLMs.

- **Input/configuration ports**:
  - `max_tokens` (IntInput) — display: "Max Tokens"; info: Maximum number of tokens to generate. Set to 0 for unlimited.
  - `model_kwargs` (DictInput) — display: "Model Kwargs"; info: Additional keyword arguments to pass to the model.
  - `json_mode` (BoolInput) — display: "JSON Mode"; info: If True, it will output JSON regardless of passing a schema.
  - `model_name` (DropdownInput) — display: "Model Name"; options: DEEPSEEK_MODELS; default: 'deepseek-chat'; info: DeepSeek model to use
  - `api_base` (StrInput) — display: "DeepSeek API Base"; default: 'https://api.deepseek.com'; info: Base URL for API requests. Defaults to https://api.deepseek.com
  - `api_key` (SecretStrInput) — display: "DeepSeek API Key"; required: true; info: The DeepSeek API Key
  - `temperature` (SliderInput) — display: "Temperature"; default: 1.0; info: Controls randomness in responses
  - `seed` (IntInput) — display: "Seed"; default: 1; info: The seed controls the reproducibility of the job.

- **Output ports**:
  - _No class-level outputs declared._

### Google Generative AI

- **Class**: `GoogleGenerativeAIComponent`
- **Source**: `models/google_generative_ai.py`
- **Description**: Generate text using Google Generative AI.

- **Input/configuration ports**:
  - `max_output_tokens` (IntInput) — display: "Max Output Tokens"; info: The maximum number of tokens to generate.
  - `model_name` (DropdownInput) — display: "Model"; options: GOOGLE_GENERATIVE_AI_MODELS; default: 'gemini-1.5-pro'; info: The name of the model to use.
  - `api_key` (SecretStrInput) — display: "Google API Key"; required: true; info: The Google API Key to use for the Google Generative AI.
  - `top_p` (FloatInput) — display: "Top P"; info: The maximum cumulative probability of tokens to consider when sampling.
  - `temperature` (SliderInput) — display: "Temperature"; default: 0.1; info: Controls randomness. Lower values are more deterministic, higher values are more creative.
  - `n` (IntInput) — display: "N"; info: Number of chat completions to generate for each prompt. Note that the API may not return the full n completions if duplicates are generated.
  - `top_k` (IntInput) — display: "Top K"; info: Decode using top-k sampling: consider the set of top_k most probable tokens. Must be positive.
  - `tool_model_enabled` (BoolInput) — display: "Tool Model Enabled"; default: False; info: Whether to use the tool model.

- **Output ports**:
  - _No class-level outputs declared._

### GroqModel

- **Class**: `GroqModel`
- **Source**: `models/groq.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `api_key` (SecretStrInput) — display: "Groq API Key"; info: API key for the Groq API.
  - `base_url` (MessageTextInput) — display: "Groq API Base"; default: 'https://api.groq.com'; info: Base URL path for API requests, leave blank if not using a proxy or service emulator.
  - `max_tokens` (IntInput) — display: "Max Output Tokens"; info: The maximum number of tokens to generate.
  - `temperature` (SliderInput) — display: "Temperature"; default: 0.1; info: Run inference with this temperature. Must by in the closed interval [0.0, 1.0].
  - `n` (IntInput) — display: "N"; info: Number of chat completions to generate for each prompt. Note that the API may not return the full n completions if duplicates are generated.
  - `model_name` (DropdownInput) — display: "Model"; options: GROQ_MODELS; default: GROQ_MODELS[0]; info: The name of the model to use.
  - `tool_model_enabled` (BoolInput) — display: "Enable Tool Models"; default: False; info: Select if you want to use models that can work with tools. If yes, only those models will be shown.

- **Output ports**:
  - _No class-level outputs declared._

### HuggingFaceEndpointsComponent

- **Class**: `HuggingFaceEndpointsComponent`
- **Source**: `models/huggingface.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `model_id` (DropdownInput) — display: "Model ID"; required: true; options: [DEFAULT_MODEL, 'mistralai/Mixtral-8x7B-Instruct-v0.1', 'mistralai/Mistral-7B-Instruct-v0.3', 'meta-llama/Llama-3.1-8B-Instruct', 'Qwen/Qwen2.5-Coder-32B-Instruct', 'Qwen/QwQ-32B-Preview', 'openai-community/gpt2', 'custom']; default: DEFAULT_MODEL; info: Select a model from HuggingFace Hub
  - `custom_model` (StrInput) — display: "Custom Model ID"; required: true; default: ''; info: Enter a custom model ID from HuggingFace Hub
  - `max_new_tokens` (IntInput) — display: "Max New Tokens"; default: 512; info: Maximum number of generated tokens
  - `top_k` (IntInput) — display: "Top K"; info: The number of highest probability vocabulary tokens to keep for top-k-filtering
  - `top_p` (FloatInput) — display: "Top P"; default: 0.95; info: If set to < 1, only the smallest set of most probable tokens with probabilities that add up to `top_p` or higher are kept for generation
  - `typical_p` (FloatInput) — display: "Typical P"; default: 0.95; info: Typical Decoding mass.
  - `temperature` (SliderInput) — display: "Temperature"; default: 0.8; info: The value used to module the logits distribution
  - `repetition_penalty` (FloatInput) — display: "Repetition Penalty"; info: The parameter for repetition penalty. 1.0 means no penalty.
  - `inference_endpoint` (StrInput) — display: "Inference Endpoint"; required: true; default: 'https://api-inference.huggingface.co/models/'; info: Custom inference endpoint URL.
  - `task` (DropdownInput) — display: "Task"; options: ['text2text-generation', 'text-generation', 'summarization', 'translation']; default: 'text-generation'; info: The task to call the model with. Should be a task that returns `generated_text` or `summary_text`.
  - `huggingfacehub_api_token` (SecretStrInput) — display: "API Token"; required: true
  - `model_kwargs` (DictInput) — display: "Model Keyword Arguments"
  - `retry_attempts` (IntInput) — display: "Retry Attempts"; default: 1

- **Output ports**:
  - _No class-level outputs declared._

### Language Model

- **Class**: `LanguageModelComponent`
- **Source**: `models/language_model.py`
- **Description**: Runs a language model given a specified provider.

- **Input/configuration ports**:
  - `provider` (DropdownInput) — display: "Model Provider"; options: ['OpenAI', 'Anthropic']; default: 'OpenAI'; info: Select the model provider
  - `model_name` (DropdownInput) — display: "Model Name"; options: OPENAI_MODEL_NAMES; default: OPENAI_MODEL_NAMES[0]; info: Select the model to use
  - `api_key` (SecretStrInput) — display: "OpenAI API Key"; required: false; info: Model Provider API key
  - `input_value` (MessageTextInput) — display: "Input"; info: The input text to send to the model
  - `system_message` (MessageTextInput) — display: "System Message"; info: A system message that helps set the behavior of the assistant
  - `stream` (BoolInput) — display: "Stream"; default: False; info: Whether to stream the response
  - `temperature` (SliderInput) — display: "Temperature"; default: 0.1; info: Controls randomness in responses

- **Output ports**:
  - _No class-level outputs declared._

### LM Studio

- **Class**: `LMStudioModelComponent`
- **Source**: `models/lmstudiomodel.py`
- **Description**: Generate text using LM Studio Local LLMs.

- **Input/configuration ports**:
  - `max_tokens` (IntInput) — display: "Max Tokens"; info: The maximum number of tokens to generate. Set to 0 for unlimited tokens.
  - `model_kwargs` (DictInput) — display: "Model Kwargs"
  - `model_name` (DropdownInput) — display: "Model Name"
  - `base_url` (StrInput) — display: "Base URL"; default: 'http://localhost:1234/v1'; info: Endpoint of the LM Studio API. Defaults to 'http://localhost:1234/v1' if not specified.
  - `api_key` (SecretStrInput) — display: "LM Studio API Key"; default: 'LMSTUDIO_API_KEY'; info: The LM Studio API Key to use for LM Studio.
  - `temperature` (FloatInput) — display: "Temperature"; default: 0.1
  - `seed` (IntInput) — display: "Seed"; default: 1; info: The seed controls the reproducibility of the job.

- **Output ports**:
  - _No class-level outputs declared._

### Maritalk

- **Class**: `MaritalkModelComponent`
- **Source**: `models/maritalk.py`
- **Description**: Generates text using Maritalk LLMs.

- **Input/configuration ports**:
  - `max_tokens` (IntInput) — display: "Max Tokens"; default: 512; info: The maximum number of tokens to generate. Set to 0 for unlimited tokens.
  - `model_name` (DropdownInput) — display: "Model Name"; options: ['sabia-2-small', 'sabia-2-medium']; default: ['sabia-2-small']
  - `api_key` (SecretStrInput) — display: "Maritalk API Key"; info: The Maritalk API Key to use for the OpenAI model.
  - `temperature` (FloatInput) — display: "Temperature"; default: 0.1

- **Output ports**:
  - _No class-level outputs declared._

### MistralAI

- **Class**: `MistralAIModelComponent`
- **Source**: `models/mistral.py`
- **Description**: Generates text using MistralAI LLMs.

- **Input/configuration ports**:
  - `max_tokens` (IntInput) — display: "Max Tokens"; info: The maximum number of tokens to generate. Set to 0 for unlimited tokens.
  - `model_name` (DropdownInput) — display: "Model Name"; options: ['open-mixtral-8x7b', 'open-mixtral-8x22b', 'mistral-small-latest', 'mistral-medium-latest', 'mistral-large-latest', 'codestral-latest']; default: 'codestral-latest'
  - `mistral_api_base` (StrInput) — display: "Mistral API Base"; info: The base URL of the Mistral API. Defaults to https://api.mistral.ai/v1. You can change this to use other APIs like JinaChat, LocalAI and Prem.
  - `api_key` (SecretStrInput) — display: "Mistral API Key"; required: true; default: 'MISTRAL_API_KEY'; info: The Mistral API Key to use for the Mistral model.
  - `temperature` (FloatInput) — display: "Temperature"; default: 0.1
  - `max_retries` (IntInput) — display: "Max Retries"; default: 5
  - `timeout` (IntInput) — display: "Timeout"; default: 60
  - `max_concurrent_requests` (IntInput) — display: "Max Concurrent Requests"; default: 3
  - `top_p` (FloatInput) — display: "Top P"; default: 1
  - `random_seed` (IntInput) — display: "Random Seed"; default: 1
  - `safe_mode` (BoolInput) — display: "Safe Mode"; default: False

- **Output ports**:
  - _No class-level outputs declared._

### Novita AI

- **Class**: `NovitaModelComponent`
- **Source**: `models/novita.py`
- **Description**: Generates text using Novita AI LLMs (OpenAI compatible).

- **Input/configuration ports**:
  - `max_tokens` (IntInput) — display: "Max Tokens"; info: The maximum number of tokens to generate. Set to 0 for unlimited tokens.
  - `model_kwargs` (DictInput) — display: "Model Kwargs"; info: Additional keyword arguments to pass to the model.
  - `json_mode` (BoolInput) — display: "JSON Mode"; info: If True, it will output JSON regardless of passing a schema.
  - `model_name` (DropdownInput) — display: "Model Name"; options: MODEL_NAMES; default: MODEL_NAMES[0]
  - `api_key` (SecretStrInput) — display: "Novita API Key"; default: 'NOVITA_API_KEY'; info: The Novita API Key to use for Novita AI models.
  - `temperature` (SliderInput) — display: "Temperature"; default: 0.1
  - `seed` (IntInput) — display: "Seed"; default: 1; info: The seed controls the reproducibility of the job.
  - `output_parser` (HandleInput) — display: "Output Parser"; input_types: ['OutputParser']; info: The parser to use to parse the output of the model

- **Output ports**:
  - _No class-level outputs declared._

### NVIDIA

- **Class**: `NVIDIAModelComponent`
- **Source**: `models/nvidia.py`
- **Description**: Generates text using NVIDIA LLMs.

- **Input/configuration ports**:
  - `max_tokens` (IntInput) — display: "Max Tokens"; info: The maximum number of tokens to generate. Set to 0 for unlimited tokens.
  - `model_name` (DropdownInput) — display: "Model Name"; options: [model.id for model in all_models]; default: None; info: The name of the NVIDIA model to use.
  - `detailed_thinking` (BoolInput) — display: "Detailed Thinking"; default: False; info: If true, the model will return a detailed thought process. Only supported by reasoning models.
  - `tool_model_enabled` (BoolInput) — display: "Enable Tool Models"; default: False; info: If enabled, only show models that support tool-calling.
  - `base_url` (MessageTextInput) — display: "NVIDIA Base URL"; default: 'https://integrate.api.nvidia.com/v1'; info: The base URL of the NVIDIA API. Defaults to https://integrate.api.nvidia.com/v1.
  - `api_key` (SecretStrInput) — display: "NVIDIA API Key"; default: 'NVIDIA_API_KEY'; info: The NVIDIA API Key.
  - `temperature` (SliderInput) — display: "Temperature"; default: 0.1; info: Run inference with this temperature.
  - `seed` (IntInput) — display: "Seed"; default: 1; info: The seed controls the reproducibility of the job.

- **Output ports**:
  - _No class-level outputs declared._

### Ollama

- **Class**: `ChatOllamaComponent`
- **Source**: `models/ollama.py`
- **Description**: Generate text using Ollama Local LLMs.

- **Input/configuration ports**:
  - `base_url` (MessageTextInput) — display: "Base URL"; default: ''; info: Endpoint of the Ollama API.
  - `model_name` (DropdownInput) — display: "Model Name"; options: []; info: Refer to https://ollama.com/library for more models.
  - `temperature` (SliderInput) — display: "Temperature"; default: 0.1
  - `format` (MessageTextInput) — display: "Format"; info: Specify the format of the output (e.g., json).
  - `metadata` (DictInput) — display: "Metadata"; info: Metadata to add to the run trace.
  - `mirostat` (DropdownInput) — display: "Mirostat"; options: ['Disabled', 'Mirostat', 'Mirostat 2.0']; default: 'Disabled'; info: Enable/disable Mirostat sampling for controlling perplexity.
  - `mirostat_eta` (FloatInput) — display: "Mirostat Eta"; info: Learning rate for Mirostat algorithm. (Default: 0.1)
  - `mirostat_tau` (FloatInput) — display: "Mirostat Tau"; info: Controls the balance between coherence and diversity of the output. (Default: 5.0)
  - `num_ctx` (IntInput) — display: "Context Window Size"; info: Size of the context window for generating tokens. (Default: 2048)
  - `num_gpu` (IntInput) — display: "Number of GPUs"; info: Number of GPUs to use for computation. (Default: 1 on macOS, 0 to disable)
  - `num_thread` (IntInput) — display: "Number of Threads"; info: Number of threads to use during computation. (Default: detected for optimal performance)
  - `repeat_last_n` (IntInput) — display: "Repeat Last N"; info: How far back the model looks to prevent repetition. (Default: 64, 0 = disabled, -1 = num_ctx)
  - `repeat_penalty` (FloatInput) — display: "Repeat Penalty"; info: Penalty for repetitions in generated text. (Default: 1.1)
  - `tfs_z` (FloatInput) — display: "TFS Z"; info: Tail free sampling value. (Default: 1)
  - `timeout` (IntInput) — display: "Timeout"; info: Timeout for the request stream.
  - `top_k` (IntInput) — display: "Top K"; info: Limits token selection to top K. (Default: 40)
  - `top_p` (FloatInput) — display: "Top P"; info: Works together with top-k. (Default: 0.9)
  - `verbose` (BoolInput) — display: "Verbose"; info: Whether to print out response text.
  - `tags` (MessageTextInput) — display: "Tags"; info: Comma-separated list of tags to add to the run trace.
  - `stop_tokens` (MessageTextInput) — display: "Stop Tokens"; info: Comma-separated list of tokens to signal the model to stop generating text.
  - `system` (MessageTextInput) — display: "System"; info: System to use for generating text.
  - `tool_model_enabled` (BoolInput) — display: "Tool Model Enabled"; default: False; info: Whether to enable tool calling in the model.
  - `template` (MessageTextInput) — display: "Template"; info: Template to use for generating text.

- **Output ports**:
  - _No class-level outputs declared._

### OpenAI

- **Class**: `OpenAIModelComponent`
- **Source**: `models/openai_chat_model.py`
- **Description**: Generates text using OpenAI LLMs.

- **Input/configuration ports**:
  - `max_tokens` (IntInput) — display: "Max Tokens"; info: The maximum number of tokens to generate. Set to 0 for unlimited tokens.
  - `model_kwargs` (DictInput) — display: "Model Kwargs"; info: Additional keyword arguments to pass to the model.
  - `json_mode` (BoolInput) — display: "JSON Mode"; info: If True, it will output JSON regardless of passing a schema.
  - `model_name` (DropdownInput) — display: "Model Name"; options: OPENAI_MODEL_NAMES; default: OPENAI_MODEL_NAMES[1]
  - `openai_api_base` (StrInput) — display: "OpenAI API Base"; info: The base URL of the OpenAI API. Defaults to https://api.openai.com/v1. You can change this to use other APIs like JinaChat, LocalAI and Prem.
  - `api_key` (SecretStrInput) — display: "OpenAI API Key"; required: true; default: 'OPENAI_API_KEY'; info: The OpenAI API Key to use for the OpenAI model.
  - `temperature` (SliderInput) — display: "Temperature"; default: 0.1
  - `seed` (IntInput) — display: "Seed"; default: 1; info: The seed controls the reproducibility of the job.
  - `max_retries` (IntInput) — display: "Max Retries"; default: 5; info: The maximum number of retries to make when generating.
  - `timeout` (IntInput) — display: "Timeout"; default: 700; info: The timeout for requests to OpenAI completion API.

- **Output ports**:
  - _No class-level outputs declared._

### OpenRouter

- **Class**: `OpenRouterComponent`
- **Source**: `models/openrouter.py`
- **Description**: OpenRouter provides unified access to multiple AI models from different providers through a single API.

- **Input/configuration ports**:
  - `api_key` (SecretStrInput) — display: "OpenRouter API Key"; required: true; info: Your OpenRouter API key
  - `site_url` (StrInput) — display: "Site URL"; info: Your site URL for OpenRouter rankings
  - `app_name` (StrInput) — display: "App Name"; info: Your app name for OpenRouter rankings
  - `provider` (DropdownInput) — display: "Provider"; required: true; options: ['Loading providers...']; default: 'Loading providers...'; info: The AI model provider
  - `model_name` (DropdownInput) — display: "Model"; required: true; options: ['Select a provider first']; default: 'Select a provider first'; info: The model to use for chat completion
  - `temperature` (SliderInput) — display: "Temperature"; default: 0.7; info: Controls randomness. Lower values are more deterministic, higher values are more creative.
  - `max_tokens` (IntInput) — display: "Max Tokens"; info: Maximum number of tokens to generate

- **Output ports**:
  - _No class-level outputs declared._

### Perplexity

- **Class**: `PerplexityComponent`
- **Source**: `models/perplexity.py`
- **Description**: Generate text using Perplexity LLMs.

- **Input/configuration ports**:
  - `model_name` (DropdownInput) — display: "Model Name"; options: ['llama-3.1-sonar-small-128k-online', 'llama-3.1-sonar-large-128k-online', 'llama-3.1-sonar-huge-128k-online', 'llama-3.1-sonar-small-128k-chat', 'llama-3.1-sonar-large-128k-chat', 'llama-3.1-8b-instruct', 'llama-3.1-70b-instruct']; default: 'llama-3.1-sonar-small-128k-online'
  - `max_output_tokens` (IntInput) — display: "Max Output Tokens"; info: The maximum number of tokens to generate.
  - `api_key` (SecretStrInput) — display: "Perplexity API Key"; required: true; info: The Perplexity API Key to use for the Perplexity model.
  - `temperature` (SliderInput) — display: "Temperature"; default: 0.75
  - `top_p` (FloatInput) — display: "Top P"; info: The maximum cumulative probability of tokens to consider when sampling.
  - `n` (IntInput) — display: "N"; info: Number of chat completions to generate for each prompt. Note that the API may not return the full n completions if duplicates are generated.
  - `top_k` (IntInput) — display: "Top K"; info: Decode using top-k sampling: consider the set of top_k most probable tokens. Must be positive.

- **Output ports**:
  - _No class-level outputs declared._

### QianfanChatEndpointComponent

- **Class**: `QianfanChatEndpointComponent`
- **Source**: `models/baidu_qianfan_chat.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `model` (DropdownInput) — display: "Model Name"; options: ['EB-turbo-AppBuilder', 'Llama-2-70b-chat', 'ERNIE-Bot-turbo-AI', 'ERNIE-Lite-8K-0308', 'ERNIE-Speed', 'Qianfan-Chinese-Llama-2-13B', 'ERNIE-3.5-8K', 'BLOOMZ-7B', 'Qianfan-Chinese-Llama-2-7B', 'XuanYuan-70B-Chat-4bit', 'AquilaChat-7B', 'ERNIE-Bot-4', 'Llama-2-13b-chat', 'ChatGLM2-6B-32K', 'ERNIE-Bot', 'ERNIE-Speed-128k', 'ERNIE-4.0-8K', 'Qianfan-BLOOMZ-7B-compressed', 'ERNIE Speed', 'Llama-2-7b-chat', 'Mixtral-8x7B-Instruct', 'ERNIE 3.5', 'ERNIE Speed-AppBuilder', 'ERNIE-Speed-8K', 'Yi-34B-Chat']; default: 'ERNIE-4.0-8K'; info: https://python.langchain.com/docs/integrations/chat/baidu_qianfan_endpoint
  - `qianfan_ak` (SecretStrInput) — display: "Qianfan Ak"; info: which you could get from https://cloud.baidu.com/product/wenxinworkshop
  - `qianfan_sk` (SecretStrInput) — display: "Qianfan Sk"; info: which you could get from https://cloud.baidu.com/product/wenxinworkshop
  - `top_p` (FloatInput) — display: "Top p"; default: 0.8; info: Model params, only supported in ERNIE-Bot and ERNIE-Bot-turbo
  - `temperature` (FloatInput) — display: "Temperature"; default: 0.95; info: Model params, only supported in ERNIE-Bot and ERNIE-Bot-turbo
  - `penalty_score` (FloatInput) — display: "Penalty Score"; default: 1.0; info: Model params, only supported in ERNIE-Bot and ERNIE-Bot-turbo
  - `endpoint` (MessageTextInput) — display: "Endpoint"; info: Endpoint of the Qianfan LLM, required if custom model used.

- **Output ports**:
  - _No class-level outputs declared._

### SambaNova

- **Class**: `SambaNovaComponent`
- **Source**: `models/sambanova.py`
- **Description**: Generate text using Sambanova LLMs.

- **Input/configuration ports**:
  - `base_url` (StrInput) — display: "SambaNova Cloud Base Url"; info: The base URL of the Sambanova Cloud API. Defaults to https://api.sambanova.ai/v1/chat/completions. You can change this to use other urls like Sambastudio
  - `model_name` (DropdownInput) — display: "Model Name"; options: SAMBANOVA_MODEL_NAMES; default: SAMBANOVA_MODEL_NAMES[0]
  - `api_key` (SecretStrInput) — display: "Sambanova API Key"; required: true; default: 'SAMBANOVA_API_KEY'; info: The Sambanova API Key to use for the Sambanova model.
  - `max_tokens` (IntInput) — display: "Max Tokens"; default: 2048; info: The maximum number of tokens to generate.
  - `top_p` (SliderInput) — display: "top_p"; default: 1.0; info: Model top_p
  - `temperature` (SliderInput) — display: "Temperature"; default: 0.1

- **Output ports**:
  - _No class-level outputs declared._

### Vertex AI

- **Class**: `ChatVertexAIComponent`
- **Source**: `models/vertexai.py`
- **Description**: Generate text using Vertex AI LLMs.

- **Input/configuration ports**:
  - `credentials` (FileInput) — display: "Credentials"; info: JSON credentials file. Leave empty to fallback to environment variables
  - `model_name` (MessageTextInput) — display: "Model Name"; default: 'gemini-1.5-pro'
  - `project` (StrInput) — display: "Project"; info: The project ID.
  - `location` (StrInput) — display: "Location"; default: 'us-central1'
  - `max_output_tokens` (IntInput) — display: "Max Output Tokens"
  - `max_retries` (IntInput) — display: "Max Retries"; default: 1
  - `temperature` (FloatInput) — display: "Temperature"; default: 0.0
  - `top_k` (IntInput) — display: "Top K"
  - `top_p` (FloatInput) — display: "Top P"; default: 0.95
  - `verbose` (BoolInput) — display: "Verbose"; default: False

- **Output ports**:
  - _No class-level outputs declared._

### xAI

- **Class**: `XAIModelComponent`
- **Source**: `models/xai.py`
- **Description**: Generates text using xAI models like Grok.

- **Input/configuration ports**:
  - `max_tokens` (IntInput) — display: "Max Tokens"; info: The maximum number of tokens to generate. Set to 0 for unlimited tokens.
  - `model_kwargs` (DictInput) — display: "Model Kwargs"; info: Additional keyword arguments to pass to the model.
  - `json_mode` (BoolInput) — display: "JSON Mode"; info: If True, it will output JSON regardless of passing a schema.
  - `model_name` (DropdownInput) — display: "Model Name"; options: XAI_DEFAULT_MODELS; default: XAI_DEFAULT_MODELS[0]; info: The xAI model to use
  - `base_url` (MessageTextInput) — display: "xAI API Base"; default: 'https://api.x.ai/v1'; info: The base URL of the xAI API. Defaults to https://api.x.ai/v1
  - `api_key` (SecretStrInput) — display: "xAI API Key"; required: true; default: 'XAI_API_KEY'; info: The xAI API Key to use for the model.
  - `temperature` (SliderInput) — display: "Temperature"; default: 0.1
  - `seed` (IntInput) — display: "Seed"; default: 1; info: The seed controls the reproducibility of the job.

- **Output ports**:
  - _No class-level outputs declared._

## needle (1 node types)

### Needle Retriever

- **Class**: `NeedleComponent`
- **Source**: `needle/needle.py`
- **Description**: A retriever that uses the Needle API to search collections.

- **Input/configuration ports**:
  - `needle_api_key` (SecretStrInput) — display: "Needle API Key"; required: true; info: Your Needle API key.
  - `collection_id` (MessageTextInput) — display: "Collection ID"; required: true; info: The ID of the Needle collection.
  - `query` (MessageTextInput) — display: "User Query"; required: true; info: Enter your question here. In tool mode, you can also specify top_k parameter (min: 20).
  - `top_k` (IntInput) — display: "Top K Results"; required: true; default: 20; info: Number of search results to return (min: 20).

- **Output ports**:
  - `result` (Output) — display: "Result"; method: `run`

## notdiamond (1 node types)

### Not Diamond Router

- **Class**: `NotDiamondComponent`
- **Source**: `notdiamond/notdiamond.py`
- **Description**: Call the right model at the right time with the world's most powerful AI model router.

- **Input/configuration ports**:
  - `input_value` (MessageInput) — display: "Input"; required: true
  - `system_message` (MessageTextInput) — display: "System Message"; info: System message to pass to the model.
  - `models` (HandleInput) — display: "Language Models"; required: true; input_types: ['LanguageModel']; info: Link the models you want to route between.
  - `api_key` (SecretStrInput) — display: "Not Diamond API Key"; required: true; default: 'NOTDIAMOND_API_KEY'; info: The Not Diamond API Key to use for routing.
  - `preference_id` (StrInput) — display: "Preference ID"; info: The ID of the router preference that was configured via the Dashboard.
  - `tradeoff` (DropdownInput) — display: "Tradeoff"; options: ['quality', 'cost', 'latency']; default: 'quality'; info: The tradeoff between cost and latency for the router to determine the best LLM for a given query.
  - `hash_content` (BoolInput) — display: "Hash Content"; default: False; info: Whether to hash the content before being sent to the NotDiamond API.

- **Output ports**:
  - `output` (Output) — display: "Output"; method: `model_select`
  - `selected_model` (Output) — display: "Selected Model"; method: `get_selected_model`

## nvidia (2 node types)

### NVIDIA Ingest

- **Class**: `NvidiaIngestComponent`
- **Source**: `nvidia/nvidia_ingest.py`
- **Description**: Process, transform, and store data.

- **Input/configuration ports**:
  - `base_url` (MessageTextInput) — display: "NVIDIA Ingestion URL"; info: The URL of the NVIDIA Ingestion API.
  - `path` (FileInput) — display: "Path"; required: true
  - `extract_text` (BoolInput) — display: "Extract Text"; default: True; info: Extract text from documents
  - `extract_charts` (BoolInput) — display: "Extract Charts"; default: False; info: Extract text from charts
  - `extract_tables` (BoolInput) — display: "Extract Tables"; default: True; info: Extract text from tables
  - `text_depth` (DropdownInput) — display: "Text Depth"; options: ['document', 'page', 'block', 'line', 'span']; default: 'document'; info: Level at which text is extracted (applies before splitting). Support for 'block', 'line', 'span' varies by document type.
  - `split_text` (BoolInput) — display: "Split Text"; default: True; info: Split text into smaller chunks
  - `split_by` (DropdownInput) — display: "Split By"; options: ['page', 'sentence', 'word', 'size']; default: 'word'; info: How to split into chunks ('size' splits by number of characters)
  - `split_length` (IntInput) — display: "Split Length"; default: 200; info: The size of each chunk based on the 'split_by' method
  - `split_overlap` (IntInput) — display: "Split Overlap"; default: 20; info: Number of segments (as determined by the 'split_by' method) to overlap from previous chunk
  - `max_character_length` (IntInput) — display: "Max Character Length"; default: 1000; info: Maximum number of characters in each chunk
  - `sentence_window_size` (IntInput) — display: "Sentence Window Size"; default: 0; info: Number of sentences to include from previous and following chunk (when split_by='sentence')

- **Output ports**:
  - `data` (Output) — display: "Data"; method: `load_file`

### NVIDIA Rerank

- **Class**: `NvidiaRerankComponent`
- **Source**: `nvidia/nvidia_rerank.py`
- **Description**: Rerank documents using the NVIDIA API.

- **Input/configuration ports**:
  - `api_key` (SecretStrInput) — display: "NVIDIA API Key"
  - `base_url` (StrInput) — display: "Base URL"; default: 'https://integrate.api.nvidia.com/v1'; info: The base URL of the NVIDIA API. Defaults to https://integrate.api.nvidia.com/v1.
  - `model` (DropdownInput) — display: "Model"; options: ['nv-rerank-qa-mistral-4b:1']; default: 'nv-rerank-qa-mistral-4b:1'

- **Output ports**:
  - `reranked_documents` (Output) — display: "Reranked Documents"; method: `compress_documents`

## olivya (1 node types)

### Place Call

- **Class**: `OlivyaComponent`
- **Source**: `olivya/olivya.py`
- **Description**: A component to create an outbound call request from Olivya's platform.

- **Input/configuration ports**:
  - `api_key` (MessageTextInput) — display: "API Key"; required: true; default: ''; info: Your API key for authentication
  - `from_number` (MessageTextInput) — display: "From Number"; required: true; default: ''; info: The Agent's phone number
  - `to_number` (MessageTextInput) — display: "To Number"; required: true; default: ''; info: The recipient's phone number
  - `first_message` (MessageTextInput) — display: "First Message"; required: false; default: ''; info: The Agent's introductory message
  - `system_prompt` (MessageTextInput) — display: "System Prompt"; required: false; default: ''; info: The system prompt to guide the interaction
  - `conversation_history` (MessageTextInput) — display: "Conversation History"; required: false; default: ''; info: The summary of the conversation

- **Output ports**:
  - `output` (Output) — display: "Output"; method: `build_output`

## outputs (2 node types)

### Chat Output

- **Class**: `ChatOutput`
- **Source**: `outputs/chat.py`
- **Description**: Display a chat message in the Playground.

- **Input/configuration ports**:
  - `input_value` (HandleInput) — display: "Text"; required: true; input_types: ['Data', 'DataFrame', 'Message']; info: Message to be passed as output.
  - `should_store_message` (BoolInput) — display: "Store Messages"; default: True; info: Store the message in the history.
  - `sender` (DropdownInput) — display: "Sender Type"; options: [MESSAGE_SENDER_AI, MESSAGE_SENDER_USER]; default: MESSAGE_SENDER_AI; info: Type of sender.
  - `sender_name` (MessageTextInput) — display: "Sender Name"; default: MESSAGE_SENDER_NAME_AI; info: Name of the sender.
  - `session_id` (MessageTextInput) — display: "Session ID"; info: The session ID of the chat. If empty, the current session ID parameter will be used.
  - `data_template` (MessageTextInput) — display: "Data Template"; default: '{text}'; info: Template to convert Data to Text. If left empty, it will be dynamically set to the Data's text key.
  - `background_color` (MessageTextInput) — display: "Background Color"; info: The background color of the icon.
  - `chat_icon` (MessageTextInput) — display: "Icon"; info: The icon of the message.
  - `text_color` (MessageTextInput) — display: "Text Color"; info: The text color of the name
  - `clean_data` (BoolInput) — display: "Basic Clean Data"; default: True; info: Whether to clean the data

- **Output ports**:
  - `message` (Output) — display: "Message"; method: `message_response`

### Text Output

- **Class**: `TextOutputComponent`
- **Source**: `outputs/text.py`
- **Description**: Display a text output in the Playground.

- **Input/configuration ports**:
  - `input_value` (MultilineInput) — display: "Text"; info: Text to be passed as output.

- **Output ports**:
  - `text` (Output) — display: "Message"; method: `text_response`

## processing (22 node types)

### Alter Metadata

- **Class**: `AlterMetadataComponent`
- **Source**: `processing/alter_metadata.py`
- **Description**: Adds/Removes Metadata Dictionary on inputs

- **Input/configuration ports**:
  - `input_value` (HandleInput) — display: "Input"; required: false; input_types: ['Message', 'Data']; info: Object(s) to which Metadata should be added
  - `text_in` (StrInput) — display: "User Text"; required: false; info: Text input; value will be in 'text' attribute of Data object. Empty text entries are ignored.
  - `metadata` (NestedDictInput) — display: "Metadata"; required: true; input_types: ['Data']; info: Metadata to add to each object
  - `remove_fields` (MessageTextInput) — display: "Fields to Remove"; required: false; info: Metadata Fields to Remove

- **Output ports**:
  - `data` (Output) — display: "Data"; method: `process_output`
  - `dataframe` (Output) — display: "DataFrame"; method: `as_dataframe`

### Combine Data

- **Class**: `MergeDataComponent`
- **Source**: `processing/merge_data.py`
- **Description**: Combines data using different operations

- **Input/configuration ports**:
  - `data_inputs` (DataInput) — display: "Data Inputs"; required: true; info: Data to combine
  - `operation` (DropdownInput) — display: "Operation Type"; options: [op.value for op in DataOperation]; default: DataOperation.CONCATENATE.value

- **Output ports**:
  - `combined_data` (Output) — display: "DataFrame"; method: `combine_data`

### Combine Text

- **Class**: `CombineTextComponent`
- **Source**: `processing/combine_text.py`
- **Description**: Concatenate two text sources into a single text chunk using a specified delimiter.

- **Input/configuration ports**:
  - `text1` (MessageTextInput) — display: "First Text"; info: The first text input to concatenate.
  - `text2` (MessageTextInput) — display: "Second Text"; info: The second text input to concatenate.
  - `delimiter` (MessageTextInput) — display: "Delimiter"; default: ' '; info: A string used to separate the two text inputs. Defaults to a whitespace.

- **Output ports**:
  - `combined_text` (Output) — display: "Combined Text"; method: `combine_texts`

### CreateDataComponent

- **Class**: `CreateDataComponent`
- **Source**: `processing/create_data.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `number_of_fields` (IntInput) — display: "Number of Fields"; default: 1; info: Number of fields to be added to the record.
  - `text_key` (MessageTextInput) — display: "Text Key"; info: Key that identifies the field to be used as the text content.
  - `text_key_validator` (BoolInput) — display: "Text Key Validator"; info: If enabled, checks if the given 'Text Key' is present in the given 'Data'.

- **Output ports**:
  - `data` (Output) — display: "Data"; method: `build_data`

### Data to Message

- **Class**: `ParseDataComponent`
- **Source**: `processing/parse_data.py`
- **Description**: Convert Data objects into Messages using any {field_name} from input data.

- **Input/configuration ports**:
  - `data` (DataInput) — display: "Data"; required: true; info: The data to convert to text.
  - `template` (MultilineInput) — display: "Template"; required: true; default: '{text}'; info: The template to use for formatting the data. It can contain the keys {text}, {data} or any other key in the Data.
  - `sep` (StrInput) — display: "Separator"; default: '\n'

- **Output ports**:
  - `text` (Output) — display: "Message"; method: `parse_data`
  - `data_list` (Output) — display: "Data List"; method: `parse_data_as_list`

### Data → DataFrame

- **Class**: `DataToDataFrameComponent`
- **Source**: `processing/data_to_dataframe.py`
- **Description**: Converts one or multiple Data objects into a DataFrame. Each Data object corresponds to one row. Fields from `.data` become columns, and the `.text` (if present) is placed in a 'text' column.

- **Input/configuration ports**:
  - `data_list` (DataInput) — display: "Data or Data List"; info: One or multiple Data objects to transform into a DataFrame.

- **Output ports**:
  - `dataframe` (Output) — display: "DataFrame"; method: `build_dataframe`

### DataFrame Operations

- **Class**: `DataFrameOperationsComponent`
- **Source**: `processing/dataframe_operations.py`
- **Description**: Perform various operations on a DataFrame.

- **Input/configuration ports**:
  - `df` (DataFrameInput) — display: "DataFrame"; info: The input DataFrame to operate on.
  - `operation` (DropdownInput) — display: "Operation"; options: OPERATION_CHOICES; info: Select the DataFrame operation to perform.
  - `column_name` (StrInput) — display: "Column Name"; info: The column name to use for the operation.
  - `filter_value` (MessageTextInput) — display: "Filter Value"; info: The value to filter rows by.
  - `ascending` (BoolInput) — display: "Sort Ascending"; default: True; info: Whether to sort in ascending order.
  - `new_column_name` (StrInput) — display: "New Column Name"; info: The new column name when renaming or adding a column.
  - `new_column_value` (MessageTextInput) — display: "New Column Value"; info: The value to populate the new column with.
  - `columns_to_select` (StrInput) — display: "Columns to Select"
  - `num_rows` (IntInput) — display: "Number of Rows"; default: 5; info: Number of rows to return (for head/tail).
  - `replace_value` (MessageTextInput) — display: "Value to Replace"; info: The value to replace in the column.
  - `replacement_value` (MessageTextInput) — display: "Replacement Value"; info: The value to replace with.

- **Output ports**:
  - `output` (Output) — display: "DataFrame"; method: `perform_operation`

### Extract Key

- **Class**: `ExtractDataKeyComponent`
- **Source**: `processing/extract_key.py`
- **Description**: Extract a specific key from a Data object or a list of Data objects and return the extracted value(s) as Data object(s).

- **Input/configuration ports**:
  - `data_input` (DataInput) — display: "Data Input"; info: The Data object or list of Data objects to extract the key from.
  - `key` (StrInput) — display: "Key to Extract"; info: The key in the Data object(s) to extract.

- **Output ports**:
  - `extracted_data` (Output) — display: "Extracted Data"; method: `extract_key`

### Filter Data

- **Class**: `FilterDataComponent`
- **Source**: `processing/filter_data.py`
- **Description**: Filters a Data object based on a list of keys.

- **Input/configuration ports**:
  - `data` (DataInput) — display: "Data"; info: Data object to filter.
  - `filter_criteria` (MessageTextInput) — display: "Filter Criteria"; info: List of keys to filter by.

- **Output ports**:
  - `filtered_data` (Output) — display: "Filtered Data"; method: `filter_data`

### Filter Values

- **Class**: `DataFilterComponent`
- **Source**: `processing/filter_data_values.py`
- **Description**: Filter a list of data items based on a specified key, filter value, and comparison operator. Check advanced options to select match comparision.

- **Input/configuration ports**:
  - `input_data` (DataInput) — display: "Input Data"; info: The list of data items to filter.
  - `filter_key` (MessageTextInput) — display: "Filter Key"; input_types: ['Data']; default: 'route'; info: The key to filter on (e.g., 'route').
  - `filter_value` (MessageTextInput) — display: "Filter Value"; input_types: ['Data']; default: 'CMIP'; info: The value to filter by (e.g., 'CMIP').
  - `operator` (DropdownInput) — display: "Comparison Operator"; options: ['equals', 'not equals', 'contains', 'starts with', 'ends with']; default: 'equals'; info: The operator to apply for comparing the values.

- **Output ports**:
  - `filtered_data` (Output) — display: "Filtered Data"; method: `filter_data`

### JSON Cleaner

- **Class**: `JSONCleaner`
- **Source**: `processing/json_cleaner.py`
- **Description**: Cleans the messy and sometimes incorrect JSON strings produced by LLMs so that they are fully compliant with the JSON spec.

- **Input/configuration ports**:
  - `json_str` (MessageTextInput) — display: "JSON String"; required: true; info: The JSON string to be cleaned.
  - `remove_control_chars` (BoolInput) — display: "Remove Control Characters"; required: false; info: Remove control characters from the JSON string.
  - `normalize_unicode` (BoolInput) — display: "Normalize Unicode"; required: false; info: Normalize Unicode characters in the JSON string.
  - `validate_json` (BoolInput) — display: "Validate JSON"; required: false; info: Validate the JSON string to ensure it is well-formed.

- **Output ports**:
  - `output` (Output) — display: "Cleaned JSON String"; method: `clean_json`

### Lambda Filter

- **Class**: `LambdaFilterComponent`
- **Source**: `processing/lambda_filter.py`
- **Description**: Uses an LLM to generate a lambda function for filtering or transforming structured data.

- **Input/configuration ports**:
  - `data` (DataInput) — display: "Data"; required: true; info: The structured data to filter or transform using a lambda function.
  - `llm` (HandleInput) — display: "Language Model"; required: true; input_types: ['LanguageModel']; info: Connect the 'Language Model' output from your LLM component here.
  - `filter_instruction` (MultilineInput) — display: "Instructions"; required: true; default: 'Filter the data to...'; info: Natural language instructions for how to filter or transform the data using a lambda function. Example: Filter the data to only include items where the 'status' is 'active'.
  - `sample_size` (IntInput) — display: "Sample Size"; default: 1000; info: For large datasets, number of items to sample from head/tail.
  - `max_size` (IntInput) — display: "Max Size"; default: 30000; info: Number of characters for the data to be considered large.

- **Output ports**:
  - `filtered_data` (Output) — display: "Filtered Data"; method: `filter_data`
  - `dataframe` (Output) — display: "DataFrame"; method: `as_dataframe`

### LLM Router

- **Class**: `LLMRouterComponent`
- **Source**: `processing/llm_router.py`
- **Description**: Routes the input to the most appropriate LLM based on OpenRouter model specifications

- **Input/configuration ports**:
  - `models` (HandleInput) — display: "Language Models"; required: true; input_types: ['LanguageModel']; info: List of LLMs to route between
  - `input_value` (HandleInput) — display: "Input"; input_types: ['Message']; info: The input message to be routed
  - `judge_llm` (HandleInput) — display: "Judge LLM"; input_types: ['LanguageModel']; info: LLM that will evaluate and select the most appropriate model
  - `optimization` (DropdownInput) — display: "Optimization"; options: ['quality', 'speed', 'cost', 'balanced']; default: 'balanced'; info: Optimization preference for model selection

- **Output ports**:
  - `output` (Output) — display: "Output"; method: `route_to_model`
  - `selected_model` (Output) — display: "Selected Model"; method: `get_selected_model`

### Message to Data

- **Class**: `MessageToDataComponent`
- **Source**: `processing/message_to_data.py`
- **Description**: Convert a Message object to a Data object

- **Input/configuration ports**:
  - `message` (MessageInput) — display: "Message"; info: The Message object to convert to a Data object

- **Output ports**:
  - `data` (Output) — display: "Data"; method: `convert_message_to_data`

### Parse DataFrame

- **Class**: `ParseDataFrameComponent`
- **Source**: `processing/parse_dataframe.py`
- **Description**: Convert a DataFrame into plain text following a specified template. Each column in the DataFrame is treated as a possible template key, e.g. {col_name}.

- **Input/configuration ports**:
  - `df` (DataFrameInput) — display: "DataFrame"; info: The DataFrame to convert to text rows.
  - `template` (MultilineInput) — display: "Template"; default: '{text}'; info: The template for formatting each row. Use placeholders matching column names in the DataFrame, for example '{col1}', '{col2}'.
  - `sep` (StrInput) — display: "Separator"; default: '\n'; info: String that joins all row texts when building the single Text output.

- **Output ports**:
  - `text` (Output) — display: "Text"; method: `parse_data`

### Parse JSON

- **Class**: `ParseJSONDataComponent`
- **Source**: `processing/parse_json_data.py`
- **Description**: Convert and extract JSON fields.

- **Input/configuration ports**:
  - `input_value` (HandleInput) — display: "Input"; required: true; input_types: ['Message', 'Data']; info: Data object to filter.
  - `query` (MessageTextInput) — display: "JQ Query"; required: true; info: JQ Query to filter the data. The input is always a JSON list.

- **Output ports**:
  - `filtered_data` (Output) — display: "Filtered Data"; method: `filter_data`

### Parser

- **Class**: `ParserComponent`
- **Source**: `processing/parser.py`
- **Description**: Format a DataFrame or Data object into text using a template. Enable 'Stringify' to convert input into a readable string instead.

- **Input/configuration ports**:
  - `stringify` (BoolInput) — display: "Stringify"; default: False; info: Enable to convert input to a string instead of using a template.
  - `template` (MultilineInput) — display: "Template"; required: true; default: 'Text: {text}'; info: Use variables within curly brackets to extract column values for DataFrames or key values for Data.For example: `Name: {Name}, Age: {Age}, Country: {Country}`
  - `input_data` (HandleInput) — display: "Data or DataFrame"; required: true; input_types: ['DataFrame', 'Data']; info: Accepts either a DataFrame or a Data object.
  - `sep` (MessageTextInput) — display: "Separator"; default: '\n'; info: String used to separate rows/items.

- **Output ports**:
  - `parsed_text` (Output) — display: "Parsed Text"; method: `parse_combined_text`

### Regex Extractor

- **Class**: `RegexExtractorComponent`
- **Source**: `processing/regex.py`
- **Description**: Extract patterns from text using regular expressions.

- **Input/configuration ports**:
  - `input_text` (MessageTextInput) — display: "Input Text"; required: true; info: The text to analyze
  - `pattern` (MessageTextInput) — display: "Regex Pattern"; required: true; default: ''; info: The regular expression pattern to match

- **Output ports**:
  - `data` (Output) — display: "Data"; method: `extract_matches`
  - `text` (Output) — display: "Message"; method: `get_matches_text`

### Save to File

- **Class**: `SaveToFileComponent`
- **Source**: `processing/save_to_file.py`
- **Description**: Save DataFrames, Data, or Messages to various file formats.

- **Input/configuration ports**:
  - `input_type` (DropdownInput) — display: "Input Type"; options: ['DataFrame', 'Data', 'Message']; default: 'DataFrame'; info: Select the type of input to save.
  - `df` (DataFrameInput) — display: "DataFrame"; info: The DataFrame to save.
  - `data` (DataInput) — display: "Data"; info: The Data object to save.
  - `message` (MessageInput) — display: "Message"; info: The Message to save.
  - `file_format` (DropdownInput) — display: "File Format"; options: DATA_FORMAT_CHOICES; info: Select the file format to save the input.
  - `file_path` (StrInput) — display: "File Path (including filename)"; default: './output'; info: The full file path (including filename and extension).

- **Output ports**:
  - `confirmation` (Output) — display: "Confirmation"; method: `save_to_file`

### SelectDataComponent

- **Class**: `SelectDataComponent`
- **Source**: `processing/select_data.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `data_list` (DataInput) — display: "Data List"; info: List of data to select from.
  - `data_index` (IntInput) — display: "Data Index"; default: 0; info: Index of the data to select.

- **Output ports**:
  - `selected_data` (Output) — display: "Selected Data"; method: `select_data`

### SplitTextComponent

- **Class**: `SplitTextComponent`
- **Source**: `processing/split_text.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `data_inputs` (HandleInput) — display: "Data or DataFrame"; required: true; input_types: ['Data', 'DataFrame']; info: The data with texts to split in chunks.
  - `chunk_overlap` (IntInput) — display: "Chunk Overlap"; default: 200; info: Number of characters to overlap between chunks.
  - `chunk_size` (IntInput) — display: "Chunk Size"; default: 1000; info: The maximum length of each chunk. Text is first split by separator, then chunks are merged up to this size. Individual splits larger than this won't be further divided.
  - `separator` (MessageTextInput) — display: "Separator"; default: '\n'; info: The character to split on. Use \n for newline. Examples: \n\n for paragraphs, \n for lines, . for sentences
  - `text_key` (MessageTextInput) — display: "Text Key"; default: 'text'; info: The key to use for the text column.
  - `keep_separator` (DropdownInput) — display: "Keep Separator"; options: ['False', 'True', 'Start', 'End']; default: 'False'; info: Whether to keep the separator in the output chunks and where to place it.

- **Output ports**:
  - `chunks` (Output) — display: "Chunks"; method: `split_text`
  - `dataframe` (Output) — display: "DataFrame"; method: `as_dataframe`

### UpdateDataComponent

- **Class**: `UpdateDataComponent`
- **Source**: `processing/update_data.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `old_data` (DataInput) — display: "Data"; required: true; info: The record to update.
  - `number_of_fields` (IntInput) — display: "Number of Fields"; default: 0; info: Number of fields to be added to the record.
  - `text_key` (MessageTextInput) — display: "Text Key"; info: Key that identifies the field to be used as the text content.
  - `text_key_validator` (BoolInput) — display: "Text Key Validator"; info: If enabled, checks if the given 'Text Key' is present in the given 'Data'.

- **Output ports**:
  - `data` (Output) — display: "Data"; method: `build_data`

## prompts (1 node types)

### PromptComponent

- **Class**: `PromptComponent`
- **Source**: `prompts/prompt.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `template` (PromptInput) — display: "Template"
  - `tool_placeholder` (MessageTextInput) — display: "Tool Placeholder"; info: A placeholder input for tool mode.

- **Output ports**:
  - `prompt` (Output) — display: "Prompt Message"; method: `build_prompt`

## prototypes (1 node types)

### Python Function

- **Class**: `PythonFunctionComponent`
- **Source**: `prototypes/python_function.py`
- **Description**: Define and execute a Python function that returns a Data object or a Message.

- **Input/configuration ports**:
  - `function_code` (CodeInput) — display: "Function Code"; info: The code for the function.

- **Output ports**:
  - `function_output` (Output) — display: "Function Callable"; method: `get_function_callable`
  - `function_output_data` (Output) — display: "Function Output (Data)"; method: `execute_function_data`
  - `function_output_str` (Output) — display: "Function Output (Message)"; method: `execute_function_message`

## retrievers (1 node types)

### MultiQueryRetriever

- **Class**: `MultiQueryRetrieverComponent`
- **Source**: `retrievers/multi_query.py`
- **Description**: Initialize from llm using default template.

- **Input/configuration ports**:
  - _No class-level inputs declared._

- **Output ports**:
  - _No class-level outputs declared._

## scrapegraph (3 node types)

### ScrapeGraphMarkdownifyApi

- **Class**: `ScrapeGraphMarkdownifyApi`
- **Source**: `scrapegraph/scrapegraph_markdownify_api.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `api_key` (SecretStrInput) — display: "ScrapeGraph API Key"; required: true; info: The API key to use ScrapeGraph API.
  - `url` (MessageTextInput) — display: "URL"; info: The URL to markdownify.

- **Output ports**:
  - `data` (Output) — display: "Data"; method: `scrape`

### ScrapeGraphSearchApi

- **Class**: `ScrapeGraphSearchApi`
- **Source**: `scrapegraph/scrapegraph_search_api.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `api_key` (SecretStrInput) — display: "ScrapeGraph API Key"; required: true; info: The API key to use ScrapeGraph API.
  - `user_prompt` (MessageTextInput) — display: "Search Prompt"; info: The search prompt to use.

- **Output ports**:
  - `data` (Output) — display: "Data"; method: `search`

### ScrapeGraphSmartScraperApi

- **Class**: `ScrapeGraphSmartScraperApi`
- **Source**: `scrapegraph/scrapegraph_smart_scraper_api.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `api_key` (SecretStrInput) — display: "ScrapeGraph API Key"; required: true; info: The API key to use ScrapeGraph API.
  - `url` (MessageTextInput) — display: "URL"; info: The URL to scrape.
  - `prompt` (MessageTextInput) — display: "Prompt"; info: The prompt to use for the smart scraper.

- **Output ports**:
  - `data` (Output) — display: "Data"; method: `scrape`

## tools (32 node types)

### arXiv

- **Class**: `ArXivComponent`
- **Source**: `tools/arxiv.py`
- **Description**: Search and retrieve papers from arXiv.org

- **Input/configuration ports**:
  - `search_query` (MessageTextInput) — display: "Search Query"; info: The search query for arXiv papers (e.g., 'quantum computing')
  - `search_type` (DropdownInput) — display: "Search Field"; options: ['all', 'title', 'abstract', 'author', 'cat']; default: 'all'; info: The field to search in
  - `max_results` (IntInput) — display: "Max Results"; default: 10; info: Maximum number of results to return

- **Output ports**:
  - `data` (Output) — display: "Data"; method: `search_papers`
  - `dataframe` (Output) — display: "DataFrame"; method: `as_dataframe`

### AstraDBCQLToolComponent

- **Class**: `AstraDBCQLToolComponent`
- **Source**: `tools/astradb_cql.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `tool_name` (StrInput) — display: "Tool Name"; required: true; info: The name of the tool.
  - `tool_description` (StrInput) — display: "Tool Description"; required: true; info: The tool description to be passed to the model.
  - `keyspace` (StrInput) — display: "Keyspace"; required: true; default: 'default_keyspace'; info: The keyspace name within Astra DB where the data is stored.
  - `table_name` (StrInput) — display: "Table Name"; required: true; info: The name of the table within Astra DB where the data is stored.
  - `token` (SecretStrInput) — display: "Astra DB Application Token"; required: true; default: 'ASTRA_DB_APPLICATION_TOKEN'; info: Authentication token for accessing Astra DB.
  - `api_endpoint` (StrInput) — display: "API Endpoint"; required: true; default: 'ASTRA_DB_API_ENDPOINT'; info: API endpoint URL for the Astra DB service.
  - `projection_fields` (StrInput) — display: "Projection fields"; required: true; default: '*'; info: Attributes to return separated by comma.
  - `tools_params` (TableInput) — display: "Tools Parameters"; required: false; default: []; info: Define the structure for the tool parameters. Describe the parameters in a way the LLM can understand how to use them. Add the parameters respecting the table schema (Partition Keys, Clustering Keys and Indexed Fields).
  - `partition_keys` (DictInput) — display: "DEPRECATED: Partition Keys"; required: false; info: Field name and description to the model
  - `clustering_keys` (DictInput) — display: "DEPRECATED: Clustering Keys"; required: false; info: Field name and description to the model
  - `static_filters` (DictInput) — display: "Static Filters"; info: Field name and value. When filled, it will not be generated by the LLM.
  - `number_of_results` (IntInput) — display: "Number of Results"; default: 5; info: Number of results to return.

- **Output ports**:
  - _No class-level outputs declared._

### AstraDBToolComponent

- **Class**: `AstraDBToolComponent`
- **Source**: `tools/astradb.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `tool_name` (StrInput) — display: "Tool Name"; required: true; info: The name of the tool to be passed to the LLM.
  - `tool_description` (StrInput) — display: "Tool Description"; required: true; info: Describe the tool to LLM. Add any information that can help the LLM to use the tool.
  - `keyspace` (StrInput) — display: "Keyspace Name"; default: 'default_keyspace'; info: The name of the keyspace within Astra where the collection is stored.
  - `collection_name` (StrInput) — display: "Collection Name"; required: true; info: The name of the collection within Astra DB where the vectors will be stored.
  - `token` (SecretStrInput) — display: "Astra DB Application Token"; required: true; default: 'ASTRA_DB_APPLICATION_TOKEN'; info: Authentication token for accessing Astra DB.
  - `api_endpoint` (SecretStrInput) — display: "api_endpoint"; required: true; default: 'ASTRA_DB_API_ENDPOINT'; info: API endpoint URL for the Astra DB service.
  - `projection_attributes` (StrInput) — display: "Projection Attributes"; required: true; default: '*'; info: Attributes to be returned by the tool separated by comma.
  - `tools_params_v2` (TableInput) — display: "Tools Parameters"; required: false; default: []; info: Define the structure for the tool parameters. Describe the parameters in a way the LLM can understand how to use them.
  - `tool_params` (DictInput) — display: "Tool params"; info: DEPRECATED: Attributes to filter and description to the model. Add ! for mandatory (e.g: !customerId)
  - `static_filters` (DictInput) — display: "Static filters"; info: Attributes to filter and correspoding value
  - `number_of_results` (IntInput) — display: "Number of Results"; default: 5; info: Number of results to return.
  - `use_search_query` (BoolInput) — display: "Semantic Search"; default: False; info: When this parameter is activated, the search query parameter will be used to search the collection.
  - `use_vectorize` (BoolInput) — display: "Use Astra DB Vectorize"; default: False; info: When this parameter is activated, Astra DB Vectorize method will be used to generate the embeddings.
  - `embedding` (HandleInput) — display: "Embedding Model"; input_types: ['Embeddings']
  - `semantic_search_instruction` (StrInput) — display: "Semantic Search Instruction"; required: true; default: 'Search query to find relevant documents.'; info: The instruction to use for the semantic search.

- **Output ports**:
  - _No class-level outputs declared._

### Bing Search API

- **Class**: `BingSearchAPIComponent`
- **Source**: `tools/bing_search_api.py`
- **Description**: Call the Bing Search API.

- **Input/configuration ports**:
  - `bing_subscription_key` (SecretStrInput) — display: "Bing Subscription Key"
  - `input_value` (MultilineInput) — display: "Input"
  - `bing_search_url` (MessageTextInput) — display: "Bing Search URL"
  - `k` (IntInput) — display: "Number of results"; required: true; default: 4

- **Output ports**:
  - _No class-level outputs declared._

### Calculator

- **Class**: `CalculatorComponent`
- **Source**: `tools/calculator_core.py`
- **Description**: Perform basic arithmetic operations on a given expression.

- **Input/configuration ports**:
  - `expression` (MessageTextInput) — display: "Expression"; info: The arithmetic expression to evaluate (e.g., '4*4*(33/22)+12-20').

- **Output ports**:
  - `result` (Output) — display: "Data"; method: `evaluate_expression`

### Calculator [DEPRECATED]

- **Class**: `CalculatorToolComponent`
- **Source**: `tools/calculator.py`
- **Description**: Perform basic arithmetic operations on a given expression.

- **Input/configuration ports**:
  - `expression` (MessageTextInput) — display: "Expression"; info: The arithmetic expression to evaluate (e.g., '4*4*(33/22)+12-20').

- **Output ports**:
  - _No class-level outputs declared._

### DataHub GraphQL MCP Server

- **Class**: `DataHubGraphQLMCPComponent`
- **Source**: `tools/datahub_graphql_mcp.py`
- **Description**: Connect to a DataHub MCP server to access data from a GraphQL endpoint.

- **Input/configuration ports**:
  - `mode` (TabInput) — display: "Mode"; options: ['Stdio', 'SSE']; default: 'SSE'; info: Select the connection mode
  - `graphql_endpoint` (MessageTextInput) — display: "GraphQL Endpoint"; required: true; default: 'http://localhost:8080/api/graphql'; info: DataHub GraphQL endpoint used by the MCP server.
  - `command` (MessageTextInput) — display: "MCP Command"; default: 'npx -y @datahub-project/datahub-mcp-server --graphql-endpoint http://localhost:8080/api/graphql'; info: Command for MCP stdio connection
  - `sse_url` (MessageTextInput) — display: "MCP SSE URL"; default: 'http://localhost:8080/mcp'; info: URL for MCP SSE connection
  - `tool` (DropdownInput) — display: "Tool"; required: true; options: []; default: ''; info: Select the tool to execute
  - `tool_placeholder` (MessageTextInput) — display: "Tool Placeholder"; default: ''; info: Placeholder for the tool

- **Output ports**:
  - `response` (Output) — display: "Response"; method: `build_output`

### DuckDuckGo Search

- **Class**: `DuckDuckGoSearchComponent`
- **Source**: `tools/duck_duck_go_search_run.py`
- **Description**: Search the web using DuckDuckGo with customizable result limits

- **Input/configuration ports**:
  - `input_value` (MessageTextInput) — display: "Search Query"; required: true; info: The search query to execute with DuckDuckGo
  - `max_results` (IntInput) — display: "Max Results"; required: false; default: 5; info: Maximum number of search results to return
  - `max_snippet_length` (IntInput) — display: "Max Snippet Length"; required: false; default: 100; info: Maximum length of each result snippet

- **Output ports**:
  - `data` (Output) — display: "Data"; method: `fetch_content`
  - `text` (Output) — display: "Text"; method: `fetch_content_text`

### Exa Search

- **Class**: `ExaSearchToolkit`
- **Source**: `tools/exa_search.py`
- **Description**: Exa Search toolkit for search and content retrieval

- **Input/configuration ports**:
  - `metaphor_api_key` (SecretStrInput) — display: "Exa Search API Key"
  - `use_autoprompt` (BoolInput) — display: "Use Autoprompt"; default: True
  - `search_num_results` (IntInput) — display: "Search Number of Results"; default: 5
  - `similar_num_results` (IntInput) — display: "Similar Number of Results"; default: 5

- **Output ports**:
  - `tools` (Output) — display: "Tools"; method: `build_toolkit`

### GleanSearchAPIComponent

- **Class**: `GleanSearchAPIComponent`
- **Source**: `tools/glean_search_api.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `glean_api_url` (StrInput) — display: "Glean API URL"; required: true
  - `glean_access_token` (SecretStrInput) — display: "Glean Access Token"; required: true
  - `query` (MultilineInput) — display: "Query"; required: true
  - `page_size` (IntInput) — display: "Page Size"; default: 10
  - `request_options` (NestedDictInput) — display: "Request Options"; required: false

- **Output ports**:
  - `data` (Output) — display: "Data"; method: `run_model`
  - `dataframe` (Output) — display: "DataFrame"; method: `as_dataframe`

### Google Search API

- **Class**: `GoogleSearchAPICore`
- **Source**: `tools/google_search_api_core.py`
- **Description**: Call Google Search API and return results as a DataFrame.

- **Input/configuration ports**:
  - `google_api_key` (SecretStrInput) — display: "Google API Key"; required: true
  - `google_cse_id` (SecretStrInput) — display: "Google CSE ID"; required: true
  - `input_value` (MultilineInput) — display: "Input"
  - `k` (IntInput) — display: "Number of results"; required: true; default: 4

- **Output ports**:
  - `results` (Output) — display: "Results"; method: `search_google`

### Google Search API [DEPRECATED]

- **Class**: `GoogleSearchAPIComponent`
- **Source**: `tools/google_search_api.py`
- **Description**: Call Google Search API.

- **Input/configuration ports**:
  - `google_api_key` (SecretStrInput) — display: "Google API Key"; required: true
  - `google_cse_id` (SecretStrInput) — display: "Google CSE ID"; required: true
  - `input_value` (MultilineInput) — display: "Input"
  - `k` (IntInput) — display: "Number of results"; required: true; default: 4

- **Output ports**:
  - _No class-level outputs declared._

### Google Serper API

- **Class**: `GoogleSerperAPICore`
- **Source**: `tools/google_serper_api_core.py`
- **Description**: Call the Serper.dev Google Search API.

- **Input/configuration ports**:
  - `serper_api_key` (SecretStrInput) — display: "Serper API Key"; required: true
  - `input_value` (MultilineInput) — display: "Input"
  - `k` (IntInput) — display: "Number of results"; required: true; default: 4

- **Output ports**:
  - `results` (Output) — display: "Results"; method: `search_serper`

### Google Serper API [DEPRECATED]

- **Class**: `GoogleSerperAPIComponent`
- **Source**: `tools/google_serper_api.py`
- **Description**: Call the Serper.dev Google Search API.

- **Input/configuration ports**:
  - `serper_api_key` (SecretStrInput) — display: "Serper API Key"; required: true
  - `query` (MultilineInput) — display: "Query"
  - `k` (IntInput) — display: "Number of results"; required: true; default: 4
  - `query_type` (DropdownInput) — display: "Query Type"; required: false; options: ['news', 'search']; default: 'search'
  - `query_params` (DictInput) — display: "Query Params"; required: false; default: {'gl': 'us', 'hl': 'en'}

- **Output ports**:
  - _No class-level outputs declared._

### MCP Server

- **Class**: `MCPToolsComponent`
- **Source**: `tools/mcp_component.py`
- **Description**: Connect to an MCP server and expose tools.

- **Input/configuration ports**:
  - `mode` (TabInput) — display: "Mode"; options: ['Stdio', 'SSE']; default: 'Stdio'; info: Select the connection mode
  - `command` (MessageTextInput) — display: "MCP Command"; default: 'uvx mcp-server-fetch'; info: Command for MCP stdio connection
  - `sse_url` (MessageTextInput) — display: "MCP SSE URL"; default: 'http://localhost:7860/api/v1/mcp/sse'; info: URL for MCP SSE connection
  - `tool` (DropdownInput) — display: "Tool"; required: true; options: []; default: ''; info: Select the tool to execute
  - `tool_placeholder` (MessageTextInput) — display: "Tool Placeholder"; default: ''; info: Placeholder for the tool

- **Output ports**:
  - `response` (Output) — display: "Response"; method: `build_output`

### Python Code Structured

- **Class**: `PythonCodeStructuredTool`
- **Source**: `tools/python_code_structured_tool.py`
- **Description**: structuredtool dataclass code to tool

- **Input/configuration ports**:
  - `tool_code` (MultilineInput) — display: "Tool Code"; required: true; info: Enter the dataclass code.
  - `tool_name` (MessageTextInput) — display: "Tool Name"; required: true; info: Enter the name of the tool.
  - `tool_description` (MessageTextInput) — display: "Description"; required: true; info: Enter the description of the tool.
  - `return_direct` (BoolInput) — display: "Return Directly"; info: Should the tool return the function output directly?
  - `tool_function` (DropdownInput) — display: "Tool Function"; required: true; options: []; info: Select the function for additional expressions.
  - `global_variables` (HandleInput) — display: "Global Variables"; input_types: ['Data']; info: Enter the global variables or Create Data Component.
  - `_classes` (MessageTextInput) — display: "Classes"
  - `_functions` (MessageTextInput) — display: "Functions"

- **Output ports**:
  - `result_tool` (Output) — display: "Tool"; method: `build_tool`

### Python REPL

- **Class**: `PythonREPLComponent`
- **Source**: `tools/python_repl_core.py`
- **Description**: A Python code executor that lets you run Python code with specific imported modules. Remember to always use print() to see your results. Example: print(df.head())

- **Input/configuration ports**:
  - `global_imports` (StrInput) — display: "Global Imports"; required: true; default: 'math,pandas'; info: A comma-separated list of modules to import globally, e.g. 'math,numpy,pandas'.
  - `python_code` (CodeInput) — display: "Python Code"; required: true; default: "print('Hello, World!')"; info: The Python code to execute. Only modules specified in Global Imports can be used.

- **Output ports**:
  - `results` (Output) — display: "Results"; method: `run_python_repl`

### Python REPL [DEPRECATED]

- **Class**: `PythonREPLToolComponent`
- **Source**: `tools/python_repl.py`
- **Description**: A tool for running Python code in a REPL environment.

- **Input/configuration ports**:
  - `name` (StrInput) — display: "Tool Name"; default: 'python_repl'; info: The name of the tool.
  - `description` (StrInput) — display: "Tool Description"; default: 'A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.'; info: A description of the tool.
  - `global_imports` (StrInput) — display: "Global Imports"; default: 'math'; info: A comma-separated list of modules to import globally, e.g. 'math,numpy'.
  - `code` (StrInput) — display: "Python Code"; default: "print('Hello, World!')"; info: The Python code to execute.

- **Output ports**:
  - _No class-level outputs declared._

### SearchAPIComponent

- **Class**: `SearchAPIComponent`
- **Source**: `tools/search_api.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `engine` (MessageTextInput) — display: "Engine"; default: 'google'
  - `api_key` (SecretStrInput) — display: "SearchAPI API Key"; required: true
  - `input_value` (MultilineInput) — display: "Input"
  - `search_params` (DictInput) — display: "Search parameters"
  - `max_results` (IntInput) — display: "Max Results"; default: 5
  - `max_snippet_length` (IntInput) — display: "Max Snippet Length"; default: 100

- **Output ports**:
  - _No class-level outputs declared._

### SearchComponent

- **Class**: `SearchComponent`
- **Source**: `tools/search.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `engine` (DropdownInput) — display: "Engine"; options: ['google', 'bing', 'duckduckgo']; default: 'google'
  - `api_key` (SecretStrInput) — display: "SearchAPI API Key"; required: true
  - `input_value` (MultilineInput) — display: "Input"
  - `search_params` (DictInput) — display: "Search parameters"
  - `max_results` (IntInput) — display: "Max Results"; default: 5
  - `max_snippet_length` (IntInput) — display: "Max Snippet Length"; default: 100

- **Output ports**:
  - `data` (Output) — display: "Data"; method: `fetch_content`
  - `text` (Output) — display: "Text"; method: `fetch_content_text`
  - `dataframe` (Output) — display: "DataFrame"; method: `as_dataframe`

### SearXNG Search

- **Class**: `SearXNGToolComponent`
- **Source**: `tools/searxng.py`
- **Description**: A component that searches for tools using SearXNG.

- **Input/configuration ports**:
  - `url` (MessageTextInput) — display: "URL"; required: true; default: 'http://localhost'
  - `max_results` (IntInput) — display: "Max Results"; required: true; default: 10
  - `categories` (MultiselectInput) — display: "Categories"; options: []; default: []
  - `language` (DropdownInput) — display: "Language"; options: []

- **Output ports**:
  - `result_tool` (Output) — display: "Tool"; method: `build_tool`

### Serp Search API

- **Class**: `SerpComponent`
- **Source**: `tools/serp.py`
- **Description**: Call Serp Search API with result limiting

- **Input/configuration ports**:
  - `serpapi_api_key` (SecretStrInput) — display: "SerpAPI API Key"; required: true
  - `input_value` (MultilineInput) — display: "Input"
  - `search_params` (DictInput) — display: "Parameters"
  - `max_results` (IntInput) — display: "Max Results"; default: 5
  - `max_snippet_length` (IntInput) — display: "Max Snippet Length"; default: 100

- **Output ports**:
  - `data` (Output) — display: "Data"; method: `fetch_content`
  - `text` (Output) — display: "Text"; method: `fetch_content_text`

### Serp Search API [DEPRECATED]

- **Class**: `SerpAPIComponent`
- **Source**: `tools/serp_api.py`
- **Description**: Call Serp Search API with result limiting

- **Input/configuration ports**:
  - `serpapi_api_key` (SecretStrInput) — display: "SerpAPI API Key"; required: true
  - `input_value` (MultilineInput) — display: "Input"
  - `search_params` (DictInput) — display: "Parameters"
  - `max_results` (IntInput) — display: "Max Results"; default: 5
  - `max_snippet_length` (IntInput) — display: "Max Snippet Length"; default: 100

- **Output ports**:
  - _No class-level outputs declared._

### Tavily AI Search

- **Class**: `TavilySearchComponent`
- **Source**: `tools/tavily.py`
- **Description**: **Tavily AI** is a search engine optimized for LLMs and RAG, aimed at efficient, quick, and persistent search results.

- **Input/configuration ports**:
  - `api_key` (SecretStrInput) — display: "Tavily API Key"; required: true; info: Your Tavily API Key.
  - `query` (MessageTextInput) — display: "Search Query"; info: The search query you want to execute with Tavily.
  - `search_depth` (DropdownInput) — display: "Search Depth"; options: ['basic', 'advanced']; default: 'advanced'; info: The depth of the search.
  - `topic` (DropdownInput) — display: "Search Topic"; options: ['general', 'news']; default: 'general'; info: The category of the search.
  - `time_range` (DropdownInput) — display: "Time Range"; options: ['day', 'week', 'month', 'year']; default: None; info: The time range back from the current date to include in the search results.
  - `max_results` (IntInput) — display: "Max Results"; default: 5; info: The maximum number of search results to return.
  - `include_images` (BoolInput) — display: "Include Images"; default: True; info: Include a list of query-related images in the response.
  - `include_answer` (BoolInput) — display: "Include Answer"; default: True; info: Include a short answer to original query.

- **Output ports**:
  - `data` (Output) — display: "Data"; method: `fetch_content`
  - `text` (Output) — display: "Text"; method: `fetch_content_text`

### Tavily AI Search [DEPRECATED]

- **Class**: `TavilySearchToolComponent`
- **Source**: `tools/tavily_search.py`
- **Description**: **Tavily AI** is a search engine optimized for LLMs and RAG, aimed at efficient, quick, and persistent search results. It can be used independently or as an agent tool. Note: Check 'Advanced' for all options.

- **Input/configuration ports**:
  - `api_key` (SecretStrInput) — display: "Tavily API Key"; required: true; info: Your Tavily API Key.
  - `query` (MessageTextInput) — display: "Search Query"; info: The search query you want to execute with Tavily.
  - `search_depth` (DropdownInput) — display: "Search Depth"; options: list(TavilySearchDepth); default: TavilySearchDepth.ADVANCED; info: The depth of the search.
  - `topic` (DropdownInput) — display: "Search Topic"; options: list(TavilySearchTopic); default: TavilySearchTopic.GENERAL; info: The category of the search.
  - `max_results` (IntInput) — display: "Max Results"; default: 5; info: The maximum number of search results to return.
  - `include_images` (BoolInput) — display: "Include Images"; default: True; info: Include a list of query-related images in the response.
  - `include_answer` (BoolInput) — display: "Include Answer"; default: True; info: Include a short answer to original query.

- **Output ports**:
  - _No class-level outputs declared._

### Wikidata

- **Class**: `WikidataComponent`
- **Source**: `tools/wikidata.py`
- **Description**: Performs a search using the Wikidata API.

- **Input/configuration ports**:
  - `query` (MultilineInput) — display: "Query"; required: true; info: The text query for similarity search on Wikidata.

- **Output ports**:
  - `data` (Output) — display: "Data"; method: `fetch_content`
  - `text` (Output) — display: "Message"; method: `fetch_content_text`

### Wikidata API [Deprecated]

- **Class**: `WikidataAPIComponent`
- **Source**: `tools/wikidata_api.py`
- **Description**: Performs a search using the Wikidata API.

- **Input/configuration ports**:
  - `query` (MultilineInput) — display: "Query"; required: true; info: The text query for similarity search on Wikidata.

- **Output ports**:
  - _No class-level outputs declared._

### Wikipedia

- **Class**: `WikipediaComponent`
- **Source**: `tools/wikipedia.py`
- **Description**: Call Wikipedia API.

- **Input/configuration ports**:
  - `input_value` (MultilineInput) — display: "Input"
  - `lang` (MessageTextInput) — display: "Language"; default: 'en'
  - `k` (IntInput) — display: "Number of results"; required: true; default: 4
  - `load_all_available_meta` (BoolInput) — display: "Load all available meta"; default: False
  - `doc_content_chars_max` (IntInput) — display: "Document content characters max"; default: 4000

- **Output ports**:
  - `data` (Output) — display: "Data"; method: `fetch_content`
  - `dataframe` (Output) — display: "DataFrame"; method: `as_dataframe`

### Wikipedia API [Deprecated]

- **Class**: `WikipediaAPIComponent`
- **Source**: `tools/wikipedia_api.py`
- **Description**: Call Wikipedia API.

- **Input/configuration ports**:
  - `input_value` (MultilineInput) — display: "Input"
  - `lang` (MessageTextInput) — display: "Language"; default: 'en'
  - `k` (IntInput) — display: "Number of results"; required: true; default: 4
  - `load_all_available_meta` (BoolInput) — display: "Load all available meta"; default: False
  - `doc_content_chars_max` (IntInput) — display: "Document content characters max"; default: 4000

- **Output ports**:
  - _No class-level outputs declared._

### WolframAlpha API

- **Class**: `WolframAlphaAPIComponent`
- **Source**: `tools/wolfram_alpha_api.py`
- **Description**: Enables queries to Wolfram Alpha for computational data, facts, and calculations across various topics, delivering structured responses.

- **Input/configuration ports**:
  - `input_value` (MultilineInput) — display: "Input Query"; info: Example query: 'What is the population of France?'
  - `app_id` (SecretStrInput) — display: "App ID"; required: true

- **Output ports**:
  - `data` (Output) — display: "Data"; method: `run_model`
  - `dataframe` (Output) — display: "DataFrame"; method: `as_dataframe`

### Yahoo Finance

- **Class**: `YfinanceComponent`
- **Source**: `tools/yahoo.py`
- **Description**: Uses [yfinance](https://pypi.org/project/yfinance/) (unofficial package) to access financial data and market information from Yahoo Finance.

- **Input/configuration ports**:
  - `symbol` (MessageTextInput) — display: "Stock Symbol"; info: The stock symbol to retrieve data for (e.g., AAPL, GOOG).
  - `method` (DropdownInput) — display: "Data Method"; options: list(YahooFinanceMethod); default: 'get_news'; info: The type of data to retrieve.
  - `num_news` (IntInput) — display: "Number of News"; default: 5; info: The number of news articles to retrieve (only applicable for get_news).

- **Output ports**:
  - `data` (Output) — display: "Data"; method: `fetch_content`
  - `text` (Output) — display: "Text"; method: `fetch_content_text`
  - `dataframe` (Output) — display: "DataFrame"; method: `as_dataframe`

### Yahoo Finance [DEPRECATED]

- **Class**: `YfinanceToolComponent`
- **Source**: `tools/yahoo_finance.py`
- **Description**: Uses [yfinance](https://pypi.org/project/yfinance/) (unofficial package) to access financial data and market information from Yahoo Finance.

- **Input/configuration ports**:
  - `symbol` (MessageTextInput) — display: "Stock Symbol"; info: The stock symbol to retrieve data for (e.g., AAPL, GOOG).
  - `method` (DropdownInput) — display: "Data Method"; options: list(YahooFinanceMethod); default: 'get_news'; info: The type of data to retrieve.
  - `num_news` (IntInput) — display: "Number of News"; default: 5; info: The number of news articles to retrieve (only applicable for get_news).

- **Output ports**:
  - _No class-level outputs declared._

## unstructured (1 node types)

### Unstructured API

- **Class**: `UnstructuredComponent`
- **Source**: `unstructured/unstructured.py`
- **Description**: Uses Unstructured.io API to extract clean text from raw source documents. Supports a wide range of file types.

- **Input/configuration ports**:
  - `api_key` (SecretStrInput) — display: "Unstructured.io Serverless API Key"; required: true; info: Unstructured API Key. Create at: https://app.unstructured.io/
  - `api_url` (MessageTextInput) — display: "Unstructured.io API URL"; required: false; info: Unstructured API URL.
  - `chunking_strategy` (DropdownInput) — display: "Chunking Strategy"; options: ['', 'basic', 'by_title', 'by_page', 'by_similarity']; default: ''; info: Chunking strategy to use, see https://docs.unstructured.io/api-reference/api-services/chunking
  - `unstructured_args` (NestedDictInput) — display: "Additional Arguments"; required: false; info: Optional dictionary of additional arguments to the Loader. See https://docs.unstructured.io/api-reference/api-services/api-parameters for more information.

- **Output ports**:
  - _No class-level outputs declared._

## vectorstores (23 node types)

### AstraDBGraphVectorStoreComponent

- **Class**: `AstraDBGraphVectorStoreComponent`
- **Source**: `vectorstores/astradb_graph.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `token` (SecretStrInput) — display: "Astra DB Application Token"; required: true; default: 'ASTRA_DB_APPLICATION_TOKEN'; info: Authentication token for accessing Astra DB.
  - `api_endpoint` (SecretStrInput) — display: "api_endpoint"; required: true; default: 'ASTRA_DB_API_ENDPOINT'; info: API endpoint URL for the Astra DB service.
  - `collection_name` (StrInput) — display: "Collection Name"; required: true; info: The name of the collection within Astra DB where the vectors will be stored.
  - `metadata_incoming_links_key` (StrInput) — display: "Metadata incoming links key"; info: Metadata key used for incoming links.
  - `keyspace` (StrInput) — display: "Keyspace"; info: Optional keyspace within Astra DB to use for the collection.
  - `embedding_model` (HandleInput) — display: "Embedding Model"; input_types: ['Embeddings']; info: Allows an embedding model configuration.
  - `metric` (DropdownInput) — display: "Metric"; options: ['cosine', 'dot_product', 'euclidean']; default: 'cosine'; info: Optional distance metric for vector comparisons in the vector store.
  - `batch_size` (IntInput) — display: "Batch Size"; info: Optional number of data to process in a single batch.
  - `bulk_insert_batch_concurrency` (IntInput) — display: "Bulk Insert Batch Concurrency"; info: Optional concurrency level for bulk insert operations.
  - `bulk_insert_overwrite_concurrency` (IntInput) — display: "Bulk Insert Overwrite Concurrency"; info: Optional concurrency level for bulk insert operations that overwrite existing data.
  - `bulk_delete_concurrency` (IntInput) — display: "Bulk Delete Concurrency"; info: Optional concurrency level for bulk delete operations.
  - `setup_mode` (DropdownInput) — display: "Setup Mode"; options: ['Sync', 'Off']; default: 'Sync'; info: Configuration mode for setting up the vector store, with options like 'Sync', or 'Off'.
  - `pre_delete_collection` (BoolInput) — display: "Pre Delete Collection"; default: False; info: Boolean flag to determine whether to delete the collection before creating a new one.
  - `metadata_indexing_include` (StrInput) — display: "Metadata Indexing Include"; info: Optional list of metadata fields to include in the indexing.
  - `metadata_indexing_exclude` (StrInput) — display: "Metadata Indexing Exclude"; info: Optional list of metadata fields to exclude from the indexing.
  - `collection_indexing_policy` (StrInput) — display: "Collection Indexing Policy"; info: Optional JSON string for the "indexing" field of the collection. See https://docs.datastax.com/en/astra-db-serverless/api-reference/collections.html#the-indexing-option
  - `number_of_results` (IntInput) — display: "Number of Results"; default: 4; info: Number of results to return.
  - `search_type` (DropdownInput) — display: "Search Type"; options: ['Similarity', 'Similarity with score threshold', 'MMR (Max Marginal Relevance)', 'Graph Traversal', 'MMR (Max Marginal Relevance) Graph Traversal']; default: 'MMR (Max Marginal Relevance) Graph Traversal'; info: Search type to use
  - `search_score_threshold` (FloatInput) — display: "Search Score Threshold"; default: 0; info: Minimum similarity score threshold for search results. (when using 'Similarity with score threshold')
  - `search_filter` (DictInput) — display: "Search Metadata Filter"; info: Optional dictionary of filters to apply to the search query.

- **Output ports**:
  - _No class-level outputs declared._

### AstraDBVectorStoreComponent

- **Class**: `AstraDBVectorStoreComponent`
- **Source**: `vectorstores/astradb.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `token` (SecretStrInput) — display: "Astra DB Application Token"; required: true; input_types: []; default: 'ASTRA_DB_APPLICATION_TOKEN'; info: Authentication token for accessing Astra DB.
  - `environment` (StrInput) — display: "Environment"; info: The environment for the Astra DB API Endpoint.
  - `database_name` (DropdownInput) — display: "Database"; required: true; info: The Database name for the Astra DB instance.
  - `api_endpoint` (StrInput) — display: "Astra DB API Endpoint"; info: The API Endpoint for the Astra DB instance. Supercedes database selection.
  - `collection_name` (DropdownInput) — display: "Collection"; required: true; info: The name of the collection within Astra DB where the vectors will be stored.
  - `keyspace` (StrInput) — display: "Keyspace"; info: Optional keyspace within Astra DB to use for the collection.
  - `embedding_choice` (DropdownInput) — display: "Embedding Model or Astra Vectorize"; options: ['Embedding Model', 'Astra Vectorize']; default: 'Embedding Model'; info: Choose an embedding model or use Astra Vectorize.
  - `embedding_model` (HandleInput) — display: "Embedding Model"; required: false; input_types: ['Embeddings']; info: Specify the Embedding Model. Not required for Astra Vectorize collections.
  - `number_of_results` (IntInput) — display: "Number of Search Results"; default: 4; info: Number of search results to return.
  - `search_type` (DropdownInput) — display: "Search Type"; options: ['Similarity', 'Similarity with score threshold', 'MMR (Max Marginal Relevance)']; default: 'Similarity'; info: Search type to use
  - `search_score_threshold` (FloatInput) — display: "Search Score Threshold"; default: 0; info: Minimum similarity score threshold for search results. (when using 'Similarity with score threshold')
  - `advanced_search_filter` (NestedDictInput) — display: "Search Metadata Filter"; info: Optional dictionary of filters to apply to the search query.
  - `autodetect_collection` (BoolInput) — display: "Autodetect Collection"; default: True; info: Boolean flag to determine whether to autodetect the collection.
  - `content_field` (StrInput) — display: "Content Field"; info: Field to use as the text content field for the vector store.
  - `deletion_field` (StrInput) — display: "Deletion Based On Field"; info: When this parameter is provided, documents in the target collection with metadata field values matching the input metadata field value will be deleted before new data is loaded.
  - `ignore_invalid_documents` (BoolInput) — display: "Ignore Invalid Documents"; info: Boolean flag to determine whether to ignore invalid documents at runtime.
  - `astradb_vectorstore_kwargs` (NestedDictInput) — display: "AstraDBVectorStore Parameters"; info: Optional dictionary of additional parameters for the AstraDBVectorStore.

- **Output ports**:
  - _No class-level outputs declared._

### Cassandra

- **Class**: `CassandraVectorStoreComponent`
- **Source**: `vectorstores/cassandra.py`
- **Description**: Cassandra Vector Store with search capabilities

- **Input/configuration ports**:
  - `database_ref` (MessageTextInput) — display: "Contact Points / Astra Database ID"; required: true; info: Contact points for the database (or AstraDB database ID)
  - `username` (MessageTextInput) — display: "Username"; info: Username for the database (leave empty for AstraDB).
  - `token` (SecretStrInput) — display: "Password / AstraDB Token"; required: true; info: User password for the database (or AstraDB token).
  - `keyspace` (MessageTextInput) — display: "Keyspace"; required: true; info: Table Keyspace (or AstraDB namespace).
  - `table_name` (MessageTextInput) — display: "Table Name"; required: true; info: The name of the table (or AstraDB collection) where vectors will be stored.
  - `ttl_seconds` (IntInput) — display: "TTL Seconds"; info: Optional time-to-live for the added texts.
  - `batch_size` (IntInput) — display: "Batch Size"; default: 16; info: Optional number of data to process in a single batch.
  - `setup_mode` (DropdownInput) — display: "Setup Mode"; options: ['Sync', 'Async', 'Off']; default: 'Sync'; info: Configuration mode for setting up the Cassandra table, with options like 'Sync', 'Async', or 'Off'.
  - `cluster_kwargs` (DictInput) — display: "Cluster arguments"; info: Optional dictionary of additional keyword arguments for the Cassandra cluster.
  - `embedding` (HandleInput) — display: "Embedding"; input_types: ['Embeddings']
  - `number_of_results` (IntInput) — display: "Number of Results"; default: 4; info: Number of results to return.
  - `search_type` (DropdownInput) — display: "Search Type"; options: ['Similarity', 'Similarity with score threshold', 'MMR (Max Marginal Relevance)']; default: 'Similarity'; info: Search type to use
  - `search_score_threshold` (FloatInput) — display: "Search Score Threshold"; default: 0; info: Minimum similarity score threshold for search results. (when using 'Similarity with score threshold')
  - `search_filter` (DictInput) — display: "Search Metadata Filter"; info: Optional dictionary of filters to apply to the search query.
  - `body_search` (MessageTextInput) — display: "Search Body"; info: Document textual search terms to apply to the search query.
  - `enable_body_search` (BoolInput) — display: "Enable Body Search"; default: False; info: Flag to enable body search. This must be enabled BEFORE the table is created.

- **Output ports**:
  - _No class-level outputs declared._

### Cassandra Graph

- **Class**: `CassandraGraphVectorStoreComponent`
- **Source**: `vectorstores/cassandra_graph.py`
- **Description**: Cassandra Graph Vector Store

- **Input/configuration ports**:
  - `database_ref` (MessageTextInput) — display: "Contact Points / Astra Database ID"; required: true; info: Contact points for the database (or AstraDB database ID)
  - `username` (MessageTextInput) — display: "Username"; info: Username for the database (leave empty for AstraDB).
  - `token` (SecretStrInput) — display: "Password / AstraDB Token"; required: true; info: User password for the database (or AstraDB token).
  - `keyspace` (MessageTextInput) — display: "Keyspace"; required: true; info: Table Keyspace (or AstraDB namespace).
  - `table_name` (MessageTextInput) — display: "Table Name"; required: true; info: The name of the table (or AstraDB collection) where vectors will be stored.
  - `setup_mode` (DropdownInput) — display: "Setup Mode"; options: ['Sync', 'Off']; default: 'Sync'; info: Configuration mode for setting up the Cassandra table, with options like 'Sync' or 'Off'.
  - `cluster_kwargs` (DictInput) — display: "Cluster arguments"; info: Optional dictionary of additional keyword arguments for the Cassandra cluster.
  - `embedding` (HandleInput) — display: "Embedding"; input_types: ['Embeddings']
  - `number_of_results` (IntInput) — display: "Number of Results"; default: 4; info: Number of results to return.
  - `search_type` (DropdownInput) — display: "Search Type"; options: ['Traversal', 'MMR traversal', 'Similarity', 'Similarity with score threshold', 'MMR (Max Marginal Relevance)']; default: 'Traversal'; info: Search type to use
  - `depth` (IntInput) — display: "Depth of traversal"; default: 1; info: The maximum depth of edges to traverse. (when using 'Traversal' or 'MMR traversal')
  - `search_score_threshold` (FloatInput) — display: "Search Score Threshold"; default: 0; info: Minimum similarity score threshold for search results. (when using 'Similarity with score threshold')
  - `search_filter` (DictInput) — display: "Search Metadata Filter"; info: Optional dictionary of filters to apply to the search query.

- **Output ports**:
  - _No class-level outputs declared._

### ChromaVectorStoreComponent

- **Class**: `ChromaVectorStoreComponent`
- **Source**: `vectorstores/chroma.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `collection_name` (StrInput) — display: "Collection Name"; default: 'langflow'
  - `persist_directory` (StrInput) — display: "Persist Directory"
  - `embedding` (HandleInput) — display: "Embedding"; input_types: ['Embeddings']
  - `chroma_server_cors_allow_origins` (StrInput) — display: "Server CORS Allow Origins"
  - `chroma_server_host` (StrInput) — display: "Server Host"
  - `chroma_server_http_port` (IntInput) — display: "Server HTTP Port"
  - `chroma_server_grpc_port` (IntInput) — display: "Server gRPC Port"
  - `chroma_server_ssl_enabled` (BoolInput) — display: "Server SSL Enabled"
  - `allow_duplicates` (BoolInput) — display: "Allow Duplicates"; info: If false, will not add documents that are already in the Vector Store.
  - `search_type` (DropdownInput) — display: "Search Type"; options: ['Similarity', 'MMR']; default: 'Similarity'
  - `number_of_results` (IntInput) — display: "Number of Results"; default: 10; info: Number of results to return.
  - `limit` (IntInput) — display: "Limit"; info: Limit the number of records to compare when Allow Duplicates is False.

- **Output ports**:
  - _No class-level outputs declared._

### Clickhouse

- **Class**: `ClickhouseVectorStoreComponent`
- **Source**: `vectorstores/clickhouse.py`
- **Description**: Clickhouse Vector Store with search capabilities

- **Input/configuration ports**:
  - `host` (StrInput) — display: "hostname"; required: true; default: 'localhost'
  - `port` (IntInput) — display: "port"; required: true; default: 8123
  - `database` (StrInput) — display: "database"; required: true
  - `table` (StrInput) — display: "Table name"; required: true
  - `username` (StrInput) — display: "The ClickHouse user name."; required: true
  - `password` (SecretStrInput) — display: "The password for username."; required: true
  - `index_type` (DropdownInput) — display: "index_type"; options: ['annoy', 'vector_similarity']; default: 'annoy'; info: Type of the index.
  - `metric` (DropdownInput) — display: "metric"; options: ['angular', 'euclidean', 'manhattan', 'hamming', 'dot']; default: 'angular'; info: Metric to compute distance.
  - `secure` (BoolInput) — display: "Use https/TLS. This overrides inferred values from the interface or port arguments."; default: False
  - `index_param` (StrInput) — display: "Param of the index"; default: "100,'L2Distance'"
  - `index_query_params` (DictInput) — display: "index query params"
  - `embedding` (HandleInput) — display: "Embedding"; input_types: ['Embeddings']
  - `number_of_results` (IntInput) — display: "Number of Results"; default: 4; info: Number of results to return.
  - `score_threshold` (FloatInput) — display: "Score threshold"

- **Output ports**:
  - _No class-level outputs declared._

### Couchbase

- **Class**: `CouchbaseVectorStoreComponent`
- **Source**: `vectorstores/couchbase.py`
- **Description**: Couchbase Vector Store with search capabilities

- **Input/configuration ports**:
  - `couchbase_connection_string` (SecretStrInput) — display: "Couchbase Cluster connection string"; required: true
  - `couchbase_username` (StrInput) — display: "Couchbase username"; required: true
  - `couchbase_password` (SecretStrInput) — display: "Couchbase password"; required: true
  - `bucket_name` (StrInput) — display: "Bucket Name"; required: true
  - `scope_name` (StrInput) — display: "Scope Name"; required: true
  - `collection_name` (StrInput) — display: "Collection Name"; required: true
  - `index_name` (StrInput) — display: "Index Name"; required: true
  - `embedding` (HandleInput) — display: "Embedding"; input_types: ['Embeddings']
  - `number_of_results` (IntInput) — display: "Number of Results"; default: 4; info: Number of results to return.

- **Output ports**:
  - _No class-level outputs declared._

### ElasticsearchVectorStoreComponent

- **Class**: `ElasticsearchVectorStoreComponent`
- **Source**: `vectorstores/elasticsearch.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `elasticsearch_url` (StrInput) — display: "Elasticsearch URL"; default: 'http://localhost:9200'; info: URL for self-managed Elasticsearch deployments (e.g., http://localhost:9200). Do not use with Elastic Cloud deployments, use Elastic Cloud ID instead.
  - `cloud_id` (SecretStrInput) — display: "Elastic Cloud ID"; default: ''; info: Use this for Elastic Cloud deployments. Do not use together with 'Elasticsearch URL'.
  - `index_name` (StrInput) — display: "Index Name"; default: 'langflow'; info: The index name where the vectors will be stored in Elasticsearch cluster.
  - `username` (StrInput) — display: "Username"; default: ''; info: Elasticsearch username (e.g., 'elastic'). Required for both local and Elastic Cloud setups unless API keys are used.
  - `password` (SecretStrInput) — display: "Password"; default: ''; info: Elasticsearch password for the specified user. Required for both local and Elastic Cloud setups unless API keys are used.
  - `embedding` (HandleInput) — display: "Embedding"; input_types: ['Embeddings']
  - `search_type` (DropdownInput) — display: "Search Type"; options: ['similarity', 'mmr']; default: 'similarity'
  - `number_of_results` (IntInput) — display: "Number of Results"; default: 4; info: Number of results to return.
  - `search_score_threshold` (FloatInput) — display: "Search Score Threshold"; default: 0.0; info: Minimum similarity score threshold for search results.
  - `api_key` (SecretStrInput) — display: "Elastic API Key"; default: ''; info: API Key for Elastic Cloud authentication. If used, 'username' and 'password' are not required.

- **Output ports**:
  - _No class-level outputs declared._

### FaissVectorStoreComponent

- **Class**: `FaissVectorStoreComponent`
- **Source**: `vectorstores/faiss.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `index_name` (StrInput) — display: "Index Name"; default: 'langflow_index'
  - `persist_directory` (StrInput) — display: "Persist Directory"; info: Path to save the FAISS index. It will be relative to where Langflow is running.
  - `allow_dangerous_deserialization` (BoolInput) — display: "Allow Dangerous Deserialization"; default: True; info: Set to True to allow loading pickle files from untrusted sources. Only enable this if you trust the source of the data.
  - `embedding` (HandleInput) — display: "Embedding"; input_types: ['Embeddings']
  - `number_of_results` (IntInput) — display: "Number of Results"; default: 4; info: Number of results to return.

- **Output ports**:
  - _No class-level outputs declared._

### GraphRAGComponent

- **Class**: `GraphRAGComponent`
- **Source**: `vectorstores/graph_rag.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `embedding_model` (HandleInput) — display: "Embedding Model"; required: false; input_types: ['Embeddings']; info: Specify the Embedding Model. Not required for Astra Vectorize collections.
  - `vector_store` (HandleInput) — display: "Vector Store Connection"; input_types: ['VectorStore']; info: Connection to Vector Store.
  - `edge_definition` (StrInput) — display: "Edge Definition"; info: Edge definition for the graph traversal.
  - `strategy` (DropdownInput) — display: "Traversal Strategies"; options: traversal_strategies()
  - `search_query` (MultilineInput) — display: "Search Query"
  - `graphrag_strategy_kwargs` (NestedDictInput) — display: "Strategy Parameters"; info: Optional dictionary of additional parameters for the retrieval strategy. Please see https://datastax.github.io/graph-rag/reference/graph_retriever/strategies/ for details.

- **Output ports**:
  - _No class-level outputs declared._

### HCDVectorStoreComponent

- **Class**: `HCDVectorStoreComponent`
- **Source**: `vectorstores/hcd.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `collection_name` (StrInput) — display: "Collection Name"; required: true; info: The name of the collection within HCD where the vectors will be stored.
  - `username` (StrInput) — display: "HCD Username"; required: true; default: 'hcd-superuser'; info: Authentication username for accessing HCD.
  - `password` (SecretStrInput) — display: "HCD Password"; required: true; default: 'HCD_PASSWORD'; info: Authentication password for accessing HCD.
  - `api_endpoint` (SecretStrInput) — display: "HCD API Endpoint"; required: true; default: 'HCD_API_ENDPOINT'; info: API endpoint URL for the HCD service.
  - `namespace` (StrInput) — display: "Namespace"; default: 'default_namespace'; info: Optional namespace within HCD to use for the collection.
  - `ca_certificate` (MultilineInput) — display: "CA Certificate"; info: Optional CA certificate for TLS connections to HCD.
  - `metric` (DropdownInput) — display: "Metric"; options: ['cosine', 'dot_product', 'euclidean']; info: Optional distance metric for vector comparisons in the vector store.
  - `batch_size` (IntInput) — display: "Batch Size"; info: Optional number of data to process in a single batch.
  - `bulk_insert_batch_concurrency` (IntInput) — display: "Bulk Insert Batch Concurrency"; info: Optional concurrency level for bulk insert operations.
  - `bulk_insert_overwrite_concurrency` (IntInput) — display: "Bulk Insert Overwrite Concurrency"; info: Optional concurrency level for bulk insert operations that overwrite existing data.
  - `bulk_delete_concurrency` (IntInput) — display: "Bulk Delete Concurrency"; info: Optional concurrency level for bulk delete operations.
  - `setup_mode` (DropdownInput) — display: "Setup Mode"; options: ['Sync', 'Async', 'Off']; default: 'Sync'; info: Configuration mode for setting up the vector store, with options like 'Sync', 'Async', or 'Off'.
  - `pre_delete_collection` (BoolInput) — display: "Pre Delete Collection"; info: Boolean flag to determine whether to delete the collection before creating a new one.
  - `metadata_indexing_include` (StrInput) — display: "Metadata Indexing Include"; info: Optional list of metadata fields to include in the indexing.
  - `embedding` (HandleInput) — display: "Embedding or Astra Vectorize"; input_types: ['Embeddings', 'dict']; info: Allows either an embedding model or an Astra Vectorize configuration.
  - `metadata_indexing_exclude` (StrInput) — display: "Metadata Indexing Exclude"; info: Optional list of metadata fields to exclude from the indexing.
  - `collection_indexing_policy` (StrInput) — display: "Collection Indexing Policy"; info: Optional dictionary defining the indexing policy for the collection.
  - `number_of_results` (IntInput) — display: "Number of Results"; default: 4; info: Number of results to return.
  - `search_type` (DropdownInput) — display: "Search Type"; options: ['Similarity', 'Similarity with score threshold', 'MMR (Max Marginal Relevance)']; default: 'Similarity'; info: Search type to use
  - `search_score_threshold` (FloatInput) — display: "Search Score Threshold"; default: 0; info: Minimum similarity score threshold for search results. (when using 'Similarity with score threshold')
  - `search_filter` (DictInput) — display: "Search Metadata Filter"; info: Optional dictionary of filters to apply to the search query.

- **Output ports**:
  - _No class-level outputs declared._

### MilvusVectorStoreComponent

- **Class**: `MilvusVectorStoreComponent`
- **Source**: `vectorstores/milvus.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `collection_name` (StrInput) — display: "Collection Name"; default: 'langflow'
  - `collection_description` (StrInput) — display: "Collection Description"; default: ''
  - `uri` (StrInput) — display: "Connection URI"; default: 'http://localhost:19530'
  - `password` (SecretStrInput) — display: "Token"; default: ''; info: Ignore this field if no token is required to make connection.
  - `connection_args` (DictInput) — display: "Other Connection Arguments"
  - `primary_field` (StrInput) — display: "Primary Field Name"; default: 'pk'
  - `text_field` (StrInput) — display: "Text Field Name"; default: 'text'
  - `vector_field` (StrInput) — display: "Vector Field Name"; default: 'vector'
  - `consistency_level` (DropdownInput) — display: "Consistencey Level"; options: ['Bounded', 'Session', 'Strong', 'Eventual']; default: 'Session'
  - `index_params` (DictInput) — display: "Index Parameters"
  - `search_params` (DictInput) — display: "Search Parameters"
  - `drop_old` (BoolInput) — display: "Drop Old Collection"; default: False
  - `timeout` (FloatInput) — display: "Timeout"
  - `embedding` (HandleInput) — display: "Embedding"; input_types: ['Embeddings']
  - `number_of_results` (IntInput) — display: "Number of Results"; default: 4; info: Number of results to return.

- **Output ports**:
  - _No class-level outputs declared._

### MongoDB Atlas

- **Class**: `MongoVectorStoreComponent`
- **Source**: `vectorstores/mongodb_atlas.py`
- **Description**: MongoDB Atlas Vector Store with search capabilities

- **Input/configuration ports**:
  - `mongodb_atlas_cluster_uri` (SecretStrInput) — display: "MongoDB Atlas Cluster URI"; required: true
  - `enable_mtls` (BoolInput) — display: "Enable mTLS"; required: true; default: False
  - `mongodb_atlas_client_cert` (SecretStrInput) — display: "MongoDB Atlas Combined Client Certificate"; required: false; info: Client Certificate combined with the private key in the following format: -----BEGIN PRIVATE KEY----- ... -----END PRIVATE KEY----- -----BEGIN CERTIFICATE----- ... -----END CERTIFICATE-----
  - `db_name` (StrInput) — display: "Database Name"; required: true
  - `collection_name` (StrInput) — display: "Collection Name"; required: true
  - `index_name` (StrInput) — display: "Index Name"; required: true
  - `embedding` (HandleInput) — display: "Embedding"; input_types: ['Embeddings']
  - `number_of_results` (IntInput) — display: "Number of Results"; default: 4; info: Number of results to return.

- **Output ports**:
  - _No class-level outputs declared._

### OpenSearchVectorStoreComponent

- **Class**: `OpenSearchVectorStoreComponent`
- **Source**: `vectorstores/opensearch.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `opensearch_url` (StrInput) — display: "OpenSearch URL"; default: 'http://localhost:9200'; info: URL for OpenSearch cluster (e.g. https://192.168.1.1:9200).
  - `index_name` (StrInput) — display: "Index Name"; default: 'langflow'; info: The index name where the vectors will be stored in OpenSearch cluster.
  - `embedding` (HandleInput) — display: "Embedding"; input_types: ['Embeddings']
  - `search_type` (DropdownInput) — display: "Search Type"; options: ['similarity', 'similarity_score_threshold', 'mmr']; default: 'similarity'
  - `number_of_results` (IntInput) — display: "Number of Results"; default: 4; info: Number of results to return.
  - `search_score_threshold` (FloatInput) — display: "Search Score Threshold"; default: 0.0; info: Minimum similarity score threshold for search results.
  - `username` (StrInput) — display: "Username"; default: 'admin'
  - `password` (SecretStrInput) — display: "Password"; default: 'admin'
  - `use_ssl` (BoolInput) — display: "Use SSL"; default: True
  - `verify_certs` (BoolInput) — display: "Verify Certificates"; default: False
  - `hybrid_search_query` (MultilineInput) — display: "Hybrid Search Query"; default: ''; info: Provide a custom hybrid search query in JSON format. This allows you to combine vector similarity and keyword matching.

- **Output ports**:
  - _No class-level outputs declared._

### PGVector

- **Class**: `PGVectorStoreComponent`
- **Source**: `vectorstores/pgvector.py`
- **Description**: PGVector Vector Store with search capabilities

- **Input/configuration ports**:
  - `pg_server_url` (SecretStrInput) — display: "PostgreSQL Server Connection String"; required: true
  - `collection_name` (StrInput) — display: "Table"; required: true
  - `embedding` (HandleInput) — display: "Embedding"; required: true; input_types: ['Embeddings']
  - `number_of_results` (IntInput) — display: "Number of Results"; default: 4; info: Number of results to return.

- **Output ports**:
  - _No class-level outputs declared._

### Pinecone

- **Class**: `PineconeVectorStoreComponent`
- **Source**: `vectorstores/pinecone.py`
- **Description**: Pinecone Vector Store with search capabilities

- **Input/configuration ports**:
  - `index_name` (StrInput) — display: "Index Name"; required: true
  - `namespace` (StrInput) — display: "Namespace"; info: Namespace for the index.
  - `distance_strategy` (DropdownInput) — display: "Distance Strategy"; options: ['Cosine', 'Euclidean', 'Dot Product']; default: 'Cosine'
  - `pinecone_api_key` (SecretStrInput) — display: "Pinecone API Key"; required: true
  - `text_key` (StrInput) — display: "Text Key"; default: 'text'; info: Key in the record to use as text.
  - `embedding` (HandleInput) — display: "Embedding"; input_types: ['Embeddings']
  - `number_of_results` (IntInput) — display: "Number of Results"; default: 4; info: Number of results to return.

- **Output ports**:
  - _No class-level outputs declared._

### Qdrant

- **Class**: `QdrantVectorStoreComponent`
- **Source**: `vectorstores/qdrant.py`
- **Description**: Qdrant Vector Store with search capabilities

- **Input/configuration ports**:
  - `collection_name` (StrInput) — display: "Collection Name"; required: true
  - `host` (StrInput) — display: "Host"; default: 'localhost'
  - `port` (IntInput) — display: "Port"; default: 6333
  - `grpc_port` (IntInput) — display: "gRPC Port"; default: 6334
  - `api_key` (SecretStrInput) — display: "API Key"
  - `prefix` (StrInput) — display: "Prefix"
  - `timeout` (IntInput) — display: "Timeout"
  - `path` (StrInput) — display: "Path"
  - `url` (StrInput) — display: "URL"
  - `distance_func` (DropdownInput) — display: "Distance Function"; options: ['Cosine', 'Euclidean', 'Dot Product']; default: 'Cosine'
  - `content_payload_key` (StrInput) — display: "Content Payload Key"; default: 'page_content'
  - `metadata_payload_key` (StrInput) — display: "Metadata Payload Key"; default: 'metadata'
  - `embedding` (HandleInput) — display: "Embedding"; input_types: ['Embeddings']
  - `number_of_results` (IntInput) — display: "Number of Results"; default: 4; info: Number of results to return.

- **Output ports**:
  - _No class-level outputs declared._

### RedisVectorStoreComponent

- **Class**: `RedisVectorStoreComponent`
- **Source**: `vectorstores/redis.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `redis_server_url` (SecretStrInput) — display: "Redis Server Connection String"; required: true
  - `redis_index_name` (StrInput) — display: "Redis Index"
  - `code` (StrInput) — display: "Code"
  - `schema` (StrInput) — display: "Schema"
  - `number_of_results` (IntInput) — display: "Number of Results"; default: 4; info: Number of results to return.
  - `embedding` (HandleInput) — display: "Embedding"; input_types: ['Embeddings']

- **Output ports**:
  - _No class-level outputs declared._

### Supabase

- **Class**: `SupabaseVectorStoreComponent`
- **Source**: `vectorstores/supabase.py`
- **Description**: Supabase Vector Store with search capabilities

- **Input/configuration ports**:
  - `supabase_url` (StrInput) — display: "Supabase URL"; required: true
  - `supabase_service_key` (SecretStrInput) — display: "Supabase Service Key"; required: true
  - `table_name` (StrInput) — display: "Table Name"
  - `query_name` (StrInput) — display: "Query Name"
  - `embedding` (HandleInput) — display: "Embedding"; input_types: ['Embeddings']
  - `number_of_results` (IntInput) — display: "Number of Results"; default: 4; info: Number of results to return.

- **Output ports**:
  - _No class-level outputs declared._

### Upstash

- **Class**: `UpstashVectorStoreComponent`
- **Source**: `vectorstores/upstash.py`
- **Description**: Upstash Vector Store with search capabilities

- **Input/configuration ports**:
  - `index_url` (StrInput) — display: "Index URL"; required: true; info: The URL of the Upstash index.
  - `index_token` (SecretStrInput) — display: "Index Token"; required: true; info: The token for the Upstash index.
  - `text_key` (StrInput) — display: "Text Key"; default: 'text'; info: The key in the record to use as text.
  - `namespace` (StrInput) — display: "Namespace"; info: Leave empty for default namespace.
  - `metadata_filter` (MultilineInput) — display: "Metadata Filter"; info: Filters documents by metadata. Look at the documentation for more information.
  - `embedding` (HandleInput) — display: "Embedding"; input_types: ['Embeddings']; info: To use Upstash's embeddings, don't provide an embedding.
  - `number_of_results` (IntInput) — display: "Number of Results"; default: 4; info: Number of results to return.

- **Output ports**:
  - _No class-level outputs declared._

### Vectara RAG

- **Class**: `VectaraRagComponent`
- **Source**: `vectorstores/vectara_rag.py`
- **Description**: Vectara's full end to end RAG

- **Input/configuration ports**:
  - `vectara_customer_id` (StrInput) — display: "Vectara Customer ID"; required: true
  - `vectara_corpus_id` (StrInput) — display: "Vectara Corpus ID"; required: true
  - `vectara_api_key` (SecretStrInput) — display: "Vectara API Key"; required: true
  - `search_query` (MessageTextInput) — display: "Search Query"; info: The query to receive an answer on.
  - `lexical_interpolation` (FloatInput) — display: "Hybrid Search Factor"; default: 0.005; info: How much to weigh lexical scores compared to the embedding score. 0 means lexical search is not used at all, and 1 means only lexical search is used.
  - `filter` (MessageTextInput) — display: "Metadata Filters"; default: ''; info: The filter string to narrow the search to according to metadata attributes.
  - `reranker` (DropdownInput) — display: "Reranker Type"; options: RERANKER_TYPES; default: RERANKER_TYPES[0]; info: How to rerank the retrieved search results.
  - `reranker_k` (IntInput) — display: "Number of Results to Rerank"; default: 50
  - `diversity_bias` (FloatInput) — display: "Diversity Bias"; default: 0.2; info: Ranges from 0 to 1, with higher values indicating greater diversity (only applies to MMR reranker).
  - `max_results` (IntInput) — display: "Max Results to Summarize"; default: 7; info: The maximum number of search results to be available to the prompt.
  - `response_lang` (DropdownInput) — display: "Response Language"; options: RESPONSE_LANGUAGES; default: 'eng'; info: Use the ISO 639-1 or 639-3 language code or auto to automatically detect the language.
  - `prompt` (DropdownInput) — display: "Prompt Name"; options: SUMMARIZER_PROMPTS; default: SUMMARIZER_PROMPTS[0]; info: Only vectara-summary-ext-24-05-sml is for Growth customers; all other prompts are for Scale customers only.

- **Output ports**:
  - `answer` (Output) — display: "Answer"; method: `generate_response`

### VectaraVectorStoreComponent

- **Class**: `VectaraVectorStoreComponent`
- **Source**: `vectorstores/vectara.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `vectara_customer_id` (StrInput) — display: "Vectara Customer ID"; required: true
  - `vectara_corpus_id` (StrInput) — display: "Vectara Corpus ID"; required: true
  - `vectara_api_key` (SecretStrInput) — display: "Vectara API Key"; required: true
  - `embedding` (HandleInput) — display: "Embedding"; input_types: ['Embeddings']
  - `number_of_results` (IntInput) — display: "Number of Results"; default: 4; info: Number of results to return.

- **Output ports**:
  - _No class-level outputs declared._

### Weaviate

- **Class**: `WeaviateVectorStoreComponent`
- **Source**: `vectorstores/weaviate.py`
- **Description**: Weaviate Vector Store with search capabilities

- **Input/configuration ports**:
  - `url` (StrInput) — display: "Weaviate URL"; required: true; default: 'http://localhost:8080'
  - `api_key` (SecretStrInput) — display: "API Key"; required: false
  - `index_name` (StrInput) — display: "Index Name"; required: true; info: Requires capitalized index name.
  - `text_key` (StrInput) — display: "Text Key"; default: 'text'
  - `embedding` (HandleInput) — display: "Embedding"; input_types: ['Embeddings']
  - `number_of_results` (IntInput) — display: "Number of Results"; default: 4; info: Number of results to return.
  - `search_by_text` (BoolInput) — display: "Search By Text"

- **Output ports**:
  - _No class-level outputs declared._

## youtube (7 node types)

### Youtube Playlist

- **Class**: `YouTubePlaylistComponent`
- **Source**: `youtube/playlist.py`
- **Description**: Extracts all video URLs from a YouTube playlist.

- **Input/configuration ports**:
  - `playlist_url` (MessageTextInput) — display: "Playlist URL"; required: true; info: URL of the YouTube playlist.

- **Output ports**:
  - `video_urls` (Output) — display: "Video URLs"; method: `extract_video_urls`

### YouTubeChannelComponent

- **Class**: `YouTubeChannelComponent`
- **Source**: `youtube/channel.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `channel_url` (MessageTextInput) — display: "Channel URL or ID"; required: true; info: The URL or ID of the YouTube channel.
  - `api_key` (SecretStrInput) — display: "YouTube API Key"; required: true; info: Your YouTube Data API key.
  - `include_statistics` (BoolInput) — display: "Include Statistics"; default: True; info: Include channel statistics (views, subscribers, videos).
  - `include_branding` (BoolInput) — display: "Include Branding"; default: True; info: Include channel branding settings (banner, thumbnails).
  - `include_playlists` (BoolInput) — display: "Include Playlists"; default: False; info: Include channel's public playlists.

- **Output ports**:
  - `channel_df` (Output) — display: "Channel Info"; method: `get_channel_info`

### YouTubeCommentsComponent

- **Class**: `YouTubeCommentsComponent`
- **Source**: `youtube/comments.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `video_url` (MessageTextInput) — display: "Video URL"; required: true; info: The URL of the YouTube video to get comments from.
  - `api_key` (SecretStrInput) — display: "YouTube API Key"; required: true; info: Your YouTube Data API key.
  - `max_results` (IntInput) — display: "Max Results"; default: 20; info: The maximum number of comments to return.
  - `sort_by` (DropdownInput) — display: "Sort By"; options: ['time', 'relevance']; default: 'relevance'; info: Sort comments by time or relevance.
  - `include_replies` (BoolInput) — display: "Include Replies"; default: False; info: Whether to include replies to comments.
  - `include_metrics` (BoolInput) — display: "Include Metrics"; default: True; info: Include metrics like like count and reply count.

- **Output ports**:
  - `comments` (Output) — display: "Comments"; method: `get_video_comments`

### YouTubeSearchComponent

- **Class**: `YouTubeSearchComponent`
- **Source**: `youtube/search.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `query` (MessageTextInput) — display: "Search Query"; required: true; info: The search query to look for on YouTube.
  - `api_key` (SecretStrInput) — display: "YouTube API Key"; required: true; info: Your YouTube Data API key.
  - `max_results` (IntInput) — display: "Max Results"; default: 10; info: The maximum number of results to return.
  - `order` (DropdownInput) — display: "Sort Order"; options: ['relevance', 'date', 'rating', 'title', 'viewCount']; default: 'relevance'; info: Sort order for the search results.
  - `include_metadata` (BoolInput) — display: "Include Metadata"; default: True; info: Include video metadata like description and statistics.

- **Output ports**:
  - `results` (Output) — display: "Search Results"; method: `search_videos`

### YouTubeTranscriptsComponent

- **Class**: `YouTubeTranscriptsComponent`
- **Source**: `youtube/youtube_transcripts.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `url` (MultilineInput) — display: "Video URL"; required: true; info: Enter the YouTube video URL to get transcripts from.
  - `chunk_size_seconds` (IntInput) — display: "Chunk Size (seconds)"; default: 60; info: The size of each transcript chunk in seconds.
  - `translation` (DropdownInput) — display: "Translation Language"; options: ['', 'en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'ja', 'ko', 'hi', 'ar', 'id']; info: Translate the transcripts to the specified language. Leave empty for no translation.

- **Output ports**:
  - `dataframe` (Output) — display: "Chunks"; method: `get_dataframe_output`
  - `message` (Output) — display: "Transcript"; method: `get_message_output`
  - `data_output` (Output) — display: "Transcript + Source"; method: `get_data_output`

### YouTubeTrendingComponent

- **Class**: `YouTubeTrendingComponent`
- **Source**: `youtube/trending.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `api_key` (SecretStrInput) — display: "YouTube API Key"; required: true; info: Your YouTube Data API key.
  - `region` (DropdownInput) — display: "Region"; options: list(COUNTRY_CODES.keys()); default: 'Global'; info: The region to get trending videos from.
  - `category` (DropdownInput) — display: "Category"; options: list(VIDEO_CATEGORIES.keys()); default: 'All'; info: The category of videos to retrieve.
  - `max_results` (IntInput) — display: "Max Results"; default: 10; info: Maximum number of trending videos to return (1-50).
  - `include_statistics` (BoolInput) — display: "Include Statistics"; default: True; info: Include video statistics (views, likes, comments).
  - `include_content_details` (BoolInput) — display: "Include Content Details"; default: True; info: Include video duration and quality info.
  - `include_thumbnails` (BoolInput) — display: "Include Thumbnails"; default: True; info: Include video thumbnail URLs.

- **Output ports**:
  - `trending_videos` (Output) — display: "Trending Videos"; method: `get_trending_videos`

### YouTubeVideoDetailsComponent

- **Class**: `YouTubeVideoDetailsComponent`
- **Source**: `youtube/video_details.py`
- **Description**: No class-level description provided.

- **Input/configuration ports**:
  - `video_url` (MessageTextInput) — display: "Video URL"; required: true; info: The URL of the YouTube video.
  - `api_key` (SecretStrInput) — display: "YouTube API Key"; required: true; info: Your YouTube Data API key.
  - `include_statistics` (BoolInput) — display: "Include Statistics"; default: True; info: Include video statistics (views, likes, comments).
  - `include_content_details` (BoolInput) — display: "Include Content Details"; default: True; info: Include video duration, quality, and age restriction info.
  - `include_tags` (BoolInput) — display: "Include Tags"; default: True; info: Include video tags and keywords.
  - `include_thumbnails` (BoolInput) — display: "Include Thumbnails"; default: True; info: Include video thumbnail URLs in different resolutions.

- **Output ports**:
  - `video_data` (Output) — display: "Video Data"; method: `get_video_details`
