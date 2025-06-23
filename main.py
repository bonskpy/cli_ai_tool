from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import sys
import settings
from available_functions import available_functions


def call_function(function_call_part: types.FunctionCall, verbose=False):
    """
    Calls a specified function from a predefined set of avialable functions.

    Args:
        function_call_part (types.FunctionCall): An object containing the name of the function to call and its arguments.
        verbose (bool, optional): If True, prints detailed information about the function call. Defaults to False.

    Returns:
        types.Content: An object containing the result of the function call or an error message if the function is unknown.
    """
    from functions.get_file_content import get_file_content
    from functions.get_files_info import get_files_info
    from functions.run_python_file import run_python_file
    from functions.write_file import write_file

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    working_directory = settings.WORKING_DIR
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
            working_directory=working_directory, verbose=verbose, **func_args  # type: ignore
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


def summarise_interaction(
    contents: list[types.Content],
    system_instruction: str | None,
    client: genai.Client,
    model: str = "gemini-2.5-flash",
):
    """\
    Provides a brief yet comprehensive summary of the AI agent's interaction.

    Args:
        contents (list[types.Content]): A list of content objects representing the interaction to be summarized.
        system_instruction (str): Instructions or context for the AI model to guide the summarization process.
        client (genai.Client): The generative AI client used to interact with the model.
        model (str, optional): The name of the AI model to use for summarization. Defaults to "gemini-2.5-flash".

    Returns:
        str: brief yet comprehensive summary of the AI agent's interaction.
    """
    if not system_instruction:
        system_instruction = (
            "Provide a brief yet comprehensive summary of the AI agent's interaction."
        )

    config: types.GenerateContentConfig = types.GenerateContentConfig(
        system_instruction=system_instruction
    )

    summary: str | None = None

    try:
        summary: str | None = client.models.generate_content(
            model=model,
            contents=contents,
            config=config,
        ).text
    except Exception as err:
        print(f"Error: summary generation failed. Details: {err}")

    return summary


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

    config: types.GenerateContentConfig = types.GenerateContentConfig(
        system_instruction=settings.SYSTEM_PROMPT, tools=[available_functions]
    )

    load_dotenv()
    gem_api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=gem_api_key)

    counter: int = 0

    while counter < settings.MAX_ITERS:

        counter += 1

        response = client.models.generate_content(
            model=settings.MODEL_ID,
            contents=contents,
            config=config,
        )

        if response.candidates:
            for candidate in response.candidates:
                contents.append(candidate.content)

        if response.function_calls:
            for call in response.function_calls:
                func_call = call_function(call, verbose=verbose)
                contents.append(func_call)

                if not func_call.parts or not func_call.parts[0].function_response:  # type: ignore
                    raise Exception("Empty function call result!")

                if func_call.parts and func_call.parts[0].function_response and verbose:  # type: ignore
                    print(f"-> {func_call.parts[0].function_response.response}")  # type: ignore

                if not func_call:
                    raise Exception("No function responses generated, exiting.")

        else:
            if response.usage_metadata and response.candidates:
                if verbose:
                    print(f"User prompt: {user_prompt}")
                    print(
                        f"Prompt tokens: {response.usage_metadata.prompt_token_count}"
                    )
                    print(
                        f"Response tokens: {response.usage_metadata.candidates_token_count}"
                    )
                candidate = response.candidates[0]
                if (
                    candidate.content
                    and candidate.content.parts
                    and candidate.content.parts[0].text
                ):
                    print(f"Response: {candidate.content.parts[0].text.strip()}")
            break

    summary = summarise_interaction(
        contents=contents, system_instruction=settings.SUMMARY_PROMPT, client=client
    )

    print(summary)


if __name__ == "__main__":
    main()
