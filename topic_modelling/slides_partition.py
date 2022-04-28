# In[103]:


# подключаем необходимые библиотеки

import numpy as np
import scipy
from scipy.spatial import distance

import gensim
from gensim import corpora
from gensim.models import LdaModel
from gensim.utils import simple_preprocess

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize

from pymystem3 import Mystem


# In[104]:


# загружаем словарь часто используемых в русском языке слов

nltk.download('stopwords')
stop_words = stopwords.words('russian')


# In[105]:


# открываем файл на чтение

with open("C:/Users/kisnikser/Documents/GitHub/Intelligent-Presentation-Generator/topic_modelling/text.txt", "r", encoding = "utf-8") as doc:
    text = doc.read()
    doc.close()


# In[106]:


# функция предобработки текста - возвращает (список предложений, токенизированный текст, список слов)

def preprocess_text(text):
    mystem = Mystem() # лемматизатор (приводит слова к начальной форме)
    preprocessed_text = list() # токенизированный текст (содержит основные слова, приведенные к начальной форме)
    sentences = sent_tokenize(text, language = "russian") # текст, разбитый на предложения
    for sentence in sentences:
        tokenized_sentence = simple_preprocess(sentence, deacc = False)
        tokenized_sentence_without_stop_words = [word for word in tokenized_sentence if word not in stop_words]
        lemmatized_sentence = [word for word in mystem.lemmatize(" ".join(tokenized_sentence_without_stop_words)) if word != " " and word != "\n"]
        preprocessed_text.append(lemmatized_sentence)
    words = [word for sentence in preprocessed_text for word in sentence] # список всех слов в тексте
    return sentences, preprocessed_text, words


# In[107]:


sentences, preprocessed_text, words = preprocess_text(text)


# In[114]:


count = len(sentences)


# In[109]:


# создаем словарь из текста (dictionary.token2id - пары: word - id)
# создаем корпус слов (пары: id - count)

dictionary = corpora.Dictionary([words])
corpus = [dictionary.doc2bow(words)]


# In[110]:


# обучаем LDA модель (по умолчанию пока что стоит 3 темы в тексте)

LDA_model = LdaModel(corpus = corpus, id2word = dictionary, num_topics = 3, passes = 1)


# In[111]:


# создаем словарь с вероятностями принадлежности слов к темам (пары: word - (p1, p2, ..., pn))

words_topics_dict = dict()
for id_, word in enumerate(list(dictionary.token2id)):
    topics = LDA_model.get_term_topics(id_, minimum_probability=0)
    probs = [topics[i][1] for i in range(len(topics))]
    words_topics_dict[word] = probs


# In[112]:


# создаем словарь с вероятностями принадлежности предложений к темам (пары: sentence - (p1, p2, ..., pn))

sentences_topics_dict = dict()
for k, sentence in enumerate(preprocessed_text):
    sentence_words_topics = [words_topics_dict.get(word) for word in sentence]
    sentences_topics_dict[k] = list(np.mean(sentence_words_topics, axis = 0))


# In[115]:


# определяем косинусные расстояния между соседними предложениями (n предложений -> (n-1) расстояний)

sentences_distances = [distance.cosine(sentences_topics_dict.get(u), sentences_topics_dict.get(v)) for (u, v) in zip(range(count - 1), range(1, count))]


# In[116]:


# функция возвращает топ k-1 предложений, после которых стоит начинать новый слайд (k - количество тем)

def slides_partition(k):
    return sorted(list(reversed(list(np.argsort(sentences_distances))))[:k-1])


# In[127]:


def get_sections(k):
    nums = slides_partition(k)
    sections_1 = [" ".join(sentences[u+1:v+1]) for (u, v) in zip([0, *nums[:-1]], nums)]
    sections_2 = [" ".join(sentences[nums[-1]+1:])]
    sections = [*sections_1, *sections_2]
    return sections


# In[132]:


sections = get_sections(3)


# %%
print(sections)
# %%
