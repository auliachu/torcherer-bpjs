import spacy


nlp = spacy.load('en_core_web_sm')


def extract_keywords(summary, origin):
    doc = nlp(summary)
    keywords = []
    for token in doc:
        if token.pos_ in ['NOUN', 'PRON', 'VERB']:
            keywords.append(token.lemma_.lower())
    final_keywords = []
    for word in origin.split():
        lower_word = word.strip('.').lower()
        if lower_word in keywords and lower_word not in final_keywords:
            final_keywords.append(lower_word)
    return final_keywords
