def find_jungle(player_data):
    jungle_items = ["Enchantment: Cinderhulk", "Enchantment: Bloodrazor", "Enchantment: Warrior", "Enchantment: Runic Echoes"]
    jungle_champions = dict()
    for player in player_data:
        champions = player_data[player]
        for champion in champions:
            for item in jungle_items:
                if item in champions[champion][3]:
                    if not champion in jungle_champions:
                        jungle_champions[champion] = champions[champion] + [[player]]
                    else:
                        jungle_champions[champion] = combine_champion_data(champions[champion] + [[player]], jungle_champions[champion])
                    break
    canditates = set()
    for champion in jungle_champions:
        data = jungle_champions[champion]
        if data[0] <= 15:
            canditates.add(champion)
            continue
        top5 = [0, 0, 0, 0, 0]
        top5_items = ["", "", "", "", ""]
        for item in data[3]:
            if item in component_items:
                continue
            if data[3][item] > min(top5):
                index = top5.index(min(top5))
                top5[index] = data[3][item]
                top5_items[index] = item
        for build in data[2]:
            differences = 0
            for item in build:
                if item in component_items:
                    continue
                if item not in top5_items:
                    differences += 1
            if differences >= 3:
                canditates.add(champion)

    return canditates, jungle_champions

def combine_champion_data(data1, data2):
    new_data = [data1[0] + data2[0], data1[1] + data2[1], data1[2] + data2[2], dict(), data1[4] + data2[4]]
    for item in data1[3]:
        if not data1[3][item] in new_data[3]:
            new_data[3][item] = 0
        new_data[3][item] += data1[3][item]

    for item in data2[3]:
        if not item in new_data[3]:
            new_data[3][item] = 0
        new_data[3][item] += data2[3][item]
    return new_data

def get_player_data():
    """
    players (dict):
        player_name (dict):
            champion_name (dict):
                [
                    frequency
                    [keystones]
                    [builds]
                    item name (dict):
                        frequency
                    [players]
                ]
    """
    with open("player_data.csv") as player_data:
        players = dict()
        for data in player_data:
            values = data.split(", ")
            values[-1] = values[-1].strip()
            if "" in values:
                values = values[:values.index("")]
            if not values[0] in players:
                players[values[0]] = dict()
            if not values[1] in players[values[0]]:
                players[values[0]][values[1]] = [0, [], [], dict()]
            players[values[0]][values[1]][0] += 1
            players[values[0]][values[1]][1].append(values[2])
            players[values[0]][values[1]][2].append(values[3:])
            for item in values[3:]:
                if not item in players[values[0]][values[1]][3]:
                    players[values[0]][values[1]][3][item] = 0
                players[values[0]][values[1]][3][item] += 1
    return players

component_items = set(["Caulfield's Warhammer", "Dagger", "Control Ward", "Zeal", "Chain Vest", "Needlessly Large Rod", "Kindlegem", "Amplifying Tome", "Ruby Crystal", "Jaurim's Fist", "Blasting Wand", "Refillable Potion", "Long Sword", "Brawler's Gloves", "Total Biscuit of Everlasting Will", "Cloth Armor", "Giant's Belt", "Crystalline Bracer", "Negatron Cloak", "Fiendish Codex", "Broken Stopwatch", "Bramble Vest", "Sheen", "Phage", "Health Potion", "B. F. Sword", "Hunter's Talisman", "Hunter's Machete", "Arcane Sweeper", "Slightly Magical Boots", "Recurve Bow", "Spectre's Cowl", "Vampiric Scepter", "Poro-Snax", "Pickaxe", "Bilgewater Cutlass", "Faerie Charm", "Serrated Dirk", "Oblivion Orb", "Hextech Revolver", "Forbidden Idol", "Glacial Shroud", "Stinger"])

if __name__ == "__main__":
    canditates, champion_data = find_jungle(get_player_data())
    print(canditates)
