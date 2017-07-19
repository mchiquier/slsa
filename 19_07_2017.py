# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 10:58:57 2017

@author: mchiquier
"""
import pandas as pd 
contacts = pd.read_excel("Q:\Analytics\Proyectos\publications\data\linkedin\ContactosEscuela.xlsx", sheetname=0)
thestudents_empresa = contacts.iloc[5:,9].tolist()
thestudents_lastname = contacts.iloc[5:,6].tolist()
thestudents_firstname = contacts.iloc[5:,5].tolist()
totalname = zip(thestudents_firstname, thestudents_lastname) 
totalnamefinal = []
import pickle
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

with open('lista_nombres', "r") as fp: 
     nombres= pickle.load(fp)

import codecs
from unidecode import unidecode

nombresupdate = []
for name_afi in nombres:
   try:
       name_afi = codecs.decode(name_afi, "utf-8")
       name_afi = unidecode(name_afi)
       nombresupdate.append(name_afi)
       
   except:
       try: 
           name_afi = codecs.encode(name_afi, "utf-8")
           name_afi = unidecode(name_afi)
           nombresupdate.append(name_afi)
               
       except:
           try:
               name_afi = codecs.decode(name_afi, "utf-8")
               name_afi = codecs.encode(name_afi, "utf-8")
               name_afi = unidecode(name_afi)
               nombresupdate.append(name_afi)
           except:
               try:
                   name_afi = codecs.encode(name_afi, "utf-8")
                   name_afi = codecs.decode(name_afi, "utf-8")
                   name_afi = unidecode(name_afi)
                   nombresupdate.append(name_afi)
               except:
                   name_afi = name_afi
                   nombresupdate.append(name_afi)
       
for totalname in totalnamefinal: 
    try:
        totalname = codecs.decode(totalname, "utf-8")
        totalname = codecs.encode(totalname, "utf-8")
        totalname = unidecode(totalname)
    except:
        try:
            totalname = codecs.encode(totalname, "utf-8")
            totalname = codecs.decode(totalname, "utf-8")
            totalname = unidecode(totalname)
        except:
            totalname = totalname

nombres1 = map(lambda x : x.lower(), nombres)
totalnamefinal1 = map(lambda x : x.lower(), totalnamefinal)
from collections import defaultdict
nombre_to_empresa = defaultdict(list)      
for every in nombres : 
    if every in totalnamefinal : 
        our_index = totalnamefinal.index['every']
        nombre_to_empresa[every] = thestudents_empresa[our_index]
        
