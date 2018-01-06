import datetime
import msvcrt

import sys

import winsound

from statistics import Statistics, StatisticsRow
from text_reader import TextReader


class TypeLesson():
    def __init__(self):
        self.is_running = False
        self.typed_chars = 0
        self.typed_errors = 0
        self.start_time = None #pas beginnen na eerste toets aanslag
        self.end_time = None
        self.error_mode = False
        self.statistics = Statistics()
        self.text_reader = None
        self.statistics_row = StatisticsRow()

    def start(self):
        self.is_running = True
        self.statistics_row = self.statistics.get_last_row()
        self.text_reader = TextReader(self.statistics_row.story_number, self.statistics_row.line_number)
        line = self.text_reader.next_line()
        print(line)
        char_number = 0

        while self.is_running:
            char = msvcrt.getch()
            if not self.start_time:
                #pas beginnen na eerste toets aanslag
                self.start_time = datetime.datetime.now()
            # char = input()
            if char == b'\x1b': #ESCAPE
                self.stop()
            elif char == b'\x08': #BACKSPACE
                if not self.error_mode:
                    char_number -= 1
                    sys.stdout.write('\x08')
                    sys.stdout.flush()

            elif char == b'\r': #ENTER
                line = self.text_reader.next_line()
                print()
                print(line)
                char_number = 0
            else:
                char = char.decode("utf-8")

                if char_number > len(line) -1:
                    self.handle_error(char)
                elif ord(line[char_number]) < 128 and (char_number > len(line) -1 or char != line[char_number]):
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
            # RED = "\x1b[1;31m"
            # sys.stdout.write(RED)
            sys.stdout.write(char)
            sys.stdout.write('\x08')
            sys.stdout.flush()
            winsound.Beep(220, 500)


    def stop(self):
        self.end_time = datetime.datetime.now()
        self.is_running = False
        self.write_stats()
        self.statistics.plot()

    def write_stats(self):
        self.statistics_row.start_time = self.start_time
        self.statistics_row.end_time = self.end_time
        self.statistics_row.typed_chars = self.typed_chars
        self.statistics_row.typed_errors = self.typed_errors
        self.statistics_row.story_number = self.text_reader.story_number
        self.statistics_row.line_number = self.text_reader.line_number



        duration = self.statistics_row.get_duration_as_time_format()
        per_minute = self.statistics_row.get_keystrokes_per_minute()
        print()
        print()
        print('Gestopt. Duur: {0}, Toetsaanslagen per minuut: {1}, Getypt: {2}, Fouten: {3}'.format(duration, round(per_minute, 0), self.typed_chars, self.typed_errors))

        self.statistics.add_row(self.statistics_row)
        self.statistics.write()


if __name__ == '__main__':
    lesson = TypeLesson()
    lesson.start()
    # lesson.is_running = False
    # lesson.stop()