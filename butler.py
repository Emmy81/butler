import os
import platform
from datetime import datetime


def show_help():
    """Displays the list of available commands to the user."""
    print("""
Available commands:

  help              Show this message
  time              Show current time
  system            Show system information
  list files        List files in the current folder
  create folder X   Create a folder named X
  find pdfs         Find PDF files
  disk usage        Show disk information
  exit              Quit Butler
""")


def show_time():
    """Prints the current local time in HH:MM:SS AM/PM format."""
    now = datetime.now()
    print(f"Current time: {now.strftime('%I:%M:%S %p')}")


def show_system():
    """Prints basic system information such as OS, architecture, and Python version."""
    print(f"Operating system: {platform.system()} {platform.release()}")
    print(f"Machine: {platform.machine()}")
    print(f"Python: {platform.python_version()}")


def list_files():
    """Lists all files and directories in the current working directory."""
    files = os.listdir(".")

    if not files:
        print("This folder is empty.")
        return

    print("\nFiles and folders:")

    for file in files:
        print(f"  - {file}")


def create_folder(command):
    """
    Creates a new directory with the specified name.
    Expects the command string to start with 'create folder '.
    """
    folder_name = command.removeprefix("create folder").strip()

    if not folder_name:
        print("Tell me the folder name.")
        return

    if os.path.exists(folder_name):
        print(f"'{folder_name}' already exists.")
        return

    os.makedirs(folder_name)
    print(f"Created folder: {folder_name}")


def find_pdfs():
    """Recursively searches for and lists all PDF files in the current directory and its subdirectories."""
    pdfs = []

    # Walk through the directory tree
    for root, directories, files in os.walk("."):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdfs.append(os.path.join(root, file))

    if not pdfs:
        print("No PDFs found.")
        return

    print("\nPDF files:")

    for pdf in pdfs:
        print(f"  - {pdf}")


def disk_usage():
    """Displays disk usage information based on file system blocks."""
    # NOTE: os.statvfs is Unix-specific and may not work on Windows
    total, used, free = os.statvfs(".").f_blocks, os.statvfs(".").f_bfree, os.statvfs(".").f_bavail

    print(f"Available blocks: {free}")
    print(f"Total blocks: {total}")


def handle_command(command):
    """
    Parses and executes the user's input command.
    Returns True to continue running, or False to exit.
    """
    command = command.strip().lower()

    if command == "help":
        show_help()

    elif command == "time":
        show_time()

    elif command == "system":
        show_system()

    elif command == "list files":
        list_files()

    elif command.startswith("create folder"):
        create_folder(command)

    elif command == "find pdfs":
        find_pdfs()

    elif command == "disk usage":
        disk_usage()

    elif command == "exit":
        return False

    else:
        print("I don't understand that command yet.")
        print("Type 'help' to see what I can do.")

    return True


def main():
    """Main entry point for the Computer Butler application loop."""
    print("""
================================
        COMPUTER BUTLER
================================

Type 'help' to see what I can do.
""")

    running = True

    while running:
        command = input("\nButler > ")
        running = handle_command(command)

    print("Goodbye.")


if __name__ == "__main__":
    main()