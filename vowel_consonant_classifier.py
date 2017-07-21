import numpy as np
import scipy.linalg as sla
import matplotlib.pyplot as plt


def clean(text):
    text = text.strip('\ufeff')
    text = text.strip('\u201c')
    text = text.strip('\u201d')
    text = text.strip('\u2018')
    text = text.strip('\u2019')
    text = text.strip('\u2014')
    text = text.rstrip()
    return text


def calculate_letter_frequencies(letters, tokens, total_num_letters):
    frequencies = []
    for index in range(len(letters)):
        frequencies.append(tokens[index] / total_num_letters)
    return frequencies


def calculate_pframe_statistics(corpus, letters):
    count, total_num_letters = 0, 0
    contexts_per_letter = [[] for i in range(len(letters))]
    num_frames_per_letter = [0 for i in range(len(letters))]
    frames_keys, frames_values = [], []
    num_tokens = [0 for x in range(len(letters))]

    while 1:
        input_line = corpus.readline()
        if not input_line or count > 5000:
            break
        line = input_line.split(' ')
        for word in line:
            count += 1
            if count > 5000:
                break
            word = list(clean(word))
            for index in range(0, len(word)):
                letter = clean(word[index])
                if letter in letters:
                    num_tokens[letters.index(letter)] += 1
                    total_num_letters += 1
                    frame = ""
                    if index == 0:
                        frame += "_*"
                    else:
                        char = clean(word[index-1])
                        if char in letters:
                            frame += char
                            frame += "*"
                        else:
                            continue
                    if index >= len(word)-1:
                        frame += "_"
                    else:
                        char = clean(word[index+1])
                        if char in letters:
                            frame += char
                        else:
                            continue
                    if frame not in frames_keys:
                        frames_keys.append(frame)
                        frames_values.append([letter])
                        num_frames_per_letter[letters.index(letter)] += 1
                    else:   # elif letter not in frames_values[frames_keys.index(frame)]:
                            # add elif if want to count repetitions
                        frames_values[frames_keys.index(frame)].append(letter)
                        num_frames_per_letter[letters.index(letter)] += 1
                    if frame not in contexts_per_letter[letters.index(letter)]:
                        contexts_per_letter[letters.index(letter)].append(frame)

    frequencies = calculate_letter_frequencies(letters, num_tokens, total_num_letters)
    print("\n\n____\n\nCOUNT IS " + str(count) + "\n\n____\n\n")
    return frames_keys, frames_values, frequencies, num_tokens


def calculate_matrix_A(letters, frames_keys, frames_values):
    A = [[0 for x in range(0, len(frames_keys))] for x in range(0, len(letters))]
    weighted_A = [[0 for x in range(0, len(frames_keys))] for x in range(0, len(letters))]
    num_contexts = [0 for x in range(0, len(letters))]

    for key in frames_keys:
        frame_index = frames_keys.index(key)
        for value in frames_values[frame_index]:
            for letter in value:
                letter_index = letters.index(letter)
                A[letter_index][frame_index] = 1  # +=1 if want to count repetitions
                weighted_A[letter_index][frame_index] += 1
                num_contexts[letter_index] += 1
    return A, weighted_A


def plot(vector1, vector2, letters):
    plt.scatter(vector1, vector2)
    plt.rc('font', **{'sans-serif': 'Arial',
                             'family': 'sans-serif'})
    for i, txt in enumerate(letters):
        plt.annotate(txt, (vector1[i], vector2[i]))
    plt.axhline(0, color='r')
    plt.show()


def classify(vector2, letters, most_frequent_letter):
    putative_vowels, putative_consonants = [], []
    if vector2[letters.index(most_frequent_letter)] > 0:
        for i in range(len(vector2)):
            if vector2[i] > 0:
                putative_vowels.append(letters[i])
            elif vector2[i]:
                putative_consonants.append(letters[i])
    else:
        for i in range(len(vector2)):
            if vector2[i] > 0:
                putative_consonants.append(letters[i])
            else:
                putative_vowels.append(letters[i])
    return putative_vowels, putative_consonants


def svd_method(corpus, letters):
    frames_keys, frames_values, frequencies, num_tokens = calculate_pframe_statistics(corpus, letters)
    most_frequent_letter = letters[frequencies.index(max(frequencies))]
    A, weighted_A = calculate_matrix_A(letters, frames_keys, frames_values)
    A = np.matrix(A).T
    U, s, V = sla.svd(A, full_matrices=True)
    vector1 = V[0]
    vector2 = V[1]
    if vector2[letters.index(most_frequent_letter)] < 0:
        vector2 = [-value for value in vector2]
    plot(vector1, vector2, letters)
    putative_vowels, putative_consonants = classify(vector2, letters, most_frequent_letter)
    return weighted_A, putative_vowels, putative_consonants, num_tokens
