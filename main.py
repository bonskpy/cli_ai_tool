from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import sys


MODEL_ID = "gemini-2.5-flash"  #  ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash", "gemini-2.5-flash-lite-preview-06-17"]


def main():

    args: list[str] = sys.argv[1:]

    if not args:
        print("\nHello from cli-ai-tool!")
        print("\nUsage MacOS:")
        print("     python3 main.py [prompt...]")
        print("Options:")
        print("     --verbose   provides additional details on program execution")
        print("Example:")
        print('     python main.py "How do I build a calculator app?" --verbose\n')
        sys.exit(1)

    user_prompt: str = " ".join(sys.argv[1:])

    contents: list = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    load_dotenv()
    gem_api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=gem_api_key)
    response = client.models.generate_content(model=MODEL_ID, contents=contents)
    if response.usage_metadata and response.text:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        print(f"Response: {response.text.strip()}")


if __name__ == "__main__":
    main()
