import os
import csv
import pandas

path = "C:/Users/Moi/Downloads"
file = 'newRecetteCarac8001.csv'
os.chdir(path)

livre = pandas.read_csv(file)
nb_elt = len(livre)
instructions_num = 2
data = pandas.DataFrame(columns=['id','recette','num_ligne'])
poubelle = list()


def processing(data,ingredientsplit):
    rec = recette.split(ingredientsplit)[1]
    rec = rec.split('Preparation')[0]
    rec = rec.split('Instructions:')[0]
    rec = rec.split('Instructions')[0]
    rec = rec.split('INSTRUCTIONS')[0]
    rec = rec.split('PREPARATION')[0]
    rec = rec.split('DIRECTIONS')[0]
    rec = rec.split('Directions')[0]
    rec = rec.split('Directions:')[0]
    rec = rec.split('Optional:')[0]
    ingredients = rec.split('\n')
    # Prétraitements pour la lecture
    ingredients = list(filter(None, ingredients))
    ingredients = [ligne.split(',')[0] for ligne in ingredients]
    # Id recette | Text ingredient | numéro de ligne
    ing_list = list()
    ids_list = list()
    lignes_list = list()
    num_lign = 1
    for ligne in ingredients:
        a = ligne.split(')')
        if a.__len__() > 1:
            ligne = ligne.split('(')[0] + ligne.split(')')[1]
        a = ligne.split('(')
        if a.__len__() > 1:
            ligne = ligne.split('(')[0]
        a = ligne.split('fresh')
        if a.__len__() > 1:
            ligne = ligne.split('fresh')[0] + ligne.split('fresh')[1]
        ligne = ligne.split(':')[0]
        ligne = ligne.replace('zucchinis', 'zucchini')
        ligne = ligne.replace('oz', ' oz')
        ligne = ligne.replace(' jar ', ' oz ')
        ligne = ligne.replace(' ml ', ' oz ')
        ligne = ligne.replace(' milliliters ', ' oz ')
        ligne = ligne.replace(' liter', ' oz')
        ligne = ligne.replace(' inches', ' oz')
        ligne = ligne.replace(' inch ', ' oz ')
        ligne = ligne.replace(' gms ', ' g ')
        ligne = ligne.replace(' grams ', ' g ')
        ligne = ligne.replace(' tablespoons ', ' tablespoon ')
        ligne = ligne.replace('½', '1/2')
        ligne = ligne.replace('¼', '1/4')
        ligne = ligne.replace('¾', '3/4')
        ligne = ligne.replace('-', ' ')
        ligne = ligne.replace('m ozzarella', 'mozzarela')
        ligne = ligne.replace('fr ozen', 'frozen')
        ligne = ligne.replace('Fr ozen', 'frozen')
        ligne = ligne.replace('M ozzarella', 'Mozzarela')
        ligne = ligne.replace('Mozzarela', 'Mozzarella')
        ligne = ligne.replace('mozzarela', 'mozzarella')
        ligne = ligne.replace(' heese', ' cheese')
        ligne = ligne.replace('tbsps', 'tbsp')
        ligne = ligne.replace('tsps', 'tbsp')
        ligne = ligne.replace('⅓', '1/3')
        ligne = ligne.replace('’', '\'')
        ligne = ligne.replace('⅔', '2/3')
        ligne = ligne.replace('⅛', '1/8')
        ligne = ligne.replace('–', '-')
        ligne = ligne.replace('•', '')
        ligne = ligne.replace('.', '')
        ligne = ligne.replace('â€¢', '')
        ligne = ligne.replace('¬', '')
        ligne = ligne.replace('”', ' oz')
        ligne = ligne.replace('←', '')
        ligne = ligne.replace('®', '')
        ligne = ligne.replace('™', '')
        ligne = ligne.replace('*', '')
        ligne = ligne.replace('“', '"')
        ligne = ligne.replace('”', '"')
        ligne = ligne.replace('"00"', '')
        ligne = ligne.replace('×', 'x')
        ligne = ligne.replace('     ', '    ')
        ligne = ligne.replace('    ', '   ')
        ligne = ligne.replace('   ', '  ')
        ligne = ligne.replace('  ', ' ')
        ligne = ligne.strip()
        if (ligne is not " " and ligne is not ""):
            ing_list.append(ligne)
            ids_list.append(id)
            lignes_list.append(num_lign)
        num_lign = num_lign + 1
    # print(ing_list)
    df1 = pandas.DataFrame()
    df1['id'] = ids_list
    df1['recette'] = ing_list
    df1['num_ligne'] = lignes_list
    data = data.append(df1)
    return data


for row_num in range(nb_elt):
    #row_num = 0 # A faire varier

    id = int(livre.iloc[row_num,0])
    recette = str(livre.iloc[row_num,instructions_num])

    #Isoler la liste des ingrédients
    if recette.split('Ingredients').__len__()>1:
        data = processing(data,'Ingredients')
    elif recette.split('INGREDIENTS').__len__()>1:
        data = processing(data,'INGREDIENTS')
    elif recette.split('Ingredient').__len__()>1:
        data = processing(data,'Ingredient')
    elif recette.split('INGREDIENT').__len__()>1:
        data = processing(data,'INGREDIENT')
    else:
        poubelle.append(id)


data.to_csv('rec_inglike3.csv',index=False)
print(data)
print(poubelle)
print(poubelle.__len__())