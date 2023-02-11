import requests
import spacy
import nltk; nltk.download('popular') 
from nltk.corpus import wordnet

nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

english_most_common_10k = 'https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-usa-no-swears.txt'

# Get the file of 10 k most common words from TXT file in a github repo
response = requests.get(english_most_common_10k)
data = response.text

set_of_common_words = {x for x in data.split('\n')}
skip_words = ["didn"]

sentence = """
Mr. and Mrs. Dursley, of number four, Privet Drive, 
were proud to say that they were perfectly normal, 
thank you very much. They were the last people you’d 
expect to be involved in anything strange or 
mysterious, because they just didn’t hold with such 
nonsense. 

Mr. Dursley was the director of a firm called 
Grunnings, which made drills. He was a big, beefy 
man with hardly any neck, although he did have a 
very large mustache. Mrs. Dursley was thin and 
blonde and had nearly twice the usual amount of 
neck, which came in very useful as she spent so 
much of her time craning over garden fences, spying 
on the neighbors. The Dursley s had a small son 
called Dudley and in their opinion there was no finer 
boy anywhere. 
"""
words = sentence.split()
normalized_words = []
original_to_explanation = {}

for word in words:
    #print(word)
    new_word = word.split("’")[0]
    new_word = ''.join(filter(str.isalnum, new_word))
    if new_word[0].isupper():
        continue
    new_word = new_word.lower()
    #if new_word in set_of_common_words or new_word in skip_words:
    #    continue
    #print(new_word)
    normalized_words.append(new_word)
    #print("token lemma:",nlp(new_word)[0].lemma_)
    token_word = nlp(new_word)[0].lemma_
    if token_word in set_of_common_words or token_word in skip_words:
        continue
    original_to_explanation[word] = wordnet.synsets(token_word)[0].definition()

#new_sentence = ' '.join(normalized_words)
#doc = nlp('did displaying words')
#doc = nlp(new_sentence)
#print (" ".join([token.lemma_ for token in doc]))
#print (" ".join([token.lemma_ for token in nlp(sentence)]))

#syns = wordnet.synsets("game")
#print(syns[0].definition())
#for k,v in original_to_explanation.items():
#    if k[-1].isalpha():
#        print(k+"("+v+")")
#    else:
#        print(k[:-1]+"("+v+")"+k[-1:])

result = []
for word in words:
    if word in original_to_explanation.keys():
        v = original_to_explanation[word]
        if word[-1].isalpha():
            result.append(word+"("+v+")")
        else:
            result.append(word[:-1]+"("+v+")"+word[-1:])
    else:
        result.append(word)
print(' '.join(result))

# https://stackoverflow.com/questions/17856242/how-to-convert-a-string-to-an-image

