"""Parses player salary data from https://hoopshype.com/salaries/players/"""
from pytest import skip
import requests
from bs4 import BeautifulSoup
import sqlite3
import os

URL = "https://hoopshype.com/salaries/players/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

results = soup.find(id="wrapper")
wrapper = results.find("div", class_="wrapper-holder")
main_div = wrapper.find("div", class_="site-main")
content_area = main_div.find("div", class_="content-area")
site_content = content_area.find("div", class_="site-content")
container_divider = site_content.find("div", class_="container divider")
entry_content = container_divider.find("div", class_="entry-content")
hoopshype = entry_content.find(
    "div", class_="hoopshype-salaries-wrap tabs tabs-noinit hoopshype-salaries-players"
)
hhsalaries = hoopshype.find("div", class_="hh-salaries-ranking")
salary_table = hhsalaries.find(
    "table", class_="hh-salaries-ranking-table hh-salaries-table-sortable responsive"
)

body = salary_table.find("tbody")
all_players = body.find_all("tr")

con = sqlite3.connect("nba.db")

cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS Salary")
cur.execute(
    """CREATE TABLE Salary (
                    [Name] VARCHAR(50) PRIMARY KEY,
                    [Salary2122] INTEGER,
                    [Salary2223] INTEGER)"""
)

for player in all_players:
    player_data = player.find_all("td")
    name = player_data[1].find("a").text.strip()
    name = name.replace("'", "")
    name = name.replace(" Jr", "")
    year2122 = int(player_data[2].get("data-value"))
    if player_data[3].get("data-value") == "0":
        year2223 = year2122
    elif float(player_data[3].get("data-value")) < 1:
        year2223 = int(100000000 * float(player_data[3].get("data-value")))
    else:
        year2223 = int(player_data[3].get("data-value"))
    player_info = [name, year2122, year2223]
    cur.execute("INSERT INTO Salary VALUES (?, ?, ?)", player_info)

con.commit()

nba_table = cur.execute("SELECT * FROM Salary")
for row in nba_table:
    print(row)

# print(steph[2].text.strip())
# print(steph_name.text.strip())

# with open("help.txt", "w") as f:
#     f.write(str(salary_table))

# print(page.text)
