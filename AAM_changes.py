# -*- coding: utf-8 -*-
"""
Created on Wed May 20 13:16:41 2026

@author: becario.adsaz
"""
import requests
import numpy as np
import os
import math
import sys

frecFCN = -(2*math.pi)/430.0027   #Free Core Nutation frequency
leaps = [50082,50629,51178,53735,54831,56108,57203,57753]
dd = os.getcwd()
today= 61187

def generar(lista,k):
    """
    Parameters
    ----------
    lista : string
        EAM data file already splited by line
    k : bool
        True if each row is not splited yet by columns

    Returns
    -------
    date, xmass, ymass, zmass, xmotion, ymotion, zmotion: list of float
        eam parameters at 00:00h
    """
    date,xmass,ymass,zmass,xmotion,ymotion,zmotion=[],[],[],[],[],[],[]
    i = 0
    for i in range(0,len(lista),8): #only keeping values at 00:00h
        if k:
            aux = lista[i].split()
        else:
            aux = lista[i]
        date.append(int(float(aux[4])))
        xmass.append(float(aux[5]))
        ymass.append(float(aux[6]))
        zmass.append(float(aux[7]))
        xmotion.append(float(aux[8]))
        ymotion.append(float(aux[9]))
        zmotion.append(float(aux[10]))        
    return date,xmass,ymass,zmass,xmotion,ymotion,zmotion

def read_aam(today):
    """
    Returns
    -------
    epoch : list of floats
        epoch of the xmass, ymass, zmass solutions  (daily at 00:00h from 1/01/2023
                                                  up until yesterday)
    xmass : list of floats
        xmass solution of the Atmospheric Angular Momentum at said epochs
    ymass : list of floats
        idem
    zmass : list of floats
        idem
    """
    # AAM Data from previous years
    direc = dd+'/datos/AAM/'
    ls = [f'{direc}ESMGFZ_AAM_v1.0_03h_2023.asc', f'{direc}ESMGFZ_AAM_v1.0_03h_2024.asc',f'{direc}ESMGFZ_AAM_v1.0_03h_2025.asc']
    date,xmass,ymass,zmass,xmotion,ymotion,zmotion = [],[],[],[],[],[],[]
    for i in range(len(ls)):
        f = open(ls[i])
        aux = (f.read()).split('\n')
        f.close()
        
        d,xma,yma,zma,xmo,ymo,zmo=generar(aux,True)
        date+=d
        xmass+=xma
        ymass+=yma
        zmass+=zma
        xmotion+=xmo
        ymotion+=ymo
        zmotion+=zmo 
    
    # AAM data from this year
    url = 'https://rz-vm480.gfz.de/repository/entry/'
    r2 = requests.get(url+"show", params = {'entryid':'df062563-2fda-4651-97be-376dfd6924ad'})
    r2t = r2.text
    ind = r2t.index('ESMGFZ_AAM_v1.0_03h_2026.asc')
    r3 = requests.get(url+'get/ESMGFZ_AAM_v1.0_03h_2026.asc',params = {'entryid':r2t[ind-36-11:ind-11]})
    aamlast = r3.text
    
    # AAM 10-day forecast data
    r4 = requests.get(url+"show", params = {'entryid':'a0dc0850-d97d-4a4b-9121-e98515e4d8c6'})
    r4t = r4.text
    r4t = r4t[r4t.index('"name":"ESMGFZ_AAM_v1.0_W')+20:]
    ind = r4t.index('"name":"ESMGFZ_AAM_v1.0_W')    
    r5 = requests.get(url+'get/'+str(r4t[ind+8:ind+55]), params = {'entryid':r4t[ind-39:ind-3]})
    aux = r5.text
    cont,cont2,i,j = 0,0,0,0
    while(cont<40):
        if aamlast[j] =="\n":
            cont+=1
        j+=1
     
        while(cont2<45):
            if aux[i] =="\n":
              cont2+=1
            i+=1
    aamlast=(aamlast[j:]).split("\n")
    ld = aux[i:].split("\n") #prediction of yesterday values (needed to predict today's)
    last_data=float(aamlast[-2].split()[4])
    if last_data +1 <= today:
        # This years' data + all missing data until today
        index = 8*(today-int(last_data))
        aamlast = [aamlast[i].split() for i in range(len(aamlast)-1)]+[ld[i].split() for i in range(0,index)]
    elif int(last_data) == today -1:
        # This years' data + today's predicted data
        aamlast = [aamlast[i].split() for i in range(len(aamlast)-1)]+[ld[0].split()]
    else:    
        return -1,0,0,0,0,0,0
    d,xma,yma,zma,xmo,ymo,zmo=generar(aamlast,False)
    date+=d
    xmass+=xma
    ymass+=yma
    zmass+=zma
    xmotion+=xmo
    ymotion+=ymo
    zmotion+=zmo
    
    return date,xmass,ymass,zmass,xmotion,ymotion,zmotion

def read_oam(today):
    """
    Returns
    -------
    epoch : list of floats
        epoch of the xmass, ymass, zmass solutions  (daily at 00:00h from 1/01/2023
                                                  up until yesterday)
    xmass : list of floats
        xmass solution of the Oceanic Angular Momentum at said epochs
    ymass : list of floats
        idem
    zmass : list of floats
        idem
    """
    direc = direc = dd+'/datos/OAM/'
    ls = [f'{direc}ESMGFZ_OAM_v1.0_03h_2023.asc', f'{direc}ESMGFZ_OAM_v1.0_03h_2024.asc', f'{direc}ESMGFZ_OAM_v1.0_03h_2025.asc']
    date,xmass,ymass,zmass,xmotion,ymotion,zmotion = [],[],[],[],[],[],[]
    for i in range(len(ls)):
        f = open(ls[i])
        aux = (f.read()).split('\n')
        f.close()
        
        d,xma,yma,zma,xmo,ymo,zmo=generar(aux,True)
        date+=d
        xmass+=xma
        ymass+=yma
        zmass+=zma
        xmotion+=xmo
        ymotion+=ymo
        zmotion+=zmo


    url = 'https://rz-vm480.gfz.de/repository/entry/'
    r2 = requests.get(url+"show", params = {'entryid':'73d23da5-4728-4b91-852d-2a630957b307'})
    r2t = r2.text
    ind = r2t.index('ESMGFZ_OAM_v1.0_03h_2026.asc')
    r3 = requests.get(url+'get/ESMGFZ_OAM_v1.0_03h_2026.asc',params = {'entryid':r2t[ind-36-11:ind-11]})
    oamlast = r3.text

    r4 = requests.get(url+"show", params = {'entryid':'0ec23b7c-960f-4225-be2d-de8f68bdb5ec'})
    r4t = r4.text
    r4t = r4t[r4t.index('"name":"ESMGFZ_OAM_v1.0')+20:]
    ind = r4t.index('"name":"ESMGFZ_OAM_v1.0')    
    r5 = requests.get(url+'get/'+str(r4t[ind+8:ind+41]), params = {'entryid':r4t[ind-39:ind-3]})
    aux = r5.text 
    
    cont,cont2,i,j = 0, 0, 0, 0
    while(cont<42): # Salto de línea en año actual
        if oamlast[j] =="\n":
          cont+=1
        j+=1
        
        while(cont2<42): # Salto de línea en predicción
            if aux[i] =="\n":
              cont2+=1
            i+=1
            
    oamlast=(oamlast[j:]).split("\n")
    ld = aux[i:].split("\n") #prediction of yesterday values (needed to predict today's)
    last_data=float(oamlast[-2].split()[4])
    if last_data +1 <= today:
        # This years' data + all missing data until today
        index = 8*(today-int(last_data))
        oamlast = [oamlast[i].split() for i in range(len(oamlast)-1)]+[ld[i].split() for i in range(0,index)]
    elif int(last_data) == today -1:
        # This years' data + today's predicted data
        oamlast = [oamlast[i].split() for i in range(len(oamlast)-1)]+[ld[0].split()]
    else:    
        return -1,0,0,0,0,0,0
    d,xma,yma,zma,xmo,ymo,zmo=generar(oamlast,False)
    date+=d
    xmass+=xma
    ymass+=yma
    zmass+=zma
    xmotion+=xmo
    ymotion+=ymo
    zmotion+=zmo
    
    return date,xmass,ymass,zmass,xmotion,ymotion,zmotion

def generarHAM(lista,k):
    i = 0
    date,xmass,ymass,zmass,xmotion,ymotion,zmotion = [],[],[],[],[],[],[]
    while i < len(lista):
        if k:
            aux = lista[i].split()
        else:
            aux = lista[i]
        date.append(float(aux[4]))
        xmass.append(float(aux[5]))
        ymass.append(float(aux[6]))
        zmass.append(float(aux[7]))
        xmotion.append(float(aux[8]))
        ymotion.append(float(aux[9]))
        zmotion.append(float(aux[10]))        
        i+=1
    return date,xmass,ymass,zmass,xmotion,ymotion,zmotion


def reduccionHAM(lista): 
    #mean value to transform solutions to 00h, not 12h
    i = 0
    lista_aux=[]
    while i+1 < len(lista):
        lista_aux.append((lista[i]+lista[i+1])/2)
        i+=1
    return lista_aux


def read_ham(today):
    """
    Returns
    -------
    epoch : list of floats
        epoch of the xmass, ymass, zmass solutions  (daily at 00:00h from 1/01/2023
                                                  up until yesterday)
    xmass : list of floats
        xmass solution of the Hydrological Angular Momentum at said epochs
    ymass : list of floats
        idem
    zmass : list of floats
        idem
    """
    direc = dd+'/datos/HAM/'
    ls = [f'{direc}ESMGFZ_HAM_v1.2_24h_2023.asc',f'{direc}ESMGFZ_HAM_v1.2_24h_2024.asc',f'{direc}ESMGFZ_HAM_v1.2_24h_2024.asc']
    #solutions are at 12h, not 00h; so we will calculate the mean value between two solutions to get 00h.
    #For 01-01 we need the 31-12 solution, which is written in the following line of the code:
    date,xmass,ymass,zmass,xmotion,ymotion,zmotion = [59944.500],[-1.077015111728597e-07],[1.872920064634999e-07],[9.658558932245592e-10],[-2.633075391255430e-11],[-1.347446554917640e-11],[2.536914218629560e-13]
    
    for i in range(len(ls)):
        f = open(ls[i])
        aux = (f.read()).split('\n')
        f.close()
        
        d,xma,yma,zma,xmo,ymo,zmo=generarHAM(aux,True)
        date+=d
        xmass+=xma
        ymass+=yma
        zmass+=zma
        xmotion+=xmo
        ymotion+=ymo
        zmotion+=zmo 
    
    url = 'https://rz-vm480.gfz.de/repository/entry/'
    r1 = requests.get(url+"show", params = {'entryid':'ca1a8036-1c8a-4a45-9d11-f3ac69e2692a'})
    r1t = r1.text
    ind = r1t.index('ESMGFZ_HAM_v1.2_24h_2026.asc')
    r2 = requests.get(url+"get/ESMGFZ_HAM_v1.2_24h_2026.asc", params = {'entryid':r1t[ind-36-11:ind-11]})
    hamlast = r2.text
    
    r4 = requests.get(url+"show", params = {'entryid':'8c9c0bb7-cbad-4507-a43c-e9591a66d7de'})
    r4t = r4.text
    r4t = r4t[r4t.index('"name":"ESMGFZ_HAM_v1.2')+20:]
    ind = r4t.index('"name":"ESMGFZ_HAM_v1.2')    
    r5 = requests.get(url+'get/'+str(r4t[ind+8:ind+41]), params = {'entryid':r4t[ind-39:ind-3]})
    aux = r5.text
    
    cont,cont2,i,j = 0, 0, 0, 0
    while(cont<49): # Salto de línea en año actual
        if hamlast[j] =="\n":
          cont+=1
        j+=1
        
        while(cont2<49): # Salto de línea en predicción
            if aux[i] =="\n":
              cont2+=1
            i+=1

    hamlast=(hamlast[j:]).split("\n")
    ld = aux[i:].split("\n") #prediction of yesterday values (needed to predict today's)
    last_data=float(hamlast[-2].split()[4])
    if last_data +1 <= today:
        # This years' data + all missing data until today
        index = (today-int(last_data))
        hamlast = [hamlast[i].split() for i in range(len(hamlast)-1)]+[ld[i].split() for i in range(0,index)]
    elif int(last_data) == today -1:
        # This years' data + today's predicted data
        hamlast = [hamlast[i].split() for i in range(len(hamlast)-1)]+[ld[0].split()]
    else:    
        return -1,0,0,0,0,0,0
    
    d,xma,yma,zma,xmo,ymo,zmo=generarHAM(hamlast,False)
    date+=d
    xmass+=xma
    ymass+=yma
    zmass+=zma
    xmotion+=xmo
    ymotion+=ymo
    zmotion+=zmo
    
    date = reduccionHAM(date)
    date = [int(item) for item in date]
    xmass = reduccionHAM(xmass)
    ymass = reduccionHAM(ymass)
    zmass = reduccionHAM(zmass)
    xmotion = reduccionHAM(xmotion)
    ymotion = reduccionHAM(ymotion)
    zmotion = reduccionHAM(zmotion)
    return date,xmass,ymass,zmass,xmotion,ymotion,zmotion

datea,xmassa,ymassa,zmassa,xmotiona,ymotiona,zmotiona = read_aam(today)
dateo,xmasso,ymasso,zmasso,xmotiono,ymotiono,zmotiono = read_oam(today)
dateh,xmassh,ymassh,zmassh,xmotionh,ymotionh,zmotionh = read_ham(today)
if datea == -1 or dateo == -1 or dateh == -1:
    print('ERROR: Not a valid date')
    sys.exit()