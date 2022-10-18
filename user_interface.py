from model_construction import select_lineup
import sqlite3
import pandas as pd
from IPython.display import display
from tabulate import tabulate

con = sqlite3.connect("nba.db")
cur = con.cursor()

print(
    """
You will be asked for the number of guards, forwards, and centers you would like in the
lineup. You can have up to 5 of each position but the decision must add up to 5 or you 
run into an error. You will also be asked for the salary year you'd like to use (this
season or next season), and your budget. 
"""
)

while True:
    try:
        guard, forward, center = input(
            """Enter the number of guards, forwards, and centers in the lineup separated 
            by a comma (ex. 2,2,1 would be a 2 guard, 2 forward, 1 center lineup): """
        ).split(",", 2)
        guard = int(guard)
        forward = int(forward)
        center = int(center)

        if (
            guard not in [0, 1, 2, 3, 4, 5]
            or forward not in [0, 1, 2, 3, 4, 5]
            or center not in [0, 1, 2, 3, 4, 5]
        ):
            raise ValueError("Not numbers")
        elif guard + forward + center != 5:
            raise ValueError("Sum to 5")

    except ValueError as e:
        if str(e) == "Not numbers":
            print("Please choose a number 0-5 for each position separated by a comma.")
        elif str(e) == "Sum to 5":
            print("Please make sure the total number of players sums to 5.")
    else:
        break

salaryInput = ""
while True:
    try:
        salaryInput = input(
            """Enter the salary year you would like to use (enter 1 for this season (2021-22) 
        or 2 for next season (2022-23)): """
        )
        if salaryInput not in ["1", "2"]:
            raise ValueError("Invalid input.")

    except ValueError:
        print("Please enter 1 or 2.")
    else:
        break

salaryYear = 2122
if salaryInput == "2":
    salaryYear = 2223

while True:
    try:
        budget = float(
            input(
                """Enter the budget of the 5-man lineup (in millions). 
            You can use a decimal but please put in a number: """
            )
        )
    except ValueError:
        print("That is not a number. Try again!")
    else:
        break

print(
    """If you would like to add weights to certain statistics, input a number
    between 0 and 10. Decimals work. A weight of 0 takes out that statistic from
    the formula. The default weight for each statistic is 1. If you do not wish
    to add weights, press 'Enter' for each prompt. Statistcs are Points, 
    True Two Point Percentage, True Three Point Percentage, Free Throw 
    Percentage, Defensive Rebounding, Offensive Rebounding, Assist to Turnover 
    Ratio, Steals and Blocks."""
)

ato = 1.0
steals = 1.0
threes = 1.0
off_reb = 1.0
free_throw = 1.0
twos = 1.0
points = 1.0
def_reb = 1.0
blocks = 1.0

while True:
    try:
        points_input = input("""Points: """)
        if points_input == "":
            next
        else:
            points = float(points_input)

    except ValueError:
        print("Invalid input. Put a number 0-10 or press 'Enter' to keep the default.")

    else:
        break

while True:
    try:
        twos_input = input("""True Two Point Percentage: """)
        if twos_input == "":
            next
        else:
            twos = float(twos_input)

    except ValueError:
        print("Invalid input. Put a number 0-10 or press 'Enter' to keep the default.")

    else:
        break

while True:
    try:
        threes_input = input("""True Three Point Percentage: """)
        if threes_input == "":
            next
        else:
            threes = float(threes_input)

    except ValueError:
        print("Invalid input. Put a number 0-10 or press 'Enter' to keep the default.")

    else:
        break

while True:
    try:
        free_throw_input = input("""Free Throw Percentage: """)
        if free_throw_input == "":
            next
        else:
            free_throw = float(free_throw_input)

    except ValueError:
        print("Invalid input. Put a number 0-10 or press 'Enter' to keep the default.")

    else:
        break

while True:
    try:
        def_reb_input = input("""Defensive Rebounding: """)
        if def_reb_input == "":
            next
        else:
            def_reb = float(def_reb_input)

    except ValueError:
        print("Invalid input. Put a number 0-10 or press 'Enter' to keep the default.")

    else:
        break

while True:
    try:
        off_reb_input = input("""Offensive Rebounding: """)
        if off_reb_input == "":
            next
        else:
            off_reb = float(off_reb_input)

    except ValueError:
        print("Invalid input. Put a number 0-10 or press 'Enter' to keep the default.")

    else:
        break

while True:
    try:
        ato_input = input("""Assist to Turnover Ratio: """)
        if ato_input == "":
            next
        else:
            ato = float(ato_input)

    except ValueError:
        print("Invalid input. Put a number 0-10 or press 'Enter' to keep the default.")

    else:
        break

while True:
    try:
        steals_input = input("""Steals: """)
        if steals_input == "":
            next
        else:
            steals = float(steals_input)

    except ValueError:
        print("Invalid input. Put a number 0-10 or press 'Enter' to keep the default.")

    else:
        break

while True:
    try:
        blocks_input = input("""Blocks: """)
        if blocks_input == "":
            next
        else:
            blocks = float(blocks_input)

    except ValueError:
        print("Invalid input. Put a number 0-10 or press 'Enter' to keep the default.")

    else:
        break


print(
    select_lineup(
        guard,
        forward,
        center,
        salaryYear,
        budget,
        points,
        twos,
        threes,
        free_throw,
        def_reb,
        off_reb,
        ato,
        steals,
        blocks,
    )
)

best_lineup = select_lineup(
    guard,
    forward,
    center,
    salaryYear,
    budget,
    points,
    twos,
    threes,
    free_throw,
    def_reb,
    off_reb,
    ato,
    steals,
    blocks,
)

# Remove salaries from lineup lists
names = []
for lineup in best_lineup:
    lineup.pop()
    names.append(lineup)

# Convert from tuples to lists
best_lineup_names = []
for lineup in names:
    for position in lineup:
        best_lineup_names.append(list(position))

# Convert from lists of tuples to lists of strings
best_lineup_names2 = []
for lineup in best_lineup_names:
    list_names = [i for sub in lineup for i in sub]
    best_lineup_names2.append(list_names)


# Select player stats for players in the best lineup
stats_list = []
for j in range(0, 5):
    name = best_lineup_names2[0][j]
    stats_list.append(
        cur.execute(
            f"""SELECT Name, Position, Points, OffensiveRebounds, DefensiveRebounds,
            Assists, Turnovers, Steals, Blocks FROM PlayerStats WHERE Name = ('{name}')""",
        ).fetchone()
    )

# Convert to pandas data frame
df = pd.DataFrame(
    stats_list,
    columns=[
        "Name",
        "Position",
        "Points",
        "Offensive Rebounds",
        "Defensive Rebounds",
        "Assists",
        "Turnovers",
        "Steals",
        "Blocks",
    ],
)

# Create headers for table
table_headers = headers = [
    "Name",
    "Position",
    "Points",
    "Offensive Rebounds",
    "Defensive Rebounds",
    "Assists",
    "Turnovers",
    "Steals",
    "Blocks",
]

# Print table with player stats for best lineup
print(
    tabulate(
        df,
        headers=table_headers,
        tablefmt="psql",
    )
)

#  WHERE Name IN ({best_lineup})

# give option for how many lineups to output
# output salary
# Visualizations: Other top lineups besides the best lineup, show key stats
# Could also show top lineups if budget was increased by a $5M, $10M, etc.
