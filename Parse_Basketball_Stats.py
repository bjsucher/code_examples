"""Parse the basketball statistics data from 
https://www.basketball-reference.com/leagues/NBA_2022_per_game.html"""
import sqlite3
import os
import requests
import unidecode
from bs4 import BeautifulSoup

con = sqlite3.connect("nba.db")

cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS PlayerStats")
cur.execute(
    """CREATE TABLE PlayerStats (
                    [Name] VARCHAR(50) PRIMARY KEY,
                    [Position] VARCHAR(2),
                    [Age] INTEGER,
                    [GamesPlayed] INTEGER,
                    [GamesStarted] INTEGER,
                    [MinutesPlayed] DECIMAL(2,1),
                    [FieldGoalsMade] DECIMAL(2,1),
                    [FieldGoalsAttempted] DECIMAL(2,1),
                    [FieldGoalPct] DECIMAL(0,3),
                    [ThreePointersMade] DECIMAL(2,1),
                    [ThreePointersAttempted] DECIMAL(2,1),
                    [ThreePointersPct] DECIMAL(0,3),
                    [TwoPointersMade] DECIMAL(2,1),
                    [TwoPointersAttempted] DECIMAL(2,1),
                    [TwoPointersPct] DECIMAL(0,3),
                    [EffectiveFieldGoalPct] DECIMAL(0,3),
                    [FreeThrowsMade] DECIMAL(2,1),
                    [FreeThrowsAttempted] DECIMAL(2,1),
                    [FreeThrowPct] DECIMAL(0,3),
                    [OffensiveRebounds] DECIMAL(2,1),
                    [DefensiveRebounds] DECIMAL(2,1),
                    [TotalRebounds] DECIMAL(2,1),
                    [Assists] DECIMAL(2,1),
                    [Steals] DECIMAL(2,1),
                    [Blocks] DECIMAL(2,1),
                    [Turnovers] DECIMAL(2,1),
                    [PersonalFouls] DECIMAL(2,1),
                    [Points] DECIMAL(2,1),
                    [Year] INT)"""
)


def parse_stats_by_year(year: int):
    """Parses the statistics by year. Currently we only use 2022 data but function
    can be used to grab data from other years as well"""
    URL = "https://www.basketball-reference.com/leagues/NBA_" + year + "_per_game.html"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find(id="wrap")
    content = results.find("div", id="content")
    stats = content.find("div", id="all_per_game_stats")
    div_stats = stats.find("div", id="div_per_game_stats")
    table_stats = div_stats.find("table", id="per_game_stats")
    body = table_stats.find("tbody")
    all_players = body.find_all("tr")
    player_name = ""

    for player in all_players:
        player_data = player.find_all("td")
        if player_data == []:
            next
        else:
            player_info = []
            if player_data[0].text == player_name:
                next
            else:
                player_name = player_data[0].text
                for i in range(len(player_data)):
                    if i == 0:
                        name = unidecode.unidecode(player_data[i].text)
                        for i in ["'", " IV", " III", " II", " Jr.", " Sr.", "."]:
                            name = name.replace(i, "")
                        player_info.append(name)
                    elif i == 1:
                        player_info.append(player_data[i].text)
                    elif i == 3:
                        next
                    elif i in [2, 4, 5]:
                        player_info.append(int(player_data[i].text))
                    else:
                        if player_data[i].text == "":
                            player_info.append(0.0)
                        else:
                            player_info.append(float(player_data[i].text))

                player_info.append(int(year))
                cur.execute(
                    "INSERT INTO PlayerStats VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    player_info,
                )

    return


parse_stats_by_year("2022")

con.commit()

# nba_table = cur.execute("SELECT * FROM PlayerStats")
# for row in nba_table:
#     print(row)
