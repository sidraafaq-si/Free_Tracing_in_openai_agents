🤖 Agent with Gemini API + Tracing

This project demonstrates how to build an AI Agent using the agents library with Google Gemini API. It also shows how to trace execution with a custom console exporter that prints model usage, inputs, and outputs in a clean format.

📦 Requirements

Python 3.9+

Dependencies:

pip install agents python-dotenv

🔑 Setup

Create a .env file in your project root and add your Gemini API key:

GEMINI_API_KEY=your_api_key_here

Make sure you have access to the Google Generative Language API .

📂 Project Structure . ├── main.py # Your agent & tracing code ├── .env # Contains GEMINI_API_KEY └── README.md # Documentation

🛠 How the Code Works

Import & Environment Setup
The required classes are imported from the agents library, and environment variables are loaded from .env.

from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_trace_processors from agents.tracing.processors import BatchTraceProcessor from agents.tracing.processor_interface import TracingExporter from agents.tracing.spans import Span from agents.tracing.traces import Trace from dotenv import load_dotenv import os

load_dotenv()

Custom Console Exporter
We create a custom exporter to print trace details clearly:

class CustomConsoleSpanExporter(TracingExporter): def export(self, items: list[Trace | Span]): for item in items: if isinstance(item, Trace): print(f"[Trace] ID: {item.trace_id} | Name: {item.name}") elif item.span_data.type == "generation": usage = item.span_data.usage or {} model = item.span_data.model user_input = item.span_data.input or [] output = item.span_data.output or []

            print("🧠 Model Used:", model)
            print("📥 Input Tokens:", usage.get("input_tokens", "N/A"))
            print("📤 Output Tokens:", usage.get("output_tokens", "N/A"))

            if user_input:
                print("🙋 User Asked:", user_input[-1].get("content", "N/A"))
            if output:
                print("🤖 Bot Replied:", output[0].get("content", "N/A"))
Processor & Model Setup
Attach the exporter to the tracing system and configure Gemini:

exporter = CustomConsoleSpanExporter() processor = BatchTraceProcessor(exporter) set_trace_processors([processor])

gemini_api_key = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI( api_key=gemini_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/" )

model = OpenAIChatCompletionsModel( model="gemini-2.0-flash", openai_client=external_client )

Agent Creation & Execution
Create the agent and run it synchronously:

agent = Agent( name="MyAgent", instructions="You are a helpful assistant.", model=model )

result = Runner.run_sync( agent, "Hello, how can you assist me today" )

print(result.final_output)

🖥 Example Output

When you run the script, you’ll see:

[Trace] ID: trace_d4d9d4073b784cbf8bd049c97f3d4a17 | Name: Agent workflow 🧠 Model Used: gemini-2.0-flash 📥 Input Tokens: 14 📤 Output Tokens: 237 🙋 User Asked: Hello, how can you assist me today 🤖 Bot Replied: Hello! I can assist you with a wide range of tasks, including...

And the final agent output:

Hello! I can assist you with a wide range of tasks, including...

✅ Summary

Uses Gemini 2.0 Flash model via agents library.

Implements custom tracing exporter for clean console logs.

Displays model, token usage, user input, and assistant reply.
