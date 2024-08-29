# Guessing Numbers

## Introduction

This is a Python terminal game that allows players to guess a number, keep track of their scores, and view a leaderboard. The game runs in a terminal environment and integrates with Google Sheets to store player data.

![alt text](docs/images/responsivegame1.png)

[Link to live page](https://guessing-game1-92439eba22ca.herokuapp.com/)

## How to Play

- Players start by choosing a difficulty level.
- The game will randomly select a number within a range depending on the chosen difficulty.
- Players guess the number, and the game provides feedback on whether the guess is too high, too low, or correct.
- The number of guesses is tracked, and the player's result is stored in a Google Sheet.

## Features

### Existing Features

- **Difficulty Levels:** Players can choose between Easy, Moderate, and Challenging levels.
- **Random Number Generation:** The game randomly selects a number within a range based on the chosen difficulty.
- **Guess Feedback:** The game provides feedback on whether the guess is too high, too low, or correct.
- **Leaderboard:** The top players are tracked in a Google Sheets leaderboard, which is updated after each game.
- **Error Handling:** The game handles invalid inputs (e.g., non-numeric input, out-of-bounds numbers) and guides the player to make valid guesses.
