import pickle
import streamlit as st
import string
import numpy as np
import pandas as pd

# //////////////////////////////////////

vocabulary = pickle.load(open("vocabulary.pkl", "rb"))
word_probs = pickle.load(open("word_probs.pkl", "rb"))


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


def split(word):
    return [(word[:i], word[i:]) for i in range(len(word) + 1)]


def delete(word):
    return [l + r[1:] for l, r in split(word) if r]


def swap(word):
    return [l + r[1] + r[0] + r[2:] for l, r in split(word) if len(r) > 1]


def replace(word):
    letters = string.ascii_lowercase
    return [l + c + r[1:] for l, r in split(word) if r for c in letters]


def insert(word):
    letters = string.ascii_lowercase
    return [l + c + r for l, r in split(word) for c in letters]


def level_one_edits(word):
    return set(delete(word) + swap(word) + replace(word) + insert(word))


def level_two_edits(word):
    return set([j for i in level_one_edits(word) for j in level_one_edits(i)])


def correct_spelling(word, vocabularies, word_probability):
    if word in vocabularies:
        print(word + " is correctly spelled.")
        return [word + " is correctly spelled."]
    suggestions = level_one_edits(word) or level_two_edits(word) or [word]
    best_guess = [w for w in suggestions if w in vocabularies]
    return [w for w in best_guess]


# def spelling_list(text, vocabularies, word_probability):
#     try:
#         return [i[0] for i in correct_spelling(text, vocabularies, word_probability)]
#     except:
#         return ["Word not found"]


# /////////////////////////////////////

st.title("Spelling autocorrector")

word = st.text_input("Enter the word")

clicked = st.button("Check")

if clicked:
    correct_words = correct_spelling(word.lower(), vocabulary, word_probs)
    if len(correct_words) > 0:
        for i in correct_words:
            st.write(i)
    else:
        st.write("No alternative word found")
