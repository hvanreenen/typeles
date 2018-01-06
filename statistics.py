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

    def get_plot_data(self):
        days = []
        means1 = []
        means2 = []
        day = ''
        entries_per_day = 0
        sum1 = 0
        sum2 = 0
        for dict_row in self.rows:
            row = StatisticsRow.to_obj(dict_row)
            if day and day != row.get_day():
                means1.append(sum1/entries_per_day)
                means2.append(sum2/entries_per_day)
                days.append(day.strftime('%m-%d'))
                entries_per_day = 0
                sum1 = 0
                sum2 = 0
            day = row.get_day()
            entries_per_day += 1
            sum1 += row.get_keystrokes_per_minute()
            sum2 += row.get_errors_per_typed_chars() * 10000
        means1.append(sum1/entries_per_day)
        means2.append(sum2/entries_per_day)
        days.append(day.strftime('%m-%d'))
        return days, means1, means2

    def plot(self):
        import matplotlib.pyplot as plt
        self.rows = []
        self.read()
        days, means1, means2 = self.get_plot_data()
        plt.plot(days, means1, 'b--', days, means2, 'r--')
        plt.show()







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

    def get_day(self):
        return self.start_time.date()

    def get_errors_per_typed_chars(self):
        return self.typed_errors / self.typed_chars

    @staticmethod
    def to_obj(dict_row):
        obj = StatisticsRow()
        obj.start_time = datetime.datetime.strptime(dict_row['start_time'][:19], '%Y-%m-%d %H:%M:%S')
        obj.end_time = datetime.datetime.strptime(dict_row['end_time'][:19], '%Y-%m-%d %H:%M:%S')
        obj.typed_chars = int(dict_row['typed_chars'])
        obj.typed_errors = int(dict_row['typed_errors'])
        obj.story_number = int(dict_row['story_number'])
        obj.line_number = int(dict_row['line_number'])
        return obj


if __name__ == '__main__':
    s = Statistics()
    s.plot()
    # # plt.plot([1,2,3,4], [2,2,3,4])
    # # plt.ylabel('some numbers')
    # # plt.show()
    #
    # t = ['2017-10-10','2017-10-11','2017-10-12','2017-10-14']
    # t2 = [2,4,6,8]
    # t3 =[ 7,6,5,4]
    #
    # # red dashes, blue squares and green triangles
    # plt.plot(t, t2, 'r--', t, t3, 'b--')
    # plt.show()
