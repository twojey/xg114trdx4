import os
import pandas
import json
import pymysql

root_path = "/Users/moi/Desktop/Repertoire_de_travail/projet_mealcheck/Ressources/data"
os.chdir(root_path)

json1 = '{    "mysql":{        "host":"localhost",        "user":"root",' \
        '        "password":"root",        "db":"Mealcheck", "port":8889    }}'
config = json.loads(json1)
class DbHelper:

    __connection = None
    __cursor = None

    def __init__(self):
        __db_config = config['mysql']
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
        self.__connection.close()

    def commit(self):
        self.__connection.commit()
__db = DbHelper()


recetteInstr = "Les recettes et les conseils suivants étaient dans un article " \
               "dans la section de la Journée de l’alimentation de l’Oregonian."
sql = "SELECT * FROM `Recette` WHERE `REC_PHOTOURL`='http://images.media-allrecipes.com/global/recipes/nophoto/nopicture-910x511.png'"
listRecette = __db.query(sql, None).fetchall()

#Lire le fichier rec_ing_like_allrecipes
filename = "Rec_ing_like_Allrecipes.csv"
df = pandas.read_csv(filename)

print(listRecette.__len__())
for recetteDict in listRecette:
    id_recette = int(recetteDict["REC_IDRECETTE"])
    #rechercher dans la colonne identifiant l'id de la recette
    #supprimer toutes les lignes qui ont cet identifiant
    df = df.drop(df[df.id == id_recette].index)

df.to_csv('REC_INGLIKE_AR.csv')

