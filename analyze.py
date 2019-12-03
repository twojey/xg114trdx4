import os
import csv
import pandas
import math

path = "C:/Users/Moi/Downloads"
os.chdir(path)
fichier = '1'
file = 'REC_FICHIER'+fichier+'.csv'
bdd1 = pandas.read_csv(file,delimiter=';',names=['id','name','ingid'])
fichier = '2'
file = 'REC_FICHIER'+fichier+'.csv'
bdd2 = pandas.read_csv(file,delimiter=';',names=['id','name','ingid'])
fichier = '3'
file = 'REC_FICHIER'+fichier+'.csv'
bdd3 = pandas.read_csv(file,delimiter=';',names=['id','name','ingid'])
fichier = '4'
file = 'REC_FICHIER'+fichier+'.csv'
bdd4 = pandas.read_csv(file,delimiter=';',names=['id','name','ingid'])


a = bdd1.append(bdd2)
a = a.append(bdd3)
a = a.append(bdd4)
print(a)
id_poubelle = list()
for id in a['id']:
    if id not in id_poubelle:
        id_poubelle.append(id)

data = pandas.DataFrame()
data['id']=id_poubelle
data.to_csv('ID_init.csv',index=False)
print(a)
print(data)