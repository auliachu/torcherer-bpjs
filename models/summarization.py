from transformers import pipeline


summarization_pipe = pipeline('summarization', model='facebook/bart-large-cnn')


def summarize(text):
    if len(text.split()) < 12:
        return text
    res = summarization_pipe(text, min_length=1, max_length=12, num_beams=4)
    return res[0]['summary_text']
