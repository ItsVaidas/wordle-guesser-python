import random

def random_word(words):
    words_with_unique_letters = []

    for word in words:
        word = word.strip()
        unique_letters = set(word)
        words_with_unique_letters.append((word, len(unique_letters)))

    words_with_unique_letters.sort(key=lambda x: x[1], reverse=True)
    words_with_unique_letters = [word for word, _ in words_with_unique_letters if _ == 5]

    return random.choice(words_with_unique_letters)

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
    return random.choice(possible_words)

simulate = True

if __name__ == "__main__":

    file = open("la-words.txt", "r")
    words = file.readlines()

    if simulate:
        count = 0
        average_guesses = 0.0
        guessed_frequency = {}

        for simulate_word in words:
            simulate_word = simulate_word.strip()

            chosen_words = []
            correct_positions = []
            incorrect_positions = []
            correct_letters = []
            incorrect_letters = []
            
            word = random_word(words)

            for i in range(12):
                chosen_words.append(word)

                correct_positions.append([position for position in range(5) if simulate_word[position] == word[position]])

                incorrect_positions.append([position for position in range(5) if simulate_word[position] != word[position]])

                correct_letters.append([letter for letter in word if simulate_word.count(letter) > 0])

                incorrect_letters.append([letter for letter in word if simulate_word.count(letter) == 0])

                word = choose_next_word(chosen_words, correct_positions, incorrect_positions, correct_letters, incorrect_letters, words)

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

        word = random_word(words)

        for i in range(12):
            chosen_words.append(word)

            print(word)

            input_correct_positions = input("Enter the number of correct positions by comma: ")
            if input_correct_positions != "":
                correct_positions.append(input_correct_positions.split(","))
            else:
                correct_positions.append([])

            input_incorrect_positions = input("Enter the number of incorrect positions by comma: ")
            if input_incorrect_positions != "":
                incorrect_positions.append(input_incorrect_positions.split(","))
            else:
                incorrect_positions.append([])

            input_correct_letters = input("Enter the number of correct letters by comma: ")
            if input_correct_letters != "":
                correct_letters.append(input_correct_letters.split(","))

            input_incorrect_letters = input("Enter the number of incorrect letters by comma: ")
            if input_incorrect_letters != "":
                incorrect_letters.append(input_incorrect_letters.split(","))

            word = choose_next_word(chosen_words, correct_positions, incorrect_positions, correct_letters, incorrect_letters, words)

    