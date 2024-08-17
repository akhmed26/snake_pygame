import pygame

class Text:
    def __init__(self, txt, fonts, pixel, color, background=None):
        self.fonts = pygame.font.SysFont(fonts, pixel)
        self.text = self.fonts.render(txt, 1, color, background)
        self.rect_txt = self.text.get_rect()