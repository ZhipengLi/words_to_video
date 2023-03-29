import requests
import spacy
import nltk; nltk.download('popular') 
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
#from PIL import Image, ImageDraw, ImageFont
import io
from os.path import abspath, dirname, join
import os
import textstat


input_directory = 'books'
output_directory = 'output'
MAX_COUNT = 5

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__), input_directory))

__output_location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__), output_directory))



nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

english_most_common_10k = 'https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-usa-no-swears.txt'
english_most_common_20k = 'https://raw.githubusercontent.com/first20hours/google-10000-english/master/20k.txt'
# Get the file of 10 k most common words from TXT file in a github repo
response = requests.get(english_most_common_20k)
data = response.text

set_of_common_words = {x for x in data.split('\n')}
skip_words = ["didn"]
difficult_words = set()

def get_wordnet_pos(word):
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {
        "J": wordnet.ADJ,
        "N": wordnet.NOUN,
        "V": wordnet.VERB,
        "R": wordnet.ADV
    }

    return tag_dict.get(tag, wordnet.NOUN)

def generate_commented_content(paragraph):
    lemmatizer = WordNetLemmatizer()
    sentences = paragraph.split("\n\n")
    original_to_explanation = {}
    count = {}
    ret = []
    for sentence in sentences:
        if len(sentence)<5:
            continue
        if 'Rowling' in sentence and 'Page' in sentence:
            continue
        words = sentence.split()
        #normalized_words = []
        result = []
        for word in words:
            #print(word)
            new_word = word.split("’")[0]
            new_word = ''.join(filter(str.isalnum, new_word))
            if not new_word:
                continue
            if new_word[0].isupper():
                continue
            #if word in original_to_explanation.keys():
            #    continue
            new_word = new_word.lower()
            #if new_word in set_of_common_words or new_word in skip_words:
            #    continue
            #print(new_word)
            #normalized_words.append(new_word)
            #print("token lemma:",nlp(new_word)[0].lemma_)
            token_word = nlp(new_word)[0].lemma_
            if token_word in set_of_common_words or token_word in skip_words:
                continue
            if wordnet.synsets(token_word):
                #original_to_explanation[word] = wordnet.synsets(token_word)[0].definition()
                #count[word] = 0
                lemma = lemmatizer.lemmatize(token_word.lower(), get_wordnet_pos(token_word))
                reading_ease_score = textstat.flesch_reading_ease(lemma)
                #if reading_ease_score < 50:
                difficult_words.add(token_word)
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
    #for k,v in original_to_explanation.items():
    #    print(k,':',v, count[k])
    #print(''.join(ret))
    return ''.join(ret)

for filename in os.listdir(__location__):
    f = os.path.join(__location__, filename)
    # checking if it is a file
    if os.path.isfile(f):
        file = open(f,mode='r', encoding="utf8")
        sentence = file.read()
        #print(sentence)
        #output_sentence = generate_commented_content(sentence)
        generate_commented_content(sentence)
        #save_file(filename, output_sentence)
        file.close()
for word in difficult_words:
    print(word)