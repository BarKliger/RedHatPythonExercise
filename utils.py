import argparse
import os
import glob
from output_classes import *

parser = argparse.ArgumentParser(description='''Perform Regex search on file/s,
                                and print what has been found''')
print_options_group = parser.add_mutually_exclusive_group()
parser.add_argument('-r', '--regex', type=str, required=True,
                    help='The regex string used to search inside the files')
parser.add_argument('-f', '--files', nargs="*", type=str, default=[],
                    help='Path of a file or a folder of files.')
print_options_group.add_argument('-u', '--underscore', action='store_true',
                                 help='prints "^" under the matching text')
print_options_group.add_argument('-c', '--color', action='store_true',
                                 help='highlight matching text with bg color')
print_options_group.add_argument('-m', '--machine', action='store_true',
                                 help='''generate machine readable output.
                                 format:
                                 file_name:no_line:start_pos:matched_text
                                 ''')
args = parser.parse_args()


def define_output():
    if args.underscore:
        output = UnderscoreOutput()
        return output
    elif args.color:
        output = ColorOutput()
        return output
    elif args.machine:
        output = MachineOutput()
        return output
    else:
        output = DefaultOutput()
        return output


def get_files():
    if(args.files == []):
        user_prompt = 'Enter file, files separated by space or a directory: '
        for i in (input(user_prompt)).split(' '):
            args.files.append(i)
    print(f"files: {args.files}")


def parse_files_path():
    full_paths = [os.path.join(os.getcwd(), path) for path in args.files]
    files = set()
    for path in full_paths:
        if os.path.isfile(path):
            files.add(path)
        else:
            files |= set(glob.glob(path + '/*'))
    return files


def run_regex_on_files(pattern, files, output):
    for f in files:
        with open(f, 'r', encoding='ascii') as file:
            lines = file.readlines()
            line_counter = 0
            for line in lines:
                line_counter += 1
                matches = pattern.finditer(line)
                if(len(list(matches)) > 0):
                    matches = pattern.finditer(line)
                    if not args.machine:  # Machine output is a special case
                        print(f"{f}:{line_counter}:", end='')  # Print prefix
                    output.print_output(f, line, line_counter, matches)