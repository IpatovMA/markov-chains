import os
import re
from hashlib import md5
import argparse

parser = argparse.ArgumentParser(description='Create text corpus')
parser.add_argument("--path", help="Path to source file or dirrectory",default="text", type=str)
parser.add_argument("--title", help="Corpus title",default="corpus", type=str)
parser.add_argument("--descr", help="Corpus description",default="This corpus has no description", type=str)
args = parser.parse_args()
all_data_path = args.path
title = args.title
description = args.descr

AVALIABLE_FORMATS = ['txt','fb2','rtf']

corpus =""

if os.path.isdir(all_data_path):
    if not all_data_path.endswith('/'):
        all_data_path = all_data_path+"/"
    
    filenames = [all_data_path +name for name in os.listdir(all_data_path) if name[(name.rfind('.')+1):] in AVALIABLE_FORMATS]
    print(f"Find {len(filenames)} text files: \n{filenames}")

    if len(filenames)==0:
        raise  FileNotFoundError(f'Dirrectory {all_data_path} contain no avaliable files! Only {AVALIABLE_FORMATS} formats are allowed') 

    for filename in filenames:
        with open(filename, 'r') as f:
            corpus += f.read()

elif os.path.isfile(all_data_path):
    if all_data_path[(all_data_path.rfind('.')+1):] in AVALIABLE_FORMATS:
        with open(all_data_path, 'r') as f:
            corpus += f.read()
    else: raise NameError(f'Wrong format! Only {AVALIABLE_FORMATS} formats are allowed')
else:
    raise FileNotFoundError(f'Cant find file {all_data_path}')


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

for spaced in ['…','.',',','!','?','(','—',')','–',":"]:
    corpus = corpus.replace(spaced, f' {spaced} ')

words = corpus.split(' ')
words= [word for word in words if word != '' and len(word)<30]
corpus = " ".join(words)

c_hash = md5(corpus.encode()).hexdigest()

corpus_dir = 'corpuses'
if not os.path.isdir(corpus_dir):
        os.mkdir(corpus_dir)

corpus_filename = f"{corpus_dir}/{title}.txt"

corpus_info = f'hash: {c_hash} \ndescription: {description} \n'

with open(corpus_filename, 'w') as cf:
    r = cf.write(corpus_info + corpus)

print(f"Save corpus of {len(words)} words in {corpus_filename} is {bool(r)}")
