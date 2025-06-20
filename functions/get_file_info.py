import os


def get_files_info(
    working_directory: str, directory: str | None = None, verbose: bool = False
) -> str:

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
        print("--- get_files_info ---")
        print(f"directory: {directory_abspath}")
        print("\n".join(file_info))
        print("-" * 20)
    return "\n".join(file_info)


# test
get_files_info("calculator", directory="pkg", verbose=True)
get_files_info("calculator", verbose=True)
get_files_info("calculator", "../", verbose=True)
get_files_info("calculator", "/bin", verbose=True)
get_files_info("calculator", ".", verbose=True)
