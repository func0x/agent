import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.call_function import call_function
from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from prompts import system_prompt


def main():
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY environment variable is not set")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=args.user_prompt)],
        )
    ]

    prompt_tokens = 0
    response_tokens = 0

    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0,
                tools=[
                    types.Tool(
                        function_declarations=[
                            schema_get_files_info,
                            schema_get_file_content,
                            schema_run_python_file,
                            schema_write_file,
                        ]
                    )
                ],
            ),
        )

        prompt_tokens += (
            response.usage_metadata.prompt_token_count
            if response.usage_metadata and response.usage_metadata.prompt_token_count
            else 0
        )
        response_tokens += (
            response.usage_metadata.candidates_token_count
            if response.usage_metadata
            and response.usage_metadata.candidates_token_count
            else 0
        )

        if response.candidates:
            for candidate in response.candidates:
                if candidate.content:
                    messages.append(candidate.content)

        if not response.function_calls:
            if args.verbose:
                print(f"User prompt: {args.user_prompt}")
                print(f"Prompt tokens: {prompt_tokens}")
                print(f"Response tokens: {response_tokens}")
            print("Response:")
            print(response.text)
            return

        function_results = []

        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose=args.verbose)

            # parts must exist
            if not function_call_result.parts:
                raise RuntimeError("Function call result has empty parts list")

            part = function_call_result.parts[0]

            # function_response must exist
            if part.function_response is None:
                raise RuntimeError("Function response is None")

            # response must exist
            if part.function_response.response is None:
                raise RuntimeError("Function response content is None")

            function_results.append(part)

            if args.verbose:
                print(f"-> {part.function_response.response}")

        messages.append(types.Content(role="user", parts=function_results))

    print("Error: Maximum number of iterations (20) reached without a final response.")
    sys.exit(1)


if __name__ == "__main__":
    main()
