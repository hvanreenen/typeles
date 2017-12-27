import csv
import datetime


class Statistics():
    def __init__(self):
        self.rows = []
        self.read()

    def get_last_row(self):
        stats_row = StatisticsRow()
        if self.rows:
            raw_row= self.rows[len(self.rows) -1]
            stats_row.__dict__ = raw_row
            stats_row.typed_chars = int(raw_row['typed_chars'])
            stats_row.typed_errors = int(raw_row['typed_errors'])
            stats_row.story_number = int(raw_row['story_number'])
            stats_row.line_number = int(raw_row['line_number'])

        return stats_row

    def add_row(self, statistic_row):
        self.rows.append(statistic_row.__dict__)

    def read(self):
        with open('stats.csv') as file:
            csvreader = csv.DictReader(file)
            for row in csvreader:
                self.rows.append(row)

    def write(self):
        with open('stats.csv', 'w', newline='') as file:
            # csvwriter = csv.writer(file, delimiter=';')
            # csvwriter.writerows(self.rows)
            fieldnames = ['start_time', 'end_time', 'typed_chars', 'typed_errors', 'story_number', 'line_number']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.rows)



class StatisticsRow():
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.typed_chars = 0
        self.typed_errors = 0
        self.story_number = 0
        self.line_number = 0

    def get_duration(self):
        """
        delta of end_time minus start_time
        :return: seconds
        """
        delta = self.end_time - self.start_time
        duration = delta.seconds
        return duration

    def get_duration_as_time_format(self):
        seconds = self.get_duration()
        return str(datetime.timedelta(seconds=seconds))

    def get_keystrokes_per_minute(self):
        seconds = self.get_duration()
        if seconds > 0:
            keystrokes_per_minute =  self.typed_chars / (seconds /60)
            return keystrokes_per_minute
        else:
            return 0


