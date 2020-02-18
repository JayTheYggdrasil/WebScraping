import sqlite3
import WebScraping as ws
from dbstuff import complete_items, component_items, all_items, ranks, insert_into_db, create_tables, to_db_name, contains_player
import time

# 30347 Players in Diamond+


class GamePlayerFormat(ws.BaseFormat):
    def __init__(self):
        self.element_type = "div"

    def verify(self, element):
        if element.get("class") == None:
            return False
        if "GameItemWrap" in element.get("class"):
            return element.div.div.div.div.decode_contents().strip() == "Ranked Solo"

    def container_to_bit(self, element):
        content = element.div.div
        things = content.contents
        # print(things)
        info = things[3]
        # print(info)
        keystone = info.contents[5].contents[1].img.get("alt")
        champion = info.contents[7].a.decode_contents()

        stats = things[7]
        rank = stats.find_all("div", class_="MMR")[0].b.decode_contents().strip()
        items = things[9].div
        # print(items)
        item_list = []
        for div in items.find_all("div", class_="Item"):
            item = div.img
            if item == None:
                continue
            name = item.get("alt")
            if name.strip() in complete_items:
                item_list.append(name)
        player_list = []
        players = things[11].find_all("div", class_="Summoner")
        role = "No roll found"
        for div in players:
            if "Requester" in div.get("class"):
                role_index = (players.index(div) % 5)
                if role_index == 0:
                    role = "Top"
                elif role_index == 1:
                    role = "Jungle"
                elif role_index == 2:
                    role = "Middle"
                elif role_index == 3:
                    role = "Bottom"
                elif role_index == 4:
                    role = "Support"
                continue
            name = div.contents[3].a.decode_contents()
            player_list.append(name)

        bit = rank, role, champion, keystone, item_list
        return bit, player_list

def main():
    # Establish database connection
    dbname = "league_of_legends.db"
    with sqlite3.connect(dbname) as conn:
        print("Connecting to database")
        cur = conn.cursor()
        create_tables(cur)

        # Region can be specified here
        player_url = "https://euw.op.gg/summoner/userName="

        # Get parameters from the user
        player = input("Player to start with: ")

        if contains_player(cur, player):
            print("Already analyzed data for this player.")
            exit()
        else:
            players_not_scraped = set()
            players_not_scraped.add(player)

        rank_cutoff = input("Lowest rank to scrape: ")

        # Start scraping
        try:
            while True:
                player = players_not_scraped.pop()
                # Slow down the loop so we aren't spamming queries
                time.sleep(3)
                try:
                    # Collect the relevant data from the web page
                    data = ws.get_data(player_url + player.replace(" ", "+"))
                    bits = ws.collect_bits(data, GamePlayerFormat)

                    # Loop through the data
                    for (rank, role, champion, keystone, items), other_players in bits:
                        if rank not in ranks:
                            print("#########", player, other_players)
                            continue
                        if ranks.index(rank) < ranks.index(rank_cutoff):
                            break


                        # Insert data into the database
                        insert_into_db(cur, conn, player, rank, role, champion, keystone, items)
                        conn.commit()

                        # Add more players to inspect
                        for p in other_players:
                            if (not contains_player(cur, p)) and len(players_not_scraped) < 100:
                                players_not_scraped.add(p)

                        print(champion, role)

                except UnicodeEncodeError:
                    print("UnicodeEncodeError: Skipping Player")
                except IndexError:
                    print("Format Failed: Skipping Player")
        except KeyboardInterrupt:
            print("Stopping")
            cur.execute("SELECT count(game_id) FROM games")
            print("We now have {} games in the database".format(cur.fetchone()))
            conn.commit()
            print("Stopped")


if __name__ == "__main__":
    main()
