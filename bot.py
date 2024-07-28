import random

def choose_next_word(chosen_words, correct_positions, incorrect_positions, correct_letters, incorrect_letters, words):
    possible_words = []

    for word in words:
        word = word.strip()

        last_word = chosen_words[-1]

        word_is_possible = True

        if len(correct_positions) > 0:
            last_word_correct_positions = correct_positions[-1]

            for position in last_word_correct_positions:
                if word[int(position)] != last_word[int(position)]:
                    word_is_possible = False
                    break
        
        if len(incorrect_positions) > 0:
            for index, i_word in enumerate(chosen_words):
                for position in incorrect_positions[index]:
                    if word[int(position)] == i_word[int(position)]:
                        word_is_possible = False
                        break

        
        if len(correct_letters) > 0:
            last_word_correct_letters = correct_letters[-1]

            for letter in last_word_correct_letters:
                if word.count(letter) == 0:
                    word_is_possible = False
                    break
        
        if len(incorrect_letters) > 0:
            for letters in incorrect_letters:
                for letter in letters:
                    if word.count(letter) > 0:
                        word_is_possible = False
                        break

        if word_is_possible:
            possible_words.append(word)
    
    # print("Possible words:", possible_words)
    return [random.choice(possible_words), possible_words]

if __name__ == "__main__":

    file = open("la-words.txt", "r")
    words = file.readlines()

    simulate = input("Do you want to simulate the game? (y/n): ")

    if simulate == "y":
        count = 0
        average_guesses = 0.0
        guessed_frequency = {}

        for simulate_word in words:
            simulate_word = simulate_word.strip()

            possible_words = words.copy()

            chosen_words = []
            correct_positions = []
            incorrect_positions = []
            correct_letters = []
            incorrect_letters = []
            
            word = "crane"

            for i in range(12):
                chosen_words.append(word)

                correct_positions.append([position for position in range(5) if simulate_word[position] == word[position]])

                incorrect_positions.append([position for position in range(5) if simulate_word[position] != word[position]])

                correct_letters.append([letter for letter in word if simulate_word.count(letter) > 0])

                incorrect_letters.append([letter for letter in word if simulate_word.count(letter) == 0])

                [word, possible_words] = choose_next_word(chosen_words, correct_positions, incorrect_positions, correct_letters, incorrect_letters, possible_words)

                if word == simulate_word:
                    average_guesses += i + 1
                    count += 1
                    guessed_frequency[i + 1] = guessed_frequency.get(i + 1, 0) + 1
                    break
            
            guessed_frequency = dict(sorted(guessed_frequency.items()))

            print("Average guesses: ", average_guesses / count, "\r", end="")
            print("Guessed frequency: ", guessed_frequency, "\r", end="")
    
        print("Average guesses: ", average_guesses / count)
        print("Guessed frequency: ", guessed_frequency)

    else:
        chosen_words = []
        correct_positions = []
        incorrect_positions = []
        correct_letters = []
        incorrect_letters = []

        possible_words = words.copy()

        word = "crane"

        print("When asked to enter shown result, please use the following key:")
        print("w: Incorrect letter")
        print("g: Correct letter in correct position")
        print("y: Correct letter in incorrect position")
        print("Example: wgywg")
        print("This means that the first letter is incorrect, the second and fourth letters are correct and in the correct position, and the third and fifth letters are correct but in the wrong position.")

        for i in range(12):
            chosen_words.append(word)

            if len(possible_words) < 10:
                print("Possible words:", possible_words)

            print("Please write the word: ", word)

            input_sequence = input("Enter shown result:\n")

            if (input_sequence == "ggggg"):
                print("Congratulations! I guessed the word in", i + 1, "guesses.")
                break

            current_correct_letters = []
            current_correct_positions = []
            current_incorrect_positions = []
            current_incorrect_letters = []
            for (index, letter) in enumerate(input_sequence):
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

            [word, possible_words] = choose_next_word(chosen_words, correct_positions, incorrect_positions, correct_letters, incorrect_letters, possible_words)

    