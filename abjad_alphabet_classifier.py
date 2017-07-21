import numpy as np
import math


def normalize(l):
    dot = 0
    for i in range(len(l)):
        dot += l[i]**2
    length = math.sqrt(dot)
    return [0 if length == 0 else num/length for num in l]


def isNaN(num):
    return num != num


def KL_based_method(weighted_A, letters, v, c):
    total, delta = 0.0, 0.0
    num_contexts = len(weighted_A[0])

    for i in range(len(letters)):
        if letters[i] not in v:
            continue
        let_i = np.asarray(normalize([delta if isNaN(num) else num+delta for num in weighted_A[i]]), dtype=np.float)
        for j in range(len(letters)):
            if sum(weighted_A[j]) == 0:
                continue
            let_j = np.asarray(normalize([delta if isNaN(num) else num+delta for num in weighted_A[j]]), dtype=np.float)
            if letters[j] in v and i != j:
                for index in range(num_contexts):
                    if let_i[index] != 0 and let_j[index] != 0:
                        total += abs(let_i[index] * np.log(let_i[index] / let_j[index]))
            elif letters[j] in c and i != j:
                for index in range(num_contexts):
                    if let_i[index] != 0 and let_j[index] != 0:
                        total -= abs(let_i[index] * np.log(let_i[index] / let_j[index]))

    print("\nKL-based method of abjad and alphabet classification result: " + str(total) +
          "\nNote that results for the KL-based method must be compared across corpora with approximately "
          "the same number of words.")


def count_method(corpus, putative_vowels, putative_consonants):
    '''Calculating percentage of words in the corpus without
    putative vowels and percetage of words without putative
    consonants'''

    num_words = 0
    num_words_without_putative_vowels = 0
    num_words_without_putative_consonants = 0
    count = 0
    while 1:
        input_line = corpus.readline()
        if not input_line or count > 5000:
            break
        line = input_line.split(' ')
        for word in line:
            count += 1
            if count > 5000:
                break
            num_words += 1
            if word == '':
                continue
            word = set(list(word))
            #print(word,putative_vowels,putative_consonants)
            intersection_vowels = len(word.intersection(putative_vowels))
            intersection_consonants = len(word.intersection(putative_consonants))
            if intersection_vowels == 0 and intersection_consonants == 0:
                num_words -= 1
                continue
            if intersection_vowels == 0:
                num_words_without_putative_vowels += 1
            if intersection_consonants == 0:
                num_words_without_putative_consonants += 1
    print("\nCount method: the percentage of words without putative vowels is " +
          str(float(num_words_without_putative_vowels)/float(num_words)) +
          " and the percentage of words without putative consonants is " +
          str(float(num_words_without_putative_consonants) / float(num_words)))


