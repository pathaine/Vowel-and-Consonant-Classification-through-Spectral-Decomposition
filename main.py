from vowel_consonant_classifier import svd_method
from abjad_alphabet_classifier import KL_based_method, count_method
from sukhotin import sukhotins_method
from preprocess import preprocess


def calculate_precision_recall_accuracy(correct_vowels, correct_consonants, putative_vowels, putative_consonants):
    tp = len(set(correct_vowels).intersection(set(putative_vowels)))  # true positive
    fp = len(set(correct_consonants).intersection(set(putative_vowels)))  # false positive
    fn = len(set(correct_vowels).intersection(set(putative_consonants)))  # false negative
    tn = len(set(correct_consonants).intersection(set(putative_consonants)))  # true negative
    if (tp + fp) == 0 or (tp + fn) == 0:
        return
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    accuracy = (tp + tn) / (tp + tn + fp + fn)

    print("putative vowels: " + str(putative_vowels) + "\nputative consonants: " + str(putative_consonants) +
          "\nPRECISION: " + str(precision) + "\nRECALL: " + str(recall) + "\nACCURACY: " + str(accuracy) + "\n")


def calculate_token_precision_recall_accuracy(correct_vowels, correct_consonants, putative_vowels,
                                              putative_consonants, num_tokens, all_letters):
    tp, fp, fn, tn = 0, 0, 0, 0

    tp_set = set(correct_vowels).intersection(set(putative_vowels))
    fp_set = set(correct_consonants).intersection(set(putative_vowels))
    fn_set = set(correct_vowels).intersection(set(putative_consonants))
    tn_set = set(correct_consonants).intersection(set(putative_consonants))

    for k in range(len(num_tokens)):
        if all_letters[k] in tp_set:
            tp += num_tokens[k]
        elif all_letters[k] in fp_set:
            fp += num_tokens[k]
        elif all_letters[k] in fn_set:
            fn += num_tokens[k]
        elif all_letters[k] in tn_set:
            tn += num_tokens[k]

    if (tp + fp) == 0 or (tp + fn) == 0:
        return

    precision = tp/(tp+fp)
    recall = tp/(tp+fn)
    accuracy = (tp + tn)/(tp + tn + fp + fn)
    #f1_measure = 2*(precision*recall)/(precision + recall)
    print("putative vowels: " + str(putative_vowels) + "\nputative consonants: " + str(putative_consonants) + \
          "\nTOKEN PRECISION: " + str(precision) + "\nTOKEN RECALL: " + str(recall) + \
          "\nTOKEN ACCURACY: " + str(accuracy) + "\n")

if __name__ == "__main__":
    """ SAMPLE TEXT SOURCES:
    ENGLISH - http://www.gutenberg.org/files/11/11-h/11-h.htm
    FRENCH  - http://www.gutenberg.org/cache/epub/4650/pg4650.html
    GREEK   - http://www.gutenberg.org/files/39536/39536-h/39536-h.htm
    ARABIC  - http://www.gutenberg.org/cache/epub/43007/pg43007.html
              https://ar.wikipedia.org/wiki/%D9%84%D8%BA%D8%A9_%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9"""

    languages = [('Texts/english.txt', 'Modern English', ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',\
                'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'], ['a', 'e', 'i', 'o', 'u'], ['b', 'c', \
                'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 't', 'v', 'x', 'z']), \
                ('Texts/french.txt', 'Modern French', ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', \
                'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'à', 'â', 'æ', 'ç', 'é', 'è', 'ê', 'ë', \
                'î', 'ï', 'ô', 'œ', 'ù', 'û', 'ü'], ['a', 'e', 'i', 'o', 'u', 'à', 'â', 'æ', 'é', 'è', 'ê', 'ë', 'î', \
                'ï', 'ô', 'œ', 'ù', 'û', 'ü'], ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', \
                's', 't', 'v', 'x', 'z']), \
                ('Texts/greek.txt', 'Modern Greek', ['α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ', 'μ', 'ν', 'ξ', \
                'ο', 'π', 'ρ', 'σ', 'ς', 'τ', 'υ', 'φ', 'χ', 'ψ', 'ω'], ['α', 'ε', 'η', 'ι', 'ο', 'υ', 'ω'], \
                ['β', 'γ', 'δ', 'ζ', 'θ', 'κ', 'λ', 'μ', 'ν', 'ξ', 'π', 'ρ', 'σ', 'ς', 'τ', 'φ', 'χ', 'ψ']), \
                ('Texts/arabic.txt', 'Arabic',\
                ['غ', 'ظ', 'ض', 'ذ', 'خ', 'ث', 'ت', 'ش', 'ر', 'ق', 'ص', 'ف', 'ع', 'س', 'ن', 'م', 'ل', 'ك', 'ي',\
                'ط', 'ح', 'ز', 'و', 'ه', 'د', 'ج', 'ب', 'أ'], [], [])]

    for i in range(len(languages)):
        #preprocess(languages[i][0], languages[i][2])
        all_letters = languages[i][2]
        correct_vowels = languages[i][3]
        correct_consonants = languages[i][4]

        print("\nClassifying vowels and consonants of " + languages[i][1] + " using SVD-based method...\n")
        corpus = open(languages[i][0], 'r', encoding='utf-8')
        weighted_A, svd_vowels, svd_consonants, num_tokens = svd_method(corpus, all_letters)
        calculate_precision_recall_accuracy(correct_vowels, correct_consonants, svd_vowels, svd_consonants)
        calculate_token_precision_recall_accuracy(correct_vowels, correct_consonants, svd_vowels,
                                                  svd_consonants, num_tokens, all_letters)
        corpus.close()

        print("\nClassifying vowels and consonants of " + languages[i][1] + " using Sukhotin's method...\n")
        corpus = open(languages[i][0], 'r', encoding='utf-8')
        sukhotin_vowels, sukhotin_consonants = sukhotins_method(corpus, all_letters)
        corpus.close()

        calculate_precision_recall_accuracy(correct_vowels, correct_consonants, sukhotin_vowels, sukhotin_consonants)

        if len(svd_vowels) > len(svd_consonants):
            KL_based_method(weighted_A, all_letters, svd_consonants, svd_vowels)
        else:
            KL_based_method(weighted_A, all_letters, svd_vowels, svd_consonants)

        corpus = open(languages[i][0], 'r', encoding='utf-8')
        count_method(corpus, set(svd_vowels), set(svd_consonants))
        corpus.close()
