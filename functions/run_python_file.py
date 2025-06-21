import os
import subprocess


def run_python_file(
    working_directory: str, file_path: str, verbose: bool = False
) -> str:
    """
    Executes a Python file located within a specified working directory.

    Args:
        working_directory (str): The base directory within which the Python file must reside.
        file_path (str): The relative or absolute path to the Python file to execute.
        verbose (bool, optional): If True, prints detailed error and output information. Defaults to False.

    Returns:
        str: The combined standard output and error from the executed Python file, or an error message if execution fails.

    Notes:
        - Only files with a ".py" extension are allowed.
        - Execution is limited to 30 seconds.
        - Exceptions are caught and returned as error messages.
    """

    working_directory_abspath: str = os.path.abspath(working_directory)

    file_abspath: str = os.path.abspath(
        os.path.join(working_directory_abspath, file_path or "")
    )

    if not os.path.isfile(file_abspath):
        if verbose:
            print("--- error ---")
            print(f'Error: File "{file_path}" not found.')
        return f'Error: File "{file_path}" not found.'

    _, extension = os.path.splitext(file_abspath)
    if extension != ".py":
        if verbose:
            print("--- error ---")
            print(f'Error: "{file_path}" is not a Python file.')
        return f'Error: "{file_path}" is not a Python file.'

    common_path = os.path.commonpath([working_directory_abspath, file_abspath])

    if common_path != working_directory_abspath:
        if verbose:
            print("--- error ---")
            print(
                f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
            )
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    try:
        commands = ["python3", file_abspath]
        result = subprocess.run(
            commands,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=working_directory_abspath,
        )
        output = []
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")

        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        if verbose:
            print("\n".join(output) if output else "No output produced.")
        return "\n".join(output) if output else "No output produced."
    except Exception as e:
        return f"Error: executing Python file: {e}"


# run_python_file("calculator", "main.py", verbose=True)
# run_python_file("calculator", "tests.py", verbose=True)
# run_python_file("calculator", "../main.py", verbose=True)
# run_python_file("calculator", "nonexistent.py", verbose=True)
