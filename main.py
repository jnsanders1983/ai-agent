import argparse
import os
import json

from call_function import available_functions, call_function
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt

def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key is None:
        raise RuntimeError("failed to load API Key from .env")
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )
    
    if not response.usage:
        raise RuntimeError("API response appears to be malformed")
    
    message = response.choices[0].message
    if message.tool_calls is not None:
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, args.verbose)
            if not result_message["content"]:
                raise Exception(f"empty response for {tool_call.function.name}")
            if args.verbose:
                print(f"-> {result_message['content']}")
    else:
        print("Response:")
        print(message.content)

if __name__ == "__main__":
    main()
