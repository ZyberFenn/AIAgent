import os
import argparse
from dotenv import load_dotenv

from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function


load_dotenv()

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [types.Content(
    role="user", 
    parts=[types.Part(text=args.user_prompt)]
    )]

api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("No API Key Found.")

client = genai.Client(api_key=api_key)


response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=messages,
    config=types.GenerateContentConfig(
        system_instruction=system_prompt,
        tools=[available_functions],
        temperature=0,
    ),
)

function_calls = response.function_calls

if function_calls:
    function_results = []
    for function_call in function_calls:
        function_call_result = call_function(function_call, verbose=args.verbose)
        if not function_call_result.parts:
            raise RuntimeError("No parts returned from function call.")
        function_response = function_call_result.parts[0].function_response
        if function_response is None:
            raise RuntimeError("No function response found.")
        if function_response.response is None:
            raise RuntimeError("No response content found.")
        function_results.append(function_call_result.parts[0])
        if args.verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
else:
    print(response.text)

if response.usage_metadata is None:
    raise RuntimeError("No Usage Metadata Found.")

if args.verbose:
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
print(f"Response: {response.text}")
