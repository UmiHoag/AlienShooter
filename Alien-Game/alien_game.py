import pygame
import time
import random
from ship import Ship
from button import Button
from button import Game_Over
import game_functions as gf
from settings import Settings
from pygame.sprite import Group
from game_stats import GameStats
from scoreboard import Scoreboard
from scoreboard import Quit_State

def run_game():
	pygame.init()
	ai_settings = Settings()
	screen = pygame.display.set_mode(
		(ai_settings.screen_width, ai_settings.screen_height))
	pygame.display.set_caption("Alien Invasion")

	FPS = 60
	clock = pygame.time.Clock()

	ship = Ship(ai_settings, screen) 
	bullets = Group()
	alien_bullets = Group()
	aliens = Group()
 
	stats = GameStats(ai_settings)
	score = Scoreboard(ai_settings, screen, stats)
	inactive = Quit_State(ai_settings, screen)

	gf.create_fleet(ai_settings, screen, ship, aliens)

	gf.load_score(stats)
	score.prep_high_score()
	score.show_score()

	play_button = Button(ai_settings, screen, "ENTER TO PLAY")
	game_over = Game_Over(ai_settings, screen, "GAME OVER")
	
	
	while True:
		clock.tick(FPS)
		gf.check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets, score, alien_bullets )
		if stats.game_active:
			ship.update()
			gf.update_bullets(ai_settings, screen, stats, score, ship, aliens, bullets)
			gf.update_enemy_bullets(ai_settings, screen, stats, score, ship, aliens, alien_bullets)
			gf.update_aliens(ai_settings, stats, score, screen, ship, aliens, bullets, alien_bullets, game_over)
		if not stats.game_active:
			game_over.draw_button()
		gf.update_screen(ai_settings, screen, stats, score, ship, aliens, bullets, play_button, inactive, alien_bullets, game_over)

run_game()