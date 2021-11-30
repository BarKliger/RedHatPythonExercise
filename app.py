import re
from utils import *


def main():
    print("Welcome to the Regex finder and Printer")
    print(f"Regex to search: {args.regex}")

    pattern = re.compile(args.regex)
    output = define_output()  # Get output type
    get_files()  # Validate if files were provided, if not get files from STDIN
    files = parse_files_path()
    run_regex_on_files(pattern, files, output)

if __name__ == '__main__':
    main()
