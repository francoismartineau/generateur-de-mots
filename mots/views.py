from django.shortcuts import render
from django.http import HttpResponse

from .mots import get_random_syllables_words, get_random_words_with_criterias,\
    mimic_text_with_random_syllables, get_wikipedia_random_words


def index(request):
    languages_select = {'partial_id': 'lang', 'label': 'Lang:', 'type': 'select', 'options': ['fr', 'en']}
    num_input = {'partial_id': 'num', 'label': 'Num:', 'type': 'number', 'default': 2}
    context = {'sections': {
        'random-with-criterias': {
            'titre': 'Trouver des mots',
            'inputs': [languages_select, num_input,
            {'partial_id': 'starts-with', 'label': 'Début', 'type': 'text'},
            {'partial_id': 'starts-with-inv', 'label': '!', 'type': 'checkbox'},
            {'partial_id': 'ends-with', 'label': 'Fin', 'type': 'text'},
            {'partial_id': 'ends-with-inv', 'label': '!', 'type': 'checkbox'},
            {'partial_id': 'contains', 'label': 'Contient (,)', 'type': 'text'},
            {'partial_id': 'syl-qty', 'label': 'Nombre de syllables', 'type': 'number'},
            {'partial_id': 'max-letter-qty', 'label': 'Max lettres', 'type': 'number'},
            {'partial_id': 'min-letter-qty', 'label': 'Min lettres', 'type': 'number'},
            {'partial_id': 'consonants-in-a-row', 'label': 'Consonnes consécutives', 'type': 'number'}]
        },        
        'random-syllables-words': {
            'titre': 'Créer des mots à partir de syllabes aléatoires',
            'inputs': [languages_select, 
            {'partial_id': 'mimic-text-source', 'label': 'Mimiquer puit', 'type': 'checkbox'},
            num_input,
            {'partial_id': 'min-syl', 'label': 'Min', 'type': 'number', 'default': 1},
            {'partial_id': 'max-syl', 'label': 'Max', 'type': 'number', 'default': 3}],            
        },
        'wikipedia-random-words': {
            'titre': 'Mots aléatoires de Wiktionary',
            'inputs': [num_input],
        },
        },}
    return render(request, 'index.html', context)

""" #DEAD
def random_words(request):
    lang, num = get_lang_and_num(request)
    words = get_random_words(lang, num)
    txt = format_words(words)
    return HttpResponse(txt)
"""

def random_syllables_words(request):
    lang, num = get_lang_and_num(request)
    min_syl = get_number(request.POST.get('min-syl', 1))
    max_syl = get_number(request.POST.get('max-syl', 1))
    if get_bool(request.POST.get('mimic-text-source', 'false')):
        source_txt = request.POST.get('text-source', '')
        txt = mimic_text_with_random_syllables(lang, source_txt)
    else:
        words = get_random_syllables_words(lang, num, min_syl, max_syl)
        txt = format_words(words)
    return HttpResponse(txt)

def random_with_criterias(request):
    lang, num = get_lang_and_num(request)
    starts_with = request.POST.get('starts-with', '')
    starts_with_inv = get_bool(request.POST.get('starts-with-inv', ''))
    ends_with = request.POST.get('ends-with', '')
    ends_with_inv = get_bool(request.POST.get('ends-with-inv', ''))
    contains = request.POST.get('contains', '').split(',')
    syl_qty = get_number(request.POST.get('syl-qty', ''))
    max_letter_qty = get_number(request.POST.get('max-letter-qty', ''))
    min_letter_qty = get_number(request.POST.get('min-letter-qty', ''))
    min_letter_qty = get_number(request.POST.get('min-letter-qty', ''))
    consonants_in_a_row = get_number(request.POST.get('consonants-in-a-row', ''))
    words = get_random_words_with_criterias(lang, num, starts_with, starts_with_inv,
        ends_with, ends_with_inv, contains, syl_qty, max_letter_qty, min_letter_qty,
        consonants_in_a_row)
    txt = format_words(words)
    return HttpResponse(txt)

def wikipedia_random_words(request):
    num = get_number(request.POST.get('num', 1))
    txt = get_wikipedia_random_words(num)
    return HttpResponse(txt)
    
# -----
def get_lang_and_num(request):
    lang = request.POST.get('lang', 'fr')
    num = get_number(request.POST.get('num', 1))
    return lang, num

def get_number(n):
    if type(n) is str:
        if n.isnumeric():
            n = int(n)
        else:
            n = 0
    return n

def get_bool(b):
    return b =='true'

def format_words(words):
    txt = ' '.join(words)
    if len(txt) == 0:
        txt = '_'
    return txt