from models.keyword_ext import extract_keywords
from models.summarization import summarize
from models.translation import translate
from models.verb_cvt import convert_to_verb1


def generate_keywords(text):
    text_en = translate(text)
    print(text_en)
    yield None, 1
    text_v1 = convert_to_verb1(text_en)
    print(text_v1)
    yield None, 2
    text_sum = summarize(text_v1)
    print(text_sum)
    yield None, 3
    keywords = extract_keywords(text_sum, text_v1)
    print(keywords)
    yield keywords, 4
