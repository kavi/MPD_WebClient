class Config:
    def __init__(self):
        self.ip='192.168.1.10'
        self.port=5000
        self.url='http://' + self.ip + ':' + str(self.port) + '/mpd/'
