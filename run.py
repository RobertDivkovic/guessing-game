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
    print("Choose your difficulty level:")
    print("1: Easy (1-50)")
    print("2: Moderate (1-100)")
    print("3: Challenging (1-1000)")

    while True:
        choice = input("Enter the number corresponding to your cohoice: ")
        if choice in levels:
            print(f"Your have choosen the {levels[choice]} level.")
            return SHEET.worksheet(levels[choice])
        else:
            print("Invalid choice, please enter 1, 2, or 3.")

level_sheet = choose_level()

def play_game(level_sheet):
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
        try:
            guess = int(input("Enter your guess: "))
            guesses =+ 1
            if guess == target:
                print("Congrats, you guessed the wanted number!")
                break
            else:
                # add feedback logic
                print("Try again!")
        except ValueError:
            print("Please enter a valid number.")

    # returns number of guesses to store later
    return guesses

number_of_guesses = play_game(level_sheet)