/**
 * Next.js App Router API route for streaming chat with tool support.
 * Place at: app/api/chat/route.ts
 */
import { openai } from '@ai-sdk/openai';
import { streamText, tool } from 'ai';
import { z } from 'zod';

export const runtime = 'edge'; // optional: use edge runtime for lower latency

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = streamText({
    model: openai('gpt-4o'),
    system:
      'You are a helpful assistant. When asked about weather, use the getWeather tool.',
    messages,
    tools: {
      getWeather: tool({
        description: 'Get the current weather for a city',
        parameters: z.object({
          city: z.string().describe('The city name'),
          units: z.enum(['metric', 'imperial']).default('metric'),
        }),
        execute: async ({ city, units }) => {
          // Replace with a real weather API call
          return {
            city,
            temperature: units === 'metric' ? 22 : 72,
            unit: units === 'metric' ? '°C' : '°F',
            condition: 'Partly cloudy',
          };
        },
      }),
    },
    maxSteps: 3,
    onFinish({ usage, finishReason }) {
      // Log usage for cost tracking / rate limiting
      console.log(
        `[chat] finish=${finishReason} promptTokens=${usage.promptTokens} completionTokens=${usage.completionTokens}`
      );
    },
  });

  return result.toDataStreamResponse({
    getErrorMessage: (error) =>
      error instanceof Error ? error.message : 'Stream error',
  });
}
