import pygame
from constans import WHITE, PRIMARY_COLOR, DEFAULT_FONT_SIZE, GRAY


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


class Button():
    def __init__(self, pos=(0, 0), text_input="", font_size=DEFAULT_FONT_SIZE, text_color=WHITE, hovering_color=None, background_color=None, image=None):
        self.font = pygame.font.Font("assets/font.ttf", font_size)
        self.text_input, self.text_color, self.hovering_color = text_input, text_color, hovering_color
        self.text = self.font.render(text_input, True, self.text_color)
        self.text_rect = self.text.get_rect(center=pos)
        self.surface = pygame.Surface(
            (self.text_rect.width, self.text_rect.height))
        if image is not None:
            self.surface.blit(pygame.transform.scale(
                pygame.image.load(image), self.size), (0, 0))
        elif background_color is not None:
            self.surface.fill(background_color)
        self.surface.blit(self.text, (4, 4))

    def update(self, screen):
        screen.blit(self.surface, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.text_rect.left, self.text_rect.right) and position[1] in range(self.text_rect.top, self.text_rect.bottom):
            return True
        return False

    def changeColor(self, position, screen):
        rect = pygame.Rect(self.text_rect.left, self.text_rect.top,
                           self.text_rect.width, self.text_rect.height)
        if self.checkForInput(position):
            self.text = self.font.render(
                self.text_input, True, self.hovering_color)
            rect.left += 5
            rect.top -= 5
        else:
            self.text = self.font.render(
                self.text_input, True, self.text_color)
        self.surface.blit(self.text, (4, 4))
        self.update(screen)


def createPrimaryButton(pos, text_input):
    return Button(pos=pos, text_input=text_input, text_color=PRIMARY_COLOR, hovering_color=WHITE, background_color=GRAY)


def createSecondaryButton(pos, text_input):
    return Button(pos=pos, text_input=text_input, text_color=WHITE, hovering_color=PRIMARY_COLOR)
