from unittest import result

from database.DB_connect import DBConnect
from model.product import Product


class DAO:
    @staticmethod
    def get_date_range():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT order_date
                    FROM `order` 
                    ORDER BY order_date """
        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last


    @staticmethod
    def read_category():
        conn = DBConnect.get_connection()

        result = []


        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT *
                            FROM  category
                             """
        cursor.execute(query)

        for row in cursor:
            result.append((row['id'], row['category_name']))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def read_product(id):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT *
                    FROM  product
                    WHERE category_id = %s
                                   """
        cursor.execute(query, (id,) )

        for row in cursor:
            results.append(Product(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def read_archi(date1, date2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ select distinct p.id, count(o.id) as vendite
                    from product p, order_item oi, `order` o  
                    where p.id = oi.product_id and oi.order_id = o.id and o.order_date between %s and %s
                    group by p.id
                    order by p.id
                                   """
        cursor.execute(query, (date1, date2, ) )

        for row in cursor:
            results.append((row['id'], row['vendite']))

        cursor.close()
        conn.close()
        return results

