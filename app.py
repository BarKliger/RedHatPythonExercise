import argparse
import os
import glob
import re
from typing import Pattern

# parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                     help='an integer for the accumulator')
# parser.add_argument('--sum', dest='accumulate', action='store_const',
#                     const=sum, default=max,
#                     help='sum the integers (default: find the max)')
parser = argparse.ArgumentParser(description='Do Regex search on file/s, and print what has been found')
print_options_group = parser.add_mutually_exclusive_group()
parser.add_argument('-r', '--regex', type=str, required=True,help='The regex string used to search inside the files')
# parser.add_argument('-f', '--files', type=str,help='The files to search the regex string against')
parser.add_argument('-f', '--files', nargs="*", help='Path of a file or a folder of files.', type=str,default=[])
parser.add_argument('--recursive', action='store_true', help='Search through subfolders')
print_options_group.add_argument('-u', '--underscore', help='prints "^" under the matching text',action='store_true')
print_options_group.add_argument('-c', '--color', help='highlight matching text ',action='store_true')
print_options_group.add_argument('-m', '--machine', help='generate machine readable output.  format: file_name:no_line:start_pos:matched_text',action='store_true')
parser.add_argument('-e', '--extension', default='', help='File extension to filter by.')
args = parser.parse_args()

def print_underscores(file, line, line_counter, match_start, match_end):
    print(f"{file}:{line_counter}: {line}", end='')
    print(' ' * (len(f"{file}:{line_counter}: ") + match_start) + ('^' * (match_end - match_start)))

def main():
    print("Welcome to the Regex finder and Printer")
    print(args.regex)
    print(args.files)
    
    text_to_search = R'''
abcdefg
abcdefg
abcdef{args.regex}g
123-456-7890
123*456*7890
123\456\7890
\
\\
\\a\
\\a\
'''
    
    pattern = re.compile(args.regex)
    # print(re.search(pattern, text_to_search))
    
    # matches = pattern.finditer(text_to_search)
    
    # for match in matches:
    #     print(match.span())
    #     print(text_to_search[match.start():match.end()])
        
        
        
    # Parse paths
    full_paths = [os.path.join(os.getcwd(), path) for path in args.files]
    files = set()
    for path in full_paths:
        if os.path.isfile(path):
            files.add(path)
        else:
            files |= set(glob.glob(path + '/*' + args.extension))

    for f in files:
        print(f)
        with open(f,'r',encoding='ascii') as file:
            lines = file.readlines()
            line_counter = 0
            for line in lines:
                line_counter += 1
                matches = pattern.finditer(line)
                for match in matches:
                    print_underscores(f, line, line_counter, match.start(), match.end())
                    # print(f"{f}:{line_counter}: {line}", end='')
                    # print(' ' * (len(f"{f}:{line_counter}: ") + match.start()), end='')
                    # print('^' * (match.end() - match.start()), end='')
                    # print()    

if __name__ == '__main__':
    main()