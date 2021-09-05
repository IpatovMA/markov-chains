import os
import re


all_data_path = "text"
filenames = [all_data_path +"/"+name for name in os.listdir(all_data_path)]

print(f"Find {len(filenames)} files: \n{filenames}")

corpus =""

for filename in filenames:
    with open(filename, 'r') as f:
        corpus += f.read()

# for fb2 source files
tag = "<[^<,^>]*>"
tag_pattern = re.compile(tag)
tag_list = re.findall(tag_pattern,corpus)
distinct_tags = list(set(tag_list))
len(distinct_tags)

for tag in distinct_tags:
    corpus = corpus.replace(tag, ' ')
corpus = corpus.replace('\xa0', '')
# ----------------------

corpus = corpus.replace('\n',' ')
corpus = corpus.replace('\t',' ')
corpus = corpus.replace('«', ' " ')
corpus = corpus.replace('»', ' " ')

for spaced in ['.',',','!','?','(','—',')','–',":"]:
    corpus = corpus.replace(spaced, f' {spaced} ')

words = corpus.split(' ')
words= [word for word in words if word != '' and len(word)<30]
corpus = " ".join(words)

corpus_filename = "corpus_file.txt"
with open(corpus_filename, 'w') as cf:
    r = cf.write(corpus)

print(f"Save corpus of {len(words)} words in {corpus_filename} is {bool(r)}")
