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

![alt text](docs/testing/runningapp1.png)

- **Guess Feedback:** The game provides feedback on whether the guess is too high, too low, or correct.
- **Leaderboard:** The top players are tracked in a Google Sheets leaderboard, which is updated after each game.
- **Error Handling:** The game handles invalid inputs (e.g., non-numeric input, out-of-bounds numbers) and guides the player to make valid guesses.

![alt text](docs/testing/runningapp2.png)

### Future Features

- **Customization:** Allow players to set their own number ranges and difficulties.
- **Multiplayer Mode:** Add support for multiplayer sessions where players compete for the best score.
- **Enhanced Leaderboard:** Include additional statistics such as the fastest time to guess the number.

## Data Model

This game uses Google Sheets to store and manage player data, ensuring persistence and real-time updates.

### 1. Google Sheets Integration

The game uses the `gspread` library to interact with Google Sheets. Two main worksheets are utilized:

- **Guesses Worksheet (`guesses`):** Stores each player's game session data.
- **Leaderboard Worksheet (`leaderboard`):** Tracks the top 10 player scores across all difficulty levels.

### 2. Data Structure

#### **Guesses Worksheet:**
Each session is logged with the following data:
- **Session ID:** A unique identifier for each session.
- **Player Name:** The name entered by the player.
- **Number of Guesses:** The total number of guesses the player made.
- **Timestamp:** The date and time of the game session.

Example:
| Session ID | Player Name | Number of Guesses | Timestamp           |
|------------|-------------|-------------------|---------------------|
| 1          | Robert      | 5                 | 2024-08-29 14:30:00 |
| 2          | Bob         | 7                 | 2024-08-29 15:00:00 |

#### **Leaderboard Worksheet:**
Top scores are maintained with:
- **Player Name**
- **Number of Guesses**
- **Timestamp**
- **Level**

Example:
| Player Name | Number of Guesses | Timestamp           | Level      |
|-------------|-------------------|---------------------|------------|
| Charlie     | 3                 | 2024-08-29 16:00:00 | Easy       |
| Dana        | 4                 | 2024-08-29 16:30:00 | Moderate   |

### 3. Data Handling

- **`store_result(guesses_sheet, player_name, number_of_guesses)`**: Saves the game session details in the `guesses` worksheet.
- **`update_leaderboard(player_name, number_of_guesses, level)`**: Updates the leaderboard if the player's score is among the top 10. The leaderboard is sorted by the number of guesses, with the lowest number at the top.

## Deployment

The project was deployed using [Heroku](https://www.heroku.com/) following these steps:

1. Fork or clone the repository.
2. Create a new Heroku app.
3. Set the buildpacks to Python.
4. Link the Heroku app to the repository.
5. Deploy the app.