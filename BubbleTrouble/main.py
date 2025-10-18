#from signal import pause
import pygame
import sys
import random
import math
import asyncio

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1000
FPS = 60
COUNTDOWN = 180
DEATH_COST = 45
LEVEL_REWARD = 45

# Setup the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bubble Trouble")

# Fonts
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
large_font = pygame.font.Font('font/Pixeltype.ttf', 350)
small_font = pygame.font.Font('font/Pixeltype.ttf', 36)

# Sounds
mono_sound = pygame.mixer.Sound('sounds/shoot.ogg')
tri_sound = pygame.mixer.Sound('sounds/pew.ogg')
laser_sound = pygame.mixer.Sound('sounds/laser2.ogg')
chain_sound = pygame.mixer.Sound('sounds/chain.ogg')
circle_die = pygame.mixer.Sound('sounds/pop2.ogg')
square_die = pygame.mixer.Sound('sounds/explode.ogg')
gameover = pygame.mixer.Sound('sounds/gameover.ogg')
gameoverBack = pygame.mixer.Sound('sounds/bass.ogg')
levelUps = pygame.mixer.Sound('sounds/yipee.ogg')
bomber = pygame.mixer.Sound('sounds/bomber.ogg')
coinsound = pygame.mixer.Sound('sounds/kaching.ogg')
pygame.mixer.music.load('sounds/background.ogg')


# Clock to control the frame rate
clock = pygame.time.Clock()

def reset_time():
    global start_time, remaining_time, timefix, pausefix
    remaining_time = COUNTDOWN
    start_time = pygame.time.get_ticks() // 1000
    timefix =0
    pausefix = 0

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = 8
        self.projectiles = pygame.sprite.Group()
        self.trail_group = pygame.sprite.Group()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        self.rect.clamp_ip(screen.get_rect())

    def shoot_mono(self):
        mono_sound.play()
        projectile = ProjectileMono(self.rect.centerx, self.rect.top)
        self.projectiles.add(projectile)

    def shoot_tri(self):
        tri_sound.play()
        projectile_straight = ProjectileMono(self.rect.centerx, self.rect.top)
        projectile_left = ProjectileTri(self.rect.centerx, self.rect.top, 60)
        projectile_right = ProjectileTri(self.rect.centerx, self.rect.top, 120)
        self.projectiles.add(projectile_straight, projectile_left, projectile_right)

    def shoot_laser(self):
        laser_sound.play()
        projectile = ProjectileLaser(self.rect.centerx, self.rect.top)
        self.projectiles.add(projectile)

    def shoot_chain(self):
        chain_sound.play()
        projectile = ProjectileChain(self.rect.centerx, self.rect.centery, self.trail_group)
        self.projectiles.add(projectile)

    def shoot_bomber(self):
        bomber.play()
        projectile = ProjectileBomber(self.rect.centerx, self.rect.centery)
        self.projectiles.add(projectile)

class ProjectileMono(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 20))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 10

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

class ProjectileTri(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.Surface((5, 20))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 10
        self.angle = math.radians(angle)

    def update(self):
        self.rect.y -= self.speed * math.sin(self.angle)
        self.rect.x += self.speed * math.cos(self.angle)
        if self.rect.bottom < 0 or self.rect.left > SCREEN_WIDTH or self.rect.right < 0:
            self.kill()

class ProjectileLaser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, SCREEN_HEIGHT))
        self.image.fill((255, 0, 100))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.duration_timer = 30

    def update(self):
        self.duration_timer -= 1
        if self.duration_timer <= 0:
            self.kill()

        self.rect.centerx = player.rect.centerx
        self.rect.bottom = player.rect.top

class ProjectileChain(pygame.sprite.Sprite):
    active_chain = None

    def __init__(self, x, y, trail_group):
        super().__init__()
        self.trail_group = trail_group
        self.image = pygame.Surface((5, 20))
        self.image.fill((128, 128, 128))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = SCREEN_HEIGHT
        self.speed = 10
        self.trail_counter = 0
        self.trail_frequency = 1
        self.left = True

        if ProjectileChain.active_chain:
            ProjectileChain.active_chain.kill_trail()
            ProjectileChain.active_chain.kill()

        ProjectileChain.active_chain = self

    def update(self):
        self.rect.y -= self.speed
        self.trail_counter += 1
        if self.trail_counter >= self.trail_frequency:
            if self.left:
                trail = Trail(self.rect.centerx - 5, self.rect.centery)
            else:
                trail = Trail(self.rect.centerx + 5, self.rect.centery)
            self.trail_group.add(trail)
            self.left = not self.left  # Alternate left and right
            self.trail_counter = 0

    def kill(self):
        self.kill_trail()
        ProjectileChain.active_chain = None
        super().kill()

    def kill_trail(self):
        for trail_sprite in self.trail_group.sprites():
            trail_sprite.kill()

class ProjectileBomber(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.size = 5
        self.color = (255, 255, 0)
        self.image = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.size, self.size), self.size)
        self.rect = self.image.get_rect()
        self.rect.center = (x, SCREEN_HEIGHT)
        self.speed = 30

    def update(self):
        self.size += self.speed
        self.image = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.size, self.size), self.size)
        self.rect = self.image.get_rect(center=self.rect.center)

        if self.size >= 200:
            self.kill()

class Trail(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill((128, 128, 128))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class WeaponHandler:
    def __init__(self, player):
        self.player = player
        self.shooting_mono = False
        self.shooting_tri = False
        self.shootMono_interval = 75
        self.shootTri_interval = 225
        self.last_shot_time_mono = 0
        self.last_shot_time_tri = 0
        self.laser_cooldown_timer = 0
        self.laser_cooldown = 180+30
        self.bomber_cooldown = 240
        self.bomber_timer = 0

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            # mono shooting
            if event.key == pygame.K_1:
                self.shooting_mono = True
            # tri shooting
            elif event.key == pygame.K_2:
                self.shooting_tri = True
            # laser shooting
            elif event.key == pygame.K_4:
               if self.laser_cooldown_timer == 0:
                    self.player.shoot_laser()
                    self.laser_cooldown_timer = self.laser_cooldown
            # chain shooting
            elif event.key == pygame.K_3:
                if ProjectileChain.active_chain:
                    ProjectileChain.active_chain.kill()
                    self.player.shoot_chain()
                else:
                    self.player.shoot_chain()
            elif event.key == pygame.K_SPACE:
                if self.bomber_timer == 0:
                    self.player.shoot_bomber()
                    self.bomber_timer = self.bomber_cooldown
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_1:
                self.shooting_mono = False
            elif event.key == pygame.K_2:
                self.shooting_tri = False

    def update(self):
        current_time = pygame.time.get_ticks()
        if self.shooting_mono and current_time - self.last_shot_time_mono > self.shootMono_interval:
            self.player.shoot_mono()
            self.last_shot_time_mono = current_time
        if self.shooting_tri and current_time - self.last_shot_time_tri > self.shootTri_interval:
            self.player.shoot_tri()
            self.last_shot_time_tri = current_time
        if self.laser_cooldown_timer > 0:
            self.laser_cooldown_timer -= 1
        if self.bomber_timer > 0:
            self.bomber_timer -= 1

class Bubble(pygame.sprite.Sprite):
    def __init__(self, x, y, size, direction):
        super().__init__()
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (0, 0, 255), (size // 2, size // 2), size // 2)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 4 * (1 + (0.15 * level))
        self.speed_x = self.speed if direction == 1 else -self.speed
        self.speed_y = random.choice([-self.speed, self.speed])
        self.size = size

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        # Check for collision with the left wall
        if self.rect.left < 0:
            self.rect.left = 0
            self.speed_x = -self.speed_x

        # Check for collision with the right wall
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.speed_x = -self.speed_x

        # Check for collision with the top wall
        if self.rect.top < 0:
            self.rect.top = 0
            self.speed_y = -self.speed_y

        # Check for collision with the floor
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.speed_y = -self.speed_y

    def split(self):
        circle_die.play()
        coin = Coin(self.rect.centerx, self.rect.centery)
        all_sprites.add(coin)
        coins.add(coin)

        if self.size > 30:
            new_size = self.size // 2
            bubble1 = Bubble(self.rect.centerx, self.rect.centery, new_size, 1)
            bubble2 = Bubble(self.rect.centerx, self.rect.centery, new_size, -1)
            return [bubble1, bubble2]
        else:
            return []

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.size = 10
        self.image = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 0), (self.size, self.size), self.size)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.rect.center = (x, y)
        self.speed = 2

    def update(self):

        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.y = SCREEN_HEIGHT
        else:
            self.rect.y += self.speed

def reset_game():
    global level
    level = 1
    reset_time()
    reset_game_after_death()

def reset_game_after_death():
    global timefix,level
    level -= 1
    timefix -= LEVEL_REWARD
    new_level()

def new_level():
    global timefix, level
    level += 1
    timefix += LEVEL_REWARD
    player.rect.centerx = SCREEN_WIDTH // 2
    player.rect.bottom = SCREEN_HEIGHT - 10
    player.projectiles.empty()
    bubbles.empty()
    all_sprites.empty()
    all_sprites.add(player)

    cut = SCREEN_WIDTH // (level + 1)
    for i in range(level):
        bubble = Bubble(cut * (i + 1), SCREEN_HEIGHT // 4, bubble_size * (1 + ((level // 3 + 1) * 1 / 8)), random.choice([0, 1]))
        bubbles.add(bubble)
        all_sprites.add(bubble)

def display():
    global remaining_time, timefix, pausefix
    if pause:
        pausefix += 17
    remaining_time = COUNTDOWN - (pygame.time.get_ticks() // 1000) - start_time + timefix + (pausefix//1000)
    score_surf = test_font.render(f'Time: {remaining_time}', False, (0, 255, 0))
    score_rect = score_surf.get_rect(center=(SCREEN_WIDTH - 100, 50))
    screen.blit(score_surf, score_rect)

    level_surf = test_font.render(f'Level: {level}', False, (0, 255, 0))
    level_rect = level_surf.get_rect(center=(100, 50))
    screen.blit(level_surf, level_rect)

async def display_game_over():
    gameoverBack.play()
    gameover.play()
    reset_time()
    screen.fill((0, 0, 0))
    game_over_text = large_font.render("GAME", False, (255, 0, 0))
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 150))
    game_over_text = large_font.render("OVER", False, (255, 0, 0))
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    play_again_text = small_font.render("Press ENTER to play again or ESC to quit", False, (255, 255, 255))
    screen.blit(play_again_text, (SCREEN_WIDTH // 2 - play_again_text.get_width() // 2, SCREEN_HEIGHT // 2 + 250))
    level_reached_text = small_font.render(f'You reached Level {level}', False, (0, 0, 255))
    screen.blit(level_reached_text, (SCREEN_WIDTH // 2 - level_reached_text.get_width() // 2, SCREEN_HEIGHT // 2 + 300))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                if event.key == pygame.K_ESCAPE:
                    return False
        await asyncio.sleep(0)
    return True

def display_pause():
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((128, 128, 128, 150))
    screen.blit(overlay, (0, 0))
    pause_text = large_font.render("PAUSED", True, (255, 255, 255))
    screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 2))

# Default initialization
player = Player()
bubbles = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
coins = pygame.sprite.Group()

bubble_size = 60

async def main():
    # Give browser time to initialize
    await asyncio.sleep(0)

    weapon_handler = WeaponHandler(player)
    reset_game()

    # Start background music (try-except for browser compatibility)
    try:
        pygame.mixer.music.play(-1)
    except:
        pass  # Music may fail in some browsers

    running = True
    global pause
    pause = False
    global timefix, remaining_time
    player_coins = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause = not pause
            else:
                weapon_handler.handle_input(event)

        # Update game state
        if not pause:
            all_sprites.update()
            player.projectiles.update()
            weapon_handler.update()

            if pygame.sprite.spritecollide(player, bubbles, False):
                timefix -= (DEATH_COST-1)
                square_die.play()
                reset_game_after_death()
                # Brief non-blocking pause after death
                await asyncio.sleep(0.5)

            # Check for collisions with projectiles
            hits = pygame.sprite.groupcollide(bubbles, player.projectiles, True, False)
            for bubble in hits:
                new_bubbles = bubble.split()
                if new_bubbles:
                    bubbles.add(new_bubbles)
                    all_sprites.add(new_bubbles)

                # Handle projectiles colliding with bubbles
                for projectile in hits[bubble]:
                    # Check if the projectile is not a laser
                    if not isinstance(projectile, ProjectileLaser) and not isinstance(projectile,ProjectileBomber):
                        # Kill the projectile if it's not a laser
                        projectile.kill()

            # Checks for collisions with the chain
            chain_hits = pygame.sprite.groupcollide(bubbles, player.trail_group, True, False)
            if chain_hits:
                for bubble in chain_hits:
                    new_bubbles = bubble.split()
                    bubbles.add(new_bubbles)
                    all_sprites.add(new_bubbles)
                ProjectileChain.active_chain.kill()  # Kill the entire chain

            # Checks for end of level
            if len(bubbles) == 0:
                levelUps.play()
                new_level()

            coin_hits = pygame.sprite.spritecollide(player, coins, True)
            for coin in coin_hits:
                player_coins += 1  # Increase the player's coin count
                coinsound.play()


        # Draw everything
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        player.projectiles.draw(screen)
        player.trail_group.draw(screen)
        display()

        if pause:
            display_pause()

        pygame.display.flip()

        if remaining_time <= 0:
            pygame.mixer.music.pause()
            continue_game = await display_game_over()
            if not continue_game:
                running = False
            else:
                reset_game()
                pygame.mixer.music.unpause()

        # Let browser control frame rate via asyncio (no manual FPS limiting)
        await asyncio.sleep(0)

    pygame.quit()

# Pygbag-compatible entry point
asyncio.run(main())
