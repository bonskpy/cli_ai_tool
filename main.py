from google import genai
from dotenv import load_dotenv
import os
import sys


MODEL_ID = "gemini-2.5-flash"  #  ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash", "gemini-2.5-flash-lite-preview-06-17"]


def main():

    args = sys.argv[1:]

    if not args:
        print("Hello from cli-ai-tool!")
        print("Usage MacOS:         python3 main.py [prompt...]")
        print("Options: --verbose   provides additional details on program execution")
        print('Example:             python main.py "How do I build a calculator app?"')
        sys.exit(1)

    user_prompt = " ".join(sys.argv[1:])

    load_dotenv()
    gem_api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=gem_api_key)
    response = client.models.generate_content(model=MODEL_ID, contents=user_prompt)
    if response.usage_metadata and response.text:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        print(f"Response: {response.text.strip()}")


if __name__ == "__main__":
    main()
