import wikipedia as wiki
from typing import List
from app.constants import BLANK, QUESTION, ANSWER, OPTIONS, NUMBER_OF_ANSWERS, FULL_QUESTION
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
import pandas as pd
from random import choice, shuffle
import re

def get_tfidf(wiki_data: List[str]):
    """Returns top 5 tfidf words ranked from highest to lowest in a dictionary"""

    vectorizer = TfidfVectorizer(use_idf=True, stop_words=set(ENGLISH_STOP_WORDS))
    tfIdf = vectorizer.fit_transform(wiki_data)
    df = pd.DataFrame(tfIdf[0].T.todense(), index=vectorizer.get_feature_names(), columns=["TF-IDF"])
    df = df.sort_values('TF-IDF', ascending=False)
    df = df.nlargest(10, 'TF-IDF')
    tfidflist = list(df.index.values)

    return tfidflist

def format_sentence(sentence: str)-> str:
    """Returns a correctly formatted sentence
    """

    sentence += '.'
    sentence = sentence.strip()
    if sentence[0].isalpha():
        sentence = sentence.capitalize()

    return sentence

    
    
def get_data(name_of_wiki_page: str):
    """Returns the data from wikipedia page name_of_wiki_page, with each index in the list being a sentence 
    """

    wiki_search = wiki.search(name_of_wiki_page)
    name_of_wiki_page_caps = name_of_wiki_page.upper()
    wiki_search_caps = [item.upper() for item in wiki_search]

    if name_of_wiki_page_caps in wiki_search_caps:
        index = wiki_search_caps.index(name_of_wiki_page_caps)
        updated_search_query = wiki_search[index]
        all_data = wiki.page(updated_search_query, auto_suggest=False).content
    else:
        updated_search_query = wiki.suggest(name_of_wiki_page)
        all_data = wiki.page(updated_search_query).content

    all_data = all_data.replace('\n',' ')
    all_data = all_data.replace('\t',' ')
    all_data = all_data.replace('=', " ")
    split_data = all_data.split('. ')

    return split_data, updated_search_query

def find_usable_sentences(wikipedia_page: List[str], special_word: str) -> List[str]:
    """returns a list of usable sentences using the information recieved from a wikipedia page, 
    finds all usable sentences that have special_word in it

    >>> find_usable_sentences(['AB','ac','ad','bb','dd'], 'a')
    ['AB','ac','ad']
    """

    possible_sentences = []

    for sentence in wikipedia_page:
        if re.search(r'\b' + special_word.lower() + r'\b', sentence.lower()):
            possible_sentences.append(sentence)

    return possible_sentences

def remove_special_word(special_word: str, sentence: str) -> str:
    """ Returns possible_sentences with special_word removed from every index,
    replaced by BLANK"""

    blanked_sentence = sentence.lower().replace(special_word, BLANK)
    
    return blanked_sentence

def get_questions(qdict) -> List[str]:
    questions = []
    for item in qdict:
        questions.append(item[FULL_QUESTION])

    return questions

def create_questions(name_of_wiki_page: str):
    """Returns a list of questions
    """
    wiki_data, updated_query = get_data(name_of_wiki_page)
    top_ten = get_tfidf(wiki_data)
    question_list = []

    for key_word in top_ten:

        possible_options = top_ten[:]
        possible_options.remove(key_word)

        possible_sentences = find_usable_sentences(wiki_data, key_word)

        full_question = choice(possible_sentences)
        all_questions = get_questions(question_list)

        if full_question in all_questions and len(possible_sentences) > 1:
            possible_sentences.remove(full_question)
            full_question = choice(possible_sentences)

        full_question_replaced = remove_special_word(key_word, full_question)

        other_options = []
        for i in range(NUMBER_OF_ANSWERS - 1):
            option = choice(possible_options)

            other_options.append(option)
            possible_options.remove(option)

        full_question_replaced = format_sentence(full_question_replaced)
        other_options.append(key_word)
        shuffle(other_options)
        question_list.append({QUESTION: full_question_replaced, ANSWER: key_word, OPTIONS: other_options, FULL_QUESTION: full_question})

    shuffle(question_list)
    return question_list, updated_query
