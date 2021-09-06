from scipy.sparse import dok_matrix
from tqdm import tqdm
import random
import os
import numpy as np
import argparse

# python main.py -k 2 --seed 'Ты не' --corpus narnija.txt --len 100


parser = argparse.ArgumentParser(description='Build markov chain')
parser.add_argument("-k", help="Size of context window. Default k=2 .",default=2, type=int)
parser.add_argument("--seed", help="Chain start word sequence", type=str)
parser.add_argument("--corpus", help="Filename of text corpus from corpuses dirrectory",default='corpus.txt', type=str)
parser.add_argument("--len", help="Chain length",default=50, type=int)
args = parser.parse_args()
k = args.k
seed = args.seed
corpus_fname= args.corpus
chain_length = args.len

corpus_data = []
# Загружаем корпус 
with open('corpuses/'+corpus_fname,'r') as f:
    corpus_data = f.readlines()


c_hash = corpus_data[0][6:-2]
c_description = corpus_data[1:-1][0][13:-2]
c_text = corpus_data[-1]

words = c_text.split(' ')

print(f"Load corpus '{corpus_fname}' : {c_description} of {len(words)} words")


cached_fname = f"cache/{c_hash}_k_{k}.npy"

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

    print("Caching . . .")
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
    with open(cached_fname,"br") as f:
        data = np.load(f,allow_pickle=True).item()
        next_word_matrix = data['next_word_matrix']
        seqs_idx_dict = data['seqs_idx_dict']
        distinct_words = data['distinct_words']



def sample_next_word(seq):
    seq_idx = seqs_idx_dict[seq]
    weights = next_word_matrix[seq_idx]
    weights /= weights.sum()
    next_word = random.choices(distinct_words,weights.toarray()[0])[0]
    return next_word




def get_chain(seed, chain_length = 15, k = 2,print_result = False):
    seq_words = seed.split(" ")

    if len(seq_words) != k:
        return f"Wrong words count! Expected {k} words, but got {len(seq_words)} ."
    
    if not seed in seqs_idx_dict.keys():
        return f"Wrong seed! Try one of this {random.choices(list(seqs_idx_dict.keys()),k=5)} ."


    if print_result:
        print(seq_words)

    for _ in range(1,chain_length):
        next_word = sample_next_word(" ".join(seq_words[-k:]))
        seq_words.append(next_word)
        if print_result:
            print(next_word)
    
    return " ".join(seq_words)


print("Writing text . . .")

if not seed: 
    seed = random.choice(list(seqs_idx_dict.keys()))

result_text = get_chain(seed,chain_length = chain_length,k = k, print_result =False )
print(result_text)

