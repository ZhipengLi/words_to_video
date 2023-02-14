import requests
import spacy
import nltk; nltk.download('popular') 
from nltk.corpus import wordnet
#from PIL import Image, ImageDraw, ImageFont
import io
from os.path import abspath, dirname, join
import os

input_directory = 'books'
output_directory = 'output'
MAX_COUNT = 5

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__), input_directory))

__output_location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__), output_directory))

def save_file(file_name, sentence):
    f = os.path.join(__output_location__, filename.split('.')[0]+"_converted.txt")
    text_file = open(f, "w", encoding="utf8")
    n = text_file.write(sentence)
    text_file.close()



def save_image(content):
    img = Image.new('RGB', (1920, 1080), (255, 255, 255))
    d = ImageDraw.Draw(img)
    current_words = []
    x,y = 0,20
    for word in content.split():
        current_words.append(word)
        left, top, right, bottom= d.textbbox((x,y),' '.join(current_words))
        if current_words and right>=1920:
            d.text((20+bottom-top,20),' '.join(current_words[:-1]), fill=(0,0,0))
            current_words = [-1]
            x+=(bottom-top+20)
        else:
            current_words =[current_words[-1]]
    d.text((20+bottom-top,20),' '.join(current_words), fill=(0,0,0))


    #d.text((20,20), content, fill=(255,0,0))

    path = join(dirname(abspath(__file__)), "image.png")
    img.save(path)



nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

english_most_common_10k = 'https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-usa-no-swears.txt'
english_most_common_20k = 'https://raw.githubusercontent.com/first20hours/google-10000-english/master/20k.txt'
# Get the file of 10 k most common words from TXT file in a github repo
response = requests.get(english_most_common_20k)
data = response.text

set_of_common_words = {x for x in data.split('\n')}
skip_words = ["didn"]

def generate_commented_content(paragraph):
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
            if word in original_to_explanation.keys():
                continue
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
                original_to_explanation[word] = wordnet.synsets(token_word)[0].definition()
                count[word] = 0
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
        for word in words:
            if word in original_to_explanation.keys():
                print(word,' count:',count[word])
                if count[word]>0:
                    if count[word] == MAX_COUNT:
                        count[word] = 0
                    result.append(word)
                    continue
                v = original_to_explanation[word]
                if word[-1].isalpha():
                    result.append(word+"("+v+")")
                else:
                    result.append(word[:-1]+"("+v+")"+word[-1:])
                count[word] +=1
            else:
                result.append(word)
        ret.append(' '.join(result))
        ret.append('\n\n')
    for k,v in original_to_explanation.items():
        print(k,':',v, count[k])
    #print(''.join(ret))
    return ''.join(ret)

for filename in os.listdir(__location__):
    f = os.path.join(__location__, filename)
    # checking if it is a file
    if os.path.isfile(f):
        file = open(f,mode='r', encoding="utf8")
        sentence = file.read()
        #print(sentence)
        output_sentence = generate_commented_content(sentence)
        save_file(filename, output_sentence)
        file.close()

exit()



# https://stackoverflow.com/questions/17856242/how-to-convert-a-string-to-an-image
#save_image(' '.join(result))

