import os
import platform
import shutil
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
    """Prints the current local time."""
    now = datetime.now()
    print(f"Current time: {now.strftime('%I:%M:%S %p')}")


def show_system():
    """Prints basic system information."""
    print(f"Operating system: {platform.system()} {platform.release()}")
    print(f"Machine: {platform.machine()}")
    print(f"Python: {platform.python_version()}")


def list_files():
    """Lists files and folders in the current directory."""
    files = os.listdir(".")

    if not files:
        print("This folder is empty.")
        return

    print("\nFiles and folders:")

    for file in files:
        print(f"  - {file}")


def create_folder(folder_name):
    """Creates a folder using the name provided by the user."""

    if not folder_name:
        print("Tell me the folder name.")
        return

    if os.path.exists(folder_name):
        print(f"'{folder_name}' already exists.")
        return

    try:
        os.makedirs(folder_name)
        print(f"Created folder: {folder_name}")

    except OSError as error:
        print(f"I couldn't create that folder: {error}")


def find_pdfs():
    """Recursively searches for PDF files."""

    pdfs = []

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
    """Displays disk usage information."""

    total, used, free = shutil.disk_usage(".")

    print(f"Total space: {total / (1024 ** 3):.2f} GB")
    print(f"Used space: {used / (1024 ** 3):.2f} GB")
    print(f"Free space: {free / (1024 ** 3):.2f} GB")


def understand_command(command):
    """
    Determines what the user wants Butler to do.

    Returns either:
        - a simple intent such as "time"
        - or an intent with data, such as ("create_folder", "School")
    """

    command = command.strip().lower()

    # List files
    if "file" in command and any(
        word in command for word in ["list", "show", "see"]
    ):
        return "list_files"

    # Time
    if "time" in command:
        return "time"

    # System information
    if "system" in command:
        return "system"

    # Find PDFs
    if "pdf" in command:
        return "find_pdfs"

    # Disk usage
    if "disk" in command:
        return "disk_usage"

    # Create folder + extract folder name
    if command.startswith("create folder"):
        folder_name = command.removeprefix("create folder").strip()

        return ("create_folder", folder_name)

    # Exit
    if command == "exit":
        return "exit"

    # Help
    if command == "help":
        return "help"

    # Unknown request
    return None


def handle_command(command):
    """Takes the user's input, determines the intent, and executes it."""

    intent = understand_command(command)

    if intent == "help":
        show_help()

    elif intent == "time":
        show_time()

    elif intent == "system":
        show_system()

    elif intent == "list_files":
        list_files()

    elif intent == "find_pdfs":
        find_pdfs()

    elif intent == "disk_usage":
        disk_usage()

    elif isinstance(intent, tuple) and intent[0] == "create_folder":
        folder_name = intent[1]
        create_folder(folder_name)

    elif intent == "exit":
        return False

    else:
        print("I don't understand that request yet.")
        print("Try asking me something I can currently do.")

    return True


def show_welcome():
    """Displays a welcome message when Butler starts."""

    print("""
================================
        COMPUTER BUTLER
================================

Type 'help' to see what I can do.
""")


def main():
    """Main entry point for the Computer Butler application."""

    show_welcome()

    running = True

    while running:
        command = input("\nButler > ")
        running = handle_command(command)

    print("Goodbye.")


if __name__ == "__main__":
    main()