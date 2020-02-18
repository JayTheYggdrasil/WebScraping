import matplotlib as plt
import sqlite3
from dbstuff import to_db_name

"""
Goals:

Analyze Champion Menu:
    Frequency of all roles, items, keystones
    Frequency of all other roles, items, and keystones given one or more role, item or keystone
    Graph of related items, roles and keystones
"""


def frequency(cur, of, given=None):
    if given is None:
        given = {}
    conditions = ""

    binding = False
    preceded = False

    if "champion" in given and given["champion"] is not None:
        conditions += "champion = '{}'".format(given["champion"])
        preceded = True
    if "item" in given and given["item"] is not None:
        conditions += " AND " if preceded else ""
        conditions += "item = '{}'".format(given["item"])
        preceded = True
        binding = True
    if "keystone" in given and given["keystone"] is not None:
        conditions += " AND " if preceded else ""
        conditions += "keystone = '{}'".format(given["keystone"])
        preceded = True
    if "role" in given and given["role"] is not None:
        conditions += " AND " if preceded else ""
        conditions += " AND role = '{}'".format(given["role"])

    if binding or of == "item":
        inner_table = "(SELECT * FROM games g, items i WHERE g.game_id = i.game_id AND {})".format(conditions)
    else:
        inner_table = "(SELECT * FROM games g WHERE {})".format(conditions)

    if of == "role" or of == "item" or of == "keystone" or of == "champion":
        cur.execute("""
            SELECT {}, COUNT({}) AS frequency
            FROM {}
            GROUP BY {}
            ORDER BY COUNT({}) DESC
        """.format(of, of, inner_table, of, of))
        return cur.fetchall()
    else:
        print("Nope.")


def contents_of(cur, champion, column):
    cur.execute(
        "SELECT {} FROM games g, items i WHERE g.game_id = i.game_id AND champion = ? GROUP BY {}".format(column, column),
        (to_db_name(champion), )
    )
    return cur.fetchall()


def relational_frequency(cur, champion):
    output = {}

    keystones = contents_of(cur, champion, "keystone")
    items = contents_of(cur, champion, "item")
    roles = contents_of(cur, champion, "role")
    given = {"champion": champion}
    for i in items:
        given["item"] = i
        frequency(cur, "item", given) + frequency(cur, "role", given) + frequency(cur, "keystone", given)


if __name__ == "__main__":
    with sqlite3.connect("league_of_legends.db") as conn:
        cur = conn.cursor()
        # cur.execute("""
        #     SELECT i.item, COUNT(item) AS frequency
        #     FROM games g, items i WHERE i.game_id = g.game_id AND g.champion = 'kayle'
        #     GROUP BY item
        #     ORDER BY COUNT(item) DESC
        # """)
        # print(cur.fetchall())

        print(frequency(cur, "champion", {"role": None, "champion": None, "item": "black_cleaver", "keystone": "prototype_omnistone"}))

        # cur.execute("""
        #     SELECT i1.item, i2.item FROM items i1, items i2, games g
        #     WHERE i1.game_id = i2.game_id AND g.game_id = i1.game_id AND i1.item != i2.item AND g.champion = 'ivern'
        #     GROUP BY i1.game_id, i1.item
        # """)
        # print(cur.fetchall())

        cur.execute("""
            SELECT name FROM games g WHERE keystone = 'prototype_omnistone' AND champion = 'gnar'
        """)
        print(cur.fetchall())