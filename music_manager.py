import pygame

class Music_Manager:
    def __init__(self):
        pygame.mixer.init()
        self.current_track = None


    def play_track(self, filepath, loops=-1):
        if self.current_track != filepath:
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.play(loops=loops)
            self.current_track = filepath

    def stop(self):
        pygame.mixer.music.stop()
        self.current_track = None