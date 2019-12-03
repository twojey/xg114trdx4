import os
import pandas
import json
import pymysql

root_path = "/Users/moi/Desktop/Repertoire_de_travail/projet_mealcheck/Ressources/data"
os.chdir(root_path)
filename = "ingredient.csv"
Table = pandas.read_csv(filename)
type_names = ["elixir", "REC_FICHIER", "RECYCLAGE"]
files_list = list()
pandas.read_csv("REC_FICHIER1.csv", delimiter=";")
for num_file in range(1, 4):
    for name in type_names:
        files_list.append(pandas.read_csv(name+str(num_file)+".csv", delimiter=';', header=None))

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
for resource_file in files_list:
    num_lines = resource_file.shape[0]
    for line_number in range(num_lines):
        id_recipe = resource_file.iloc[line_number, 0]
        ingredient_name = str(resource_file.iloc[line_number, 1])
        ingredient_name = ingredient_name.replace('"', '')
        ingredient_name = ingredient_name.replace('"', '')
        guid_ingredient = resource_file.iloc[line_number, 2]
        val_list = list()
        val_list.append(id_recipe)
        val_list.append(ingredient_name)
        val_list.append(guid_ingredient)

        sql = "INSERT INTO `RECETTE_INGREDIENT`(`RECING_RECETTEID`, `RECING_INGREDIENTNAME`, `RECING_INGREDIENTID` ) " \
              "VALUES ("+str(id_recipe)+",\""+str(ingredient_name)+"\",\""+str(guid_ingredient)+"\")"
        print(sql)
        __db.query(sql, None)
        __db.commit()
