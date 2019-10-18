"""A simple Hangman Game"""
from math import floor
from math import ceil
import os
from random import choice
import re
from colorama import Fore, Style


def wait():
    """Wait for user input"""
    try:
        input()
    except KeyboardInterrupt:
        pass


def instructions():
    """Print Initial Instructions for the user"""
    print("Let's go over the rules first!! Press Enter to continue...")
    wait()
    clear_screen()

    print("You'll be given a name... [Press Enter]")
    wait()
    clear_screen()

    print("You have to guess the name by guessing the "
          "characters in the name, one by one... [Press Enter]")
    wait()
    clear_screen()

    print("Based on the length and complexity of the name, "
          "you'll be given a finite number of chances [Press Enter]")
    wait()
    clear_screen()

    print("For every character you guess incorrectly, "
          "you'll miss a chance [Press Enter]")
    wait()
    clear_screen()

    print("You lose when your chances get down to ZERO [Press Enter]")
    wait()
    clear_screen()

    print("You win if you guess the name with some chances "
          "left on the board [Press Enter]")
    wait()
    clear_screen()


def get_genre(f_name):
    """Randomly choose a genre from available values"""
    return choice(list(open(f_name))).replace('\n', '')


def get_name(genre):
    """Randomly choose a genre for the user"""
    name = choice(list(open(genre)))
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


def guess(ch, chances):
    """Check if the given character is in the name,if chances permits.
    Returns chances_left, return_msg, guess_flag
    guess_flag is one of:
    e: if chance was unsuccessful
    s: if chance was successful
    """
    ch = ch.upper()
    guess_flag = 'e'
    if ch == '':
        return_msg = "Please give an Input"
    elif not ch.isalpha():
        return_msg = "You haven't given an english alphabet"
    elif len(ch) != 1:
        return_msg = "Length of the character should be 1"
    elif ch in GUESSED:
        return_msg = "You have already used {}".format(ch.upper())
    elif ch in NAME:
        return_msg = Fore.GREEN + Style.BRIGHT + "Congrats! {} is in the name".format(ch.upper()) + Style.RESET_ALL
        ind = [i for i, ltr in enumerate(NAME) if ltr == ch]
        for i in ind:
            CODED[i] = ch
        GUESSED.append(ch)
        guess_flag = 's'
    else:
        return_msg = "{} is not in the Name".format(ch.upper()) + Style.RESET_ALL
        GUESSED.append(ch)
        chances -= 1
    return chances, return_msg, guess_flag


def stats():
    """Print Stats for user, if he wants to see it,
    or compulsorily at the end of the game"""
    print("-" * 15)
    print("You have played {} times".format(PLAYED))
    print("You have won " + Fore.GREEN + str(WON) + Style.RESET_ALL + " times")
    print("You have lost " + Fore.RED + str(LOSS) + Style.RESET_ALL + " times")
    print_new_line()


def replay():
    """Ask user if he wants to play another round"""
    print("Press T and ENTER for your tally for this game or Y to play again")
    inp = input().upper()
    if inp == 'T':
        stats()
        print("Press Enter to Continue")
        wait()
    return inp


def clear_screen():
    """Clear Screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_new_line():
    """Print a blank new line"""
    print("")


def print_main_info(msg, end="\n"):
    """Print INFO text"""
    print(Fore.LIGHTCYAN_EX + Style.BRIGHT + msg + Style.RESET_ALL)


def print_warning_info(msg, end="\n"):
    """Print WARNING text"""
    print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT + msg + Style.RESET_ALL)


if __name__ == '__main__':

    GENRE_FILE = "Genres.txt"

    clear_screen()

    print_main_info("Welcome!! To a simple and exciting game of Hangman")
    print_new_line()

    print_main_info("Do you want to go over the instructions or just dive"
                    "in ?? [Y for instructions, N for passing it ]")

    if input().upper() == 'Y':
        clear_screen()
        instructions()

    clear_screen()

    print_main_info("Let's BEGIN.... [Press Enter]")

    wait()
    clear_screen()

    MASK = "_"

    PLAYED = WON = LOSS = 0

    CONT = 'Y'

    while CONT in ('Y', 'T', ''):
        PLAYED += 1
        clear_screen()

        GENRE = get_genre(GENRE_FILE)
        F_NAME = GENRE + ".txt"

        NAME = get_name(F_NAME)

        CODED = get_coded_name(NAME, MASK)
        PREV_CHANCES = CHANCES = get_chances(NAME)

        GUESSED = []

        guessed_msg = ''
        guessed_flag = 's'

        while CHANCES > 0:

            clear_screen()

            print("The Genre is " + Fore.LIGHTGREEN_EX + Style.BRIGHT +
                  GENRE.upper() + Style.RESET_ALL)

            print(*CODED)

            if CHANCES <= 2:
                print(Fore.RED + Style.BRIGHT + "CHANCES = "
                                                "{}".format(CHANCES) + Style.RESET_ALL)

            else:
                print("CHANCES = {}".format(CHANCES))

            if guessed_msg and guessed_flag == 's':
                print(guessed_msg)
            elif guessed_msg:
                print_warning_info(guessed_msg)

            PREV_CHANCES = CHANCES

            CHAR = input("Guess a character: ")
            CHANCES, guessed_msg, guessed_flag = guess(CHAR, CHANCES)

            if ''.join(CODED) == NAME:
                print(*CODED)
                break

        if CHANCES == 0:
            clear_screen()
            LOSS += 1
            print(Fore.RED + Style.BRIGHT + "You LOSE :( " + Style.RESET_ALL)
            print(Fore.GREEN + Style.BRIGHT + "The Correct Name was "
                                              ":: {}".format(NAME) + Style.RESET_ALL)
            print_new_line()

        else:
            clear_screen()
            WON += 1
            print(Fore.GREEN + Style.BRIGHT + "You WIN" + Style.RESET_ALL)
            print_new_line()

        CONT = replay()

    print_main_info("Thanks for playing: ")
    stats()

    print_main_info(Fore.WHITE + Style.BRIGHT + "Press Enter to EXIT" + Style.RESET_ALL)
    wait()
