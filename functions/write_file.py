import os


def write_file(
    working_directory: str, file_path: str, content: str, verbose: bool = False
) -> str:
    """
    Writes the given content to a file within the specified working directory, ensuring security and directory creation.

    Args:
        working_directory (str): The base directory within which file writes are permitted.
        file_path (str): The relative path to the file to write, from the working directory.
        content (str): The content to write to the file.
        verbose (bool, optional): If True, prints detailed status and error messages. Defaults to False.

    Returns:
        str: A message indicating success or describing the error encountered.

    Notes:
        - Does not raise exceptions directly; returns error messages as strings instead.
    """

    working_directory_abspath: str = os.path.abspath(working_directory)

    file_abspath: str = os.path.abspath(
        os.path.join(working_directory_abspath, file_path or "")
    )

    common_path = os.path.commonpath([working_directory_abspath, file_abspath])

    if common_path != working_directory_abspath:
        if verbose:
            print("--- error ---")
            print(
                f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
            )
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(file_abspath):
        try:
            os.makedirs(os.path.dirname(file_abspath), exist_ok=True)
        except Exception as e:
            if verbose:
                print("--- error ---")
                print(f"Error: creating directory: {e}")
            return f"Error: creating directory: {e}"
    if os.path.exists(file_abspath) and os.path.isdir(file_abspath):
        if verbose:
            print("--- error ---")
            print(f'Error: "{file_path}" is a directory, not a file')
        return f'Error: "{file_path}" is a directory, not a file'

    try:
        with open(file_abspath, "w", encoding="utf-8") as f:
            f.write(content)
        if verbose:
            print("--- write_file ---")
            print(
                f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
            )
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except OSError as err:
        if verbose:
            print("--- error ---")
            print(f"Error: Failed to write to {file_path}: {err}")
        return f"Error: Failed to write to {file_path}: {err}"


# write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum", verbose=True)
# write_file(
#     "calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet", verbose=True
# )
# write_file("calculator", "/tmp/temp.txt", "this should not be allowed", verbose=True)
