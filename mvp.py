#!/usr/bin/env python
# coding: utf-8

# In[4]:


import os



# In[25]:


def flatten_list(l):
    return [item for sublist in l for item in sublist]


# In[27]:


EXISTING_ARTICLES = flatten_list([walk[2] for walk in os.walk('source/articles') if walk[2]] )
EXISTING_ARTICLES


# In[2]:


# get GPT
import openai

openai.api_key = open('openai.apikey').read()
openai.Model.list()

""


# In[41]:


def get_questions():
    SET_ROLE_PROMPT = f'You are an AI entity designed to find questions people can ask. ' \
    + 'You provide anything exaclty in the requested format by the user.'

    PROMPT = "You have the following questions:\n\n" + '\n'.join(EXISTING_ARTICLES) \
    +f"Give me 10 NEW questions starting with 'How' or 'Why'. Do not write anything else, only the questions. Every question should be in a new line and end with a question mark. Do not give me any of the existing questions."

    message_history = [
            {"role": "system", "content": SET_ROLE_PROMPT},
            {"role": "user", "content": PROMPT},    
    ]

    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=message_history)
    msg = completion.choices[0].message.content
    
    return msg


# In[42]:


def get_article_for_question(q):
    SET_ROLE_PROMPT = f'Your name is Marcus Applebee. You are a content creator with more than 10 years of experience specialising in SEO-optimised posts. ' \
    +'You always provide clear answers to questions. You take the question, and break it into pieces. ' \
    +'You assume the asker doesnt know anything about the topic so you introduce every piece of information in sequence explainin every concept you need to answer the question. ' \
    +'Your outputs should be engaging and professional. You use markdown to format your articles.\n\n' \
    +'Important: Do NOT use placeholders for date location etc.' 

    PROMPT = f"Write me a news article answering the following question in detail: {q}"

    message_history = [
            {"role": "system", "content": SET_ROLE_PROMPT},
            {"role": "user", "content": PROMPT},    
    ]


    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=message_history)
    msg = completion.choices[0].message.content
    
    return msg


# In[43]:


import random

# return a tuple with three elements:
# year, month, day. All random between 2016 and now.
def get_random_date():
    year = str(2016 + int(random.random()*7)).zfill(4)
    month = str(int(random.random()*12)+1).zfill(2)
    day = str(int(random.random()*30)+1).zfill(2)
    return (year, month, day)

date = get_random_date()
date


# In[44]:


# API call
QUESTIONS = get_questions().split("\n")


# In[45]:


QUESTIONS


# In[46]:


ARTICLES = {}

# multiple API calls
for q in QUESTIONS:
    q_url = q.replace(" ", "-").replace("?", "")
    path = f"./articles/{q_url}.md"
    if os.path.exists(path):
        print(f"<{q}>: article already exists ")
        continue
    else:
        print(f"<{q}>: creating article")
        article = get_article_for_question(q)
        ARTICLES[q_url] = article


# In[49]:


os.makedirs(os.path.join('source', 'articles', *date), exist_ok=True)

for qurl, article in ARTICLES.items():
    open(os.path.join('source', 'articles', *date, qurl + '.md'), 'w').write(article)   


# In[ ]:




