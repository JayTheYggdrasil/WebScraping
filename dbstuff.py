import sqlite3
from typing import Iterable

dbname = ":memory:"

ranks = ["Iron 4", "Iron 3", "Iron 2", "Iron 1", "Bronze 4", "Bronze 3", "Bronze 2", "Bronze 1", "Silver 4", "Silver 3",
         "Silver 2", "Silver 1", "Gold 4", "Gold 3", "Gold 2", "Gold 1", "Platinum 4", "Platinum 3", "Platinum 2",
         "Platinum 1", "Diamond 4", "Diamond 3", "Diamond 2", "Diamond 1", "Master", "Grandmaster", "Challenger"]

champions = ["AATROX", "AHRI", "AKALI", "ALISTAR", "AMUMU", "ANIVIA", "ANNIE", "APHELIOS", "ASHE", "AURELION", "SOL", "AZIR", "BARD", "BLITZCRANK", "BRAND", "BRAUM", "CAITLYN", "CAMILLE", "CASSIOPEIA", "CHO'GATH", "CORKI", "DARIUS", "DIANA", "DR.", "MUNDO", "DRAVEN", "EKKO", "ELISE", "EVELYNN", "EZREAL", "FIDDLESTICKS", "FIORA", "FIZZ", "GALIO", "GANGPLANK", "GAREN", "GNAR", "GRAGAS", "GRAVES", "HECARIM", "HEIMERDINGER", "ILLAOI", "IRELIA", "IVERN", "JANNA", "JARVAN", "IV", "JAX", "JAYCE", "JHIN", "JINX", "KAI'SA", "KALISTA", "KARMA", "KARTHUS", "KASSADIN", "KATARINA", "KAYLE", "KAYN", "KENNEN", "KHA'ZIX", "KINDRED", "KLED", "KOG'MAW", "LEBLANC", "LEE", "SIN", "LEONA", "LISSANDRA", "LUCIAN", "LULU", "LUX", "MALPHITE", "MALZAHAR", "MAOKAI", "MASTER", "YI", "MISS", "FORTUNE", "MORDEKAISER", "MORGANA", "NAMI", "NASUS", "NAUTILUS", "NEEKO", "NIDALEE", "NOCTURNE", "NUNU", "&", "WILLUMP", "OLAF", "ORIANNA", "ORNN", "PANTHEON", "POPPY", "PYKE", "QIYANA", "QUINN", "RAKAN", "RAMMUS", "REK'SAI", "RENEKTON", "RENGAR", "RIVEN", "RUMBLE", "RYZE", "SEJUANI", "SENNA", "SETT", "SHACO", "SHEN", "SHYVANA", "SINGED", "SION", "SIVIR", "SKARNER", "SONA", "SORAKA", "SWAIN", "SYLAS", "SYNDRA", "TAHM", "KENCH", "TALIYAH", "TALON", "TARIC", "TEEMO", "THRESH", "TRISTANA", "TRUNDLE", "TRYNDAMERE", "TWISTED", "FATE", "TWITCH", "UDYR", "URGOT", "VARUS", "VAYNE", "VEIGAR", "VEL'KOZ", "VI", "VIKTOR", "VLADIMIR", "VOLIBEAR", "WARWICK", "WUKONG", "XAYAH", "XERATH", "XIN", "ZHAO", "YASUO", "YORICK", "YUUMI", "ZAC", "ZED", "ZIGGS", "ZILEAN", "ZOE", "ZYRA"]

_all_items = ["Boots of Speed", "Enchantment: Warrior", "Faerie Charm", "Rejuvenation Bead", "Giant's Belt", "Cloak of Agility", "Blasting Wand",
             "Sapphire Crystal", "Ruby Crystal", "Cloth Armor", "Chain Vest", "Null-Magic Mantle", "Long Sword",
             "Pickaxe", "B. F. Sword", "Hunter's Talisman", "Hunter's Machete", "Dagger", "Recurve Bow",
             "Amplifying Tome", "Vampiric Scepter", "Doran's Shield", "Doran's Blade", "Doran's Ring", "Negatron Cloak",
             "Needlessly Large Rod", "Dark Seal", "Cull", "Health Potion", "Showdown Health Potion",
             "Total Biscuit of Rejuvenation", "Kircheis Shard", "Refillable Potion", "Corrupting Potion",
             "Oracle's Extract", "Guardian's Horn", "Poro-Snax", "Diet Poro-Snax", "Control Ward", "Shurelya's Reverie"
             "Elixir of Iron", "Elixir of Sorcery", "Elixir of Wrath", "Commencing Stopwatch", "Stopwatch",
             "Slightly Magical Boots", "Abyssal Mask", "Archangel's Staff", "Manamune", "Berserker's Greaves"
             "Archangel's Staff (Quick Charge)", "Manamune (Quick Charge)", "Boots of Swiftness", "Catalyst of Aeons",
             "Sorcerer's Shoes", "Frozen Mallet", "Glacial Shroud", "Iceborn Gauntlet", "Guardian Angel", "Rod of Ages",
             "Chalice of Harmony", "Rod of Ages (Quick Charge)", "Hextech GLP-800", "Infinity Edge", "Mortal Reminder",
             "Last Whisper", "Lord Dominik's Regards", "Seraph's Embrace", "Mejai's Soulstealer", "Muramana", "Phage",
             "Phantom Dancer", "Ninja Tabi", "Zeke's Convergence", "Jaurim's Fist", "Sterak's Gage"
             "Sheen", "Spirit Visage", "Kindlegem", "Sunfire Cape", "Tear of the Goddess", "Black Cleaver",
             "Bloodthirster", "Tear of the Goddess (Quick Charge)", "Ravenous Hydra", "Thornmail", "Bramble Vest",
             "Tiamat", "Trinity Force", "Warden's Mail", "Warmog's Armor", "Runaan's Hurricane", "Zeal", "Statikk Shiv",
             "Rabadon's Deathcap", "Wit's End", "Rapid Firecannon", "Stormrazor", "Lich Bane", "Stinger",
             "Banshee's Veil", "Aegis of the Legion", "Redemption", "Fiendish Codex", "Knight's Vow", "Frozen Heart",
             "Mercury's Treads", "Guardian's Orb", "Aether Wisp", "Forbidden Idol", "Nashor's Tooth"
             "Rylai's Crystal Scepter", "Boots of Mobility", "Executioner's Calling", "Guinsoo's Rageblade"
             "Caulfield's Warhammer", "Serrated Dirk", "Void Staff", "Haunting Guise", "Mercurial Scimitar",
             "Quicksilver Sash", "Youmuu's Ghostblade", "Randuin's Omen", "Bilgewater Cutlass", "Hextech Revolver",
             "Hextech Gunblade", "Duskblade of Draktharr", "Liandry's Torment", "Hextech Protobelt-01",
             "Blade of the Ruined King", "Hexdrinker", "Maw of Malmortius", "Zhonya's Hourglass"
             "Ionian Boots of Lucidity", "Morellonomicon", "Athene's Unholy Grail", "Umbral Glaive", "Sanguine Blade",
             "Guardian's Hammer", "Locket of the Iron Solari", "Seeker's Armguard", "Gargoyle Stoneplate",
             "Adaptive Helm", "Hex Core mk-1", "Hex Core mk-2", "Perfect Hex Core", "Prototype Hex Core",
             "Spectre's Cowl", "Mikael's Crucible", "Luden's Echo", "Warding Totem (Trinket)", "Arcane Sweeper",
             "Greater Stealth Totem (Trinket)", "Greater Vision Totem (Trinket)", "Farsight Alteration", "Oracle Lens",
             "Molten Edge", "Forgefire Cape", "Rabadon's Deathcrown", "Infernal Mask", "Obsidian Cleaver", "Salvation",
             "Circlet of the Iron Solari", "Trinity Fusion", "Zhonya's Paradox", "Frozen Fist", "Youmuu's Wraithblade"
             "Might of the Ruined King", "Luden's Pulse", "Ardent Censer", "Essence Reaver", "Black Spear",
             "Frosted Snax", "Super Spicy Snax", "Espresso Snax", "Rainbow Snax Party Pack!", "Dawnbringer Snax",
             "Nightbringer Snax", "Stalker's Blade", "Skirmisher's Sabre", "Dead Man's Plate", "Titanic Hydra",
             "Bami's Cinder", "Righteous Glory", "Crystalline Bracer", "Lost Chapter", "Death's Dance", "Edge of Night",
             "Spellthief's Edge", "Frostfang Shard of True Ice", "Steel Shoulderguards", "Runesteel Spaulders",
             "Pauldrons of Whiterock", "Relic Shield", "Targon's Buckler", "Bulwark of the Mountain", "Spectral Sickle",
             "Harrowing Crescent", "Black Mist Scythe", "Twin Shadows", "Spellbinder", "Oblivion Orb"]

_complete_items = ["Shurelya's Reverie", "Abyssal Mask", "Archangel's Staff", "Manamune", "Berserker's Greaves",
                  "Boots of Swiftness", "Enchantment: Warrior",  "Enchantment: Runic Echoes",
                  "Sorcerer's Shoes", "Frozen Mallet", "Glacial Shroud", "Iceborn Gauntlet", "Guardian Angel",
                  "Rod of Ages", "Hextech GLP-800", "Infinity Edge", "Mortal Reminder",
                  "Lord Dominik's Regards", "Mejai's Soulstealer", "Muramana", "Phantom Dancer",
                  "Ninja Tabi", "Seraph's Embrace", "Zeke's Convergence", "Jaurim's Fist", "Sterak's Gage",
                  "Spirit Visage", "Sunfire Cape", "Black Cleaver", "Bloodthirster",
                  "Ravenous Hydra", "Thornmail", "Tiamat", "Trinity Force",
                  "Warmog's Armor", "Runaan's Hurricane", "Statikk Shiv", "Rabadon's Deathcap", "Wit's End",
                  "Rapid Firecannon", "Stormrazor", "Lich Bane", "Banshee's Veil" "Aegis of the Legion", "Redemption",
                  "Knight's Vow", "Frozen Heart", "Mercury's Treads", "Nashor's Tooth", "Rylai's Crystal Scepter",
                  "Boots of Mobility", "Guinsoo's Rageblade", "Void Staff", "Mercurial Scimitar", "Youmuu's Ghostblade",
                  "Randuin's Omen", "Hextech Gunblade", "Duskblade of Draktharr", "Liandry's Torment",
                  "Hextech Protobelt-01", "Blade of the Ruined King", "Maw of Malmortius", "Zhonya's Hourglass",
                  "Ionian Boots of Lucidity", "Morellonomicon", "Athene's Unholy Grail", "Umbral Glaive",
                  "Sanguine Blade", "Locket of the Iron Solari", "Seeker's Armguard", "Gargoyle Stoneplate",
                  "Adaptive Helm", "Hex Core mk-1", "Hex Core mk-2", "Perfect Hex Core", "Prototype Hex Core",
                  "Mikael's Crucible", "Luden's Echo", "Molten Edge", "Forgefire Cape", "Rabadon's Deathcrown",
                  "Infernal Mask", "Obsidian Cleaver", "Salvation", "Circlet of the Iron Solari", "Trinity Fusion",
                  "Zhonya's Paradox", "Frozen Fist", "Youmuu's Wraithblade", "Might of the Ruined King",
                  "Luden's Pulse", "Ardent Censer", "Essence Reaver", "Stalker's Blade", "Skirmisher's Sabre",
                  "Dead Man's Plate", "Titanic Hydra", "Righteous Glory", "Death's Dance", "Edge of Night",
                  "Spellthief's Edge", "Frostfang Shard of True Ice", "Steel Shoulderguards", "Runesteel Spaulders",
                  "Pauldrons of Whiterock", "Relic Shield", "Targon's Buckler", "Bulwark of the Mountain",
                  "Spectral Sickle", "Harrowing Crescent", "Black Mist Scythe", "Twin Shadows", "Spellbinder"]


def to_db_name(item):
    if isinstance(item, Iterable) and not isinstance(item, str):
        o = []
        for i in item:
           o.append(to_db_name(i))
        return o
    a = item.lower()
    a = a.replace(" ", "_")
    a = a.replace(":", "")
    a = a.replace("'", "")
    a = a.replace("-", "")
    return a


item_namespace = to_db_name(_complete_items)

complete_items = set(_complete_items)
all_items = set(_all_items)
component_items = all_items - complete_items


def create_tables(cur):
    try:
        cur.execute("""CREATE TABLE games (
                game_id INTEGER PRIMARY KEY,
                name VARCHAR(40),
                rank VARCHAR(20),
                role VARCHAR(10),
                champion VARCHAR(40),
                keystone VARCHAR(40)
            );"""
        )

        cur.execute("""CREATE TABLE players (
                    name VARCHAR(40)
                );"""
        )

        cur.execute(
            """CREATE TABLE items (
                game_id int,
                item VARCHAR(40)
            );"""
        )
    except sqlite3.OperationalError:
        print("db already exists")


def insert_into_db(cur, conn, name, rank, role, champion, keystone, items):
    items = to_db_name(items)
    champion = to_db_name(champion)
    keystone = to_db_name(keystone)

    i = (name, rank, role, champion, keystone)
    cur.execute('INSERT INTO games (name, rank, role, champion, keystone) VALUES (?, ?, ?, ?, ?)', i)
    id = cur.lastrowid
    conn.commit()
    cur.execute('INSERT INTO players VALUES (?)', (name, ))
    conn.commit()

    for item in items:
        cur.execute("INSERT INTO items VALUES (?, ?)", (id, item))
        conn.commit()


def contains_player(cur, name):
    cur.execute("SELECT name FROM players WHERE name = ?", (name,))
    return cur.fetchone() is not None

def test(cur, conn):
    for i in range(100):
        insert_into_db(cur, conn, "jeff" + str(i), "Iron 4", "Top", "Kindred", "Press The Attack", ["Shurelya's Reverie",
                                                                                               'Abyssal Mask'])

    cur.execute("SELECT * FROM games WHERE name='jeff5'")
    print(cur.fetchall())

    cur.execute("SELECT * FROM games, items WHERE name='jeff0' AND games.game_id=items.game_id")
    print(cur.fetchall())

    cur.execute("SELECT * FROM items")
    print(cur.fetchall())

    cur.execute("SELECT item as TEXT FROM items GROUP BY game_id")
    v = cur.fetchall()
    print(v)


if __name__ == "__main__":
    with sqlite3.connect(dbname) as conn:
        cur = conn.cursor()
        create_tables(cur)
        test(cur, conn)
