import pandas as pd 
from gensim import corpora, models, similarities
import preprocesado as pp

long_descriptions = pd.read_excel("Q:/Analytics/Proyectos/publications/data/linkedin/Book1.xlsx", sheetname=0)
short_descriptions = pd.read_excel("Q:/Analytics/Proyectos/publications/data/linkedin/Book2.xlsx", sheetname=0)
titles = pd.read_excel("Q:/Analytics/Proyectos/publications/data/linkedin/Book3.xlsx", sheetname=0)
ubicacion = pd.read_excel("Q:/Analytics/Proyectos/publications/data/linkedin/folletos_cursos.xlsx", sheetname=0)


# 2 listas, 1 cada columna
#using a single bracket returns a series and tolist() works on series of a panda dataframe
listofkeys_sd = short_descriptions.iloc[:,0].tolist()
listofvalues_sd = short_descriptions.iloc[:,1].tolist()

#merge the 2 lists into a list of tuples 
tuple_sd = zip(listofkeys_sd, listofvalues_sd)

#make a list for the descriptions with the same key, 
#then make a dictionary of these lists
from collections import defaultdict
sd_dictionary = defaultdict(list)

#update the short description dictionary to only hold the non-multiple 
#short description ids
for key, value in tuple_sd:
    if 'key' in sd_dictionary.keys(): 
        del(sd_dictionary[key])
    else :
        sd_dictionary[key]=value
    
#which ids is that? make a list of it
#dictlistofids = []
#for key, value in sd_dictionary.iteritems():
 #   temp = [key]
  #  dictlistofids.append(temp)

#list of titles and lists straight from excel (including repeated ids)
listofkeys_titles = titles.iloc[:,0].tolist()
listofvalues_titles = titles.iloc[:,1].tolist()

#what indeces of the two lists are the ones with no repeats 
#dictlistofids =map(lambda x: x[0],dictlistofids)
#indeces = map(lambda x:listofkeys_titles.index(x), dictlistofids)
#listofkeys_titles = map(lambda x: listofkeys_titles[x],indeces)
#listofvalues_titles = map(lambda x: listofvalues_titles[x],indeces)

tuple_titles = zip(listofkeys_titles, listofvalues_titles)

#make dictionary of titles and ids for the ids that dont have repeats 
titles_dictionary = defaultdict(list)
for key, value in tuple_titles: 
    if key in sd_dictionary :     
        titles_dictionary[key] = value

# 2 listas, 1 cada columna 
listofkeys_ld = long_descriptions.iloc[:,0].tolist()
listofvalues_ld = long_descriptions.iloc[:,1].tolist()

#make a dictionary from the 2 lists for the long descriptions
ld_dictionary = defaultdict(list)
tuple_ld = zip(listofkeys_ld, listofvalues_ld)
    
 #for every "nan" value in the long description dictionary, replace with the 
 #value from the short description dictionary of that key. 
for key, value in tuple_ld:
    if key in sd_dictionary :
        ld_dictionary[key] = value
    if (not (value == value) or '#??????##??????##??????##??????##??????##??????' in value):
             ld_dictionary[key] = sd_dictionary[key]


the_themes = list(set(listofvalues_sd))

appended_ld_dictionary = defaultdict(list)
def check_ld(x) :
    appended_ld_dictionary[x] = []
    for key, value in sd_dictionary.iteritems():
        if value == x:
            appended_ld_dictionary[x].append(ld_dictionary[key])
ignore1 = map(check_ld, the_themes)

appended_titles_dictionary = defaultdict(list)  
def check_titles(x) :
    appended_titles_dictionary[x] = []
    for key, value in sd_dictionary.iteritems():   
        if value == x: 
            appended_titles_dictionary[x].append(titles_dictionary[key])       

ignore2 = map(check_titles, the_themes)

for key,value in appended_ld_dictionary.items() : 
   appended_ld_dictionary[key] = ". ".join(value)
    
for key,value in appended_titles_dictionary.iteritems() : 
    appended_titles_dictionary[key] = "".join(value)    
#tf idf
#create the corpora for short description dictionary
# listofvalues_sd is my document
#stoplist = set('for a of the and to in'.split())
#texts = [[word for word in document.lower().split() if word not in stoplist] 
#for document in listofvalues_sd]


#stanford_classifier = 'C:/Users/mchiquier/Downloads/stanford-ner-2014-06-16/stanford-ner-2014-06-16/classifiers/all.3class.distsim.crf.ser.gz'
#stanford_ner_path = 'C:/Users/mchiquier/Downloads/stanford-ner-2014-06-16/stanford-ner-2014-06-16/stanford-ner.jar'


#st = StanfordNERTagger(stanford_classifier, stanford_ner_path, encoding='utf-8')

#st = StanfordNERTagger(,)
#result = st.tag('Mia Chiquier trabaja en AFI y le gusta mucho Rocio'.split())
documents = map(pp.limpiar, appended_titles_dictionary.values())
documents = map(pp.lematizacion_limpieza, documents)
#create the corpus3


#
#st = StanfordNERTagger(stanford_classifier, stanford_ner_path, encoding='utf-8')
#
#st = StanfordNERTagger(,)
#result = st.tag('Mia Chiquier trabaja en AFI y le gusta mucho Rocio'.split())


###TOP 30 TITLES
documents = map(pp.limpiar_cursos, appended_titles_dictionary.values())

import nltk
import numpy as np
import json

from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer(tokenizer=nltk.word_tokenize)
tfs = tfidf.fit_transform(documents)
ourmatrix = tfs.toarray()

feature_names = tfidf.get_feature_names()
response = tfidf.transform(documents)

top15wordsarray = []
for a in range(len(ourmatrix)) : 
    top15_title = (-ourmatrix).argsort()[a][:30] 
    tf_idf = ourmatrix[a][top15_title]
    top15words_title = []
    for b in range(len(top15_title)) : 
        top15words_title.append(feature_names[top15_title[b]])
        top15 = dict(zip(top15words_title,tf_idf))
    top15wordsarray.append(top15words_title)
    
top30_tfidf_title = dict(zip(the_themes,top15wordsarray))

with open('temas_title_tfidf.json', 'w') as fp:
    json.dump(top30_tfidf_title, fp)
    
   
#from pprint import pprint  # pretty-printer
#pprint(texts)

#create the corpus
#dictionary = corpora.Dictionary(texts)
#print(dictionary)
#print(dictionary.token2id)
#corpus = [dictionary.doc2bow(text) for text in texts]
#print(corpus)

#tfidf
#tfidf = models.TfidfModel(corpus)
#corpus_tfidf = tfidf[corpus]

#weight_{i,j} = frequency_{i,j} * log_2(D / document_freq_{i})
#index = similarities.MatrixSimilarity(tfidf[corpus])
#sims = index[corpus_tfidf]

#listofkeys_ubicacion = ubicacion.iloc[6:,0].tolist()
#listofvalues_ubicacion = ubicacion.iloc[6:,4].tolist()
#listofvalues_ubicacion = map(lambda x : x.replace('\\', '/'), listofvalues_ubicacion)
#tuples_folletos = zip(listofkeys_ubicacion, listofvalues_ubicacion)

#folletos_words = defaultdict(list)

#import pyPdf
#counter = 0

#def letsopen(path) : 
 #   error = []
  #  global counter
   # counter = counter + 1
    #if (counter % 200 == 0) :
     #   print(str(counter))
    #try:
        
    #except:
     #   error.append(path)
    #return error
    
 #reverse the direction of backslash   

    
#for key,value in tuples_folletos: 
 #   try : 
  #      pdf = pyPdf.PdfFileReader(open(value,'rb'))
   #     thetext = ""
    #    if pdf.isEncrypted:
     #       pdf.decrypt('')
      #  else : 
       #     pdf = pdf
        #
       # for pagen in range(pdf.getNumPages())  :
        #    page =  pdf.getPage(pagen)
         #   folletos_words[key] = folletos_words[key] + page.extractText()
   # except:
    #    continue
        
#appended_folletos_dictionary = defaultdict(list)
#def check_folletos(x) :
 #   appended_folletos_dictionary[x] = []
  #  for key, value in sd_dictionary.iteritems():
   #     if value == x:
    #        appended_folletos_dictionary[x].append(folletos_words[key])

#ignore1 = map(check_folletos, the_themes)


#for key,value in appended_folletos_dictionary.items(): 
#    appended_folletos_dictionary[key] = [x for x in appended_folletos_dictionary[key] if x!=[]]
 #   appended_folletos_dictionary[key] = ". ".join(appended_folletos_dictionary[key])
  #  appended_folletos_dictionary[key] = pp.limpiar_cursos(appended_folletos_dictionary[key])


#documents2 = map(pp.limpiar_cursos, appended_folletos_dictionary.values())

#tfidf = TfidfVectorizer(tokenizer=nltk.word_tokenize)
#tfs2 = tfidf.fit_transform(documents2)
#ourmatrix2 = tfs2.toarray()

#feature_names2 = tfidf.get_feature_names()
#response2 = tfidf.transform(documents2)

#top15wordsarray2 = []
#for a in range(len(ourmatrix2)) : 
 #   top15_ld2 = (-ourmatrix2).argsort()[a][:15] 
  #  top15words_ld2 = []
   # for b in range(len(top15_ld2)) : 
    #    top15words_ld2.append(feature_names2[top15_ld[b]])
    # top15wordsarray2.append(top15words_ld2)










