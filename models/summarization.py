from transformers import pipeline


summarization_pipe = pipeline('summarization', model='facebook/bart-large-cnn')


def summarize(text):
    res = summarization_pipe(text, min_length=1, max_length=32, num_beams=4)
    return res[0]['summary_text']
