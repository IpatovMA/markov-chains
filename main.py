from scipy.sparse import dok_matrix
from tqdm import tqdm
import random
import os
import numpy as np
# from module import *


# Загружаем корпус 
with open('corpus_file.txt','r') as f:
    corpus = f.read()

words = corpus.split(' ')

print(f"Load corpus of {len(words)} words")

k = 2 # длина цепочки

cached_fname = f"cache/cache_k_{k}_corp_{len(words)}.npy"

if not os.path.isfile(cached_fname): 
    # кэша нет

    distinct_words = list(set(words))
    word_idx_dict = {word: i for i, word in enumerate(distinct_words)}

    seqs_of_k_words = [ ' '.join(words[i:i+k]) for i, _ in enumerate(words[:-k]) ]
    distinct_seqs_of_k_words = list(set(seqs_of_k_words))
    seqs_idx_dict = {word: i for i, word in enumerate(distinct_seqs_of_k_words)}

    next_word_matrix = dok_matrix((len(distinct_seqs_of_k_words), len(distinct_words)))

    print("Building dok matrix . . .")
    for i, word in tqdm(enumerate(seqs_of_k_words[:-k])):
        seq_idx = seqs_idx_dict[word]
        next_word_idx = word_idx_dict[words[i+k]]
        next_word_matrix[seq_idx, next_word_idx] +=1
    print("Done!")

    print("Caching dok matrix . . .")
    if not os.path.isdir('cache'):
        os.mkdir('cache')

    with open(cached_fname,"bw") as f:
        cache = {'next_word_matrix':next_word_matrix,
                    'seqs_idx_dict':seqs_idx_dict,
                    'distinct_words':distinct_words}
        np.save(f,cache,allow_pickle=True)

    print("Done!\n")
else:
    # кэш есть
    print("Loading cached dok matrix . . .")
    with open(cached_fname,"br") as f:
        data = np.load(f,allow_pickle=True).item()
        next_word_matrix = data['next_word_matrix']
        seqs_idx_dict = data['seqs_idx_dict']
        distinct_words = data['distinct_words']


    print("Done! \n")


def sample_next_word(seq):
    seq_idx = seqs_idx_dict[seq]
    weights = next_word_matrix[seq_idx]
    weights /= weights.sum()
    next_word = random.choices(distinct_words,weights.toarray()[0])[0]
    return next_word



def get_chain(sequence, chain_length = 15, k = 2,print_result = False):
    seq_words = sequence.split(" ")

    if len(seq_words) != k:
        return "Wrong words count! Expected {k} words, but got {len(seq_words)} ."
    
    if print_result:
        print(seq_words)

    for _ in range(1,chain_length):
        next_word = sample_next_word(" ".join(seq_words[-k:]))
        seq_words.append(next_word)
        if print_result:
            print(next_word)
    
    return " ".join(seq_words)


print("Writing text . . .")
result_text = get_chain("вышел вперед",chain_length = 50,print_result =False )
print(result_text)

