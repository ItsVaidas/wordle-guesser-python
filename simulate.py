from multiprocessing import Process, Manager
from collections import defaultdict
from math import log2
import matplotlib
from sympy.physics.control.control_plots import plt

matplotlib.interactive(True)
from matplotlib.figure import Figure

matplotlib.use('TkAgg')

current_stats = {}

def calculate_feedback(guess, solution):
    """Generate feedback for a guess compared to the solution (Wordle rules)."""
    feedback = ["w"] * 5  # Start with all incorrect ('w')

    # Track remaining letters in solution for handling 'y' feedback
    remaining_letters = list(solution)

    # Mark correct positions ('g')
    for i in range(5):
        if guess[i] == solution[i]:
            feedback[i] = "g"
            remaining_letters[i] = None  # Mark this position as resolved

    # Mark correct letters in incorrect positions ('y')
    for i in range(5):
        if feedback[i] == "w" and guess[i] in remaining_letters:
            feedback[i] = "y"
            remaining_letters[remaining_letters.index(guess[i])] = None  # Mark this letter as used

    return "".join(feedback)


def calculate_entropy(word, possible_words):
    """Calculate the entropy of a word based on its feedback groups."""
    feedback_groups = defaultdict(list)

    for solution in possible_words:
        feedback = calculate_feedback(word, solution)
        feedback_groups[feedback].append(solution)

    # Compute the entropy
    entropy = 0
    total_words = len(possible_words)
    for group in feedback_groups.values():
        probability = len(group) / total_words
        entropy -= probability * log2(probability)

    return entropy


def filter_possible_words(chosen_words, correct_positions, incorrect_positions, correct_letters, incorrect_letters, words):
    """Filter the list of possible words based on known constraints."""
    filtered_words = []

    last_word = chosen_words[-1]

    for word in words:
        word_is_possible = True

        # Check correct positions (green feedback)
        if len(correct_positions) > 0:
            last_word_correct_positions = correct_positions[-1]
            for position in last_word_correct_positions:
                if word[position] != last_word[position]:
                    word_is_possible = False
                    break

        # Check incorrect positions (yellow feedback)
        if len(incorrect_positions) > 0:
            for index, prev_word in enumerate(chosen_words):
                for position in incorrect_positions[index]:
                    if word[position] == prev_word[position]:
                        word_is_possible = False
                        break

        # Check correct letters (all green and yellow feedback)
        if len(correct_letters) > 0:
            last_word_correct_letters = correct_letters[-1]
            for letter in last_word_correct_letters:
                if word.count(letter) < last_word_correct_letters.count(letter):
                    word_is_possible = False
                    break

        # Check incorrect letters (gray feedback)
        if len(incorrect_letters) > 0:
            all_incorrect_letters = set(letter for sublist in incorrect_letters for letter in sublist)
            for letter in all_incorrect_letters:
                if word.count(letter) > 0 and letter not in last_word_correct_letters:
                    word_is_possible = False
                    break
                elif word.count(letter) > 0 and letter in last_word_correct_letters:
                    if word.count(letter) != last_word_correct_letters.count(letter):
                        word_is_possible = False

        if word_is_possible:
            filtered_words.append(word)

    return filtered_words


def choose_next_word(chosen_words, correct_positions, incorrect_positions, correct_letters, incorrect_letters, words):
    """Choose the next best word using entropy-based scoring and constraints."""
    possible_words = filter_possible_words(
        chosen_words, correct_positions, incorrect_positions, correct_letters, incorrect_letters, words
    )

    if not possible_words:
        raise ValueError("No possible words left!")

    best_word = max(possible_words, key=lambda word: calculate_entropy(word, possible_words))
    return best_word, possible_words

def simulate(initial_word, words, current_stats):
    count = 0
    average_guesses = 0.0
    guessed_frequency = {}

    for simulate_word in words:  # Limit to 100 words for testing
        simulate_word = simulate_word.strip()

        possible_words = words.copy()
        chosen_words = []
        correct_positions = []
        incorrect_positions = []
        correct_letters = []
        incorrect_letters = []

        word = initial_word  # First guess, can be adjusted

        for i in range(12):
            if word == simulate_word:
                average_guesses += i + 1
                count += 1
                guessed_frequency[i + 1] = guessed_frequency.get(i + 1, 0) + 1
                break

            chosen_words.append(word)
            correct_positions.append([pos for pos in range(5) if simulate_word[pos] == word[pos]])
            incorrect_positions.append([pos for pos in range(5) if simulate_word[pos] != word[pos]])

            # Update correct/incorrect letters
            tmp_simulate_word = simulate_word
            current_correct_letters = []
            current_incorrect_letters = []
            for letter in word:
                if tmp_simulate_word.count(letter) > 0:
                    current_correct_letters.append(letter)
                    tmp_simulate_word = tmp_simulate_word.replace(letter, "", 1)
                else:
                    current_incorrect_letters.append(letter)

            correct_letters.append(current_correct_letters)
            incorrect_letters.append(current_incorrect_letters)

            try:
                word, possible_words = choose_next_word(
                    chosen_words, correct_positions, incorrect_positions, correct_letters, incorrect_letters, possible_words
                )
            except ValueError:
                print(f"Simulation failed for word: {simulate_word}")
                break

        current_stats[initial_word] = round(average_guesses / count, 2)

    return round(average_guesses / count, 2)

# Function to calculate feedback and entropy remains the same

def show_stats(current_stats):
    while True:
        plt.clf()

        sorted_stats = sorted(current_stats.items(), key=lambda x: x[1])[:10]
        www, scores = zip(*sorted_stats) if sorted_stats else ([], [])

        plt.bar(www, scores)

        for i in range(len(www)):
            plt.text(i, scores[i], scores[i], ha='center', va='bottom')

        plt.pause(2)  # Make this as low as possible
        plt.gcf().canvas.flush_events()  # Force GUI to update


if __name__ == "__main__":
    with Manager() as manager:
        current_stats = manager.dict()

        with open("la-words.txt", "r") as file:
            words = [line.strip() for line in file.readlines()]


            show_stats_process = Process(target=show_stats, args=(current_stats,))
            show_stats_process.start()


            print("Starting simulation")
            threads = []

            for initial_word in words[:5]:
                threads.append(Process(target=simulate, args=(initial_word, words, current_stats)))

            current_threads = []
            i = 0

            while i < len(threads):
                if len(current_threads) < 10:
                    threads[i].start()
                    current_threads.append(threads[i])
                    i += 1
                else:
                    for t in current_threads:
                        t.join()
                    current_threads = []

            for t in current_threads:
                t.join()

            print("Simulation ended")

            best = min(current_stats, key=current_stats.get)

            print(f"\nBest word: {best}")
            print(f"Best score: {current_stats[best]}")