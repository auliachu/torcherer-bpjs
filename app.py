import streamlit as st
import requests
import json
import os
import nltk
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
from nltk import pos_tag, download
from moviepy.editor import VideoFileClip, concatenate_videoclips
from transformers import MarianMTModel, MarianTokenizer, BartForConditionalGeneration, BartTokenizer
import spacy

# Initial setup: Download necessary NLTK resources
download('punkt')
download('wordnet')
download('averaged_perceptron_tagger')

# Load models for translation and summarization
model_name_translation = "Helsinki-NLP/opus-mt-id-en"
model_translation = MarianMTModel.from_pretrained(model_name_translation)
tokenizer_translation = MarianTokenizer.from_pretrained(model_name_translation)

model_name_summarization = "facebook/bart-large-cnn"
model_summarization = BartForConditionalGeneration.from_pretrained(model_name_summarization)
tokenizer_summarization = BartTokenizer.from_pretrained(model_name_summarization)

nlp = spacy.load("en_core_web_sm")

# Load JSON data for video paths and labels
file_path = 'WLASL_v0.3.json'
with open(file_path, 'r') as file:
    data = json.load(file)

label = []
videos = []
lbl = []

for item in data:
    label.append(item['gloss'])
    for instance in item['instances']:
        combined_path = os.path.join('/root/.cache/kagglehub/datasets/risangbaskoro/wlasl-processed/versions/5/videos/', instance['video_id']) + '.mp4'
        if os.path.exists(combined_path):
            videos.append(combined_path)
            lbl.append(label.index(item['gloss']))

lbl_asli = []
video_asli = []
lbl_asli.append(lbl[0])
video_asli.append(videos[0])
gh = lbl[0]
for i in range(1, len(lbl)):
    if lbl[i] != gh:
        lbl_asli.append(lbl[i])
        video_asli.append(videos[i])
        gh = lbl[i]

# Streamlit app structure
st.title("ChatGPT UI - Translate & Video Combiner")
st.subheader("Input text in Indonesian and generate a video")

input_text = st.text_input("Masukkan kalimat dalam bahasa Indonesia:")

if input_text:
    # Translate text
    input_ids = tokenizer_translation.encode(input_text, return_tensors="pt")
    output_ids = model_translation.generate(input_ids)
    translated_text = tokenizer_translation.decode(output_ids[0], skip_special_tokens=True)

    st.write("Terjemahan ke Bahasa Inggris:", translated_text)

    # Convert to verb form and extract keywords
    def get_base_form(verb):
        lemmatizer = nltk.WordNetLemmatizer()
        return lemmatizer.lemmatize(verb, pos='v')

    def convert_to_verb1(sentence):
        words = word_tokenize(sentence)
        base_verbs = [get_base_form(word) if pos_tag([word])[0][1].startswith('VB') else word for word in words]
        return ' '.join(base_verbs)

    converted_sentences = convert_to_verb1(translated_text)

    # Summarize and extract keywords
    inputs = tokenizer_summarization([converted_sentences], max_length=1024, return_tensors="pt", truncation=True)
    summary_ids = model_summarization.generate(inputs["input_ids"], max_length=10, num_beams=4, early_stopping=True)
    summary = tokenizer_summarization.decode(summary_ids[0], skip_special_tokens=True)

    doc = nlp(summary)
    keywords = [token.lemma_.lower() for token in doc if token.pos_ in ["NOUN", "PRON", "VERB"]]

    final_keywords = []
    for word in converted_sentences.split():
        lower_word = word.strip('.').lower()
        if lower_word in keywords and lower_word not in final_keywords:
            final_keywords.append(lower_word)

    st.write("Kata kunci:", final_keywords)

    # Match keywords with labels
    matched_keywords = [kw for kw in final_keywords if kw in label]
    indices = [label.index(video) for video in matched_keywords]

    if indices:
        st.write("Indeks video:", indices)
        clips = [VideoFileClip(video_asli[i]) for i in indices]
        final_clip = concatenate_videoclips(clips)
        final_clip.write_videofile("combined_video.mp4", codec='libx264')
        
        # Display video
        st.video("combined_video.mp4")
    else:
        st.write("Tidak ada video yang cocok dengan kata kunci.")
