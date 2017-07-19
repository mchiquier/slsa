# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 09:35:52 2017

@author: mchiquier
"""

import pandas as pd 
from collections import defaultdict
import preprocesado as pp
import json
import parseLinkedin as pl
#import os
#import glob
from datetime import datetime

global file_list1 
file_list1 = []
global file_list2 
file_list2 = []
global file_listofjsons
file_listofjsons = []

#dir_name = 'Q:/Analytics/Proyectos/publications/output/linkedin/linkedin_escuela'
#pattern = os.path.join(dir_name,'*.pdf')
#file_list0 = glob.glob(pattern)
#we will not use the above as file_list0, instead we will use the list of names that we want in pdf names
with open ('Q:/Analytics/Proyectos/publications/output/linkedin/dict_name_id.json') as f: 
    mydata = json.load(f)
    mydata = {v.lower(): k for k, v in mydata.iteritems()}
    
## i have to write a function that will extract the name of the pdf of the name of the person i want
##check in dictionary of id of pdf to person name is the person name of the new_dict is there
## if it is in this dictionary then find out the id number and extract the pdf of this id number
##make a list of pdf files that have this 



def check(name) : 
    #MAKE SURE BOTH THE NAMES IN MYDATA AND THE NAMES IN THE FILE_LIST0 AKA THE APPENDED DICT_NAMESPERTHEME 
    #ARE BOTH LOWER CASE AND WITHOUT PUNCTUATION AKA CLEAN IT UP 
    try:
            index = mydata[name]
            pdf = 'Q:/Analytics/Proyectos/publications/output/linkedin/linkedin_escuela/a (' + str(index) + ').pdf'
            global file_list1
            file_list1.append(pdf)
    except:
        print('the name wont come up in the index dictionary' + name)
       

def extract_studentlol((path,j)):
    try :     
        cv = pl.cv_to_json(path)
        educacion = cv["Education"]
        name = cv['Basic']['name']
        years = []
        curso_afi = []
        global file_list2
        for dic in educacion:
            if('Afi' in dic['universidad'] or 'AFI' in dic['universidad'] or 
               'EFA' in dic['universidad'] or 'A.F.I.' in dic['universidad'] or
            'Escuela de Finanzas' in dic['universidad']):
                file_list2.append(path)
                print('in AFI: appended', j)
            else: 
                print('Not educated in AFI',j)
        print('there is no education in pdf')
    except:
       print('try except error')
        
        
#file_list0 = zip(file_list0, range(len(file_list0)))
#n = map(extract_student,file_list0)

i = 1
def remove_exp((path,j)):
    global file_listofjsons
    desc_exp = {}
    global i
    i = i + 1 
    if(i % 100==0):
        print(i)
    try:
        cv = pl.cv_to_json(path)
        educacion = cv["Education"]
        name = cv['Basic']['name']
        years = []
        curso_afi = []
        for dic in educacion:
            if('Afi' in dic['universidad'] or 'AFI' in dic['universidad'] or 
               'EFA' in dic['universidad'] or 'A.F.I.' in dic['universidad'] or
            'Escuela de Finanzas' in dic['universidad']):
                years.append(dic['year_fin'])
                curso_afi.append(dic)
        experiencia = cv['Experience']
        experiencia_post = []

        try:  
            years = [x[0] for x in years]
            for year in years:
                for exp in experiencia:
                    if(datetime.strptime(exp['year_inicio'][0], '%Y') < datetime.strptime(year, '%Y')):
                        experiencia_post.append(exp)               
            experiencia = experiencia_post
            exp =experiencia
        except:
            exp = experiencia        
       
        educacion = cv["Education"]
        educacion_pre = []
        try:
            for year in years:
                for ed in educacion:
                    if(datetime.strptime(ed['year_fin'][0], '%Y') < datetime.strptime(year, '%Y')):
                        educacion_pre.append(ed)               
            educacion = educacion_pre
            educacion =  map(lambda x: x['titulacion'], educacion)
        except:
            educacion =  map(lambda x: x['titulacion'], educacion)

        lista_duracion = [x['duracion'] for x in exp]
        duracion = []   
        if( 'menos de un a\xc3\xb1o' in lista_duracion and len(lista_duracion) == 1):
            duracion = "Menos de un año"
        else: 
            if('less than a year' in lista_duracion and len(lista_duracion) == 1):
                duracion = "Menos de un año"
            else:
                while('menos de un a\xc3\xb1o' in lista_duracion):
                   lista_duracion.remove('menos de un a\xc3\xb1o')
                while('less than a year' in lista_duracion):
                   lista_duracion.remove('less than a year')
                duracion = map(pl.duracion_parcial, lista_duracion)
                duracion = sum(duracion)
                
        experiencia_total = duracion
        descripcion_exp = map(lambda x: x['descripcion'], experiencia)
        descripcion_exp = '\n'.join(descripcion_exp)
        summary = cv["Summary"]

        educacion = '\n'.join(educacion)
        puestos  = map(lambda x: x['puesto'],experiencia)
        puestos = ' '.join(puestos)
        texto = [summary,descripcion_exp,puestos,educacion]
        texto = ' '.join(texto)
        texto = pp.limpiar_cursos(texto)
        desc_exp['descripcion'] = texto
        desc_exp['experiencia_total'] = experiencia_total
        desc_exp['cursos_afi'] = curso_afi
        id_candidato = path.split('(')[1].split(')')[0]
        filename = 'text_' + str(id_candidato)+ '.json'
        with open(filename, 'w') as fp:
            json.dump(desc_exp, fp,ensure_ascii = False,encoding= 'utf-8') 
        file_listofjsons.append('C:/Users/mchiquier/Desktop/publications/00_linkedIn/' + filename)
    except:
        print('ERROR',j)

thestudents = pd.read_excel("Q:/Analytics/Proyectos/publications/data/linkedin/ContactosEscuela.xlsx", sheetname=0)
coursetothemes = pd.read_excel("Q:/Analytics/Proyectos/publications/data/linkedin/descripcion_cursos.xlsx", sheetname=0)
themeidtoname = pd.read_excel("Q:/Analytics/Proyectos/publications/data/linkedin/id_to_theme.xlsx", sheetname=0)

thestudents_courseid = thestudents.iloc[7:,32].tolist()
thestudents_lastname = thestudents.iloc[5:,6].tolist()
thestudents_firstname = thestudents.iloc[5:,5].tolist()
totalname = zip(thestudents_firstname, thestudents_lastname) 
totalnamefinal = []

#making one total name out of first and last name, this is the lsit from it
#create a one thing of first and last name
for names in totalname:
    first = names[0]
    second = names[1] 
    finalname = []
    if not isinstance(second, int): 
        if first == first :
            finalname = first
            if second == second :
             finalname = finalname + ' ' + second
             totalnamefinal.append(finalname)
             ''.join(totalnamefinal)

coursetothemes_courseid = coursetothemes.iloc[6:,0].tolist()
coursetothemes_themeid = coursetothemes.iloc[6:,5].tolist()

themeidtoname_id = themeidtoname.iloc[5:,0].tolist()
themeidtoname_name = themeidtoname.iloc[5:,1].tolist()

#creating a list of tuples that contain name and lastname
#creating a dictionary that will hold the total name and the courseid
courseid_studentname = dict(zip(thestudents_courseid, totalnamefinal))
courseid_themeid = dict(zip(coursetothemes_courseid, coursetothemes_themeid))
themeid_themename = dict(zip(themeidtoname_id, themeidtoname_name))
dict_namespertheme = defaultdict(list)


for courseid in courseid_studentname : 
    name = courseid_studentname[courseid]
    if courseid in courseid_themeid.keys():
        themeid = courseid_themeid[courseid]
        themename = themeid_themename[themeid]
        if themename in dict_namespertheme :
            dict_namespertheme[themename].append(name)
        else : 
             dict_namespertheme[themename]

finaldict = defaultdict(list)

thespecial = 'silvia cardoso'

for theme in dict_namespertheme : 
    global file_list1
    global file_list2
    global file_listofjsons
    file_list1 = []
    file_list2 = []
    file_listofjsons = []
    file_list0 = dict_namespertheme[theme]
    for index in range(len(file_list0)) : 
        file_list0[index] = file_list0[index].lower()
    a = map(check, file_list0)
    file_list1 = zip(file_list1, range(len(file_list1)))

    b = map(extract_studentlol, file_list1)
    file_list2n = zip(file_list2, range(len(file_list2)))
    cv_json = map(remove_exp,file_list2n)
    finaldict[theme] = file_listofjsons
   
superpersona_pertheme = defaultdict(list)

    
for key, value in finaldict.iteritems(): 
    if len(value) != 0 : 
        for path in value : 
            with open (path) as f: 
                person = json.load(f)
                desc = person["descripcion"] 
                if desc != '' : 
#         desc =  desc.encode('utf8', 'replace')
                    superpersona_pertheme[key].append(desc)
   


for key,value in superpersona_pertheme.iteritems() : 
   superpersona_pertheme[key] = "".join(value) 
     
#############TRANSLATE
#import traduccion
#from traduccion import translate

#text= superpersona_pertheme['Finanzas cuantitativas']
#traduccion.translate(text)

#for theme in superpersona_pertheme : 
 #   superpersona_pertheme[theme] = translate(superpersona_pertheme[theme])
###############

   
#make lsa with super person and the 21 themes: 
    #appended_titles_dictionary and one of superpersona_pertheme[key]
#make term-frequency matrix: 
from cursos import appended_titles_dictionary

titlespertheme_list = []
for key,value in appended_titles_dictionary.iteritems() : 
    titlespertheme_list.append(value)
#superpersona_asesoramientofinancerio_list.append(superpersona_pertheme['Asesoramiento financiero'])
    
from sklearn.feature_extraction.text import TfidfVectorizer
#NOW WE BEGIN LSA
import nltk
import numpy as np

tfidf = TfidfVectorizer(tokenizer=nltk.word_tokenize)
tfs = tfidf.fit_transform(titlespertheme_list)
titlespertheme_tfidf = tfs.toarray()

#choosing which eigenvalues of s to set to zero
import itertools
import sklearn
import pickle 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn import cluster
import scipy as sc
U, s, V = np.linalg.svd(titlespertheme_tfidf, full_matrices=False)
indeces = range(0,20)
list_of_perms = list(itertools.permutations(indeces,3))
b = 0
bestdiff = 100
besteigs = [0, 0, 0]
#for every permutation, we will assign these indeces' eigenvalues to zero, i.e. eliminating those eigenvectors
#for each_perm in list_of_perms:
#    #assign this permutation of 3 indeces to zero in the eigenvalue section 
#    def setindex (each_perm):
#      
#    #this will be the matrix of the LSA'd themes, i.e. each theme contains the titles of the courses that fit to that theme
#    vectorizer = TfidfVectorizer(tokenizer=nltk.word_tokenize, decode_error="replace")
#    tfidfmatrix = vectorizer.fit_transform(titlespertheme_list)
#    newvectormatrix = vectorizer.transform(list(superpersona_pertheme['Banca']))
#    newvectormatrix = newvectormatrix.toarray()
#    newvector = np.sum(newvectormatrix, axis = 0)
#    newvector = np.asarray(newvector.T)
##Load it later
#    for superpersonatheme in superpersona_pertheme: 
#        differenceforallthemes = 0
#        #here we are calculating the projection of the new document, and getting a matrix with the weighting of each word per topic
#        result = transformer.transform(loaded_vec.fit_transform(list(superpersona_pertheme['Banca'])))
#        #sum up all the word embeddings to get the document embedding
#     
#        
#        bestsimilarity = 0
#        differencepersuperpersona = 0
#        for actualtheme in range(0,20) :         
#        #find the corresponding theme for the superpersona theme
#        #the row of the vec_train matrix is a document and the row of sumresult is also a document
#            if np.dot(vec_train[actualtheme], sumresult) > bestsimilarity :
#                bestsimilarity = np.dot(vec_train[actualtheme], sumresult)
#                differencepersuperpersona = 1-bestsimilarity
#        if differencepersuperpersona != 1 : 
#         #this is the difference between superpersona of a theme and its theme
#            totaldiffperperm = totaldiffperperm + differencepersuperpersona
#        #sum all the differences between superpersona and their theme for a particular permutation
#            if totaldiffperperm < bestdiff : #which permutation gives the lowest totaldifference
#                bestdiff = totaldiffperperm
#                besteigs = list(each_perm)

        

