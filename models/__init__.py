from models.keyword_ext import extract_keywords
from models.summarization import summarize
from models.translation import translate
from models.verb_cvt import convert_to_verb1


def generate_keywords(text):
    text_en = translate(text)
    text_v1 = convert_to_verb1(text_en)
    text_sum = summarize(text_v1)
    keywords = extract_keywords(text_sum, text_v1)
    return keywords
