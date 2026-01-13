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


final_response = None
response_usage = None
rate_limit_hit = False

for _ in range(20):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=[available_functions],
                temperature=0,
            ),
        )
    except Exception as exc:
        status_code = getattr(exc, "status_code", None)
        is_rate_limit = status_code == 429 or "RESOURCE_EXHAUSTED" in str(exc)
        if is_rate_limit:
            print("Rate limit exceeded; ending early.")
            final_response = "Rate limit exceeded. Please retry later."
            rate_limit_hit = True
            break
        raise

    response_usage = response.usage_metadata

    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

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

        messages.append(types.Content(role="user", parts=function_results))
        continue

    final_response = response.text
    print(final_response)
    break

if final_response is None:
    print("Error: Maximum iterations reached without a final response.")
    raise SystemExit(1)

if response_usage is None and not rate_limit_hit:
    raise RuntimeError("No Usage Metadata Found.")

if args.verbose:
    print(f"User prompt: {args.user_prompt}")
    if response_usage is not None:
        print(f"Prompt tokens: {response_usage.prompt_token_count}")
        print(f"Response tokens: {response_usage.candidates_token_count}")
print(f"Response: {final_response}")
