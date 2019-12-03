import json
import os
import pandas
import pymysql
import re

# Redirection
root_path = "/Users/moi/Desktop/Repertoire_de_travail/projet_mealcheck/Ressources/data"
os.chdir(root_path)

# Init
filename = "allrecipes-recipes.json"
rec_ing_like = pandas.DataFrame(columns=['id', 'recette', 'num_ligne'])
recipe_number = 0
last_id = 10949+1

#Connexion database
json1 = '{    "mysql":{        "host":"localhost",        "user":"root",' \
        '        "password":"root",        "db":"Mealcheck", "port":8889    }}'
config = json.loads(json1)
class DbHelper:

    __connection = None;
    __cursor = None;

    def __init__(self):
        __db_config = config['mysql'];
        self.__connection = pymysql.connect(host=__db_config['host'],
                                            user = __db_config['user'],
                                            password = __db_config['password'],
                                            db = __db_config['db'],
                                            port = __db_config['port'],
                                            charset = 'utf8',

                                            cursorclass = pymysql.cursors.DictCursor)
        self.__cursor = self.__connection.cursor()

    def query(self, query, params):
        self.__cursor.execute(query, params)
        return self.__cursor

    def close(self):
        self.__connection.close();

    def commit(self):
        self.__connection.commit();
__db = DbHelper()
recetteInstr = "Les recettes et les conseils suivants étaient dans un article " \
               "dans la section de la Journée de l’alimentation de l’Oregonian."

# Parcours du Json
with open(filename, 'r') as f:
    lines = [re.sub("\{\]]*", "", one_object.rstrip()) for one_object in f.readlines()]
    json_as_list = "".join(lines).split('}')
    for elem in json_as_list:
        if len(elem) > 0:
            data = json.loads(elem[::1] + "}")
            # Données utiles
            cook_time = data['cook_time_minutes']
            ingredients = data["ingredients"]
            instructions = data['instructions']
            photo_url = data['photo_url']
            prep_time = data['prep_time_minutes']
            rating_stars = data['rating_stars']
            count_reviews = data['review_count']
            title = data['title']
            base_url = data['url']
            base = 'Allrecipes'
            instructions = '\n'.join(instructions)

            # Ajout en base de donnée
            sql = "INSERT INTO `Recette`(`REC_IDRECETTE`, `REC_TITLE`, `REC_DESCRIPTION`, `REC_PHOTOURL`, `nom_base`," \
                  " `REC_RATING`, `lien_site`, `REC_TIME`, `REC_ACTIVETIME`, `REC_COOKTIME`, `REC_PREPTIME`, `REC_COUNTREVIEWS`) " \
                  "VALUES (" + str(last_id) + ",\"" + str(title) + "\",\"" +str(instructions)+"\",\"" + photo_url +"\",\""+base +"\","\
                  + str(rating_stars)+",\""+str(base_url)+"\","+str(cook_time)+","\
                  +str(prep_time)+","+str(cook_time)+","+str(prep_time)+","+str(count_reviews)+")"
            print(sql)
            __db.query(sql, None)
            __db.commit()

            # Ajouter la liste d'ingrédients dans le CSV REC ING LIKE
            last_id = last_id + 1
            num_line = 1
            for line in ingredients:
                rec_ing_like = rec_ing_like.append({'id': last_id, 'recette': line, 'num_ligne': num_line}, ignore_index=True)
                num_line = num_line + 1

rec_ing_like.to_csv('Rec_ing_like_Allrecipes.csv')


