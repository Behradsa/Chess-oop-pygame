import pygame


class Square:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.promotion = False
        self.en_passant = None
        self.abs_x = x * width
        self.abs_y = y * height
        self.abs_pos = (self.abs_x, self.abs_y)
        self.pos = (x, y)
        self.color = "light" if (x + y) % 2 == 0 else "dark"
        self.draw_color = (218, 217, 181) if self.color == "light" else (128, 163, 82)
        self.highlight_color = (
            (228, 158, 119) if self.color == "light" else (203, 118, 41)
        )
        self.occupying_piece = None
        self.coord = self.get_coord()
        self.highlight = False

        self.rect = pygame.Rect(self.abs_x, self.abs_y, self.width, self.height)

    def get_coord(self):
        columns = "abcdefgh"
        return columns[self.x] + str(self.y + 1)

    def draw(self, display):
        if self.highlight:
            pygame.draw.rect(display, self.highlight_color, self.rect)
        else:
            pygame.draw.rect(display, self.draw_color, self.rect)

        if self.occupying_piece != None:
            centering_rect = self.occupying_piece.img.get_rect()
            centering_rect.center = self.rect.center
            display.blit(self.occupying_piece.img, centering_rect.topleft)