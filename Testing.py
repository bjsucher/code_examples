"""Test functions for NBA-Best."""
from model_construction import (
    get_max,
    guard_normalize_query,
    forward_normalize_query,
    center_normalize_query,
    get_position_combinations,
    select_lineup,
)


def test_get_max():
    "Test the get_max function."
    assert get_max("TwoPointersPct", "'PG', 'SG'") == 0.673
    assert get_max("TwoPointersAttempted", "'PG', 'SG'") == 16.2
    assert round(get_max("Assists / Turnovers", "'PG', 'SG'"), 1) == 7.3
    assert get_max("Blocks", "'C'") == 2.8


def test_guard_normalize_query():
    "Test the guard_normalize_query function."
    assert (
        guard_normalize_query("'PG', 'SG'")
        == """
        CREATE TABLE GuardsNormalizedStats AS
            SELECT
                ps.Name,
                Position,
                ROUND(ThreePointersAttempted  * ThreePointersPct /
                    4.446,3) AS j_threes,
                ROUND((Assists / Turnovers) / 7.333333333333334,3) AS j_atr,
                ROUND(Steals / 2, 3) AS j_stl,
                ROUND(OffensiveRebounds / 1.8, 3) AS j_or,
                ROUND((FreeThrowsAttempted * FreeThrowPct) /
                    6.5992,3) AS j_ft,
                ROUND((TwoPointersAttempted * TwoPointersPct) /
                    8.6508,3) AS j_twos,
                ROUND(("Points") / 28.4) AS j_points
            FROM PlayerStats ps
            LEFT JOIN Salary s
            ON ps.Name = s.Name
            WHERE ps.Position IN ('PG', 'SG')
            AND GamesPlayed > 15
            AND ThreePointersAttempted > 2
            ORDER BY s.Salary2122
            """
    )


def test_forward_normalize_query():
    "Test the guard_normalize_query function."
    assert (
        forward_normalize_query("'PF', 'SF'")
        == """
        CREATE TABLE ForwardsNormalizedStats AS
            SELECT
                ps.Name,
                Position,
                ROUND(ThreePointersAttempted  * ThreePointersPct /
                    3.0357999999999996,3) AS j_threes,
                ROUND((Assists / Turnovers) / 4.2,3) AS j_atr,
                ROUND(DefensiveRebounds / 9.6, 3) AS j_dr,
                ROUND(OffensiveRebounds / 2.6, 3) AS j_or,
                ROUND((FreeThrowsAttempted * FreeThrowPct) /
                    8.2308,3) AS j_ft,
                ROUND((TwoPointersAttempted * TwoPointersPct) /
                    9.24,3) AS j_twos,
                ROUND(Blocks / 2.3, 3) AS j_blocks,
                ROUND(Points / 30.3, 3) AS j_points
            FROM PlayerStats ps
            LEFT JOIN Salary s
            ON ps.Name = s.Name
            WHERE ps.Position IN ('PF', 'SF')
            AND GamesPlayed > 15
            AND ThreePointersAttempted > 2
            ORDER BY s.Salary2122
            """
    )


def test_center_normalize_query():
    "Test the center_normalzie_query function."
    assert (
        center_normalize_query("'C'")
        == """
        CREATE TABLE CentersNormalizedStats AS
            SELECT
                ps.Name,
                Position,
                ROUND((Assists / Turnovers) / 3.7777777777777777,3) AS j_atr,
                ROUND(DefensiveRebounds / 11, 3) AS j_dr,
                ROUND(OffensiveRebounds / 3.1, 3) AS j_or,
                ROUND((FreeThrowsAttempted * FreeThrowPct) /
                    9.6052,3) AS j_ft,
                ROUND((TwoPointersAttempted * TwoPointersPct) /
                    8.9976,3) AS j_twos,
                ROUND(Blocks / 2.8, 3) AS j_blocks,
                ROUND(Points / 30.6, 3) AS j_points
            FROM PlayerStats ps
            LEFT JOIN Salary s
            ON ps.Name = s.Name
            WHERE ps.Position IN ('C')
            AND GamesPlayed > 15
            AND ThreePointersAttempted > 2
            ORDER BY s.Salary2122
            """
    )


def test_get_position_combinations():
    "Test get_position_combinations function."
    assert get_position_combinations(
        "forward", 40, 1, 2122, 3.0, 3.0, 2.0, 4.0, 4.0, 5.0, 4.0, 2.0, 2.0
    ) == [
        [
            ("Giannis Antetokounmpo",),
            ("LeBron James",),
            ("Kevin Durant",),
            ("Pascal Siakam",),
            ("Kristaps Porzingis",),
            ("Jayson Tatum",),
            ("Julius Randle",),
            ("Scottie Barnes",),
            ("Miles Bridges",),
            ("John Collins",),
            ("Brandon Ingram",),
            ("Paul George",),
            ("Jaylen Brown",),
            ("Jaren Jackson",),
            ("Kyle Kuzma",),
            ("Zach LaVine",),
            ("Tobias Harris",),
            ("RJ Barrett",),
            ("Khris Middleton",),
            ("Saddiq Bey",),
            ("OG Anunoby",),
            ("Aaron Gordon",),
            ("Harrison Barnes",),
            ("Keldon Johnson",),
            ("Jerami Grant",),
            ("Kevin Love",),
            ("Andrew Wiggins",),
            ("Gordon Hayward",),
            ("Franz Wagner",),
            ("Mikal Bridges",),
            ("Lauri Markkanen",),
            ("Desmond Bane",),
            ("Dillon Brooks",),
            ("JaeSean Tate",),
            ("Chris Boucher",),
            ("Terance Mann",),
            ("Isaiah Roby",),
            ("Bojan Bogdanovic",),
            ("Luguentz Dort",),
            ("Otto Porter",),
        ],
        [
            21.389999999999997,
            17.593,
            16.709,
            16.3,
            16.252,
            16.236,
            15.458999999999998,
            14.331000000000001,
            13.875999999999998,
            13.495000000000001,
            13.475999999999999,
            13.343,
            13.012,
            12.99,
            12.829,
            12.669,
            12.603000000000002,
            12.165,
            12.13,
            12.071,
            11.94,
            11.757,
            11.756,
            11.613,
            11.602999999999998,
            11.344,
            11.218,
            10.760000000000002,
            10.669000000000002,
            10.662,
            10.658999999999999,
            10.658000000000001,
            10.594,
            10.505999999999998,
            10.436,
            10.399,
            10.198,
            10.157000000000002,
            10.009,
            9.957,
        ],
        [
            39344900,
            41180544,
            42018900,
            33003936,
            31650600,
            28103500,
            21780000,
            7280400,
            5421493,
            23000000,
            29467800,
            39344970,
            26758928,
            9180560,
            13000000,
            19500000,
            35995950,
            8623920,
            35500000,
            2824320,
            16071429,
            16409091,
            20284091,
            2145720,
            20002500,
            31258256,
            31579390,
            29925000,
            5007840,
            5557725,
            15690909,
            2033160,
            12200000,
            1517981,
            7020000,
            1782621,
            1782621,
            18700000,
            1782621,
            2389641,
        ],
    ]
    assert get_position_combinations(
        "guard", 20, 1, 2122, 2.0, 3.0, 4.0, 7.0, 1.0, 2.0, 3.0, 9.0, 1.0
    ) == [
        [
            ("Dejounte Murray",),
            ("Luka Doncic",),
            ("Ja Morant",),
            ("Trae Young",),
            ("Donovan Mitchell",),
            ("Kyrie Irving",),
            ("Shai Gilgeous-Alexander",),
            ("Stephen Curry",),
            ("Fred VanVleet",),
            ("LaMelo Ball",),
            ("Devin Booker",),
            ("Chris Paul",),
            ("Anthony Edwards",),
            ("Gary Trent",),
            ("DeAaron Fox",),
            ("Jrue Holiday",),
            ("Darius Garland",),
            ("Terry Rozier",),
            ("Bradley Beal",),
            ("Damian Lillard",),
        ],
        [
            20.508,
            20.253,
            20.049,
            19.753,
            19.744,
            19.527,
            19.515,
            19.162000000000003,
            19.055,
            18.756,
            18.286,
            17.969,
            17.9,
            17.414,
            17.082,
            17.076,
            16.994,
            16.461000000000002,
            16.363,
            16.351999999999997,
        ],
        [
            15428880,
            10174391,
            9603360,
            8326471,
            28103500,
            35328700,
            5495532,
            45780966,
            19675926,
            8231760,
            31650600,
            30800000,
            10245480,
            16000000,
            28103500,
            32431333,
            7040880,
            17905263,
            33724200,
            39344900,
        ],
    ]


def test_select_lineup():
    "Test the select_lineup function."
    assert select_lineup(2, 2, 1, 2122, 95, 3, 2, 3, 4, 1, 3, 4, 2, 4) == [
        [
            (
                ("Ja Morant", "Trae Young"),
                ("Kristaps Porzingis", "Jayson Tatum"),
                ("Jonas Valanciunas",),
            ),
            91683931,
        ],
        [
            (
                ("Ja Morant", "Luka Doncic"),
                ("Kristaps Porzingis", "Jayson Tatum"),
                ("Jonas Valanciunas",),
            ),
            93531851,
        ],
        [
            (
                ("Trae Young", "Luka Doncic"),
                ("Kristaps Porzingis", "Jayson Tatum"),
                ("Jonas Valanciunas",),
            ),
            92254962,
        ],
        [
            (
                ("Ja Morant", "Trae Young"),
                ("Jayson Tatum", "Pascal Siakam"),
                ("Jonas Valanciunas",),
            ),
            93037267,
        ],
        [
            (
                ("Ja Morant", "Luka Doncic"),
                ("Jayson Tatum", "Pascal Siakam"),
                ("Jonas Valanciunas",),
            ),
            94885187,
        ],
    ]
