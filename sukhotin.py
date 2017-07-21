
def sukhotins_method(corpus, all_letters):

    mat = [[0 for x in range(len(all_letters))] for x in range(len(all_letters))]
    count = 0
    for line in corpus:
        if count > 5000:
            break
        line = line.split(' ')
        for word in line:
            count +=1
            if count > 5000:
                break
            word = word.strip("\n")
            for i in range(len(word)-1):
                if word[i] in all_letters and word[i+1] in all_letters and word[i] != word[i+1]:
                    index1 = all_letters.index(word[i])
                    index2 = all_letters.index(word[i + 1])
                    mat[index1][index2] += 1
                    mat[index2][index1] += 1
    corpus.close()

    putative_vowels = []
    putative_consonants = [x for x in all_letters]
    sums = [0 for x in range(len(all_letters))]

    for i in range(len(all_letters)):
        sums[i] = sum(mat[i])

    while max(sums) > 0:
        mx_index = sums.index(max(sums))
        putative_vowels.append(all_letters[mx_index])
        putative_consonants.remove(all_letters[mx_index])
        for i in range(len(sums)):
            sums[i] -= mat[i][mx_index]*2
        sums[mx_index] = 0

    return putative_vowels, putative_consonants
