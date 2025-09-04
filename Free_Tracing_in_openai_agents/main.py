from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_trace_processors
import os
from agents.tracing.processors import ConsoleSpanExporter, BatchTraceProcessor, default_processor
from dotenv import load_dotenv

from agents.tracing.processor_interface import TracingExporter
from agents.tracing.spans import  Span
from agents.tracing.traces import Trace
load_dotenv()




class CustomConsoleSpanExporter(TracingExporter):
    def export(self, items: list[Trace | Span]):
        for item in items:
            if isinstance(item, Trace):
                print(f"[Trace] ID: {item.trace_id} | Name: {item.name}")
            elif item.span_data.type == "generation":
                usage = item.span_data.usage or {}
                model = item.span_data.model
                user_input = item.span_data.input or []
                output = item.span_data.output or []

                print("🧠 Model Used:", model)
                print("📥 Input Tokens:", usage.get("input_tokens", "N/A"))
                print("📤 Output Tokens:", usage.get("output_tokens", "N/A"))

                if user_input:
                    print("🙋 User Asked:", user_input[-1].get("content", "N/A"))
                if output:
                    print("🤖 Bot Replied:", output[0].get("content", "N/A"))

exporter = CustomConsoleSpanExporter()
proccessor = BatchTraceProcessor(exporter)
    

set_trace_processors([proccessor,
                     # default_processor()
                      ])
gemini_api_key = os.getenv("GEMINI_API_KEY")


external_client = AsyncOpenAI(
    api_key = gemini_api_key,
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client = external_client
)

agent = Agent(
    name = "MyAgent",
    instructions = "You are a helpful assistant.",  
    model = model
)


result = Runner.run_sync(
    agent,
    "Hello, how can you assist me today"
)

print(result.final_output)
