'use client';

import { useChat } from 'ai/react';
import { useRef, useEffect } from 'react';

/**
 * Minimal streaming chat component using Vercel AI SDK useChat hook.
 *
 * Requires an API route at /api/chat that calls:
 *   import { streamText } from 'ai';
 *   const result = streamText({ model, messages });
 *   return result.toDataStreamResponse();
 */
export function StreamingChat() {
  const bottomRef = useRef<HTMLDivElement>(null);
  const {
    messages,
    input,
    handleInputChange,
    handleSubmit,
    isLoading,
    error,
    stop,
    reload,
  } = useChat({ api: '/api/chat' });

  // Auto-scroll to latest message
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="flex flex-col h-full max-w-2xl mx-auto">
      {/* Message history */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {messages.length === 0 && (
          <p className="text-center text-gray-400 mt-12">
            Start a conversation below.
          </p>
        )}

        {messages.map((m) => (
          <div
            key={m.id}
            className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`rounded-2xl px-4 py-2 max-w-[80%] whitespace-pre-wrap text-sm ${
                m.role === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-900'
              }`}
            >
              {m.content}
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 rounded-2xl px-4 py-2 text-sm text-gray-400 animate-pulse">
              ●●●
            </div>
          </div>
        )}

        {error && (
          <div className="flex justify-center">
            <div className="bg-red-50 border border-red-200 rounded-lg px-4 py-2 text-sm text-red-700 flex items-center gap-2">
              <span>Something went wrong.</span>
              <button
                onClick={reload}
                className="underline hover:no-underline font-medium"
              >
                Retry
              </button>
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* Input area */}
      <div className="border-t p-4">
        <form onSubmit={handleSubmit} className="flex gap-2 items-end">
          <textarea
            value={input}
            onChange={handleInputChange}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSubmit(e as unknown as React.FormEvent);
              }
            }}
            placeholder="Type a message… (Shift+Enter for newline)"
            rows={1}
            disabled={isLoading}
            className="flex-1 border rounded-xl px-3 py-2 text-sm resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
            style={{ minHeight: '40px', maxHeight: '120px' }}
          />

          {isLoading ? (
            <button
              type="button"
              onClick={stop}
              className="px-3 py-2 rounded-xl border text-sm bg-gray-50 hover:bg-gray-100"
            >
              ■ Stop
            </button>
          ) : (
            <button
              type="submit"
              disabled={!input.trim()}
              className="px-4 py-2 rounded-xl bg-blue-600 text-white text-sm font-medium disabled:opacity-40 hover:bg-blue-700 transition-colors"
            >
              Send
            </button>
          )}
        </form>
        <p className="text-xs text-gray-400 mt-1 text-center">
          Powered by Vercel AI SDK
        </p>
      </div>
    </div>
  );
}
