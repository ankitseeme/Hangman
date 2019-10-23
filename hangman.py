"""A simple Hangman Game"""
from math import floor
from math import ceil
import os
from random import choice
import sys
import re
from colorama import Fore, Style

SCRIPT_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))


def wait():
    """Wait for user input"""
    try:
        input()
    except KeyboardInterrupt:
        pass


def instructions():
    """Print Initial Instructions for the user"""
    print_input_text("Let's go over the rules first!! Press Enter to continue...", " : ")
    wait()
    clear_screen()

    print_input_text("You'll be given a word or phrase... [Press Enter]", " : ")
    wait()
    clear_screen()

    print_input_text("You have to guess the word by guessing the "
                     "characters in the name, one by one... [Press Enter]", " : ")
    wait()
    clear_screen()

    print_input_text("Based on the length and complexity of the word, "
                     "you'll be given a finite number of chances [Press Enter]", " : ")
    wait()
    clear_screen()

    print_input_text("For every character you guess incorrectly, "
                     "you'll miss a chance [Press Enter]", " : ")
    wait()
    clear_screen()

    print_input_text("You lose when your chances get down to ZERO [Press Enter]", " : ")
    wait()
    clear_screen()

    print_input_text("You win if you guess the name with some chances "
                     "left on the board [Press Enter]", " : ")
    wait()
    clear_screen()


def get_genre(f_name):
    """Randomly choose a genre from available values"""
    return choice(list(open(os.path.join(SCRIPT_PATH, f_name)))).replace('\n', '')


def get_name(genre):
    """Randomly choose a genre for the user"""
    name = choice(list(open(os.path.join(SCRIPT_PATH, genre))))
    name = name.replace('\n', '')
    name = name.upper()
    return name


def get_coded_name(name, mask):
    """Mask characters of the word"""
    coded = re.sub(r'[a-zA-Z]', mask, name)
    coded = list(coded)
    return coded


def get_chances(name):
    """Get number of chances to be given
    to user as per the complexity of the word"""
    length = len(name)
    unique = len(set(name.replace(' ', '')))
    if unique < length / 2:
        chances = ceil(int(length / 2))
    else:
        chances = floor(int(length / 2))
    if chances < 4:
        return 4
    if chances > 11:
        return 11
    return chances


def guess(char_choice, chances):
    """Check if the given character is in the name,if chances permits.
    Returns chances_left, return_msg, guess_flag
    guess_flag is one of:
    e: if chance was unsuccessful
    s: if chance was successful
    """
    char_choice = char_choice.upper()
    guess_flag = 'e'

    if char_choice == '':
        return_msg = "Please give an Input"

    elif not char_choice.isalpha():
        return_msg = "You haven't given an english alphabet"

    elif len(char_choice) != 1:
        return_msg = "Length of the character should be 1"

    elif char_choice in GUESSED:
        return_msg = "You have already used {}".format(char_choice.upper())

    elif char_choice in NAME:
        return_msg = Fore.GREEN + Style.BRIGHT + "Congrats! {} is in the name" \
            .format(char_choice.upper()) + Style.RESET_ALL
        ind = [i for i, ltr in enumerate(NAME) if ltr == char_choice]
        for i in ind:
            CODED[i] = char_choice
        GUESSED.append(char_choice)
        guess_flag = 's'

    else:
        return_msg = "{} is not in the Name".format(char_choice.upper()) + Style.RESET_ALL
        GUESSED.append(char_choice)
        chances -= 1

    return chances, return_msg, guess_flag


def print_stats():
    """Print Stats for user, if he wants to see it,
    or compulsorily at the end of the game"""
    clear_screen()
    print_main_info("You played {} time(s)".format(PLAYED))
    print("You won " + Fore.LIGHTGREEN_EX + Style.BRIGHT +
          str(WON) + Style.RESET_ALL + " time(s)")
    print("You lost " + Fore.LIGHTRED_EX + Style.BRIGHT +
          str(LOSS) + Style.RESET_ALL + " time(s)")
    print_new_line()


def replay():
    """Ask user if he wants to play another round"""
    print_input_text("Press ENTER to PLAY AGAIN, T for TALLY, and N to see TALLY and EXIT", " : ")
    inp = input().upper()
    if inp == 'T':
        print_stats()
        print_input_text("Press ENTER to Continue", " : ")
        wait()
    return inp


def clear_screen():
    """Clear Screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_new_line():
    """Print a blank new line"""
    print("")


def print_main_info(msg, line_sep="\n"):
    """Print INFO text"""
    print(Fore.LIGHTCYAN_EX + Style.BRIGHT + msg + Style.RESET_ALL, end=line_sep)


def print_warning_info(msg, line_sep="\n"):
    """Print WARNING text"""
    print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT + msg + Style.RESET_ALL, end=line_sep)


def print_input_text(msg, line_sep="\n"):
    """Print text message for INPUT"""
    print(Fore.YELLOW + Style.BRIGHT + msg + Style.RESET_ALL, end=line_sep)


if __name__ == '__main__':

    clear_screen()

    GENRE_FILE = "Genres.txt"
    MASK = "_"
    PLAYED = WON = LOSS = 0
    CONT = 'Y'

    print_main_info("Welcome!! To a simple and exciting game of Hangman")
    print_new_line()

    print_input_text("Do you want to go over the instructions or just dive"
                     "in ?? [Y for instructions, N for passing it]", " : ")

    if input().upper() == 'Y':
        clear_screen()
        instructions()

    clear_screen()
    print_main_info("Let's BEGIN.... [Press Enter]", " : ")

    wait()
    clear_screen()

    while CONT in ('Y', 'T', ''):
        PLAYED += 1
        clear_screen()

        GENRE = get_genre(GENRE_FILE)
        FILE_NAME = GENRE + ".txt"

        NAME = get_name(FILE_NAME)

        CODED = get_coded_name(NAME, MASK)

        PREV_CHANCES = CHANCES = get_chances(NAME)

        GUESSED = []
        GUESSED_MSG = ''
        GUESSED_FLAG = 's'

        while CHANCES > 0:

            clear_screen()

            print("The Genre is " + Fore.LIGHTBLUE_EX + Style.BRIGHT +
                  GENRE.upper() + Style.RESET_ALL)

            print(*CODED)

            if CHANCES <= 2:
                print(Fore.RED + Style.BRIGHT + "CHANCES = {}"
                      .format(CHANCES) + Style.RESET_ALL)

            else:
                print("CHANCES = {}".format(CHANCES))

            if GUESSED_MSG and GUESSED_FLAG == 's':
                print(GUESSED_MSG)
            elif GUESSED_MSG:
                print_warning_info(GUESSED_MSG)

            PREV_CHANCES = CHANCES

            CHAR = input("Guess a character: ")
            CHANCES, GUESSED_MSG, GUESSED_FLAG = guess(CHAR, CHANCES)

            if ''.join(CODED) == NAME:
                print(*CODED)
                break

        if CHANCES == 0:
            clear_screen()
            LOSS += 1
            print(Fore.RED + Style.BRIGHT + "You LOSE :(" + Style.RESET_ALL)

        else:
            clear_screen()
            WON += 1
            print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "You WIN :)" + Style.RESET_ALL)

        print_main_info("The Correct Answer was", " :: ")
        print_warning_info(NAME)
        print_new_line()

        CONT = replay()

    print_main_info("Thanks for playing: ")
    print_stats()

    print_main_info(Fore.WHITE + Style.BRIGHT + "Press Enter to EXIT" + Style.RESET_ALL)
    wait()
