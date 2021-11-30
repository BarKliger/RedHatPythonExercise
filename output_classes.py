import abc


class Output():

    @abc.abstractmethod
    def print_output(self):
        pass
        # print(f"{self.file}:{self.line_counter}: ",end='')


class DefaultOutput(Output):

    def print_output(self, file, line, line_counter, matches):
        # self.print_fore_string()
        print(line, end='\n')


class UnderscoreOutput(Output):

    def print_output(self, file, line, line_counter, matches):
        str1 = ' ' * len(f"{file}:{line_counter}:")
        str2 = ''
        for match in matches:
            str2 = (str2 + (' ' * (match.start() - len(str2))) +
                    (('^' * (match.end() - match.start()))))
        underscore_line = str1 + str2
        print(line, end='')
        print(underscore_line)


class ColorOutput(Output):

    def print_output(self, file, line, line_counter, matches):
        counter = 0
        start_highlight = '\x1b[6;30;42m'
        end_highlight = '\x1b[0m'
        highlighted_str = ''
        last_end = 0
        for match in matches:
            highlighted_str = (highlighted_str + line[counter:match.start()] +
                               start_highlight +
                               line[match.start():match.end()] + end_highlight)
            counter = match.end()
            last_end = match.end()
        if(counter <= len(line)):
            highlighted_str = highlighted_str + line[last_end:len(line)]
        print(highlighted_str)


class MachineOutput(Output):

    def print_output(self, file, line, line_counter, matches):
        for match in matches:
            # self.print_fore_string()
            print("{}:{}:{}:{}".format(file, line_counter, match.start(), line[match.start():match.end()]))