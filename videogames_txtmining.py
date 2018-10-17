# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 21:28:14 2018

@author: user
"""

from datetime import datetime
from elasticsearch import helpers, Elasticsearch
es = Elasticsearch()
import csv
import requests
from lxml import html
import collections
from urllib.parse import urljoin
from elasticsearch import Elasticsearch
import json    
import pandas as pd
import os
import nltk
from textblob import TextBlob




#directory = r'C:\Users\user\Documents\year 2\text minng'
res = requests.get('http://localhost:9200')
print (res.content)
es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])



file = r'C:\Users\user\Documents\year 2\text minng\Video_Games_5.json'

df = pd.read_json(file, lines = True)


data = df.to_json(orient='records', lines=True)
cols = list(df.columns)
print (cols)



#let's fix the datetime field for python
df['reviewTime'] = pd.to_datetime(df['reviewTime'], format='%m %d, %Y')
print (df.columns)


#what are the most reviewed items?
df2=df['asin'].value_counts()
print(df2)
#who are the most prolific reviewers?
df3=df['reviewerID'].value_counts()
print(df3)
#what are the most recently reviewed items?
df4 = df.sort_values(by=['reviewTime'], ascending=False)
df4.head
df4[['asin','reviewTime','overall']]

#what kind of hashtags do prolific hashtag users use in videogame reviews?
df['hastags'] = df['reviewText'].apply(lambda x: len([x for x in x.split() if x.startswith('#')]))
    
df[['reviewText','hastags']].head(10)
df.head(10)
df.columns
dfsorted = df.sort_values(by=['hastags'], ascending=False)
dfsorted[['reviewText','hastags']].head(20)
dfsorted.count

#view the actual text in Kibana

csvPath2 = r'C:\Users\user\Documents\year 2\text minng\groupproject_hashytags40.csv'
data2 = df.to_csv(orient= records, lines = True)

with open(csvPath2, encoding='utf-8') as y:
    READER = csv.DictReader(y)
    helpers.bulk(es, READER, index='mallikav40', doc_type='mallikag40')

del y
   
#now create the index pattern in Kibana but select "I don't want to use the time filter."
#many of these "#" are not being used as hashtags but as number symbols.


#did unhappy reviewers have installation problems, like I do for everything python or textmining related?
#using Kibana-discover tab made a new csv out of 'reviewText : "install*"' and <3 star rating query.

file2 = r'C:\Users\user\Documents\year 2\text minng\New Saved Search.csv'

WANTED = 40 


with open(file2) as searchfile:
    for line in searchfile:
        left,sep,right = line.partition('Install')
        if sep:  
            print(sep,right[:WANTED])
            
#produces good snapshot of install problems faced by reviewers not happy with the product.

#THE END            
            
