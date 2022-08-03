import os
import random
import re
import string
import requests                     # pip install requests
from bs4 import BeautifulSoup       # pip install beautifulsoup4

#import spacy                                    # pip install spacy
#french_nlp = spacy.load("fr_core_news_sm")
#eng_nlp = spacy.load("en_core_web_sm")

# -------------------------------------
# WIKIPEDIA SCRAPPER : add words continuously
# [start] [stop]

# -------------------------------------
# WORD TYPES
# select: type de mot
# un choix non vide ajoute une autre boite
"""
def get_words_of_types(lang, types):
    nlp = {'fr': french_nlp, 'en': eng_nlp}[lang]
    all_words = list(get_all_words(lang))
    words = []
    for t in types:
        random.shuffle(all_words)
        for w in all_words:
            if t == get_word_type(nlp, w):
                words.append(w)
                break
    return words

def get_word_type(nlp, word):
    t = nlp(word)[0].pos_
    return t
"""

# -------------------------------------
# WIKIPEDIA random word(s)
def get_wikipedia_random_words(num):
    txt = ''
    for i in range(num):
        if i > 0:
            txt += ' '
        txt += fetch_word_from_wikipedia()
    return txt

def fetch_word_from_wikipedia():
    url = "https://en.wiktionary.org/wiki/Special:Random"
    response = requests.get(
        url=url,
    )
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find(id="firstHeading")
    return title.text

# -------------------------------------
def get_random_words_with_criterias(lang, num, starts_with, starts_with_inv,
        ends_with, ends_with_inv, contains, syl_qty, max_letter_qty, min_letter_qty, consonants_in_a_row):
    words = []
    for word in get_all_words(lang):
        match = check_starts_with(word, starts_with, starts_with_inv) and check_ends_with(word, ends_with, ends_with_inv)\
            and word_contains(word, contains) and check_syl_qty(word, syl_qty)\
            and check_letter_qty(word, max_letter_qty, min_letter_qty) and check_consonants_in_a_row(word, consonants_in_a_row)
        if match:
            words.append(word)
    random.shuffle(words)
    return words[:num]

def check_starts_with(word, starts_with, inv):
    return starts_with == '' or word.startswith(starts_with) != inv

def check_ends_with(word, ends_with, inv):
    return ends_with == '' or word.endswith(ends_with) != inv    

def word_contains(word, contains):
    return len(contains) == 0 or all(c in word for c in contains)

def check_syl_qty(word, syl_qty):
    res = not syl_qty or syl_qty == len(split_syllables(word))
    return res

def check_letter_qty(word, max_letter_qty, min_letter_qty):
    res = True
    if max_letter_qty > 0:
        res = res and len(word) <= max_letter_qty
    if min_letter_qty > 0:
        res = res and len(word) >= min_letter_qty
    return res

def check_consonants_in_a_row(word, qty):
    if qty == 0:
        res = True
    else:
        res = False
        counter = 0
        for letter in word:
            if is_consonant(letter):
                counter += 1
                if counter == qty:
                    res = True
                    break
            else:
                counter = 0
    return res

# -------------------------------------
def mimic_text_with_random_syllables(lang, source_text):
    new_syllables = get_some_syllables(lang, 1000)
    txt = ''
    for chunk in split_by_tokens(source_text, punctuations):
        if chunk in punctuations:
            punct = chunk
            txt += punct
        else:
            source_word = chunk
            word = ''
            for source_syl in split_syllables(source_word):
                syl = random.choice(new_syllables)
                if first_char_is_capitalized(source_syl):
                    if all_chars_are_capitalized(source_syl):
                        syl = syl.upper()
                    else:
                        syl = syl.capitalize()
                word += syl
            txt += word
    return txt

first_char_is_capitalized = lambda w: w[0].isupper()
all_chars_are_capitalized = lambda w: all(c.isupper() for c in w)

def get_random_syllables_words(lang, num, min_syl, max_syl):
    syllables = get_some_syllables(lang, num=num*max_syl)
    random.shuffle(syllables)
    words = []
    syl_counter = 0
    word = ''
    for syl in syllables:
        if len(words) == num:
            break
        if syl_counter == 0:
            syl_counter = random.randint(min_syl, max_syl)
            if word != '':
                words.append(word)
            word = ''
        word += syl
        syl_counter -= 1
    return words

def get_some_syllables(lang, num):
    syllables = []
    words = list(get_all_words(lang))
    random.shuffle(words)
    for word in words:
        syllables += split_syllables(word)
        if len(syllables) >= num:
            break
    return syllables 

def split_syllables(word):
    syllables = []
    curr_syl = ""
    for letter in word:
        if is_vowel(letter):
            curr_syl += letter
        elif is_consonant(letter):
            curr_syl += letter
            if has_vowel(curr_syl): 
                syllables.append(curr_syl)
                curr_syl = ""
    if curr_syl != "":
        if has_vowel(curr_syl):
            syllables.append(curr_syl)
        else:
            if len(syllables) > 0:
                syllables[-1] += curr_syl
            else:
                syllables = [curr_syl]
    return syllables

# -------------------------------------
def get_all_words(lang):
    txt_folder = 'static/mots/txt'
    words_path = {
        'fr': os.path.join(txt_folder, 'motsFrançais.txt'),
        'en': os.path.join(txt_folder, 'motsAnglais.txt'),
        }[lang.lower()]
    with open(words_path, 'r', encoding='utf-8') as words_file:
        for word in words_file:
            yield word.strip().lower()


consonants = 'bcdfghjklmnpqrstvwxyz'
is_consonant = lambda letter: letter.lower() in consonants
vowels = 'aeiouy'
accents = 'éèêëàâäôòöìîïùûü'
is_vowel = lambda letter: letter.lower() in vowels + accents
has_vowel = lambda word: any(is_vowel(letter) for letter in word)
punctuations = ' –—’“”«»…\n'+string.punctuation

def split_by_tokens(txt, tokens):
    def get_regex_pattern():
        regex_special_chars =  '.+*?^$()[]{}|\\'
        pattern = '('
        for i, punctuation in enumerate(tokens):
            if punctuation in regex_special_chars:
                pattern += '\\'
            pattern += punctuation
            if i < len(tokens)-1:
                pattern += '|'
        pattern += ')'
        return pattern
    words = re.split(get_regex_pattern(), txt)
    return words

if __name__ == "__main__":
    #print('start')
    #types = ['DET', 'NOUN', 'VERB', 'DET', 'NOUN']
    #words = get_words_of_types('en', types)
    #txt = ' '.join(words)
    #print(txt)
    #exit()
    txt = """Bonjour, comment allez-vous?
Je vais bien merci.

Ok!"""

    txt = mimic_text_with_random_syllables('fr', txt)
    print(txt)