# Bubble Trouble

Bubble Trouble is an exciting, time-based game developed using Pygame. Players navigate through various levels, facing different challenges while using a variety of weapons to defeat enemies. The game includes custom sounds, textures, and a unique level system to enhance the gaming experience.

## Features

- **Time-Based Gameplay**: Complete levels within a specified time limit.
- **Multiple Weapons**: Choose from various weapons, each with unique characteristics:
  - Mono Shooter
  - Tri Shooter
  - Laser
  - Chain Shooter
  - Bomber
- **Custom Sounds**: Includes custom sound effects for different actions and events.
- **Custom Textures**: Unique textures to enhance the visual appeal of the game.
- **Level System**: Progress through multiple levels, with each level introducing new challenges.
- **Coins**: Collect coins to increase your score.
- **Pause and Game Over Screens**: Properly handles game pause and game over states with informative displays.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/bubble-trouble.git
   cd bubble-trouble
2. **Install Dependencies**:
Make sure you have Python and Pygame installed. You can install Pygame using pip:
   ```bash
   pip install game
3. **Run the Game**:
   ```bash
    python main.py

## How to Play
- **Movement**: Use the left and right arrow keys to move the player.
- **Shooting**:
  - Press '1' to shoot Mono Bullets.
  - Press '2' to shoot Tri Bullets.
  - Press '3' to shoot a Chain.
  - Press '4' to shoot a Laser.
  - Press 'Space' to deploy a Bomber.
-**Pause**: Press the 'ESC' key to pause the game
-**Objective**: Destroy all bubbles in each level before time runs out. Collect coins to increase your score.

# Game Overview

## Main Classes

- **Player**: The main character controlled by the player.
- **ProjectileMono, ProjectileTri, ProjectileLaser, ProjectileChain, ProjectileBomber**: Different projectile types with unique behaviors.
- **WeaponHandler**: Manages the player's weapons and shooting mechanics.
- **Bubble**: The primary enemy that splits into smaller bubbles when hit.
- **Coin**: Collectible items that increase the player's score.

## Main Functions

- `reset_game()`: Resets the game state.
- `new_level()`: Initializes a new level with appropriate enemies and settings.
- `display()`: Updates and displays the game HUD.
- `display_game_over()`: Shows the game over screen and handles replay logic.
- `display_pause()`: Shows the pause screen.
