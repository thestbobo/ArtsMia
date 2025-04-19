from database.DB_connect import DBConnect
from model.artObject import ArtObject
from model.connessioni import Connessione

class DAO():

    @staticmethod
    def get_all_objects():
        cnx = DBConnect.get_connection()
        result = []

        cursor = cnx.cursor(dictionary=True)
        query = "select * from objects o"
        cursor.execute(query, ())
        for row in cursor:
            result.append(ArtObject(**row))

        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def get_all_connessioni(idMap):
        cnx = DBConnect.get_connection()
        result = []

        cursor = cnx.cursor(dictionary=True)
        query = """
        SELECT eo1.object_id as o1, eo2.object_id as o2, count(*) as peso
        FROM exhibition_objects eo1, exhibition_objects eo2 
        WHERE eo1.exhibition_id = eo2.exhibition_id 
        and eo1.object_id < eo2.object_id 
        group by eo1.object_id, eo2.object_id 
        order by peso desc
        """
        cursor.execute(query, ())
        for row in cursor:
            result.append(Connessione(idMap[row["o1"]],
                                      idMap[row["o2"]],
                                      row["peso"]))

        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def get_peso(self, v1: ArtObject, v2: ArtObject):
        cnx = DBConnect.get_connection()
        result = []

        cursor = cnx.cursor(dictionary=True)
        query = """
            SELECT count(*)
    FROM exhibition_objects eo1, exhibition_objects eo2 
    WHERE eo1.exhibition_id = eo2.exhibition_id 
    and eo1.object_id < eo2.object_id 
    and eo1.onject_id = %s
    and eo1.onject_id = %s
            """
        cursor.execute(query, (v1.object_id, v2.object_id))
        for row in cursor:
            result.append(ArtObject(**row))

        cursor.close()
        cnx.close()
        return result



