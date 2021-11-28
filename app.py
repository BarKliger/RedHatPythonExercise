import argparse
import os
import glob
import re

parser = argparse.ArgumentParser(description='Do Regex search on file/s, and print what has been found')
print_options_group = parser.add_mutually_exclusive_group()
parser.add_argument('-r', '--regex', type=str, required=True,help='The regex string used to search inside the files')
parser.add_argument('-f', '--files', nargs="*", help='Path of a file or a folder of files.', type=str,default=[])
parser.add_argument('--recursive', action='store_true', help='Search through subfolders')
print_options_group.add_argument('-u', '--underscore', help='prints "^" under the matching text',action='store_true')
print_options_group.add_argument('-c', '--color', help='highlight matching text ',action='store_true')
print_options_group.add_argument('-m', '--machine', help='generate machine readable output.  format: file_name:no_line:start_pos:matched_text',action='store_true')
parser.add_argument('-e', '--extension', default='', help='File extension to filter by.')
args = parser.parse_args()

def print_underscores(file, line, line_counter, matches):
    str1 = ' ' * len(f"{file}:{line_counter}: ")
    str2 = ''
    for match in matches:
        str2 = str2 + (' ' * (match.start() - len(str2))) + (('^' * (match.end() - match.start()))) #build the underscore line string
    underscore_line = str1 + str2
    print(f"{file}:{line_counter}: {line}", end='')
    print(underscore_line)

def print_highlight(file, line, line_counter, matches):
    
    start_highlight = '\x1b[6;30;42m'
    end__highlight = '\x1b[0m'
    highlighted_str = ''
    counter = 0
    last_end = 0
    for match in matches:
        # ttttabcdefgabcdefg6786876abc
        #     ^  
        # 
        highlighted_str = highlighted_str + line[counter:match.start()] + start_highlight + line[match.start():match.end()] + end__highlight #build the underscore line string
        counter = match.end()
        last_end = match.end()
    if(counter <= len(line)):
        highlighted_str = highlighted_str + line[last_end:len(line)]
    # print(start_highlight + 'Success!' + end__highlight + 'bbbb' + start_highlight + 'Success!' + end__highlight)
    print(f"{file}:{line_counter}: {highlighted_str}")
    
def main():
    print("Welcome to the Regex finder and Printer")
    print(args.regex)
    print(args.files)
    
    pattern = re.compile(args.regex)

    # Parse paths
    full_paths = [os.path.join(os.getcwd(), path) for path in args.files]
    files = set()
    for path in full_paths:
        if os.path.isfile(path):
            files.add(path)
        else:
            files |= set(glob.glob(path + '/*' + args.extension))

    for f in files:
        # print(f)
        with open(f,'r',encoding='ascii') as file:
            lines = file.readlines()
            line_counter = 0
            for line in lines:
                line_counter += 1
                matches = pattern.finditer(line)
                if(len(list(matches)) > 0):
                    # matches = pattern.finditer(line)
                    # print_underscores(f, line, line_counter, matches)
                    matches = pattern.finditer(line)
                    print_highlight(f, line, line_counter, matches)

if __name__ == '__main__':
    main()