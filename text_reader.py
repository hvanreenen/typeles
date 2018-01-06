import data


class TextReader():
    def __init__(self, story_number = 0, line_number = 0):
        self.story_number = story_number
        self.line_number = line_number
        self.words = []

    def next_line(self):

        if not self.words:
            self.read_story()
        if self.line_number * 8 > len(self.words):
            self.next_story()
        raw_line = ' '.join(self.words[self.line_number * 8: (self.line_number + 1) * 8])
        line = ''
        for c in raw_line:
            if ord(c) < 256:
                line += c
            else:
                try:
                    c.encode('latin1')
                    line += c
                except:
                    o = ord(c)
                    pass
        self.line_number += 1
        return line

    def read_story(self):
        story = data.texts[self.story_number]

        story = story.replace('\r', '')
        story = story.replace('\n', ' ')
        story = story.replace('’', "'")
        # story = story.replace('\n', '. ')
        # story = story.replace('. .', '.').replace(':.', '.').replace('..', '.')
        self.words = story.split(' ')

    def next_story(self):
        self.story_number += 1
        self.line_number = 0
        self.read_story()

if __name__ == '__main__':
    t = TextReader(1,129)
    print(t.next_line())
    print(t.next_line())
    print(t.next_line())
    print(t.next_line())
    print(t.next_line())
    print(t.next_line())


