"""Build and compile model."""
import sqlite3
from itertools import combinations, product

con = sqlite3.connect("nba.db")

cur = con.cursor()


def get_max(column: str, position: str):
    "Get max value for a given variable."
    max = cur.execute(
        f"""
        SELECT MAX({column}) FROM PlayerStats
        WHERE GamesPlayed > 15
        AND ThreePointersAttempted > 2
        AND Position IN ({position})
        """,
        # The ThreePointersAttempted variable is actually the average number of
        # 3 pointers attempted per game, so I decied that 2 was a reasonable
        # average to reduce an individual playing in just a few games and
        # hitting most of his 3's
    )
    return max.fetchone()[0]


# My idea is to normalize each of the metrics by the maximum value in all of
# the data, since this is a competition then we can compare individuals to
# others

# The argument could be made that since we are selecting players by position,
# then we should normalize by the max for a specific metric only among players
# in that same position, which is very fair. BUT I am going to start more
# simple than that.

# UPDATE: I added in the functionality to only include players in that position
# for the maximum calculation.


###############################################################################
# Guards
###############################################################################


def guard_normalize_query(position: str):
    """Create columns that are normalized."""
    query = f"""
        CREATE TABLE GuardsNormalizedStats AS
            SELECT
                ps.Name,
                Position,
                ROUND(ThreePointersAttempted  * ThreePointersPct /
                    {get_max("ThreePointersAttempted * ThreePointersPct",
                    position)},3) AS j_threes,
                ROUND((Assists / Turnovers) / {get_max("Assists / Turnovers",
                    position)},3) AS j_atr,
                ROUND(Steals / {get_max("Steals", position)}, 3) AS j_stl,
                ROUND(OffensiveRebounds / {get_max("OffensiveRebounds",
                    position)}, 3) AS j_or,
                ROUND((FreeThrowsAttempted * FreeThrowPct) /
                    {get_max("FreeThrowsAttempted * FreeThrowPct",
                    position)},3) AS j_ft,
                ROUND((TwoPointersAttempted * TwoPointersPct) /
                    {get_max("TwoPointersAttempted * TwoPointersPct",
                    position)},3) AS j_twos,
                ROUND(("Points") / {get_max("Points", position)}) AS j_points
            FROM PlayerStats ps
            LEFT JOIN Salary s
            ON ps.Name = s.Name
            WHERE ps.Position IN ({position})
            AND GamesPlayed > 15
            AND ThreePointersAttempted > 2
            ORDER BY s.Salary2122
            """
    return query


cur.execute("DROP TABLE IF EXISTS GuardsNormalizedStats")
cur.execute(guard_normalize_query("'PG', 'SG'"))
con.commit()


def guard_selections(
    table: str,
    number_players: int,
    w1: float,
    w2: float,
    w3: float,
    w4: float,
    w5: float,
    w6: float,
    w7: float,
):
    "Make Selections."
    query = f"""
    SELECT
        Name,
        ({w1} * j_threes) + ({w2} * j_atr) + ({w3} * j_stl) + ({w4} * j_or) +
        ({w5} * j_ft) + ({w6} * j_twos) + ({w7} * j_points) AS rank
    FROM {table}
    ORDER BY rank DESC
    LIMIT {number_players}
    """
    return query


top5 = []
guard_ranked = cur.execute(
    guard_selections("GuardsNormalizedStats", 2, 3, 3, 2, 1, 4, 2, 3)
)
for i in guard_ranked:
    top5.append(i[0])


###############################################################################
# Forwards
###############################################################################


def forward_normalize_query(position: str):
    "Create columns that are normalized"
    query = f"""
        CREATE TABLE ForwardsNormalizedStats AS
            SELECT
                ps.Name,
                Position,
                ROUND(ThreePointersAttempted  * ThreePointersPct /
                    {get_max("ThreePointersAttempted * ThreePointersPct",
                    position)},3) AS j_threes,
                ROUND((Assists / Turnovers) / {get_max("Assists / Turnovers",
                    position)},3) AS j_atr,
                ROUND(DefensiveRebounds / {get_max("DefensiveRebounds",
                    position)}, 3) AS j_dr,
                ROUND(OffensiveRebounds / {get_max("OffensiveRebounds",
                    position)}, 3) AS j_or,
                ROUND((FreeThrowsAttempted * FreeThrowPct) /
                    {get_max("FreeThrowsAttempted * FreeThrowPct",
                    position)},3) AS j_ft,
                ROUND((TwoPointersAttempted * TwoPointersPct) /
                    {get_max("TwoPointersAttempted * TwoPointersPct",
                    position)},3) AS j_twos,
                ROUND(Blocks / {get_max("Blocks", position)}, 3) AS j_blocks,
                ROUND(Points / {get_max("Points", position)}, 3) AS j_points
            FROM PlayerStats ps
            LEFT JOIN Salary s
            ON ps.Name = s.Name
            WHERE ps.Position IN ({position})
            AND GamesPlayed > 15
            AND ThreePointersAttempted > 2
            ORDER BY s.Salary2122
            """
    return query


cur.execute("DROP TABLE IF EXISTS ForwardsNormalizedStats")
cur.execute(forward_normalize_query("'PF', 'SF'"))
con.commit()


def forward_selections(
    table: str,
    number_players: int,
    w1: float,
    w2: float,
    w3: float,
    w4: float,
    w5: float,
    w6: float,
    w7: float,
    w8: float,
):
    "Make Selections."
    query = f"""
    SELECT
        Name,
        ({w1} * j_threes) + ({w2} * j_atr) + ({w3} * j_dr) + ({w4} * j_or) +
        ({w5} * j_ft) + ({w6} * j_twos) + ({w7} * j_blocks) + ({w8} *j_points)
            AS rank
    FROM {table}
    ORDER BY rank DESC
    LIMIT {number_players}
    """
    return query


forward_ranked = cur.execute(
    forward_selections("ForwardsNormalizedStats", 2, 2, 2, 3, 3, 3, 3, 4, 3)
)
for i in forward_ranked:
    top5.append(i[0])

###############################################################################
# Centers
###############################################################################


def center_normalize_query(position: str):
    "Create columns that are normalized"
    query = f"""
        CREATE TABLE CentersNormalizedStats AS
            SELECT
                ps.Name,
                Position,
                ROUND((Assists / Turnovers) / {get_max("Assists / Turnovers",
                    position)},3) AS j_atr,
                ROUND(DefensiveRebounds / {get_max("DefensiveRebounds",
                    position)}, 3) AS j_dr,
                ROUND(OffensiveRebounds / {get_max("OffensiveRebounds",
                    position)}, 3) AS j_or,
                ROUND((FreeThrowsAttempted * FreeThrowPct) /
                    {get_max("FreeThrowsAttempted * FreeThrowPct",
                    position)},3) AS j_ft,
                ROUND((TwoPointersAttempted * TwoPointersPct) /
                    {get_max("TwoPointersAttempted * TwoPointersPct",
                    position)},3) AS j_twos,
                ROUND(Blocks / {get_max("Blocks", position)}, 3) AS j_blocks,
                ROUND(Points / {get_max("Points", position)}, 3) AS j_points
            FROM PlayerStats ps
            LEFT JOIN Salary s
            ON ps.Name = s.Name
            WHERE ps.Position IN ({position})
            AND GamesPlayed > 15
            AND ThreePointersAttempted > 2
            ORDER BY s.Salary2122
            """
    return query


cur.execute("DROP TABLE IF EXISTS CentersNormalizedStats")
cur.execute(center_normalize_query("'C'"))
con.commit()


def center_selections(
    table: str,
    number_players: int,
    w1: float,
    w2: float,
    w3: float,
    w4: float,
    w5: float,
    w6: float,
    w7: float,
):
    "Make Selections."
    query = f"""
    SELECT
        Name,
        ({w1} * j_atr) + ({w2} * j_dr) + ({w3} * j_or) + ({w4} * j_ft) +
        ({w5} * j_twos) + ({w6} * j_blocks) + ({w7} * j_points) AS rank
    FROM {table}
    ORDER BY rank DESC
    LIMIT {number_players}
    """
    return query


center_ranked = cur.execute(
    center_selections("CentersNormalizedStats", 1, 7, 3, 5, 8, 2, 4, 4)
)
for i in center_ranked:
    top5.append(i[0])

salaryTop5 = []
for i in top5:
    salary = cur.execute(f"SELECT Salary2122 FROM Salary WHERE Name = '{i}'")
    for j in salary:
        salaryTop5.append(j[0])


def get_position_combinations(
    type: str,
    numPlayers: int,
    numInLineup: int,
    salaryYear: int,
    points: float,
    twos: float,
    threes: float,
    free_throw: float,
    def_reb: float,
    off_reb: float,
    ato: float,
    steals: float,
    blocks: float,
):
    """Gets all the combinations for the position desired based on the user
    input criteria"""
    name = []
    rating = []
    if type == "guard":
        data = cur.execute(
            guard_selections(
                "GuardsNormalizedStats",
                numPlayers,
                threes,
                ato,
                steals,
                off_reb,
                free_throw,
                twos,
                points,
            )
        )
    elif type == "forward":
        data = cur.execute(
            forward_selections(
                "ForwardsNormalizedStats",
                numPlayers,
                threes,
                ato,
                def_reb,
                off_reb,
                free_throw,
                twos,
                blocks,
                points,
            )
        )
    elif type == "center":
        data = cur.execute(
            center_selections(
                "CentersNormalizedStats",
                numPlayers,
                ato,
                def_reb,
                off_reb,
                free_throw,
                twos,
                blocks,
                points,
            )
        )

    for i in data:
        name.append(i[0])
        rating.append(i[1])

    salary = []
    for i in name:
        player_salary = cur.execute(
            f"SELECT Salary{salaryYear} FROM Salary WHERE Name = '{i}'"
        )
        for j in player_salary:
            salary.append(j[0])

    name_combos = list(combinations(name, numInLineup))

    rating_combos = list(combinations(rating, numInLineup))
    rating_combo_sum = []
    for i in rating_combos:
        rating_combo_sum.append(sum(i))

    salary_combos = list(combinations(salary, numInLineup))
    salary_combo_sum = []
    for i in salary_combos:
        salary_combo_sum.append(sum(i))

    all_data = [name_combos, rating_combo_sum, salary_combo_sum]

    return all_data


def select_lineup(
    num_guard: int,
    num_forward: int,
    num_center: int,
    salaryYear: int,
    budget: float,
    points: float,
    twos: float,
    threes: float,
    free_throw: float,
    def_reb: float,
    off_reb: float,
    ato: float,
    steals: float,
    blocks: float,
):
    """Gets the lineup based on the user input. Runs the functions above to get the
    different combinations. Starts with the top 5 players at each position, and goes
    up to the top 40 incrementally by 1 until it gets a lineup that meets the criteria.
    Prints a line that tells the user to change the input if no lineup is found."""
    num_combo = 5
    output = []
    used_combos = []
    while len(output) < 5:
        if num_combo == 40:
            print("Invalid input. Please try a higher budget or change a field.")
            break

        guards = get_position_combinations(
            "guard",
            num_combo,
            num_guard,
            salaryYear,
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
        forwards = get_position_combinations(
            "forward",
            num_combo,
            num_forward,
            salaryYear,
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
        centers = get_position_combinations(
            "center",
            num_combo,
            num_center,
            salaryYear,
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
        num_combo += 1

        all_name = [guards[0], forwards[0], centers[0]]
        all_name_combos = list(product(*all_name))

        all_salary = [guards[2], forwards[2], centers[2]]
        all_salary_combos = list(product(*all_salary))
        all_salary_combos_sum = []
        for i in all_salary_combos:
            all_salary_combos_sum.append(sum(i))

        salary_index = []
        for i in range(len(all_salary_combos_sum)):
            if all_salary_combos_sum[i] < (budget * 1000000):
                salary_index.append(i)

        if salary_index == []:
            continue

        all_rating = [guards[1], forwards[1], centers[1]]
        all_rating_combos = list(product(*all_rating))
        all_rating_combos_sum = []
        for i in all_rating_combos:
            all_rating_combos_sum.append(sum(i))

        while len(output) < 5 and salary_index != []:
            best_index = 0
            best_rating = 0
            for i in salary_index:
                if all_rating_combos_sum[i] > best_rating:
                    best_rating = all_rating_combos_sum[i]
                    best_index = i

            if all_name_combos[best_index] in used_combos:
                salary_index.remove(best_index)
            else:
                output.append(
                    [all_name_combos[best_index], all_salary_combos_sum[best_index]]
                )
                used_combos.append(all_name_combos[best_index])
                salary_index.remove(best_index)

    return output
