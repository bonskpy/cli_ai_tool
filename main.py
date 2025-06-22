from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import sys
import settings
from available_functions import available_functions


def call_function(function_call_part: types.FunctionCall, verbose=False):

    from functions.get_file_content import get_file_content
    from functions.get_files_info import get_files_info
    from functions.run_python_file import run_python_file
    from functions.write_file import write_file

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    working_directory = "./calculator"
    func_name: str | None = function_call_part.name
    func_args: dict | None = function_call_part.args

    functions_map = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    if func_name in functions_map:

        func_call = functions_map[func_name](
            working_directory=working_directory, verbose=True, **func_args  # type: ignore
        )

        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=func_name,
                    response={"result": func_call},
                )
            ],
        )

    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=func_name if func_name else "Unknown",
                    response={"error": f"Unknown function: {func_name}"},
                )
            ],
        )


def main():

    args: list[str] = sys.argv[1:]
    verbose: bool = "--verbose" in args

    if not args:
        print("\nHello from cli-ai-tool!")
        print("\nUsage MacOS:")
        print("     python3 main.py [prompt...]")
        print("Options:")
        print("     --verbose   provides additional details on program execution")
        print("Example:")
        print('     python main.py "How do I build a calculator app?" --verbose\n')
        sys.exit(1)

    user_prompt: str = " ".join(arg for arg in args if not arg.startswith("--"))

    contents: list = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    config = types.GenerateContentConfig(
        system_instruction=settings.SYSTEM_PROMPT, tools=[available_functions]
    )

    load_dotenv()
    gem_api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=gem_api_key)
    response = client.models.generate_content(
        model=settings.MODEL_ID,
        contents=contents,
        config=config,
    )

    if response.function_calls:
        for call in response.function_calls:
            # print(f"Calling function: {call.name}({call.args})")
            func_call = call_function(call, verbose=verbose)

            if func_call.parts and func_call.parts[0].function_response and verbose:
                print(f"-> {func_call.parts[0].function_response.response}")

    if response.usage_metadata and response.text:
        if verbose:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        print(f"Response: {response.text.strip()}")


if __name__ == "__main__":
    main()
