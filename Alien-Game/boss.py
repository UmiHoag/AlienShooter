import pygame
from pygame.sprite import Sprite

class Boss(Sprite):
	def __init__(self, ai_settings, screen):
            super(Boss, self).__init__(ai_settings, screen)
            self.screen = screen
            self.ai_settings = ai_settings

            self.image = pygame.image.load('Assignment1/images/boss.png').convert_alpha()
            self.rect = self.image.get_rect()

            self.rect.x = ai_settings.screen_width / 2 - self.rect.width / 2
            self.rect.y = 30

            self.x = float(self.rect.x)


def blitme(self):
		self.screen.blit(self.image, self.rect)


def check_edges(self):
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right - 10:
			return True
		elif self.rect.left <= 10:
			return True

def update(self):
		self.x += self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction
		self.rect.x = self.x

