import nltk


nltk_dir = './.venv/nltk_data'
nltk.download('wordnet', nltk_dir)
nltk.download('punkt_tab', nltk_dir)
nltk.download('averaged_perceptron_tagger_eng', nltk_dir)
