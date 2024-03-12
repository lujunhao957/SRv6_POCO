
class pathinfo(object):
    def __init__(self, path, buffer_duration_probability,continuous_playback_duration_probability):
        self.path=path
        self.buffer_duration_probability=buffer_duration_probability
        self.continuous_playback_duration_probability=continuous_playback_duration_probability

    def get_path(self):
        return self.path

    def get_buffer_duration_probability(self):
        return self.buffer_duration_probability

    def get_continuous_playback_duration_probability(self):
        return self.continuous_playback_duration_probability