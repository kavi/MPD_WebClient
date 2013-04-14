class MpdStatus:
    def __init__(self):
        self.volume = 0
        self.elapsed = 0
        self.state = ''

    def __str__(self):
        return "[Volume=" + str(self.volume) + ", elapsed=" + str(self.elapsed) + ", state=" + self.state + "]"

    def __repr__(self):
        return __str__(self)

class MpdSong:
    def __init__(self):
        self.title = ''
        self.artist = ''
        self.album = ''
        self.trackno = 0
        self.elapsed = 0
        self.length = 0
        self.pos = -1

    def __str__(self):
        return "[pos=" + str(self.pos) + ", title=" + self.title + ", Artist=" + self.artist + ", Album=" + self.album + ", Track=" + str(self.trackno) + ", length=" + str(self.length) + ", elapsed=" + str(elapsed) + "]"

    def __repr__(self):
        return __str__(self)

if __name__ == '__main__':
    s = MpdSong()
    print s
