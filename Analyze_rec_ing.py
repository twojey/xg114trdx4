import os
import csv
import pandas
import math
from collections import Counter
from matplotlib import pyplot as plt

path = "C:/Users/Moi/Downloads"
fichier = '1'
file = 'toxic'+fichier+'.csv'
os.chdir(path)
columns = ['id','ing']
bdd1 = pandas.read_csv(file)
fichier = '2'
file = 'toxic'+fichier+'.csv'
bdd2 = pandas.read_csv(file)
fichier = '3'
file = 'toxic'+fichier+'.csv'
bdd3 = pandas.read_csv(file)
fichier='4'
file = 'toxic'+fichier+'.csv'
bdd4 = pandas.read_csv(file)

bdd1.columns = columns
bdd2.columns = columns
bdd3.columns = columns
bdd4.columns = columns

a = bdd1.append(bdd2)
a = a.append(bdd3)
a = a.append(bdd4)

id_poubelle = list()
for id in a['id']:
    if id not in id_poubelle:
        id_poubelle.append(id)

data = pandas.DataFrame()
data['id']=id_poubelle
data.to_csv('ID_Poubelle.csv',index=False)
b = Counter(a['id'])
print(a)
c = list(b.values())
print(Counter(c))
print(b)
plt.hist(b.values(),bins=range(0,20))
plt.show()