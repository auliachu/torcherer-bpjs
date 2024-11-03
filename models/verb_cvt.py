import nltk


lemmatizer = nltk.WordNetLemmatizer()


def convert_to_verb1(text):
    words = nltk.word_tokenize(text)
    base_verbs = [
        lemmatizer.lemmatize(word, pos='v')
        if nltk.pos_tag([word])[0][1].startswith('VB') else word
        for word in words
    ]
    return ' '.join(base_verbs)
