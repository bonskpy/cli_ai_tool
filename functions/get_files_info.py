import os
from google.genai import types


def get_files_info(
    working_directory: str, directory: str | None = None, verbose: bool = False
) -> str:
    """
    Lists information about files and directories within a specified directory.

    Args:
        working_directory (str): The root directory within which file listing is permitted.
        directory (str | None, optional): The subdirectory (relative to working_directory) to list. Defaults to None.
        verbose (bool, optional): If True, prints detailed information. Defaults to False.

    Returns:
        str: A formatted string listing each file and directory in the target directory,
        including file size (in bytes) and whether it is a directory. Returns an error message
        if the directory is invalid or outside the permitted working directory.

    Notes:
        - Errors are returned as strings for AI to digest.
    """
    working_directory_abspath: str = os.path.abspath(working_directory)

    if directory:
        directory_abspath: str = os.path.abspath(
            os.path.join(working_directory_abspath, directory)
        )

        common_path = os.path.commonpath([working_directory_abspath, directory_abspath])

        if common_path != working_directory_abspath:
            print("--- error ---")
            print(
                f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
            )
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(directory_abspath):
            print("--- error ---")
            print(f'Error: "{directory}" is not a directory')
            return f'Error: "{directory}" is not a directory'

    else:
        directory_abspath = working_directory_abspath

    directory_content = os.listdir(directory_abspath)

    file_info = []

    for file in directory_content:
        file_path = os.path.join(directory_abspath, file)
        file_size = os.path.getsize(file_path)
        file_is_dir = os.path.isdir(file_path)
        file_info.append(f"- {file}: file_size:{file_size} bytes, is_dir={file_is_dir}")

    if verbose:
        print(f"--- get_files_info: directory: {directory_abspath}")
        print("\n".join(file_info), "\n")
    return "\n".join(file_info)


schema_get_files_info: types.FunctionDeclaration = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)


# test
# get_files_info("calculator", directory="pkg", verbose=True)
# get_files_info("calculator", verbose=True)
# get_files_info("calculator", "../", verbose=True)
# get_files_info("calculator", "/bin", verbose=True)
# get_files_info("calculator", ".", verbose=True)
