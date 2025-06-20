import os


def get_file_content(
    working_directory: str,
    file_path: str | None = None,
    max_chars: int = 10000,
    verbose: bool = False,
) -> str:

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


get_file_content("calculator", "main.py", verbose=True)
get_file_content("calculator", "pkg/calculator.py", verbose=True)
get_file_content("calculator", "/bin/cat", verbose=True)
get_file_content("calculator", "lorem.txt", verbose=True)
