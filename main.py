import datetime
import msvcrt

import sys

from statistics import Statistics, StatisticsRow
from text_reader import TextReader


class TypeLesson():
    def __init__(self):
        self.is_running = False
        self.typed_chars = 0
        self.typed_errors = 0
        self.start_time = datetime.datetime.now()
        self.end_time = None
        self.error_mode = False
        self.statistics = Statistics()
        self.text_reader = None
        self.statistics_row = StatisticsRow()

    def start(self):
        self.is_running = True
        self.statistics_row = self.statistics.get_last_row()
        self.text_reader = TextReader(self.statistics_row.story_number)
        line_number = self.statistics_row.line_number
        line = self.text_reader.get_line(line_number)
        print(line)
        char_number = 0

        while self.is_running:
            char = msvcrt.getch()
            # char = input()
            if char == b'\x1b': #ESCAPE
                self.stop()
            elif char == b'\x08': #BACKSPACE
                if not self.error_mode:
                    char_number -= 1
                    sys.stdout.write('\x08')
                    sys.stdout.flush()
            elif char == b'\r': #ENTER
                line_number += 1
                line = self.text_reader.get_line(line_number)
                print()
                print(line)
                char_number = 0
            else:
                char = char.decode("utf-8")


                if char_number > len(line) -1 or char != line[char_number]:
                    self.handle_error(char)
                else:
                    self.error_mode = False

                if not self.error_mode:
                    self.typed_chars += 1
                    char_number += 1
                    sys.stdout.write(char)
                    sys.stdout.flush()

            # print(char_number, char, self.error_mode)


    def handle_error(self, char):
        if not self.error_mode:
            self.error_mode = True
            self.typed_errors += 1
            sys.stdout.write(char)
            sys.stdout.write('\x08')
            sys.stdout.flush()


    def stop(self):
        self.end_time = datetime.datetime.now()
        self.is_running = False
        self.write_stats()

    def write_stats(self):
        self.statistics_row.start_time = self.start_time
        self.statistics_row.end_time = self.end_time
        self.statistics_row.typed_chars = self.typed_chars
        self.statistics_row.typed_errors = self.typed_errors
        self.statistics_row.story_number = self.text_reader.story_number
        self.statistics_row.line_number = self.text_reader.line_number



        duration = self.statistics_row.get_duration()
        per_minute = self.statistics_row.get_keystrokes_per_minute()
        print()
        print()
        print('Gestopt. Duur: {}, Toetsaanslagen per minuut: {}, Getypt: {}, Fouten: {}'.format(duration, per_minute, self.typed_chars, self.typed_errors))

        self.statistics.add_row(self.statistics_row)
        self.statistics.write()


if __name__ == '__main__':
    lesson = TypeLesson()
    lesson.start()
    # lesson.is_running = False
    # lesson.stop()