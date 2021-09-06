# markov chains for generating text 
You can generate meaningless but grammatically correct text with help of markov chains

## Creating text corpus

```
python create_corpus.py [--title TITLE] [--desc DESCRIPTION] [--path PATH = '/text']
```
* TITLE is the name of the corpus file to be created. 
* DESCRIPTION is text description of corpus
* PATH is path to source text file or dirrectory with sources text files

Grats! You create test corpus file in `/corpuses` 

## Textes generation

```
python main.py [-k K=2] [--corpus CORPUS = 'corpus.txt']  [--len LEN = 50] [--seed SEED] ]
```
* K is k parameter of markov chain, size of context window 
* CORPUS is filename of the text corpus from the '/corpuses' directory
* LEN is generated text length
* SEED is start word sequence. If `None` - get random seed from corpus sequences

## Examples
**IN**
```
python create_corpus.py --title narnija --desc '7 книг Хроники Нарнии'         
```
**OUT**
```          
Find 7 text files: 
['text/Клайв С. Льюис_6_Племяник чародея.fb2', 'text/Клайв С. Льюис_2_Принц Каспиан.fb2', 'text/Клайв С. Льюис_3_Плавание утреннего путника.fb2', 'text/Клайв С. Льюис_4_Серебряное кресло.fb2', 'text/Клайв С. Льюис_5_Конь и его мальчик.fb2', 'text/Клайв С. Льюис_1_Лев, колдунья и платяной шкаф.fb2', 'text/Клайв С. Льюис_7_Последняя битва.fb2']
Save corpus of 307741 words in corpuses/narnija.txt is True
```
**IN**
```
python main.py -k 3  --corpus narnija.txt --len 20
```
**OUT**
```          
Load corpus 'narnija.txt' : 7 книг Хроники Нарнии of 307741 words
Building dok matrix . . .
307735it [00:25, 12209.19it/s]
Done!
Caching . . .
Done!

Writing text . . .
они спускались через край стола на пол . Волосы на затылках отросли так , что вес всей шеренги был сосредоточен в первых
```
**IN**
```
python main.py -k 3 --seed 'и он обратится' --corpus narnija.txt --len 20
```
**OUT**
```          
Load corpus 'narnija.txt' : 7 книг Хроники Нарнии of 307741 words
Writing text . . .
и он обратится в туман . Внезапно , в девять утра , они оказались рядом с маленькой деревушкой . На песке они
```
