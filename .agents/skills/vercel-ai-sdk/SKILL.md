---
name: vercel-ai-sdk
description: Build AI-powered streaming chat, completion, and generative UI with the Vercel AI SDK. Covers useChat, useCompletion, useObject hooks, streaming UI with RSC, and multi-provider model integration. Use when adding AI chat interfaces, streaming text responses, structured data generation, or generative UI to React/Next.js apps.
---

# Vercel AI SDK

Build streaming AI experiences — chat interfaces, completions, structured output, and generative UI — with the Vercel AI SDK (`ai` package).

## Overview

The Vercel AI SDK provides a unified, model-agnostic API across three layers:

| Layer | Package | Purpose |
|-------|---------|---------|
| **Core** | `ai` | Model calls: `generateText`, `streamText`, `generateObject`, `streamObject` |
| **UI** | `ai/react` or `@ai-sdk/react` | React hooks: `useChat`, `useCompletion`, `useObject` |
| **RSC** | `ai/rsc` | Server Components streaming UI: `streamUI`, `createStreamableUI` |

**When to use this skill:**
- Building a chat interface with streaming responses
- Adding AI text completion to a form or editor
- Generating structured data (JSON) from prompts
- Rendering streamed React components from the server
- Integrating multiple AI providers (OpenAI, Anthropic, Google, etc.)

**Do not use this skill when:**
- You only need a one-shot REST call to an AI API (use `fetch` directly)
- You are using a non-React framework (AI SDK UI is React-only)
- You need local model inference (use Ollama's REST API instead)

---

## Installation

```bash
# Core SDK (required)
npm install ai

# Provider package (choose one or more)
npm install @ai-sdk/openai       # OpenAI / Azure OpenAI
npm install @ai-sdk/anthropic    # Anthropic Claude
npm install @ai-sdk/google       # Google Gemini
npm install @ai-sdk/mistral      # Mistral AI
npm install @ai-sdk/cohere       # Cohere

# React UI hooks (bundled with ai >=3.0, but can install separately)
npm install @ai-sdk/react
```

---

## AI SDK Core

### Text Generation

```typescript
// app/api/chat/route.ts (Next.js App Router)
import { openai } from '@ai-sdk/openai';
import { streamText } from 'ai';

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = streamText({
    model: openai('gpt-4o'),
    messages,
  });

  return result.toDataStreamResponse();
}
```

### Structured Object Generation

```typescript
// app/api/extract/route.ts
import { openai } from '@ai-sdk/openai';
import { streamObject } from 'ai';
import { z } from 'zod';

const schema = z.object({
  title: z.string(),
  summary: z.string(),
  tags: z.array(z.string()),
});

export async function POST(req: Request) {
  const { text } = await req.json();

  const result = streamObject({
    model: openai('gpt-4o'),
    schema,
    prompt: `Extract metadata from: ${text}`,
  });

  return result.toTextStreamResponse();
}
```

### One-Shot Generation (Non-Streaming)

```typescript
import { generateText, generateObject } from 'ai';
import { anthropic } from '@ai-sdk/anthropic';
import { z } from 'zod';

// Simple text
const { text } = await generateText({
  model: anthropic('claude-3-5-sonnet-20241022'),
  prompt: 'Write a haiku about TypeScript.',
});

// Structured output
const { object } = await generateObject({
  model: anthropic('claude-3-5-sonnet-20241022'),
  schema: z.object({ rating: z.number().min(1).max(5), reason: z.string() }),
  prompt: 'Rate this code review: ...',
});
```

---

## AI SDK UI — React Hooks

### `useChat` — Chat Interface

The primary hook for building chat UIs with streaming.

```tsx
'use client';

import { useChat } from 'ai/react';

export function Chat() {
  const { messages, input, handleInputChange, handleSubmit, isLoading, error } =
    useChat({
      api: '/api/chat',          // default
      initialMessages: [],
      onFinish: (message) => {
        console.log('Stream complete:', message);
      },
      onError: (err) => {
        console.error('Stream error:', err);
      },
    });

  return (
    <div className="flex flex-col h-screen">
      {/* Message list */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((m) => (
          <div
            key={m.id}
            className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`rounded-lg px-4 py-2 max-w-xs ${
                m.role === 'user'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-100 text-gray-900'
              }`}
            >
              {m.content}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 rounded-lg px-4 py-2 animate-pulse">
              Thinking…
            </div>
          </div>
        )}
      </div>

      {/* Input form */}
      <form onSubmit={handleSubmit} className="p-4 border-t flex gap-2">
        <input
          value={input}
          onChange={handleInputChange}
          placeholder="Type a message…"
          disabled={isLoading}
          className="flex-1 border rounded px-3 py-2"
        />
        <button
          type="submit"
          disabled={isLoading || !input.trim()}
          className="px-4 py-2 bg-blue-500 text-white rounded disabled:opacity-50"
        >
          Send
        </button>
      </form>

      {error && (
        <div className="p-2 text-sm text-red-500 text-center">
          Error: {error.message}
        </div>
      )}
    </div>
  );
}
```

### `useChat` — Advanced Options

```tsx
const {
  messages,
  input,
  handleInputChange,
  handleSubmit,
  isLoading,
  error,
  stop,          // abort streaming
  reload,        // retry last message
  append,        // programmatically add a message
  setMessages,   // replace message list
  setInput,      // programmatically set input
} = useChat({
  api: '/api/chat',
  id: 'my-chat-session',        // persist between route changes
  body: { userId: 'abc123' },   // extra body fields sent to API
  headers: { 'X-Auth': token }, // extra headers
  maxSteps: 5,                  // agentic multi-step tool calls
  onFinish(message, { usage, finishReason }) {
    console.log('Tokens used:', usage.totalTokens);
  },
});

// Append a message programmatically (e.g., "suggested prompts")
<button onClick={() => append({ role: 'user', content: 'Summarize this' })}>
  Summarize
</button>

// Stop streaming mid-response
<button onClick={stop} disabled={!isLoading}>Stop</button>
```

### `useCompletion` — Text Completion

For non-chat completion (e.g., autocomplete, text expansion):

```tsx
'use client';

import { useCompletion } from 'ai/react';

export function AutoComplete() {
  const { completion, input, handleInputChange, handleSubmit, isLoading } =
    useCompletion({ api: '/api/completion' });

  return (
    <div className="space-y-4">
      <form onSubmit={handleSubmit}>
        <textarea
          value={input}
          onChange={handleInputChange}
          rows={4}
          className="w-full border rounded p-2"
          placeholder="Start typing…"
        />
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Completing…' : 'Complete'}
        </button>
      </form>

      {completion && (
        <div className="border rounded p-3 bg-gray-50 whitespace-pre-wrap">
          {completion}
        </div>
      )}
    </div>
  );
}
```

**API Route for completion:**

```typescript
// app/api/completion/route.ts
import { openai } from '@ai-sdk/openai';
import { streamText } from 'ai';

export async function POST(req: Request) {
  const { prompt } = await req.json();

  const result = streamText({
    model: openai('gpt-4o-mini'),
    prompt,
    maxTokens: 512,
  });

  return result.toDataStreamResponse();
}
```

### `experimental_useObject` — Streaming Structured Output

Stream a structured JSON object as it's generated:

```tsx
'use client';

import { experimental_useObject as useObject } from 'ai/react';
import { z } from 'zod';

const recipeSchema = z.object({
  name: z.string(),
  ingredients: z.array(z.object({ item: z.string(), amount: z.string() })),
  steps: z.array(z.string()),
  prepTime: z.number(),
});

export function RecipeGenerator() {
  const { object, submit, isLoading } = useObject({
    api: '/api/recipe',
    schema: recipeSchema,
  });

  return (
    <div className="space-y-4">
      <button
        onClick={() => submit({ dish: 'pasta carbonara' })}
        disabled={isLoading}
        className="px-4 py-2 bg-green-500 text-white rounded"
      >
        {isLoading ? 'Generating…' : 'Generate Recipe'}
      </button>

      {object && (
        <div className="border rounded p-4 space-y-2">
          {/* Fields appear as they stream in */}
          {object.name && <h2 className="text-xl font-bold">{object.name}</h2>}

          {object.ingredients && (
            <ul className="list-disc pl-5">
              {object.ingredients.map((ing, i) => (
                <li key={i}>
                  {ing?.amount} {ing?.item}
                </li>
              ))}
            </ul>
          )}

          {object.prepTime && (
            <p className="text-sm text-gray-500">Prep: {object.prepTime} min</p>
          )}
        </div>
      )}
    </div>
  );
}
```

---

## Tool Calling (Agentic Patterns)

### Define Tools in the API Route

```typescript
// app/api/chat/route.ts
import { openai } from '@ai-sdk/openai';
import { streamText, tool } from 'ai';
import { z } from 'zod';

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = streamText({
    model: openai('gpt-4o'),
    messages,
    tools: {
      getWeather: tool({
        description: 'Get current weather for a location',
        parameters: z.object({
          location: z.string().describe('City and state, e.g. "San Francisco, CA"'),
          unit: z.enum(['celsius', 'fahrenheit']).default('celsius'),
        }),
        execute: async ({ location, unit }) => {
          // Replace with real weather API call
          return { temperature: 22, condition: 'sunny', location, unit };
        },
      }),
    },
    maxSteps: 3, // allow multi-step tool use
  });

  return result.toDataStreamResponse();
}
```

### Render Tool Results in the UI

```tsx
'use client';

import { useChat } from 'ai/react';

export function AgentChat() {
  const { messages, input, handleInputChange, handleSubmit } = useChat({
    maxSteps: 3,
  });

  return (
    <div>
      {messages.map((m) => (
        <div key={m.id}>
          {m.role === 'user' && <p className="text-right">{m.content}</p>}

          {m.role === 'assistant' && (
            <div>
              {/* Text content */}
              {m.content && <p>{m.content}</p>}

              {/* Tool invocations */}
              {m.toolInvocations?.map((ti) => (
                <div key={ti.toolCallId} className="border rounded p-2 my-1 bg-yellow-50">
                  <p className="text-xs text-gray-500">Tool: {ti.toolName}</p>
                  {'result' in ti && (
                    <pre className="text-sm">{JSON.stringify(ti.result, null, 2)}</pre>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      ))}

      <form onSubmit={handleSubmit}>
        <input value={input} onChange={handleInputChange} />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}
```

---

## Generative UI with React Server Components (`ai/rsc`)

Stream React components directly from the server for rich, progressive UI.

### Server Action

```typescript
// app/actions.ts
'use server';

import { createAI, streamUI, createStreamableValue } from 'ai/rsc';
import { openai } from '@ai-sdk/openai';
import { z } from 'zod';
import { Spinner } from '@/components/Spinner';
import { WeatherCard } from '@/components/WeatherCard';

export async function submitUserMessage(userInput: string) {
  const ui = streamUI({
    model: openai('gpt-4o'),
    prompt: userInput,
    text: ({ content, done }) => <p>{content}</p>,
    tools: {
      showWeather: {
        description: 'Show a weather card',
        parameters: z.object({ location: z.string() }),
        generate: async function* ({ location }) {
          yield <Spinner />;          // show while fetching
          const data = await fetchWeather(location);
          return <WeatherCard data={data} />;
        },
      },
    },
  });

  return { ui: ui.value };
}

export const AI = createAI<
  { role: string; content: string }[],
  React.ReactNode[]
>({
  actions: { submitUserMessage },
  initialAIState: [],
  initialUIState: [],
});
```

### Client Component

```tsx
// app/page.tsx
'use client';

import { useActions, useUIState } from 'ai/rsc';
import type { AI } from './actions';

export default function Page() {
  const [uiState, setUiState] = useUIState<typeof AI>();
  const { submitUserMessage } = useActions<typeof AI>();

  return (
    <div>
      {uiState.map((ui, i) => (
        <div key={i}>{ui}</div>
      ))}

      <form
        onSubmit={async (e) => {
          e.preventDefault();
          const input = (e.currentTarget[0] as HTMLInputElement).value;
          setUiState((prev) => [...prev, <p key={prev.length}>{input}</p>]);
          const { ui } = await submitUserMessage(input);
          setUiState((prev) => [...prev, ui]);
        }}
      >
        <input name="message" placeholder="Ask anything…" />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}
```

### Wrap App with AI Provider

```tsx
// app/layout.tsx
import { AI } from './actions';

export default function Layout({ children }: { children: React.ReactNode }) {
  return <AI>{children}</AI>;
}
```

---

## Attachments and Multi-Modal

### File Attachments in Chat

```tsx
'use client';

import { useChat } from 'ai/react';
import { useRef, useState } from 'react';

export function MultiModalChat() {
  const { messages, input, handleInputChange, handleSubmit } = useChat();
  const fileRef = useRef<HTMLInputElement>(null);
  const [attachments, setAttachments] = useState<FileList | undefined>();

  return (
    <form
      onSubmit={(e) => {
        handleSubmit(e, {
          experimental_attachments: attachments,
        });
        setAttachments(undefined);
        if (fileRef.current) fileRef.current.value = '';
      }}
    >
      <input
        ref={fileRef}
        type="file"
        accept="image/*"
        multiple
        onChange={(e) => setAttachments(e.target.files ?? undefined)}
      />
      <input value={input} onChange={handleInputChange} />
      <button type="submit">Send</button>
    </form>
  );
}
```

---

## Error Handling

### Client-Side

```tsx
const { error, reload } = useChat({
  onError: (err) => {
    // Log to monitoring service
    console.error('AI stream error', err);
  },
});

{error && (
  <div className="p-3 bg-red-50 border border-red-200 rounded flex items-center gap-2">
    <span className="text-red-700">{error.message}</span>
    <button
      onClick={reload}
      className="text-sm underline text-red-600"
    >
      Retry
    </button>
  </div>
)}
```

### API Route Error Handling

```typescript
import { openai } from '@ai-sdk/openai';
import { streamText } from 'ai';

export async function POST(req: Request) {
  try {
    const { messages } = await req.json();

    const result = streamText({
      model: openai('gpt-4o'),
      messages,
    });

    return result.toDataStreamResponse({
      getErrorMessage: (error) => {
        if (error instanceof Error) {
          // Don't leak full stack trace to client
          return error.message;
        }
        return 'An unexpected error occurred';
      },
    });
  } catch (err) {
    return new Response(
      JSON.stringify({ error: 'Failed to process request' }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
}
```

---

## System Prompts and Context

```typescript
// app/api/chat/route.ts
import { openai } from '@ai-sdk/openai';
import { streamText } from 'ai';
import { cookies } from 'next/headers';

export async function POST(req: Request) {
  const { messages } = await req.json();
  const cookieStore = cookies();
  const locale = cookieStore.get('locale')?.value ?? 'en';

  const result = streamText({
    model: openai('gpt-4o'),
    system: `You are a helpful assistant. Always respond in ${locale}. 
             Be concise and accurate.`,
    messages,
    temperature: 0.7,
    maxTokens: 2048,
  });

  return result.toDataStreamResponse();
}
```

---

## Best Practices

### ✅ Do This

1. **Always stream responses** — never block the UI waiting for a full LLM response:
   ```typescript
   // ✅ Stream for better UX
   const result = streamText({ model, messages });
   return result.toDataStreamResponse();
   ```

2. **Use `maxSteps` for agentic flows** — enable multi-step tool use:
   ```typescript
   const result = streamText({ model, messages, tools, maxSteps: 5 });
   ```

3. **Validate tool parameters with Zod** — never trust LLM-provided inputs:
   ```typescript
   parameters: z.object({
     amount: z.number().positive(),
     currency: z.enum(['USD', 'EUR', 'GBP']),
   }),
   ```

4. **Use `onFinish` for side effects** — token counting, logging, persistence:
   ```typescript
   useChat({
     onFinish: (message, { usage }) => {
       trackTokenUsage(usage.totalTokens);
     },
   });
   ```

5. **Provide `id` to `useChat`** — preserve conversation across renders:
   ```typescript
   useChat({ id: `session-${userId}` });
   ```

### ❌ Don't Do This

1. **Don't use `generateText` in streaming API routes** — it blocks until the full response is ready:
   ```typescript
   // ❌ Blocks the response
   const { text } = await generateText({ model, messages });
   return Response.json({ text });
   ```

2. **Don't expose API keys in client components** — always call from server routes:
   ```typescript
   // ❌ Never put keys in 'use client' components
   const result = await streamText({ model: openai('gpt-4o') }); // client-side
   ```

3. **Don't skip error boundaries** — AI streams can fail mid-flight:
   ```tsx
   // ❌ No error handling
   const { messages } = useChat();
   
   // ✅ Handle errors
   const { messages, error } = useChat({ onError: (e) => report(e) });
   ```

4. **Don't render raw `m.content` for tool messages** — check `m.role` first:
   ```tsx
   // ❌ Tool messages may have empty content
   {messages.map((m) => <p>{m.content}</p>)}
   
   // ✅ Guard content rendering
   {messages.map((m) => m.content && <p key={m.id}>{m.content}</p>)}
   ```

---

## TypeScript Types Reference

```typescript
import type {
  Message,           // Chat message { id, role, content, toolInvocations }
  CreateMessage,     // Omit<Message, 'id'>
  UseChatOptions,    // Options for useChat
  UseChatHelpers,    // Return type of useChat
  ToolInvocation,   // { toolName, toolCallId, args, state, result? }
  CoreMessage,       // Server-side message type
  CoreTool,          // Tool definition for streamText
} from 'ai';
```

---

## Common Patterns

### Persist Chat History

```tsx
'use client';

import { useChat } from 'ai/react';
import { useEffect } from 'react';

const STORAGE_KEY = 'chat-history';

export function PersistentChat() {
  const { messages, input, handleInputChange, handleSubmit, setMessages } =
    useChat({
      onFinish: (msg) => {
        const all = [...messages, msg];
        localStorage.setItem(STORAGE_KEY, JSON.stringify(all));
      },
    });

  useEffect(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) setMessages(JSON.parse(saved));
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  return (/* ... */);
}
```

### Abort / Stop Streaming

```tsx
const { isLoading, stop } = useChat();

{isLoading && (
  <button
    onClick={stop}
    className="px-3 py-1 text-sm border rounded hover:bg-gray-100"
  >
    ■ Stop generating
  </button>
)}
```

### Custom Fetch / Authentication

```tsx
useChat({
  fetch: async (url, options) => {
    const token = await getAuthToken();
    return fetch(url, {
      ...options,
      headers: {
        ...options?.headers,
        Authorization: `Bearer ${token}`,
      },
    });
  },
});
```

---

## Multi-Provider Setup

```typescript
// lib/ai.ts — centralized model factory
import { openai } from '@ai-sdk/openai';
import { anthropic } from '@ai-sdk/anthropic';
import { google } from '@ai-sdk/google';

export type ModelProvider = 'openai' | 'anthropic' | 'google';

export function getModel(provider: ModelProvider = 'openai') {
  switch (provider) {
    case 'openai':
      return openai('gpt-4o');
    case 'anthropic':
      return anthropic('claude-3-5-sonnet-20241022');
    case 'google':
      return google('gemini-1.5-pro');
    default:
      throw new Error(`Unknown provider: ${provider}`);
  }
}
```

---

## Resources

- [Vercel AI SDK Docs](https://sdk.vercel.ai/docs)
- [AI SDK UI Reference](https://sdk.vercel.ai/docs/ai-sdk-ui/overview)
- [AI SDK RSC Reference](https://sdk.vercel.ai/docs/ai-sdk-rsc/overview)
- [Providers & Models](https://sdk.vercel.ai/providers/ai-sdk-providers)
- [GitHub: vercel/ai](https://github.com/vercel/ai)
- [Examples & Templates](https://sdk.vercel.ai/examples)
