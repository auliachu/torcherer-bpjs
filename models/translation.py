from transformers import pipeline

translation_pipe = pipeline('translation', model='Helsinki-NLP/opus-mt-id-en')


def translate(text):
    res = translation_pipe(text)
    return res[0]['translation_text']
