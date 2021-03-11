import os
import time
class Blinking_light():
    def __init__(self, threading,frequency=0.5):
        self.on = False
        self.frequency = frequency

        threading.start_new_thread(self.switch)

    def switch(self):
        self.on = not self.on
        time.sleep(self.frequency)

    def render(self):
        if self.on:
            return '###'
        else:
            return '   '

class In_progress_light():
    def __init__(self,threding,frequency=0.5):
        self.counter = 0
        self.frequency = frequency
        threding.start_new_thread(self.swap_counter)
    def swap_counter(self):
        def valid_counter(counter):
            if counter > 3:
                return 0
            else:
                return counter
        
        self.counter = valid_counter(self.counter + 1)
        time.sleep(self.frequency)
    
    def render(self):
        return ('#' * self.counter).rjust(3)
    
        


class Cli_element():
    def __init__(self):
        self.content = []
        self.width = 0
        self.height = 0

    def refresh_height(self):
        self.height = len(self.content)

    # <section_name> = [{<id>:<value>,<cells>},... <rows>]
    def generate_element_as_column(self, **kwargs):
        def calculate_column_cell_width(**kwargs):
            cell_width = max(max(
                max((len(str(key)) + len(str(value)) + 5) for key, value in row.items()) for row in content)
                             for section_name, content in kwargs.items())
            row_width = max(cell_width * max(
                max(len(row) for row in content) for section_name, content in kwargs.items()),
                            max(len(str(section_name)) + 1 for section_name, content in kwargs.items()))
            return row_width, cell_width

        self.width, cell_width = calculate_column_cell_width(**kwargs)
        for section_name, content in kwargs.items():
            self.content.append(('=%s' % section_name).ljust(self.width - 1, '='))
            for row in content:
                self.content.append('')
                for key, value in row.items():
                    self.content[-1] += ('%s: ' % key) + ('%s | ' % value).rjust(cell_width - len(key) - 2)
            self.content = [line.ljust(self.width) for line in self.content]
        self.refresh_height()

    # <y_id> = [<cells values>]
    def generate_element_as_map(self, name, x_indexes, **kwargs):
        def calculate_column_cell_y_index_width(name, x_indexes, **kwargs):
            cell_width = max(
                max(len(x_index) for x_index in x_indexes),
                max(max(len(str(value)) for value in content) for key, content in kwargs.items())
            ) + 1
            y_index_width = max(len(str(key)) for key, value in kwargs.items()) + 3
            column_width = max(y_index_width + (cell_width * len(x_indexes)), (len(name) + 1))
            return column_width, cell_width, y_index_width

        self.width, cell_width, y_index_width = calculate_column_cell_y_index_width(name, x_indexes,
                                                                                    **kwargs)
        self.content.append(('=%s' % name).ljust(self.width - 1, '='))
        self.content.append(
            ' ' * y_index_width + ''.join([('%s ' % x_index).rjust(cell_width) for x_index in x_indexes]))
        self.content.append('-' * (self.width - 1))
        self.content.extend([''.join(line) for line in [[('%s | ' % y_index).rjust(y_index_width) + ''.join(
            [('%s ' % value).rjust(cell_width) for value in content])] for y_index, content in
                                                        kwargs.items()]])
        self.refresh_height()

    def generate_element_as_screen(self, name, *args):
        def align_the_width_of_the_elements(*args):
            for column in args:
                for element in column:
                    element.content = [line.ljust(max(ele.width for ele in column)) for line in
                                       element.content]

        def align_the_height_of_the_columns(*args):
            for column in args:
                while sum(element.height for element in column) < max(
                        sum(element.height for element in column) for column in args):
                    column[-1].content.append(' ' * column[-1].width)
                    for element in column:
                        element.refresh_height()

        align_the_height_of_the_columns(*args)
        align_the_width_of_the_elements(*args)
        for column in args:
            if not column == args[-1]:
                for element in column:
                    element.content = [''.join([line, '  ||  ']) for line in element.content]
        contests = [[line for ele in column for line in ele.content] for column in args]
        self.content = [''.join(elements) for elements in zip(*contests)]
        self.content.insert(0, (('=%s' % name).ljust(len(self.content[0]) - 1, '=')) + ' ')
        self.content.append('=' * (len(self.content[0]) - 1) + ' ')
        if len(self.content[0]) + 4 > os.get_terminal_size()[0]:
            self.content = ["Make terminal window wider!!!".center(os.get_terminal_size()[0])]
        else:
            self.content = [('||' + line + '||').center(os.get_terminal_size()[0]) for line in self.content]



