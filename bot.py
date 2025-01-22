import random


def calculate_letter_frequencies(words):
    """Calculate the frequency of letters in the given list of words."""
    letters_frequencies = {}
    for word in words:
        for letter in word:
            letters_frequencies[letter] = letters_frequencies.get(letter, 0) + 1

    # Normalize the frequencies for scoring
    for letter in letters_frequencies:
        letters_frequencies[letter] = round(letters_frequencies[letter] / len(words) * 10)
    return letters_frequencies


def get_best_word(words, letters_frequencies, used_letters):
    """Get the best word based on letter frequencies and unused letters."""
    possible_words = []
    for word in words:
        score = 0
        unique_letters = set(word)
        for letter in unique_letters:
            score += letters_frequencies.get(letter, 0)
            if letter in used_letters:
                score -= 1  # Penalize reusing guessed letters
        possible_words.append([word, score])

    possible_words = sorted(possible_words, key=lambda x: x[1], reverse=True)
    best_score = possible_words[0][1]
    return random.choice([word[0] for word in possible_words if word[1] == best_score])


def choose_next_word(chosen_words, correct_positions, incorrect_positions, correct_letters, incorrect_letters, words, letters_frequencies):
    """Choose the next best word based on feedback."""
    possible_words = []
    used_letters = set("".join(chosen_words))

    last_word = chosen_words[-1]

    for word in words:
        word = word.strip()
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

        if word_is_possible:
            possible_words.append(word)

    if not possible_words:
        raise ValueError("No possible words found!")

    return [get_best_word(possible_words, letters_frequencies, used_letters), possible_words]


if __name__ == "__main__":
    with open("la-words.txt", "r") as file:
        words = [line.strip() for line in file.readlines()]

    letters_frequencies = calculate_letter_frequencies(words)
    simulate = input("Do you want to simulate the game? (y/n): ")

    if simulate == "y":
        count = 0
        average_guesses = 0.0
        guessed_frequency = {}

        for simulate_word in words:  # Limit for testing
            simulate_word = simulate_word.strip()

            possible_words = words.copy()
            chosen_words = []
            correct_positions = []
            incorrect_positions = []
            correct_letters = []
            incorrect_letters = []

            word = "crane"  # First guess, can be adjusted

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
                        chosen_words, correct_positions, incorrect_positions, correct_letters, incorrect_letters, possible_words, letters_frequencies
                    )
                except ValueError:
                    print(f"Simulation failed for word: {simulate_word}")
                    break

            guessed_frequency = dict(sorted(guessed_frequency.items()))
            print("Average guesses: ", average_guesses / count, "\r", end="")
            print("Guessed frequency: ", guessed_frequency, "\r", end="")

        print("\nAverage guesses: ", average_guesses / count)
        print("Guessed frequency: ", guessed_frequency)

    else:
        chosen_words = []
        correct_positions = []
        incorrect_positions = []
        correct_letters = []
        incorrect_letters = []
        possible_words = words.copy()
        word = "crane"  # First guess

        print("When asked to enter shown result, please use the following key:")
        print("w: Incorrect letter")
        print("g: Correct letter in correct position")
        print("y: Correct letter in incorrect position")
        print("Example: wgywg")

        for i in range(12):
            chosen_words.append(word)

            if len(possible_words) < 10:
                print("Possible words:", possible_words)

            print("Please write the word: ", word)
            input_sequence = input("Enter shown result:\n")

            if input_sequence == "ggggg":
                print(f"Congratulations! I guessed the word in {i + 1} guesses.")
                break

            current_correct_letters = []
            current_correct_positions = []
            current_incorrect_positions = []
            current_incorrect_letters = []

            for index, letter in enumerate(input_sequence):
                if letter == "w":
                    current_incorrect_letters.append(word[index])
                elif letter == "g":
                    current_correct_positions.append(index)
                    current_correct_letters.append(word[index])
                elif letter == "y":
                    current_incorrect_positions.append(index)
                    current_correct_letters.append(word[index])
                else:
                    print("Invalid input")

            correct_positions.append(current_correct_positions)
            incorrect_positions.append(current_incorrect_positions)
            correct_letters.append(current_correct_letters)
            incorrect_letters.append(current_incorrect_letters)

            try:
                word, possible_words = choose_next_word(
                    chosen_words, correct_positions, incorrect_positions, correct_letters, incorrect_letters, possible_words, letters_frequencies
                )
            except ValueError:
                print("I'm sorry, I couldn't find any possible words.")
                break
