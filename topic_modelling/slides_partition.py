#!/usr/bin/env python
# coding: utf-8

# In[31]:


# подключаем необходимые библиотеки

#-----------------------------------------
# библиотеки для работы основной части программы
import numpy as np
from scipy.spatial import distance

import gensim
from gensim import corpora
from gensim.models import LdaModel
from gensim.utils import simple_preprocess

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize

from pymystem3 import Mystem

import os
import sys
#-----------------------------------------
# библиотеки для поиска изображений в интернете
from bing_image_downloader import downloader
#from PIL import Image


# In[32]:


# дополнительные стоп-слова русского языка
with open("..\\topic_modelling\\stopwords_ru.txt", "r", encoding = "utf-8") as doc:
    stop_words_ru = doc.read().splitlines()
    doc.close


# In[33]:


# загружаем словарь часто используемых в русском языке слов

nltk.download('stopwords')
stop_words = stopwords.words('russian')
stop_words.extend(stop_words_ru)


# In[34]:


# функция открытия файла на чтение

def readFile():
    file = sys.argv[1]
    with open(file, "r", encoding = "utf-8") as doc:
        text = doc.read()
        doc.close()
    return text


# In[35]:


# функция предобработки текста - возвращает (список предложений, токенизированный текст, список слов)

def preprocessText(text):
    mystem = Mystem() # лемматизатор (приводит слова к начальной форме)
    preprocessed_text = list() # токенизированный текст (содержит основные слова, приведенные к начальной форме)
    sentences = sent_tokenize(text, language = "russian") # текст, разбитый на предложения
    for sentence in sentences:
        tokenized_sentence = simple_preprocess(sentence, deacc = False)
        tokenized_sentence_without_stop_words = [word for word in tokenized_sentence if word not in stop_words]
        lemmatized_sentence = [word for word in mystem.lemmatize(" ".join(tokenized_sentence_without_stop_words))                              if word != " " and word != "\n"]
        preprocessed_text.append(lemmatized_sentence)
    words = [word for sentence in preprocessed_text for word in sentence] # список всех слов в тексте
    return sentences, preprocessed_text, words


# In[36]:


# функция возвращает словарь с вероятностями принадлежности предложений к темам (пары: sentence - (p1, p2, ..., pn))
# и обученную на тексте модель LDA_model

def getSentencesTopics(preprocessed_text, n):
    dictionary = corpora.Dictionary(preprocessed_text)
    corpus = [dictionary.doc2bow(sentence) for sentence in preprocessed_text]
    # обучаем LDA модель
    LDA_model = LdaModel(corpus = corpus, id2word = dictionary, num_topics = n, alpha = 'auto', passes = 100)
    # создаем словарь с вероятностями принадлежности предложений к темам (пары: sentence - (p1, p2, ..., pn))
    sentences_topics_dict = dict()
    for k, sentence in enumerate(preprocessed_text):
        sentence_topics = LDA_model.get_document_topics(dictionary.doc2bow(sentence), minimum_probability = 0)
        sentences_topics_dict[k] = [prob[1] for prob in sentence_topics]
    return sentences_topics_dict, LDA_model


# In[37]:


# функция возвращает расстояния между соседними предложениями

def getSentencesDistances(sentences_topics_dict):
    count = len(sentences_topics_dict)
    sentences_distances = [distance.cosine(sentences_topics_dict.get(u), sentences_topics_dict.get(v))                           for (u, v) in zip(range(count - 1), range(1, count))]
    return sentences_distances


# In[38]:


# функция возвращает топ n-1 предложений, после которых стоит начинать новый слайд (n - количество тем)

def splitText(sentences_distances, n):
    return sorted(list(reversed(list(np.argsort(sentences_distances))))[:n-1])


# In[39]:


# функция возвращает ключевые слова каждого абзаца

def getKeyWords(LDA_model, sentences_topics_dict, n):
    # создаем список ключевых слов каждой темы
    topics_words = [LDA_model.show_topics(num_words = 1, formatted = False)[k][1][0][0] for k in range(n)]
    # создаем список с вероятностями принадлежности всякого предложения каждой теме
    sentences_topics_list = list(sentences_topics_dict.values())
    # создаем список расстояний между соседними предложениями
    sentences_distances = getSentencesDistances(sentences_topics_dict)
    # создаем список номеров предложений, после которых стоит начинать новый слайд
    nums = splitText(sentences_distances, n)
    # создаем список номеров тем каждого абзаца
    topics_1 = [np.argmax(np.mean(sentences_topics_list[0:nums[0]+1], axis = 0))]
    topics_2 = [np.argmax(np.mean(sentences_topics_list[u+1:v+1], axis = 0)) for (u, v) in zip(nums[:-1], nums[1:])]
    topics_3 = [np.argmax(np.mean(sentences_topics_list[nums[-1]+1:], axis = 0))]
    topics = [*topics_1, *topics_2, *topics_3]
    # создаем список ключевых слов каждого абзаца
    sections_words = [topics_words[k] for k in topics]
    return sections_words


# In[40]:


# функция разделения текста на абзацы - возвращает список абзацев

def getSections(sentences, sentences_distances, n):
    nums = splitText(sentences_distances, n)
    sections_1 = [" ".join(sentences[0:nums[0]+1])]
    sections_2 = [" ".join(sentences[u+1:v+1]) for (u, v) in zip(nums[:-1], nums[1:])]
    sections_3 = [" ".join(sentences[nums[-1]+1:])]
    sections = [*sections_1, *sections_2, *sections_3]
    return sections


# In[41]:


def getImages(sections_words):
    for k, word in enumerate(sections_words):
        downloader.download(word, limit = 1, output_dir = "../topic_modelling/images/image_" + str(k),                            adult_filter_off = False, force_replace = False, timeout = 60, verbose = False)
        os.system("rename ..\\topic_modelling\\images\\image_" + str(k) + "\\" + word + "\\* image_" + str(k) + ".jpg")
        os.system("move ..\\topic_modelling\\images\\image_" + str(k) + "\\" + word + "\\image_" + str(k) + ".jpg"                  + " ..\\topic_modelling\\images")
        os.system("rmdir /S /Q ..\\topic_modelling\\images\\image_" + str(k))


# In[42]:


# MAIN METHOD: функция разделения текста на абзацы (выполняет все действия последовательно)

def makeSections(n):
    text = readFile()
    sentences, preprocessed_text, words = preprocessText(text)
    sentences_topics_dict, LDA_model = getSentencesTopics(preprocessed_text, n)
    sections_words = getKeyWords(LDA_model, sentences_topics_dict, n)
    getImages(sections_words)
    sentences_distances = getSentencesDistances(sentences_topics_dict)
    sections = getSections(sentences, sentences_distances, n)
    return sections, sections_words


# In[43]:


# функция записи абзацев в отдельные файлы

def printSections(sections):
    names = []
    for i, section in enumerate(sections):
        name = "section_" + str(i) + ".txt"
        names.append(name)
        with open("..\\latex_presentation\\" + name, "w", encoding = "utf-8") as fout:
            fout.write(section)
            fout.close()
    return names


# In[44]:


# функция записывает названия слайдов в отдельный файл

def writeKeyWords(keywords):
    with open("..\\latex_presentation\\keywords.txt", "w", encoding = "utf-8") as fout:
        for word in keywords:
            fout.write(word + "\n")
        fout.close()


# In[47]:


sections, sections_words = makeSections(3)
sections_words_capitalized = [word.capitalize() for word in sections_words]
writeKeyWords(sections_words_capitalized)
names = printSections(sections)
os.chdir("..\\latex_presentation")
os.system(".\\main.exe " + " ".join(names))

