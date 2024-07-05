class Settings():
	"""A class to store all settings for Alien invasion"""

	def __init__(self):
		# Settings
		self.screen_width = 1440
		self.screen_height = 790
		self.bg_color = (0,0,0)
		# (255,255,255)

		# ship settings.
		self.ship_limit = 2

		self.bullet_width = 4
		self.bullet_height = 15
		self.bullet_color = 8, 230, 0
		self.bullets_allowed = 3

		self.enemy_bullet_color = 230, 8, 0
		self.enemy_bullets_allowed = 7

		self.fleet_drop_speed = 8

		self.speed_up_scale = 1.1
		self.score_scale = 1.5 
  
		# Boss settings
		self.boss_speed_factor = 5  
		self.boss_points = 500 
		self.boss_bullet_speed_factor = 8  
		self.boss_bullet_cooldown = 60

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		self.ship_speed_factor = 8
		self.bullet_speed_factor = 17
		self.alien_speed_factor = 4
		self.enemy_bullet_speed_factor = 8

		self.fleet_direction = 1

		self.alien_points = 50

	def increase_speed(self):
		self.ship_speed_factor *= self.speed_up_scale
		self.bullet_speed_factor *= self.speed_up_scale
		self.alien_speed_factor *= self.speed_up_scale
		self.enemy_bullet_speed_factor *= self.speed_up_scale
		self.alien_points = int(self.alien_points * self.score_scale)
