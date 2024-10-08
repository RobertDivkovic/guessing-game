import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import random

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('guessing_game')

guesses_sheet = SHEET.worksheet('guesses')


def choose_level():
    """
    Prompt players to select which difficulty level they want and
    it returns selected sheet.
    Validates input of expected values.
    """
    levels = {'1': 'easy', '2': 'moderate', '3': 'challenging'}
    print("\nHello, welcome to numbers guessing game.\n")
    print("Choose your difficulty level and find the wanted number:\n")
    print("1: Easy (1-50 numbers)\n")
    print("2: Moderate (1-100 numbers)\n")
    print("3: Challenging (1-1000 numbers)\n")

    while True:
        choice = input("Enter the number corresponding to your choice: \n")
        if choice in levels:
            print(f"Your have chosen the {levels[choice]} level.\n")
            return SHEET.worksheet(levels[choice])
        else:
            print("Invalid choice, please enter 1, 2, or 3.\n")


def provide_feedback(guess, target, level):
    """
    Provide feedback based on how close is the guess to the wanted number.
    Depending on level, the feedback will vary.
    """
    if level == 'easy':
        if abs(guess - target) <= 5:
            print("You are within 5 numbers range of the wanted number.\n")
        elif abs(guess - target) <= 10:
            print("You are within 10 numbers range of the wanted number.\n")
        elif abs(guess - target) <= 20:
            print("You are within 20 numbers range of the wanted number.\n")
    elif level == 'moderate':
        if abs(guess - target) <= 10:
            print("You are within 10 numbers range of the wanted number.\n")
        elif abs(guess - target) <= 25:
            print("You are within 25 numbers range of the wanted number.\n")
        elif abs(guess - target) <= 50:
            print("You are within 50 numbers range of the wanted number.\n")
    elif level == 'challenging':
        if abs(guess - target) <= 50:
            print("You are within 50 numbers range of the wanted number.\n")
        elif abs(guess - target) <= 150:
            print("You are within 150 numbers range of the wanted number.\n")
        elif abs(guess - target) <= 300:
            print("You are within 300 numbers range of the wanted number.\n")


def play_game(level_sheet, level):
    """
    Handle the main game loop; asks players for guesses, gives feedback,
    and tracks the number of guesses
    """
    # Get all the numbers from the chosen level sheet
    numbers = level_sheet.col_values(1)
    numbers = [int(num) for num in numbers]

    # randomly selects a wanted number from the sheet
    target = random.choice(numbers)

    print(f"The number to guess is between {min(numbers)} and {max(numbers)}.")

    guesses = 0

    while True:
        guess = input("Enter your guess: \n")
        # Validate that the input is a number
        if guess.isdigit():
            guess = int(guess)
            guesses += 1
            if guess == target:
                print("Congrats, you guessed the wanted number!\n")
                break
            else:
                # provide feedback based on the guess and level
                provide_feedback(guess, target, level)
        else:
            print("Input invalid. Please enter a valid number.")
    # returns number of guesses to store later
    return guesses


def store_result(guesses_sheet, player_name, number_of_guesses):
    """
    Stores session result in the 'guesses' sheet,
    including player name, number of guesses,
    and the timestamp. It also tracks session ID.
    """

    session_id = len(guesses_sheet.get_all_values()) + 1
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    guesses_sheet.append_row([
        session_id,
        player_name,
        number_of_guesses,
        timestamp
    ]
    )


def display_summary(guesses_sheet, player_name):
    """
    Displays the game summary for the player by
    retrieving their session data from 'guesses' sheet.
    """
    # get all datra from the sheet
    records = guesses_sheet.get_all_records()

    # Find the records for player
    player_records = (
        [record for record in records if record['Player Name'] == player_name])

    if player_records:
        print("\nGame Summary:")
        for record in player_records:
            print(
                f"\nSession ID: {record['Session ID']}, "
                f"Number of Guesses: {record['Number of guesses']}, "
                f"Timestamp: {record['Timestamp']}\n")
    else:
        print("No records found for this player.\n")


def update_leaderboard(player_name, number_of_guesses, level):
    """
    Updates 'leaderboard' sheet with players score if
    it qualifies to be in the top 10 scores.
    Combine scores across all levels.
    """
    leaderboard_sheet = SHEET.worksheet('leaderboard')
    leaderboard = leaderboard_sheet.get_all_values()[1:]  # Excludes header row

    # conveert leaderboard data to list of dictionaries
    leaderboard = [
        {
            'Player Name': row[0],
            'Number of Guesses': int(row[1]),
            'Timestamp': row[2],
            'Level': row[3]
        }
        for row in leaderboard
    ]

    # Add the player's score to the leaderboard
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_entry = {
        'Player Name': player_name,
        'Number of Guesses': number_of_guesses,
        'Timestamp': timestamp,
        'Level': level
    }
    leaderboard.append(new_entry)
    # Sort leaderboard by the number of guesses (ascending order)
    leaderboard = sorted(leaderboard, key=lambda x: x['Number of Guesses'])
    # Keep only the top 10 scores
    leaderboard = leaderboard[:10]
    # Clear the current leaderboard sheet and write the updated leaderboard
    leaderboard_sheet.clear()
    row_data = [
        'Player Name',
        'Number of Guesses',
        'Timestamp',
        'Level']
    leaderboard_sheet.append_row(row_data)

    for entry in leaderboard:
        leaderboard_sheet.append_row([
            entry['Player Name'],
            entry['Number of Guesses'],
            entry['Timestamp'],
            entry['Level']
        ])


def display_leaderboard():
    """
    Displays the top 10 players on the combined leaderboard.
    """
    leaderboard_sheet = SHEET.worksheet('leaderboard')
    leaderboard = leaderboard_sheet.get_all_values()[1:]  # Exclude header row

    if not leaderboard:
        print("The leaderboard is currently empty.\n")
        return

    print("\n--- Leaderboard ---")
    for idx, row in enumerate(leaderboard, start=1):
        print(
            f"{idx}. {row[0]} - {row[1]} guesses on {row[2]} "
            f"(Level: {row[3]})")
    print("-------------------")


def main():
    """
    The main loop for the number guessing game.

    This function controls the overall flow of the game, including:
    Prompting the player to choose a difficulty level.
    Collecting the player's name and ensuring it contains only letters.
    Running the game session where the player guesses the number.
    Storing the results of the game in a Google Sheets worksheet.
    Updating the leaderboard if the player's score qualifies.
    Asking the player if they want to view the leaderboard,
    accepting only "yes" or "no" responses.
    Asking the player if they want to play again,
    accepting only "yes" or "no" responses.

    The game will continue in a loop, allowing the player to play multiple
    sessions until they choose to quit.
    """
    while True:
        # choose level and play the game
        level_sheet = choose_level()
        level = level_sheet.title  # Get level name
        # Validate player's name input
        while True:
            player_name = input("Enter your name: ")
            if player_name.isalpha():
                break
            else:
                print("Invalid name. Please use letters only.")

        number_of_guesses = play_game(level_sheet, level)

        # store the result in the guesses sheet
        store_result(guesses_sheet, player_name, number_of_guesses)

        # Update the leaderboard with the player's score
        update_leaderboard(player_name, number_of_guesses, level)

        # Ask if the player wants to view the leaderboard
        while True:
            view_leaderboard = input(
                "Do you want to view the leaderboard? (yes/no): ").lower()
            if view_leaderboard in ['yes', 'no']:
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

        if view_leaderboard == 'yes':
            display_leaderboard()

        # Ask if the player wants to play again
        while True:
            play_again = input("Do you want to play again? (yes/no): ").lower()
            if play_again in ['yes', 'no']:
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

        if play_again != 'yes':
            print("Thanks for playing! Goodbye!")
            break


if __name__ == "__main__":
    main()
