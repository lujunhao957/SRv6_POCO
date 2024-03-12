

class pathqos(object):
    def __init__(self, path,rtt ,std, avg, loss):
        self.path = path
        self.rtt=rtt
        self.std=std
        self.avg=avg
        self.loss=loss

    def get_path(self):
        return self.path

    def get_rtt(self):
        return self.rtt

    def get_std(self):
        return self.std

    def get_avg(self):
        return self.avg

    def get_loss(self):
        return self.loss