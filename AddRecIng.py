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


# Créer une fonction d'ajout de table
def add_resourcefile(filename, delimiter=','):
    resource = pandas.read_csv(filename, delimiter=delimiter)   # Lire un fichier ressource (ex REC_FICHIERX)
    nb_elt, nb_col = resource.shape
    for i in range(nb_elt):    # Parcourir le fichier
        # Ajouter la ligne courante à la base de donnée
        sql = "INSERT INTO `RECETTE_INGREDIENT` VALUES ("
        sql = sql+" "+str(resource.iloc[i, 0])
        for col in range(1,nb_col):
            row_elt = resource.iloc[i, col]
            sql = sql+", \""+str(row_elt)+'"'
        sql = sql+' )'


# add_resourcefile("REC_FICHIER1.csv",delimiter=';')


# Fonction nettoyage de la table
def del_resourcefile(filename, delimiter=','):
    resource = pandas.read_csv(filename, delimiter=delimiter, header=None)      # Lire un fichier ressource (ex PoubelleX)
    nb_elt, nb_col = resource.shape
    # Se connecter à la base de donnée
    id = 0
    for i in range(nb_elt):    # Parcourir le fichier
        if id != resource.iloc[i, 0]:    # Quand un nouvel identifiant apparait
            # Supprimer toutes les lignes contenant l'identifiant
            sql = "DELETE FROM `RECETTE_INGREDIENT` WHERE `RECING_RECETTEID`=" + str(resource.iloc[i, 0])
            print(sql)
        id = resource.iloc[i, 0]
        __db.query(sql, None).fetchall()
        __db.commit()

del_resourcefile('toxic2.csv', delimiter=',')
del_resourcefile('toxic3.csv', delimiter=',')
del_resourcefile('toxic4.csv', delimiter=',')

