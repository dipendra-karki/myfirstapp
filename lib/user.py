from psycopg2 import sql
from uuid import uuid4
from hashlib import sha256

from db import Db
import logging
logging.basicConfig(level=logging.DEBUG)

class User(object):

    @staticmethod
    def create(data):
        query = sql.SQL("""
        INSERT INTO cars
            (
            brand
            )
        VALUES
            (
            {brand}
            )
        RETURNING
            *
        """).format(
            brand = sql.Literal(data.get('brand'))
        )

        return Db.exec_query(query, returning = True)      

    @staticmethod
    def update(id, data):
        logging.info(id)
        query = sql.SQL("""
        UPDATE
            cars
        SET
            brand={brand}
        WHERE
            id={id}
        RETURNING
            *
        """).format(
            brand=sql.Literal(data.get('brand')),
            id=sql.Literal(id)
        )

        return Db.exec_query(query, returning = True)

    @staticmethod
    def query():
        query = sql.SQL("""
        SELECT
            *
        FROM
            cars
        """)

        return Db.exec_query(query, returning_multi = True)

    @staticmethod
    def search(data):
        # search = sql.Literal(data.get('search'))
        # pattern = '{}%'.format(search)
        query = sql.SQL("""
            SELECT
             *
            FROM
                cars c
            WHERE c.brand ILIKE {search}
         """).format(
            search = sql.Literal(data.get('search')+'%'))
        # st = 'SELECT * from cars c WHERE LOWER(c.brand) LIKE LOWER(%s)'
        # cursor = Db.get_cursor()
        # return cursor.execute(st, (pattern,), returning_multi=True)
        logging.info(query)
        return Db.exec_query(query, returning_multi = True)
    


    @staticmethod
    def remove(id):
        logging.info(id)
        query = sql.SQL("""
        DELETE FROM
            cars
        WHERE
            id={id}
        RETURNING
            *
        """).format(
            id = sql.Literal(id)
        )
        return Db.exec_query(query, returning = True)

    @staticmethod
    def find_by_id(id):
        query = sql.SQL("""
        SELECT
            *
        FROM
            cars
        WHERE
            id = {id}
        """).format(
            id = sql.Literal(id)
        )
        logging.info(query)
        return Db.exec_query(query, returning = True)