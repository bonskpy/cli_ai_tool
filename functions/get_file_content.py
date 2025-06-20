import os
import config


def get_file_content(
    working_directory: str, file_path: str | None = None, verbose: bool = False
) -> str | None:

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

    with open(file_abspath, "r", encoding="utf-8") as f:
        file_content = (
            f.read(config.MAX_CHARS)
            + f'[...File "{file_path}" truncated at 10000 characters]'
        )

    return file_content


get_file_content("calculator", "main.py")
get_file_content("calculator", "pkg/calculator.py")
get_file_content("calculator", "/bin/cat")
