import os
import csv
import pandas
import math

path = "C:/Users/Moi/Downloads"
fichier = '1'
file = 'ID_init.csv'
os.chdir(path)
bdd1 = pandas.read_csv(file)
fichier = '2'
file = 'ID_poubelle.csv'
bdd2 = pandas.read_csv(file)

id_poubelle = list()
list1 = list()
list2 = list()
for id in bdd1['id']:
    list1.append(id)
for id in bdd2['id']:
    list2.append(id)

for id in list1:
    if not id in list2:
        id_poubelle.append(id)

print(len(list2),len(list1))
print(len(id_poubelle))
data = pandas.DataFrame()
data['id']=id_poubelle
data.to_csv('ID_valides.csv',index=False)