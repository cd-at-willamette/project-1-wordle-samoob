########################################
# Name: Sivana
# Collaborators (if any):
# GenAI Transcript (if any):
# Estimated time spent (hr): 3 days 
# Description of any added extensions: Create the balanced dictionary and animate win 
########################################
from WordleGraphics import *  # WordleGWindow, N_ROWS, N_COLS, CORRECT_COLOR, PRESENT_COLOR, MISSING_COLOR, UNKNOWN_COLOR
import random
import time
import threading
from collections import defaultdict


ENGLISH_WORDS = [
    "diddy", "slurp", "yeast", "brian", "sassy", "zesty",
    "blade", "kushi", "zabba", "freak", "brent", "slurp",
    "whiff", "yakub", "cushi", "erwin", "proof", "ahmed",
    "hamsa", "glock", "motek", "kanye", "chaim", "allah",
    "zamnn", "skull", "texas", "zaddy", "brazy", "jazzi",
    "crunk", "canva"  "apple", "brick", "chair", "dance", "eagle", "flame", "globe", "heart", 
    "input", "jelly", "knife", "lemon", "mouse", "nurse", "ocean", "piano", 
    "queen", "radio", "spice", "train", "uncle", "vivid", "water", "xenon", 
    "yacht", "zebra", "climb", "drive", "froze", "grape"
]

def create_balanced_dictionary(words):
    position_freq = defaultdict(lambda: defaultdict(int))

    for word in words:
        if len(word) == 5:
            for index, letter in enumerate(word):
                position_freq[index][letter] += 1

    balanced_words = []
    selected_letters = [set() for _ in range(5)]

    for word in words:
        if len(word) == 5:
            can_add = True
            for index, letter in enumerate(word):
                if letter in selected_letters[index]:
                    can_add = False
                    break
            if can_add:
                balanced_words.append(word)
                for index, letter in enumerate(word):
                    selected_letters[index].add(letter)

    return balanced_words

def get_random_word(balanced_words):
    return random.choice(balanced_words)

def is_english_word(word):
    return word in ENGLISH_WORDS

def wordle():
    gw = WordleGWindow()

    # Create the balanced dictionary
    balanced_dictionary = create_balanced_dictionary(ENGLISH_WORDS)
    secret_word = get_random_word(balanced_dictionary)

    def animate_win(): # animate win extension 
        current_row = gw.get_current_row()

        def run_animation():
            for col in range(N_COLS):
                for color in ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00", "#0000FF", "#4B0082", "#9400D3"]:
                    gw.set_square_color(current_row, col, color)
                    time.sleep(0.1)
            for col in range(N_COLS):
                gw.set_square_color(current_row, col, CORRECT_COLOR)

        threading.Thread(target=run_animation).start()

    def enter_action():
        current_row = gw.get_current_row()
        guess_word = ''.join([gw.get_square_letter(current_row, col) for col in range(N_COLS)]).lower()

        print(f"User guess: {guess_word}")  # Debugging statement

        if not is_english_word(guess_word):
            print(f"Guess '{guess_word}' is not in the word list.")  # Debugging output
            gw.show_message("Not in word list")
            return

        secret_word_list = list(secret_word)
        used_indices = set()
        correct_guess = True

        # Color correct letters (green)
        for col in range(len(guess_word)):
            if guess_word[col] == secret_word[col]:
                gw.set_square_color(current_row, col, CORRECT_COLOR)
                used_indices.add(col)
                secret_word_list[col] = None
            else:
                correct_guess = False

        # Color present letters (yellow)
        for col in range(len(guess_word)):
            if guess_word[col] != secret_word[col] and guess_word[col] in secret_word_list:
                for i in range(len(secret_word_list)):
                    if secret_word_list[i] == guess_word[col] and i not in used_indices:
                        gw.set_square_color(current_row, col, PRESENT_COLOR)
                        used_indices.add(i)
                        secret_word_list[i] = None  # Mark this letter as used
                        break

        # Check for win condition
        if correct_guess:
            gw.show_message("You win!")
            animate_win()
            gw.set_current_row(N_ROWS)

        # Check for loss condition
        if current_row == N_ROWS - 1:
            gw.show_message(f"You lose! The word was: {secret_word}")
            gw.set_current_row(N_ROWS)
        else:
            gw.set_current_row(current_row + 1)  # Move to next row

    gw.add_enter_listener(enter_action)

if __name__ == "__main__":
    wordle()




