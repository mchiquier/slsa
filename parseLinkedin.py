# -*- coding: utf-8 -*-
"""
Created on Tue Jun 06 10:47:53 2017

@author: rparrilla
"""

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
import re


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

def key_dict(key,dic):
    dic[key] = ' '
    return dic
def convert_cv_to_json(path):
    text = convert_pdf_to_txt(path)
    text = text.replace("\x0c", "")
    cv = {}
    text_list =  text.split('\n\n')
    text_list_2 = text.split('\n')
    cv['Basic'] = {}
    basic = text_list[0].split('\n')
    cv['Basic']['name'] = basic[0]
    cv['Basic']['local'] = basic[1]
    cv['Basic']['puesto_actual'] = basic[2]
    list_var = ['Summary','Education','Experience']
    not_var = set(list_var) - set(text_list_2)

    try:
        index_s = [text_list.index(s) for s in text_list if s.startswith("Summary")][0]
    except IndexError:
        index_s = 0
        
    try:
        index_exp = [text_list.index(s) for s in text_list if s.startswith("Experience")][0]
    except IndexError:
        index_exp = index_s + 1
        
    try:
       index_ed = [text_list.index(s) for s in text_list if (s.startswith("Education"))][0]# or s.startswith("\x0cEducation"))][0]
    except IndexError:
        index_ed = len(text_list)-2 #index_exp + 1
        
       
    summary = range(index_s,index_exp)
    experience = range(index_exp,index_ed)
    education = range(index_ed, len(text_list)-1)
    
    cv['Summary'] = map(lambda x: ""+ str(text_list[x]), summary)
    cv['Summary']  = '\n\n'.join(cv['Summary'] )
    
    cv['Experience'] = map(lambda x: ""+ str(text_list[x]), experience)
    cv['Experience']  = '\n\n'.join(cv['Experience'] )
    
    cv['Education'] = map(lambda x: ""+ str(text_list[x]), education)
    cv['Education']  = '\n\n'.join(cv['Education'] )

    if(len(not_var) > 0):
        cv = [key_dict(x,cv) for x in list(not_var)][0]
             
    return(cv)

def index_description(index,lista):
    a = map(lambda x: ""+ lista[x], index)
    a  = '\n'.join(a)
    return(a)


def separar_experiencia(lista):
    
    trabajo = {}

    trabajo['descripcion'] = lista[1]
    lista_year = lista[0].rpartition(',')[-1]
    lista = lista[0].rpartition(',')[:-1]
    trabajo['puesto'] = lista[0].split(" at ")[0]
    try:
        trabajo['empresa'] = lista[0].split(" at ")[1]
    except:
        trabajo['empresa'] = ''

    trabajo['mes_inicio'] = re.findall(r'(\w+) [0-9]{4} \xc2\xa0-', lista_year)
    trabajo['mes_inicio'].append(re.findall(r'(\w+) de [0-9]{4} \xc2\xa0-', lista_year))
    trabajo['mes_inicio'] = [x for x in trabajo['mes_inicio'] if x!=[]]
    try:
        if(len(trabajo['mes_inicio']) >1):
            trabajo['mes_inicio'] = trabajo['mes_inicio'][1]
    except:
        None
    
    trabajo['year_inicio'] = re.findall(r'(\w+) \xc2\xa0-', lista_year)
    trabajo['mes_fin'] = re.findall(r'-\xc2\xa0 (\w+) .*', lista_year)
        
    reg = re.compile(r'(\w+)\xc2\xa0')
    if(bool(reg.search(lista_year))):
        trabajo['year_fin'] = re.findall(r'(\w+)\xc2\xa0', lista_year)
    else:
        reg = re.compile(r'-\xc2\xa0 \w+ ([0-9]{4})')
        if(bool(reg.search(lista_year))):
            trabajo['year_fin'] = re.findall(r'-\xc2\xa0 \w+ ([0-9]{4})', lista_year)
        else:
            trabajo['year_fin'] = re.findall(r'-\xc2\xa0 (\w+)\xc2\xa0', lista_year)
   
    trabajo['duracion'] = re.findall(r'\(.*?\)', lista_year)
    
    if(trabajo['mes_fin']== trabajo['mes_inicio'] and trabajo['mes_inicio'] != [] and trabajo['mes_fin'] !=[] and trabajo['year_inicio']==trabajo['year_fin']):
        trabajo['duracion'] = 0
    else:
        if(trabajo['duracion'] == []):
            trabajo['duracion'] = 0
        else:
            trabajo['duracion'] = trabajo['duracion'][0][1:-1]
    
    if(len(trabajo['year_fin']) ==0 or trabajo['year_fin'] == ["Present"]):
        trabajo['year_fin']  = "Actualidad"
    return(trabajo)


def experiencia(cv):
    exp = cv['Experience']
    exp = exp.replace("Experience","",1)
    exp_list = exp.split("\n")
    regexp = "\xc2\xa0-\xc2\xa0"   
    index = [exp_list.index(s) for s in exp_list if regexp in s]
    index_menos = [i-1 for i in index]
    quitar_index = [i for i in index_menos if exp_list[i] == ""]
    n = len(exp_list)
    exp_list = [exp_list[i] for i in range(n) if i not in quitar_index]
    
    index = [exp_list.index(s) for s in exp_list if regexp in s]
    lista_fechas =  [exp_list[x] for x in index]
    lista_puestos = [exp_list[x-2:x] for x in index]
    lista_puestos = map(lambda x: ' '.join(x) , lista_puestos)

    lista_join = [a + ',' + b for a in lista_puestos for b in lista_fechas if lista_puestos.index(a) == lista_fechas.index(b)]
    
    inicio_desc = map(lambda x: x + 1,index)
    fin_desc = map(lambda x: x - 3,index)
    fin_desc = fin_desc[1:]
    fin_desc.append(len(exp_list))
    index_desc = [range(a,b) for a in inicio_desc for b in fin_desc if inicio_desc.index(a) == fin_desc.index(b)]
    
    lista_desc = map(lambda index: index_description(index,exp_list),index_desc)
    
    full_lista = zip(lista_join, lista_desc)
    cv['Experience'] = map(separar_experiencia, full_lista)
    return(cv)


def separar_educacion_year(texto):
    educacion = {}
    
    educacion['year_inicio'] = re.findall(r',\xc2\xa0(\w+)\xc2\xa0-', texto)
    educacion['year_fin'] = re.findall(r'\xc2\xa0-\xc2\xa0(\w+)', texto)
    
    educacion['universidad'] = texto.split('\n')[1]
    
    texto = texto.split('\n')[2:]

    titulacion = ''.join(texto)
    ['' + str(texto[x]) for x in range(0,len(texto))]
    last_coma = titulacion.rfind(',')
    educacion['titulacion'] = titulacion[0:last_coma]
    return(educacion)


def separar_educacion(texto):
    educacion = {}
    
    educacion['year_inicio'] = ""
    educacion['year_fin'] = ""
    
    educacion['universidad'] = texto.split('\n')[0]
    
    texto = texto.split('\n')[1]
    educacion['titulacion'] = texto
    return(educacion)


def educacion(cv):
    nombre = cv['Basic']['name']
    ed = cv['Education']
    reg = re.compile(r'(\xc2\xa0-\xc2\xa0[0-9]{4})\n\n')
    if(bool(reg.search(ed))):
        ed = re.split(r'(\xc2\xa0-\xc2\xa0[0-9]{4})\n\n',ed)[:-1]
        ed= ''.join(ed)
       
        
    reg_2 = re.compile(r'(\xc2\xa0-\xc2\xa0[0-9]{4})')
    if(bool(reg_2.search(ed))):      
        
        ed_list = re.split(r'(\xc2\xa0-\xc2\xa0[0-9]{4})',ed)

        n = len(ed_list)

        edu_list = [] 
        if(n > 1):
            edu_list = [ed_list[i] + ed_list[i+1] for i in range(0,n-1)  if i%2 == 0]
        else:
            edu_list = [ed_list[0]]

        edu_list[0] = edu_list[0].split('\n')[1:]
        edu_list[0] = '\n'.join(edu_list[0])
        edu_list[0] = '\n' + edu_list[0]
        cv['Education'] = map(separar_educacion_year, edu_list)
        
    else: 
        ed = ed.replace("Education\n","",1)
        ed_list = ed.split('\n\n')
        ed_list = [x for x in ed_list if ((not nombre in x) and (not "Interests" in x))]
        ed_list = "\n".join(ed_list)
        edu_list = ed_list.split("\n")
        n = len(edu_list)
        edu_list = [edu_list[i] + "\n" +  edu_list[i+1] for i in range(0,n-1)  if i%2 == 0]
        cv['Education'] = map(separar_educacion, edu_list)
    
    return(cv)


def duracion_parcial(texto):
    texto = str(texto)
    reg_m = re.compile(r'(m*s)')
    meses = 0
    mes = str()
    reg = re.compile(r'(a\xc3\xb1o)')
    reg2 = re.compile(r'(year)')

    if(bool(reg.search(texto))):
        year = int(re.split(r'(a\xc3\xb1o)',texto)[0])
        meses = 12*year
        
        if(bool(reg_m.search(texto))):
            
            if(year !=1):
                mes = re.split(r'(a\xc3\xb1os)',texto)[2]
            else:
                mes =  re.split(r'(a\xc3\xb1o)',texto)[2]
            if(mes != ""):
                mes = int(re.split(r'( mes)',mes)[0])
                meses += mes
      
    if(bool(reg2.search(texto))):
        year = int(re.split(r'(year)',texto)[0])
        meses = 12*year
        
        if(bool(reg_m.search(texto))):
            
            if(year !=1):
                mes = re.split(r'(years)',texto)[2]
            else:
                mes =  re.split(r'(year)',texto)[2]
            if(mes != ""):
                mes = int(re.split(r'(month)',mes)[0])
                meses += mes
            
    if(bool(reg_m.search(texto)) and not (bool(reg.search(texto)) or bool(reg2.search(texto)))):
            mes = int(re.split(r'( m.*s)',texto)[0])
            meses += mes
    return(meses)


def cv_to_json(path):
    cv = convert_cv_to_json(path)
    cv = experiencia(cv)
    cv = educacion(cv)
    exp = cv['Experience']
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
            duracion = map(duracion_parcial, lista_duracion)
            duracion = sum(duracion)
    cv['Experiencia_total_meses'] = duracion
    return(cv)

