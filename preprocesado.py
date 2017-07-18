# -*- coding: utf-8 -*-
"""
Created on Tue May 23 10:13:07 2017

@author: rparrilla
"""
import nltk 
from nltk.tokenize import word_tokenize
import string
import re
from pattern.es import parsetree
from BeautifulSoup import BeautifulSoup
import codecs

"""Detectar idioma"""

import langid
langid.set_languages(['en','es'])

langid.classify('data'.encode('utf-8').decode('utf-8'))[0]!="es"


"""LIMPIAR"""
from unidecode import unidecode
from translation import bing

j=1

def lemma_esp(text):
    text = codecs.decode(text, "utf-8")
    text = unidecode(text)
    try:
        if(langid.classify(text.encode('utf-8').decode('utf-8'))[0]!="es"):
            return text
        else:
            s = parsetree(text, lemmata = True)
            lista_palabras = s.sentences[0].words
            lista_lemas = map(lambda x: x.lemma,lista_palabras)
            texto= ' '.join(lista_lemas)
            return texto
    except:
            s = parsetree(text, lemmata = True)
            lista_palabras = s.sentences[0].words
            lista_lemas = map(lambda x: x.lemma,lista_palabras)
            texto= ' '.join(lista_lemas)        
            return texto

def traducir_esp(text):
    errores_trad = []
    texto = ''
    global j 
    j = j + 1
    if(j%100 ==0):
       print(j)
    try:
        texto = bing(text, dst = 'es')
    except:
        errores_trad.append(text)
    return texto, errores_trad
        

def reemplazar_simb(text):
    symbols = [u'\u2022', u'\u25E6',u'\u2018', '\'s','-','\*',u'\u00B4', u'\xb7']
    punt = string.punctuation
    for char in text:
        if(char in punt or char in symbols):
            text = string.replace(text,char,' ')
    return text

def limpiar(text):
    if not isinstance(text, unicode) :
        text = codecs.decode(text, "utf-8")
    text = unidecode(text)
    text = text.lower()

    lista = ['director', 'jefe', 'manager', 'ejecutivo','ceo','gerente','becario','auxiliar','asociado',
     'subdirector','chief','head','becaria','intern','internship','practicas','proyecto','responsable',
     'delegado','senior','junior','proyectos','inspector','presidente','vicepresidente',
     'founder','general','owner', 'leader','team','managing','project','pmo',
     'co','profesional','socio','partner','consultant','consultor','consultora','ejecutivo','fundador',
     'miembro','member','analista','analyst','consejero','directora','cofounder','trainee',
     'equipo','principal','executive','presidente','preseident','oficina','seleccion','board director','directors','board',
     'freelance','coordinador','coordinadora','socia','regional','staff','departamento','área','area',
     'encargado','encargada','tecnico','tecnica','coordinator',
     'coordinador','coordinadora','trainer','colaborador','helper','estudiante', 'zona','lecturer',
     'vendedor','associate','profesor','student','jefa','presidencia','vicesecretario',
     'vicesecretaria','directivo','comercial','delegado','delegada','profesora','verano','summer','diplomatura','grado','licenciatura',
     'graduado','diplomado','graduada','licenciado','licenciada','diplomada']  
              
    lista2 = ['strong','p','br','n','h']
    stop_words = nltk.corpus.stopwords.words('spanish')
    stop_words_2 = nltk.corpus.stopwords.words('english')
    stopwords =stop_words + stop_words_2
    number = re.compile(r'[0-9]')
    
    cleaned_text = reemplazar_simb(text)
   
    eliminar =  stopwords + lista + lista2
    txt_token = word_tokenize(cleaned_text)
    txt_token = map(lambda x: number.sub("", x), txt_token)
    txt_token = map(lambda x: reemplazar_simb(x), txt_token)
    txt_token = filter(lambda x: x not in eliminar, txt_token)
        
    text = ' '.join(txt_token)
    
    return text 

"""Limpiar html"""

#import sys  
#
#reload(sys)  
#sys.setdefaultencoding('utf-8')

def limpiar_html(text):
    
    text = BeautifulSoup(text,convertEntities=BeautifulSoup.HTML_ENTITIES).text
    return text


"""Lematización"""

def reemplazar_puestos(text):
    
    text = text.lower()
    lista_reemplazar = {'seo': 'optimización de motores de búsqueda',
                        'sem':'search engine marketing',
                        'cto':'director de tecnologóa',
                        'cdo': 'jefe de operaciones digitales',
                        'sales':'ventas',
                        'coo': 'jefe de operaciones',
                        'hhrr': 'recursos humanos',
                        'hr': 'recursos humanos','rh': 'recursos humanos',
                        'rrhh': 'recursos humanos',
                        'investment advisor':'asesor de inversiones',
                        'cuenta': 'cuentas',
                        'redactora':'redactor',
                        'cfo':'director financiero',
                        'cco':'Director Ejecutivo de Comunicaciones',
                        'cio':'director de sistemas',
                        'prl': 'Prevención de riesgos laborales'} 
    for key,value in lista_reemplazar.items():
         if(text == key):
             text = codecs.decode(value, "utf-8")
             text = unidecode(text)
    return text

def lematizacion_limpieza(text):
    text = codecs.decode(text, "utf-8")
    text = unidecode(text)
    text = text.lower()
    
    lista = ['director', 'jefe', 'manager', 'ejecutivo','ceo','gerente','becario','auxiliar','asociado',
     'subdirector','chief','head','becaria','intern','internship','practicas','proyecto','responsable',
     'delegado','senior','junior','proyectos','inspector','presidente','vicepresidente',
     'founder','general','owner', 'leader','team','managing','project','pmo',
     'co','profesional','socio','partner','consultant','consultor','consultora','ejecutivo','fundador',
     'miembro','member','analista','analyst','consejero','directora','cofounder','trainee',
     'equipo','principal','executive','presidente','preseident','oficina','seleccion','board director','directors','board',
     'freelance','coordinador','coordinadora','socia','regional','staff','departamento','área','area',
     'encargado','encargada','tecnico','tecnica','coordinator',
     'coordinador','coordinadora','trainer','colaborador','helper','estudiante', 'zona','lecturer',
     'vendedor','associate','profesor','student','jefa','presidencia','vicesecretario',
     'vicesecretaria','directivo','comercial','delegado','delegada','profesora','verano','summer','diplomatura','grado','licenciatura',
     'graduado','diplomado','graduada','licenciado','licenciada','diplomada','online','asistente','adjunto',
     'ayudante','cofundador','centro','oficial','vice','afi','align','bull','espana','ano','anos'] 
    
        
    txt_token = word_tokenize(text)
    txt_token = map(lambda x: reemplazar_puestos(x), txt_token)
    txt_token = map(lambda x:  lemma_esp(x), txt_token)
    txt_token = filter(lambda x: x not in lista, txt_token)

    text = ' '.join(txt_token)
    return text



def limpiar_cursos(text):
    try:
        if not isinstance(text, unicode) :
            text = codecs.decode(text, "utf-8")
    except:
        try:
            text = codecs.decode(text, "utf-8")
        except:
            text= text
            
    finally:
        text = limpiar_html(text)
        text = unidecode(text)
        text = text.lower()
    
        lista = ['jefa',  'fundador',  'founder',  'summer',  'vendedor',  'executive',  'manager', 
                 'nbsp',  'left',  'becario',  'staff',  'delegada',  'zona',  'freelance',  'estudiante',  
                 'delegado',  'board',  'ndash',  'blockquote',  'comercial',  'ceo',  'regional', 
                 'ayudante',  'efa',  'escuela',  'jornada',  'trav',  'proyectos',  'profesional',  'cofounder', 
                 'gerente',  'colaborador',  'vicepresidente',  'intern',  'online',  'pmo',  'profesora',  'asociado',
                 'junior',  'managing',  'curso',  'directivo',  'ntilde',  'consejero',  'leader',  'associate',  'internship',
                 'team',  'subdirector',  'departamento',  'coordinadora',  '\xc3\xa1rea',  'profesor',  'asistente', 
                 'consultora',  'practicas',  'vicesecretario',  'proyecto',  'vicesecretaria',  'trainer',  'grado',  'jefe',  'becaria', 
                 'seleccion',  'diplomatura',  'trainee',  'owner',  'cr',  'li',  'presidencia',  'presidente',  'pr',  'cofundador',  'bull', 
                 'board director',  'area',  'adjunto',  'responsable',  'miembro',  'master',  'equipo',  'head',  'auxiliar', 
                 'analista',  'line',  'analyst',  'verano',  'tecnica',  'coordinador',  'consultor',  'co',  'ejecutivo',  'consultant',  
                 'align',  'tecnico',  'project',  'ul',  'tema',  'helper',  'general',  'coordinator',  'socio',  'partner',  'inspector', 
                 'edicion',  'socia',  'oficial',  'afi',  'licenciatura',  'preseident',  'chief',  'member',  'oficina',  'licenciado',
                 'licenciada',  'lecturer',  'diplomada',  'diplomado',  'centro',  'director',  'encargada',  'student', 
                 'encargado',  'directora',  'vice',  'alumno',  'alumni',  'principal',  'directors',  'graduado',  'senior',  'graduada', 
                 'strong','p','br','h','src','img','href','alt','graduados','examen','cualificacion','objetivos','programa','aplicadas','presencial',
                 'campus','formacion','forma','alumnos','accede','agenda','asistentes','actividades',
                 'profesionales','dia','herramientas','ademas','mes','madrid','clases'
                 'presentacion','target','blank','novedad','experto','speaker','summary','mas','profesor','profesores',
                 'grupos','clases','temas','traves','delcampus','delaula','ejemplos','practicos','companeros',
                 'metodologia','presenciales','ano','anos','aquellos','ello','supone','etc','tiempo','desplazamiento','asistir',
                 'vez','participar','principales','objetivo','objetivos','cada','sesion','clase','distancia',
                 'practica','todas','algun','importante','expertos']
        
        meses = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto',
                 'septiembre','octubre','noviembre','diciembre']
        
        
        number = re.compile(r'[0-9]')
        
        cleaned_text = reemplazar_simb(text)
       
        stop_words = nltk.corpus.stopwords.words('spanish')
        stop_words = map(unidecode,stop_words)
        stop_words_2 = nltk.corpus.stopwords.words('english')
        stopwords =stop_words + stop_words_2
    
        eliminar = stopwords +  lista + meses

        txt_token = word_tokenize(cleaned_text)
        txt_token = map(lambda x: number.sub(" ", x), txt_token)
        txt_token = map(lambda x: reemplazar_simb(x), txt_token)
        txt_token = filter(lambda x: x not in eliminar, txt_token)
        txt_token = map(lambda x: codecs.decode(reemplazar_puestos(x), "utf-8"), txt_token)
       # txt_token = map(lambda x:  lemma_esp(x), txt_token)
        txt_token = filter(lambda x: x not in lista, txt_token)     
        
        for i in range(len(txt_token)-1):
            if('ii' in txt_token[i+1] and txt_token[i] == 'solvencia'):
                 txt_token[i] = string.replace(txt_token[i],'solvencia','solvencia-ii')
        
        txt_token = filter(lambda x: x!='ii', txt_token)
        text = ' '.join(txt_token)
        
        return text 








