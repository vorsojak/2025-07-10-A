from database.DB_connect import DBConnect
from model.arco import Arco
from model.category import Category
from model.product import Product


class DAO:
    def __init__(self):
        pass

    @staticmethod
    def getDateRange():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT distinct (order_date)
                 from orders o
                 order by order_date"""

        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def getCategorie():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                from bike_store_full.categories c"""

        cursor.execute(query)

        for row in cursor:
            results.append(Category(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getProductsByCategory(c):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from products p
                    where p.category_id = %s"""

        cursor.execute(query, (c.category_id,))

        for row in cursor:
            results.append(Product(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(c, d1, d2, idMapP):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select t1.product_id as id1, t2.product_id as id2, t1.n as t1n, t2.n as t2n, (t1.n+t2.n) as peso 
                    from (select p.product_id, count(*) as n
                    from products p, order_items oi,  orders o
                    where o.order_id = oi.order_id and oi.product_id = p.product_id 
                    and o.order_date between %s and %s
                    and p.category_id = %s
                    group by p.product_id) t1
                    join (select p.product_id, count(*) as n
                    from products p, order_items oi,  orders o
                    where o.order_id = oi.order_id and oi.product_id = p.product_id 
                    and o.order_date between %s and %s
                    and p.category_id = %s
                    group by p.product_id) t2
                    ON t1.product_id <> t2.product_id
                    where t1.n >= t2.n
                    order by peso asc"""

        cursor.execute(
            query,
            (
                d1,
                d2,
                c.category_id,
                d1,
                d2,
                c.category_id,
            ),
        )

        for row in cursor:
            results.append(Arco(idMapP[row["id1"]], idMapP[row["id2"]], row["peso"]))

        cursor.close()
        conn.close()
        return results

    # @staticmethod
    """def getProdotti():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """  # select * from products p
    """
        cursor.execute(query)

        for row in cursor:
            results.append(Product(**row))

        cursor.close()
        conn.close()
        return results"""
