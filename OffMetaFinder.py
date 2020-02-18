# import matplotlib as plt
import sqlite3
from dbstuff import to_db_name

"""
Goals:

Analyze Champion Menu:
    Frequency of all roles, items, keystones
    Frequency of all other roles, items, and keystones given one or more role, item or keystone
    Graph of related items, roles and keystones
"""

_keystone = "keystone"
_role = "role"
_item = "item"
_champion = "champion"

def frequency(of, given=None):
    if given is None:
        given = {}
    conditions = ""

    binding = False
    preceded = False

    if _champion in given and given[_champion] is not None:
        conditions += "champion = '{}'".format(given[_champion])
        preceded = True
    if _item in given and given[_item] is not None:
        conditions += " AND " if preceded else ""
        conditions += "item = '{}'".format(given[_item])
        preceded = True
        binding = True
    if _keystone in given and given[_keystone] is not None:
        conditions += " AND " if preceded else ""
        conditions += "keystone = '{}'".format(given[_keystone])
        preceded = True
    if "role" in given and given["role"] is not None:
        conditions += " AND " if preceded else ""
        conditions += " AND role = '{}'".format(given["role"])

    if binding or of == "item":
        inner_table = "(SELECT * FROM games g, items i WHERE g.game_id = i.game_id AND {})".format(conditions)
    else:
        inner_table = "(SELECT * FROM games g WHERE {})".format(conditions)

    if of == _champion or of == _item or of == _role or of == _keystone:
        return """
            SELECT {}, COUNT({}) AS frequency
            FROM {}
            GROUP BY {}
            ORDER BY COUNT({}) DESC
        """.format(of, of, inner_table, of, of)
    else:
        print("Nope.")


def contents_of(cur, champion, column):
    cur.execute(
        "SELECT {} FROM games g, items i WHERE g.game_id = i.game_id AND champion = ? GROUP BY {}".format(column, column),
        (to_db_name(champion), )
    )
    return cur.fetchall()


def relational_frequency(cur, champion):
    # GOAL: Create a new table like
    # {object: Any, with: Any, frequency}

    # 1. Union every game object so that we have
    # {game_id, object}

    union_query = """
        SELECT game_id, role AS object FROM games WHERE champion = '{}'
        UNION
        SELECT game_id, keystone AS object FROM games WHERE champion = '{}'
        UNION
        SELECT g.game_id, item AS object FROM games g, items i WHERE champion = '{}' AND g.game_id = i.game_id
    """.format(champion, champion, champion)

    # 2. Join using game_id to get
    # {object, with}

    join_query = """
        SELECT a.object, b.object AS with FROM ({}) a, ({}) b WHERE a.game_id = b.game_id AND a.object != b.object
    """.format(union_query, union_query)

    # 3. Get the frequency of each "object, with" pair

    return "SELECT object, with, COUNT(with) AS frequency FROM ({}) GROUP BY object, with".format(join_query)


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

        cur.execute(frequency(_role, {_role: None, _champion: "khazix", _item: None, _keystone: None}))
        print(cur.fetchall())

        cur.execute(relational_frequency(cur, "khazix"))
        print(cur.fetchall())

        # cur.execute("""
        #     SELECT i1.item, i2.item FROM items i1, items i2, games g
        #     WHERE i1.game_id = i2.game_id AND g.game_id = i1.game_id AND i1.item != i2.item AND g.champion = 'ivern'
        #     GROUP BY i1.game_id, i1.item
        # """)
        # print(cur.fetchall())

        cur.execute("""
            SELECT name FROM games g WHERE champion = 'khazix' AND keystone = 'phase_rush'
        """)
        print(cur.fetchall())
