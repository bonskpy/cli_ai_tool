import os
from google.genai import types


def get_file_content(
    working_directory: str,
    file_path: str | None = None,
    max_chars: int = 10000,
    verbose: bool = False,
) -> str:
    """
    Reads the content of a file within a specified working directory.

    Args:
        working_directory (str): The base directory within which file access is permitted.
        file_path (str | None, optional): The relative path to the file from the working directory. Defaults to None.
        max_chars (int, optional): The maximum number of characters to read from the file. Defaults to 10000.
        verbose (bool, optional): If True, prints additional information about the file read operation. Defaults to False.

    Returns:
        str: The content of the file up to `max_chars` characters,
             or an error message if the file cannot be read or is outside the permitted directory.

    Notes:
        - If the file is larger than `max_chars`, the content is truncated and a notice is appended.
        - The function prevents reading files outside the specified working directory for security.
        - Error messages are printed and returned as strings in case of failure.
    """
    working_directory_abspath: str = os.path.abspath(working_directory)

    file_abspath: str = os.path.abspath(
        os.path.join(working_directory_abspath, file_path or "")
    )

    common_path = os.path.commonpath([working_directory_abspath, file_abspath])

    if common_path != working_directory_abspath:
        print("--- error ---")
        print(
            f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        )
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(file_abspath):
        print("--- error ---")
        print(f'Error: File not found or is not a regular file: "{file_path}"')
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(file_abspath, "r", encoding="utf-8") as f:
            file_content = f.read(max_chars)
            if len(file_content) == max_chars:
                file_content += f'[...File "{file_path}" truncated at 10000 characters]'
        if verbose:
            print(f'File "{file_path}": {len(file_content)} characters read.')
        return file_content
    except OSError as err:
        print(f"Error: Failed to open {file_path}: {err}")
        return f"Error: Failed to open {file_path}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a file path up to 10000 characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the file to read content from, relative to the working directory.",
            ),
        },
    ),
)

# get_file_content("calculator", "main.py", verbose=True)
# get_file_content("calculator", "pkg/calculator.py", verbose=True)
# get_file_content("calculator", "/bin/cat", verbose=True)
# get_file_content("calculator", "lorem.txt", verbose=True)
