import pygame

class Slider:
    def __init__(self, x, y, width, min_val, max_val, start_val):
        self.rect = pygame.Rect(x, y, width, 6)
        self.min_val = min_val
        self.max_val = max_val
        self.handle_radius = 10
        self.dragging = False
        self.value = start_val
        self.handle_x = self.value_to_pos(start_val)

    def value_to_pos(self, value):
        ratio = (value - self.min_val) / (self.max_val - self.min_val)
        return int(self.rect.x + ratio * self.rect.width)

    def pos_to_value(self, x):
        ratio = (x - self.rect.x) / self.rect.width
        ratio = max(0, min(1, ratio))
        return self.min_val + ratio * (self.max_val - self.min_val)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if abs(mx - self.handle_x) < self.handle_radius and abs(my - self.rect.y) < 15:
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mx, _ = event.pos
            self.handle_x = max(self.rect.x, min(mx, self.rect.x + self.rect.width))
            self.value = self.pos_to_value(self.handle_x)

    def draw(self, screen, font):
        pygame.draw.rect(screen, (200, 200, 200), self.rect)
        pygame.draw.circle(screen, (50, 150, 255), (self.handle_x, self.rect.y + 3), self.handle_radius)
        text = font.render(f"{int(self.value)} mph", True, (255, 255, 255))
        screen.blit(text, (self.rect.x, self.rect.y - 30))