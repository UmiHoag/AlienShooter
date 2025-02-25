import sys
from time import sleep
import pygame
from bullet import Bullet
from bullet import Enemy_Bullet
from alien import Alien
from boss import Boss
import random

# Spacebar held flag
spacebar_held = False

def check_keydown_events(event, ai_settings, screen, ship, bullets, stats):  
	global spacebar_held
	if event.key == pygame.K_q:
		filename = 'highscore.txt'
		with open(filename, 'w') as file_object:
			file_object.write(str(stats.high_score))
		sys.exit()
	if stats.game_active:
		if event.key == pygame.K_RIGHT:
			ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			ship.moving_left = True
		elif event.key == pygame.K_SPACE: 
			fire_bullet(ai_settings, screen, ship, bullets)
			spacebar_held = True

def start_game(ai_settings, screen, stats, play_button, ship, aliens, bullets, event, sb, enemy_bullets):
	if not stats.game_active:
		if event.key == pygame.K_RETURN:
			reset_game(ai_settings, screen, stats, play_button, ship, aliens, bullets, sb, enemy_bullets)
   
def fire_bullet(ai_settings, screen, ship, bullets):
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)

def alien_shoot(ai_settings, screen, aliens, enemy_bullets):
	if len(enemy_bullets) < ai_settings.enemy_bullets_allowed:
		new_bullet = Enemy_Bullet(ai_settings, screen, aliens)
		enemy_bullets.add(new_bullet)


def check_keyup_events(event, ai_settings, ship): 
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False
	elif event.key == pygame.K_SPACE:
		global spacebar_held
		spacebar_held = False

def check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets, sb, enemy_bullets):
 global spacebar_held	
 for event in pygame.event.get():
		if event.type == pygame.QUIT:
			filename = 'highscore.txt'
			with open(filename, 'w') as file_object:
				file_object.write(str(stats.high_score))
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, ship, bullets, stats)
			start_game(ai_settings, screen, stats, play_button, ship, aliens, bullets, event, sb, enemy_bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ai_settings, ship)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y, event, sb, enemy_bullets)
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
			spacebar_held = True  # Set the flag when spacebar is pressed
			fire_bullet(ai_settings, screen, ship, bullets)
		elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
			spacebar_held = False  # Reset the flag when spacebar is released

		if spacebar_held and stats.game_active:
			fire_bullet(ai_settings, screen, ship, bullets)
        

def check_play_button(ai_settings, screen, stats, play_button, ship, aliens, 
	bullets, mouse_x, mouse_y, event, sb, enemy_bullets):
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		pygame.mouse.set_visible(False)
		reset_game(ai_settings, screen, stats, play_button, ship, aliens, bullets, sb, enemy_bullets)

	elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
		reset_game(ai_settings, screen, stats, play_button, ship, aliens, bullets, sb, enemy_bullets)


def reset_game(ai_settings, screen, stats, play_button, ship, aliens, bullets, sb, enemy_bullets):
	ai_settings.initialize_dynamic_settings()
	pygame.mouse.set_visible(False)
	stats.reset_stats()
	stats.game_active = True
	sb.prep_score()
	sb.prep_high_score()
	sb.prep_level()
	sb.prep_ships()
	sb.show_score()

	aliens.empty()
	bullets.empty()
	enemy_bullets.empty()

	create_fleet(ai_settings, screen, ship, aliens)
	ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, qs, enemy_bullets, game_over):
	screen.fill(ai_settings.bg_color)
	ship.blitme()
	aliens.draw(screen)

	sb.show_score()

	for bullet in bullets.sprites():
		bullet.draw_bullet()

	if not stats.game_active:
		play_button.draw_button()
		qs.show_quit()

	if game_over.over:
		game_over.draw_button()

	if stats.game_active:	
		for enemy_bullet in enemy_bullets.sprites():
			enemy_bullet.draw_enemy_bullet()

		if random.randrange(0, 65) == 1:
			alien_shoot(ai_settings, screen, aliens, enemy_bullets)

		pygame.sprite.groupcollide(bullets, enemy_bullets, True, True)

		game_over.over = False

	pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
	bullets.update()
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)

	check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def update_enemy_bullets(ai_settings, screen, stats, sb, ship, aliens, enemy_bullets):
	enemy_bullets.update()
	for enemy_bullet in enemy_bullets.copy():
		if enemy_bullet.rect.top >= ai_settings.screen_height:
			enemy_bullets.remove(enemy_bullet)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score()
		check_high_score(stats, sb)

	if len(aliens) == 0:
		bullets.empty()
		ai_settings.increase_speed()

		# increase level
		stats.level += 1
		sb.prep_level()

		create_fleet(ai_settings, screen, ship, aliens)


def get_number_aliens_x(ai_settings, alien_width):
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
	available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number + 30
	aliens.add(alien)
 
def create_boss(ai_settings, screen, aliens):
    boss = Boss(ai_settings, screen)
    aliens.add(boss)

def create_fleet(ai_settings, screen, ship, aliens):
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings, screen, aliens, alien_number, row_number)
		
	
def check_fleet_edges(ai_settings, aliens):
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break


def change_fleet_direction(ai_settings, aliens):
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1


def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets, enemy_bullets, game_over):
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets, enemy_bullets, game_over)
			break


def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets, enemy_bullets, game_over):
	if stats.ships_left > 0:
		stats.ships_left -= 1
  
		enemies = []
		for alien in aliens:
			enemies.append(alien.rect.y)

		sb.prep_ships()

		bullets.empty()
		enemy_bullets.empty()

		ship.center_ship()
		alien = Alien(ai_settings, screen)
		for alien in aliens:
			alien.rect.top -= enemies[0] - 110 
		aliens.update()
  
		pygame.display.update()

		# pause.
		sleep(0.6)
	else:
		stats.ships_left = -1
		sb.prep_ships()
		stats.game_active = False
		pygame.mouse.set_visible(True)
		game_over.over = True


def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets, enemy_bullets, game_over):
	check_fleet_edges(ai_settings, aliens)
	aliens.update()

	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets, enemy_bullets, game_over)

	if pygame.sprite.spritecollideany(ship, enemy_bullets):
		ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets, enemy_bullets, game_over)

	check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets, enemy_bullets, game_over)


def check_high_score(stats, sb):
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()

def load_score(stats):
	filename = 'highscore.txt'
	try:
		with open(filename) as file_object:
			score = file_object.read()
			stats.high_score = int(score)
	except FileNotFoundError:
		pass
			
