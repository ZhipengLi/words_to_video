import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import textstat

# Download WordNet data if not already installed
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download("punkt")
nltk.download('omw-1.4')

def get_wordnet_pos(word):
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {
        "J": wordnet.ADJ,
        "N": wordnet.NOUN,
        "V": wordnet.VERB,
        "R": wordnet.ADV
    }

    return tag_dict.get(tag, wordnet.NOUN)

def process_text(input_file, output_file, threshold=5):
    lemmatizer = WordNetLemmatizer()
    difficult_words = set()

    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            words = nltk.word_tokenize(line)
            for word in words:
                lemma = lemmatizer.lemmatize(word.lower(), get_wordnet_pos(word))
                reading_ease_score = textstat.flesch_reading_ease(lemma)
                if reading_ease_score < threshold:
                    difficult_words.add(lemma)

    with open(output_file, 'w') as f:
        for word in sorted(difficult_words):
            f.write(word + '\n')

if __name__ == "__main__":
    process_text('input.txt', 'difficult_words.txt')