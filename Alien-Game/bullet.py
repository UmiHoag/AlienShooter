import pygame
from pygame.sprite import Sprite
import random

class Bullet(Sprite):
	def __init__(self, ai_settings, screen, ship):
		super().__init__()
		self.screen = screen

		self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
		self.rect.centerx = ship.rect.centerx
		self.rect.top = ship.rect.top

		self.y = float(self.rect.y)

		self.color = ai_settings.bullet_color
		self.speed_factor = ai_settings.bullet_speed_factor


	def update(self):
		self.y -= self.speed_factor
		self.rect.y = self.y
		

	def draw_bullet(self):
		pygame.draw.rect(self.screen, self.color, self.rect)

class Enemy_Bullet(Sprite):
	def __init__(self, ai_settings, screen, aliens):
		super().__init__()
		self.screen = screen

		self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
		enemies = []
		for alien in aliens:
			enemies.append(alien)
			alien = random.choice(enemies)
		self.rect.centerx = alien.rect.centerx
		self.rect.bottom = alien.rect.bottom

		self.y = float(self.rect.y)

		self.color = ai_settings.enemy_bullet_color
		self.speed_factor = ai_settings.enemy_bullet_speed_factor


	def update(self):
		self.y += self.speed_factor
		self.rect.y = self.y

	def draw_enemy_bullet(self):
		pygame.draw.rect(self.screen, self.color, self.rect)
