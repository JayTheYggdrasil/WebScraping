# csv output format: Username, Champion, Keystone, Build
import WebScraping as ws
import sys
import time

class GamePlayerFormat(ws.BaseFormat):
    def __init__(self):
        self.element_type = "div"

    def verify(self, element):
        if element.get("class") == None:
            return False
        return "GameItemWrap" in element.get("class")

    def container_to_bit(self, element):
        content = element.div.div
        things = content.contents
        # print(things)
        info = things[3]
        # print(info)
        keystone = info.contents[5].contents[1].img.get("alt")
        champion = info.contents[7].a.decode_contents()

        ignore = ["Farsight Alteration", "Warding Totem (Trinket)", "Oracle Lens"]
        items = things[9].div
        # print(items)
        item_list = []
        for div in items.find_all("div", class_="Item"):
            item = div.img
            if item == None:
                continue
            name = item.get("alt")
            if name in ignore:
                continue
            item_list.append(name)
        item_list += [""] * (6 - len(item_list))
        player_list = []
        players = things[11].find_all("a")
        for a in players:
            if "Requester" in a.get("class"):
                continue
            name = a.decode_contents()
            player_list.append(name)


        bit = [champion, keystone] + item_list
        return bit, player_list

def get_players(player_file):
    players = set()
    f = open(player_file, "r+")
    for player in f:
        players.add(player.rstrip())
    f.close()
    return players

if __name__ == "__main__":
    player_url = "https://na.op.gg/summoner/userName="
    player = sys.argv[1]
    current_players = get_players("players_scraped")
    if player == "c":
        print("Attempting to continue from players not yet scraped.")
        players_not_scraped = get_players("players_not_scraped")
    elif player in current_players:
        print("Already analyzed data for this player.")
        exit()
    else:
        players_not_scraped = set()
        players_not_scraped.add(player)
    try:
        with open("players_scraped", "a+") as f:
            with open("player_data.csv", "a+") as player_data:
                while True:
                    player = players_not_scraped.pop()
                    try:
                        f.write(player + "\n")
                        data = ws.get_data(player_url + player.replace(" ", "+"))
                        bits = ws.collect_bits(data, GamePlayerFormat)
                        for player_values, other_players in bits:
                            # print(player_values, other_players)
                            #Deal with other players first
                            for p in other_players:
                                if not p in current_players:
                                    players_not_scraped.add(p)
                            #Now gather player data
                            print("hi", player, player_values)
                            player_data.write(player + ", " + ", ".join(player_values) + "\n")
                        time.sleep(1)
                    except UnicodeEncodeError:
                        print("UnicodeEncodeError: Skipping Player")
    except KeyboardInterrupt:
        # print("Stopping")
        # with open("players_not_scraped", "w+") as f:
        #     for player in players_not_scraped:
        #         f.write(player + "\n")
        print("Stopped")
