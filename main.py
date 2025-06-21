from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import sys
import settings
from available_functions import available_functions


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
            print(f"Calling function: {call.name}({call.args})")

    if response.usage_metadata and response.text:
        if verbose:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        print(f"Response: {response.text.strip()}")


if __name__ == "__main__":
    main()
