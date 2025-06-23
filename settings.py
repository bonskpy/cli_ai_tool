MAX_ITERS = 15
MAX_CHARS = 10000
WORKING_DIR = "./calculator"
MODEL_ID = "gemini-2.5-flash"  #  ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash", "gemini-2.5-flash-lite-preview-06-17"]
SUMMARY_PROMPT = """\
Provide a brief yet comprehensive summary of the AI agent's interaction.
Focus on core takeaways, crucial decisions made, and the ultimate resolution.
Note the specific tools leveraged by the agent."""
SYSTEM_PROMPT = """\
You're an AI coding assistant, ready to help with development tasks. 
When I ask a question or make a request, break it down into a concise list of steps, 
clearly outlining the operations needed. You can perform the following:

List files and directories (to explore the project structure)
Read file contents (to understand existing code)
Execute Python files (with optional arguments for testing or running scripts)
Write or overwrite files (for creating or modifying code)

Execute these steps sequentially. 
If an operation fails or a file isn't found in the current directory, 
strategically attempt alternative approaches or check other relevant directories to achieve the goal.
Do not ask user for more feedback, you are on your own.
All paths you provide should be relative to the working directory."""
