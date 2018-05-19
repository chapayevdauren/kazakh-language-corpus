# coding=utf-8
import io
from collections import defaultdict

# read unigrams

with io.open('unigram.txt', 'r', encoding='utf-8') as f:
    unigrams_array = [line.rstrip(u'\n') for line in f]

unigrams_dict = defaultdict()
for u in unigrams_array:
    u_spl = u.split()
    unigrams_dict[u_spl[0]] = u_spl[1]

# read bigrams

# with io.open('bigram.txt', 'r', encoding='utf-8') as f:
#     bigrams_array = [line.rstrip(u'\n') for line in f]
#
# bigrams_dict = defaultdict()
# for b in bigrams_array:
#     b_spl = b.split()
#     if len(b_spl) > 1 and b_spl[-1].isdigit():
#         bigrams_dict[' '.join(b_spl[:-1])] = b_spl[-1]


# read trigrams

# with io.open('trigram.txt', 'r', encoding='utf-8') as f:
#     trigrams_array = [line.rstrip(u'\n') for line in f]
#
# trigrams_dict = defaultdict()
# for t in trigrams_array:
#     t_spl = t.split()
#     if len(t_spl) > 1 and t_spl[-1].isdigit():
#         trigrams_dict[' '.join(t_spl[:-1])] = t_spl[-1]


alphabet = 'аәбвгғдеёжзийкқлмнңоөпрстуұүфхһцчшщъыіьэюя'


def edits1(word):
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]
    replaces = [a + c + b[1:] for a, b in splits for c in alphabet.decode('utf-8') if b]
    inserts = [a + c + b for a, b in splits for c in alphabet.decode('utf-8')]
    return set(deletes + transposes + replaces + inserts)


def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in unigrams_dict)


def known_unigram(words): return set(w for w in words if w in unigrams_dict)


def known_bigram(words): return set(w for w in words if w in bigrams_dict)


def correct_one(word):
    candidates = known_unigram(word) or known_unigram(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=unigrams_dict.get)


def correct(word):
    candidates = known_unigram(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=unigrams_dict.get)


words = raw_input("Enter word: ")
w_spl = words.split()
if len(w_spl) == 1:
    print(correct_one(w_spl[0].decode('utf-8')))
# else:
#     print bigrams_dict[words.decode('utf-8')]
