from transformers import pipeline
from sentence_transformers import SentenceTransformer

print("Downloading models...")

pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
pipeline("ner", model="Jean-Baptiste/roberta-large-ner-english")
SentenceTransformer("all-MiniLM-L6-v2")

print("Done!")