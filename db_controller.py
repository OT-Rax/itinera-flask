import mysql.connector

class Db_controller:
    def __init__(self):
        pass

    def get_stands(self, ids):
        mydb = mysql.connector.connect(
          host="localhost",
          user="hu03",
          password="JxnUWFEnh7",
          database="itinera"
        )
        cursor = mydb.cursor(buffered=True)
        #cursor.execute("SELECT id, full_price, medium_visit_time, start_time, end_time FROM stands WHERE id IN ? LIMIT 10"%(ids))
        cursor.execute(f'SELECT id, full_price, medium_visit_time, start_time, end_time FROM stands WHERE id in ({ids})')
        stands = cursor.fetchall()
        return stands;

    def get_stands_distances(self, stands):
        mydb = mysql.connector.connect(
          host="localhost",
          user="hu03",
          password="JxnUWFEnh7",
          database="itinera"
        )
        cursor = mydb.cursor(buffered=True)
        distance_matrix = [[0 for _ in range(len(stands))] for _ in range(len (stands))]
        for i in range(len(stands)):
            for j in range(len(stands)):
                if i == j:
                    distance_matrix[i][j] = 99999
                else:
                    print(stands[i][0])
                    print(stands[j][0])
                    cursor.execute(f"SELECT distance FROM links WHERE origin_stand_id = {stands[i][0]} AND destination_stand_id = {stands[j][0]}")
                    distance = cursor.fetchone()[0]
                    distance_matrix[i][j] = distance
        print(distance_matrix)
        return distance_matrix;
