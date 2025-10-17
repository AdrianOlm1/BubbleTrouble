# Bubble Trouble

Bubble Trouble is an exciting, time-based game developed using Pygame. Players navigate through various levels, facing different challenges while using a variety of weapons to defeat enemies. The game includes custom sounds, textures, and a unique level system to enhance the gaming experience.

## Play Online

Play the game directly in your browser: [https://adrianolm1.github.io/BubbleTrouble/](https://adrianolm1.github.io/BubbleTrouble/)

The web version is automatically deployed using GitHub Pages and pygbag whenever changes are pushed to the main branch.

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

### Play in Browser (Recommended)
Simply visit [https://adrianolm1.github.io/BubbleTrouble/](https://adrianolm1.github.io/BubbleTrouble/) to play instantly without any installation!

### Run Locally

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/AdrianOlm1/BubbleTrouble.git
   cd BubbleTrouble
   ```

2. **Install Dependencies**:
   Make sure you have Python and Pygame installed. You can install Pygame using pip:
   ```bash
   pip install pygame
   ```

3. **Run the Game**:
   ```bash
   cd BubbleTrouble
   python main.py
   ```

### Build Web Version Locally

1. **Install pygbag**:
   ```bash
   pip install pygbag
   ```

2. **Build and serve the game**:
   ```bash
   pygbag BubbleTrouble
   ```
   Then open your browser to `http://localhost:8000`

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

## Web Deployment

This game is automatically deployed to GitHub Pages using pygbag. The deployment workflow:

1. Converts the Pygame code to run in the browser using WebAssembly
2. Packages all assets (sounds, fonts, graphics) into the web build
3. Deploys to GitHub Pages automatically on every push to main branch

### Setting Up GitHub Pages

To enable deployment for your own fork:

1. Go to your repository Settings
2. Navigate to "Pages" in the left sidebar
3. Under "Build and deployment", set Source to "GitHub Actions"
4. Push changes to the main branch to trigger automatic deployment
5. Your game will be available at `https://[your-username].github.io/BubbleTrouble/`

The game will work with all sounds and assets in the browser!
