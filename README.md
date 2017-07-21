# Vowel and Consonant Classification through Spectral Decomposition
Given an undeciphered alphabetic writing system or mono-alphabetic cipher, we can determine: \
(1) which of its letters are vowels and which are consonants; and \
(2) whether the writing system is a vocalic alphabet or an abjad.

The methods are thoroughly explained in: [Citation to be added when camera-ready is published]

To run the code on the current text samples:
```
python3 main.py
```

To run the code on your own text samples, modify line 60 of main.py.
```
languages = [('/path/to/text/sample.txt','Language Name', [list of all of this language's letters], [list of all of this language's vowels],[list of all of this language's consonants]), ...]
```

MolerAndMorrison.m (Moler and Morrison, 1983) and Sukhotin.py (Sukhotin, 1962; Guy, 1991) are baselines for our work.

##Sources

Jacques BM Guy. 1991. Vowel identification: an old (but good) algorithm. Cryptologia 15(3):258–262.

Cleve Moler and Donald Morrison. 1983. Singular value analysis of cryptograms. American Mathematical Monthly pages 78–87.

B.V. Sukhotin. 1962. Eksperimental’noe vydelenie klassov bukv s po- moshch’ju elektronnoj vychislitel’noj mashiny. Problemy strukturnoj lingvistiki 234:198–106.
