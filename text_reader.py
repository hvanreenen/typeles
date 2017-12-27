import data


class TextReader():
    def __init__(self, story_number = 0, line_number = 0):
        self.story_number = story_number
        self.line_number = line_number
        self.words = []

    def get_line(self, line_number):
        self.line_number = line_number
        if not self.words:
            story = data.texts[self.story_number]
            self.words = story.split(' ')
        if self.line_number * 8 > len(self.words):
            self.next_story()
        return ' '.join(self.words[self.line_number * 8: (self.line_number + 1) * 8])

    def next_story(self):
        self.story_number += 1
        story = data.texts[self.story_number]
        self.words = story.split(' ')
        self.line_number = 0
