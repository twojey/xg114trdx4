import os
import csv
import pandas
import math

path = "C:/Users/Moi/Downloads"


def cycle(fichier):
    file = 'POUBELLE_FICHIER' + fichier + '.csv'
    os.chdir(path)
    livre = pandas.read_csv(file)
    nb_elt = len(livre)  # 3412,fichier 1
    instructions_num = 1
    data = pandas.DataFrame()
    poubelle = list()
    print(nb_elt)
    poubelle = list()
    ids = list()
    for row_num in range(nb_elt):
        id = int(livre.iloc[row_num, 0])
        ing = str(livre.iloc[row_num, instructions_num])
        ing = ing.split('+')[0]
        ing = ing.split(' for ')[0]
        ing = ing.split(' or ')[0]
        ing = ing.split(' and ')[0]
        # print(ing)
        ing = ing.replace('inches', 'oz')
        condition = ing == 'nan'
        condition2 = False
        stopwords = ['salt','pepper','Salt','Oil','Dressing','Garnish','Optional','Filling','Crust','Toppings',
                     'Marinade','MARINADE','Equipment','toppings','Topping','topping','TOPPING','Layer','LAYER',
                     'LAYER','GANACHE','Breading','Sauce','Dough','CRUST','SAUCE','Salad','Vegetables','FOR',
                     'Skewers','skewers','toothpicks','For','cooking']
        for word in stopwords:
            if word in ing:
                condition2 = True

        # Mots à virer
        words_list = ['granulated', 'large', 'for frying', 'to taste', '  peeled', 'peeled', 'Peeled',
                      'for deep frying',
                      'for garnish', 'for shallow friying', 'for spreading', 'as required', 'small', 'medium',
                      'refined',
                      'powder', 'green', 'yellow', 'sprigs', ' spray', 'scraped', 'raw', 'thick', 'shaving', 'Hard',
                      'Large','hard',
                      'long', 'wedges', 'roundels', 'Fresh', 'A few', ' few', 'cold', 'browned', 'warm', 'About ',
                      'about ', 'Any ','full ']
        for word in words_list:
            if word in ing:
                ing = ing.replace(word, '')

        ing = ing.replace('  ', ' ')
        ing = ing.replace(' can ', ' oz ')
        ing = ing.strip()
        if not (condition or condition2):
            poubelle.append(ing)
            ids.append(id)
    data['id'] = ids
    data['recette'] = poubelle
    data.to_csv('Poubelle_' + fichier + '.csv', index=False)
    print(len(poubelle), nb_elt)
    print(poubelle[0:10])


cycle('1')
cycle('2')
cycle('3')
cycle('4')
