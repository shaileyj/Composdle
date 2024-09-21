import random
import musicalbeeps

player = musicalbeeps.Player(volume=0.2, mute_output=True)

# makes it easier to use colored text
ESC = '\x1b'
YELLOW = ESC + '[30m' + ESC + '[43m'
GREEN = ESC + '[30m' + ESC + '[42m'
BLACK = ESC + '[30m' + ESC + '[47m'
NOTHING = ESC + '[39m' + ESC + '[49m'


# sorts the words by length
def generate_melody(length, possible_notes):
    melody = ""
    for i in range(length):
        melody += possible_notes[random.randrange(0, len(possible_notes))]
    return melody


def play_musicle(length, possible_notes):
    answer = generate_melody(length, possible_notes)
    colors = [BLACK]*length
    num_guesses = 0
    guess = ''

    # makes dictionary where each digit of the answer is the key
    # and the amount of times it appears is the term
    answer_chs = dict()
    for letter in answer:
        if letter not in answer_chs:
            answer_chs[letter] = 1
        else:
            answer_chs[letter] += 1

    while guess != answer and num_guesses < 15:
        guess = input("Enter a guess: ").upper()
        check = True
        for note in guess:
            if note not in possible_notes:
                check = False
        if len(guess) == length and check:
            # plays guessed melody
            for index in range(len(guess)):
                if index == "#" or index == "b":
                    continue
                elif index != len(guess)-1 and (guess[index + 1] == "#" or guess[index + 1] == "b"):
                    played_note = guess[index] + "4" + guess[index + 1]
                else:
                    played_note = guess[index] + "4"
                player.play_note(played_note, 0.5)
            player.play_note("pause", 0.5)

            # finds green + creates a new string with non-red
            # digits for both the guess and the answer
            curr_answer_chs = answer_chs.copy()
            for index, letter in enumerate(guess):
                if letter == answer[index]:
                    colors[index] = GREEN
                    curr_answer_chs[letter] -= 1
                elif letter in answer and curr_answer_chs[letter] > 0:
                    colors[index] = YELLOW
                    curr_answer_chs[letter] -= 1
                else:
                    colors[index] = BLACK
            string = ''
            for i in range(length):
                string += colors[i]
                string += guess[i]
            print(string, NOTHING)
            num_guesses += 1

        elif len(guess) != length:
            print(NOTHING, "please enter a word of length ", length)
        else:
            print(NOTHING, "please use ")

    if guess == answer:
        print("Correct! The answer was", answer)
        return True
    else:
        print("Oh no. The answer was", answer)
        return False


c_major_scale = ["C", "D", "E", "F", "G", "A", "B"]
play_musicle(5, c_major_scale)
