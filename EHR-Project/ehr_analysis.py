"""Change EHR analysis to work with SQLite database."""

import datetime as dt
import sqlite3
import os

DAYS_IN_YEAR = 365.25

"""Create database to store data and open connection"""
if os.path.exists("ehr.db"):
    os.remove("ehr.db")
con = sqlite3.connect("ehr.db")


def parse_patient_data(filename: str):
    """Parse patient data into SQLite datbase"""
    cur = con.cursor()
    cur.execute(
        """CREATE TABLE Patient (
                        [Patient_ID] INTEGER PRIMARY KEY, 
                        [Gender] VARCHAR(10),
                        [Date_Of_Birth] VARCHAR(10),
                        [Race] VARCHAR(20))"""
    )
    with open(filename) as file:
        next(file)  # O(1)
        for line in file:  # N times
            content = line.split("\t")  # O(1)
            content[2] = content[2].split()[0]
            cur.execute("INSERT INTO Patient VALUES (?, ?, ?, ?)", content[:4])

    return


def parse_lab_data(filename: str):
    """Parse lab data into SQLite database"""
    cur = con.cursor()
    cur.execute(
        """CREATE TABLE Lab (
                        [Patient_ID] INTEGER PRIMARY KEY,
                        [Admission_ID] INTEGER,
                        [Lab_Name] VARCHAR(70),
                        [Lab_Value] DECIMAL(6,2),
                        [Lab_Units] VARCHAR(20),
                        [Lab_Date] VARCHAR(10))"""
    )
    with open(filename) as file:
        next(file)  # O(1)
        for line in file:  # NM times
            content = line.split("\t")  # O(1)
            content[3] = float(content[3])
            content[5] = content[5].split()[0]
            cur.execute("INSERT INTO Lab VALUES (?, ?, ?, ?, ?, ?)", content)

    return


def num_older_than(age: float) -> int:
    """Count number of patients older than a user-defined age. We assume that
    date of birth is the third column in the patients text file."""
    cur = con.cursor()
    count_older = cur.execute(
        """SELECT COUNT(Patient_ID)
            FROM Patient
            WHERE (JULIANDAY('now') - JULIANDAY(Date_Of_Birth)) / ? > ?""",
        [DAYS_IN_YEAR, age],
    ).fetchall()

    return count_older[0][0]


def sick_patients(lab: str, gt_lt: str, value: float) -> set[int]:
    """Get list of patients that had an observation based on the outcome of a
    certain lab. Assume that the lab name and the lab value are the 3rd and 4th
    columns."""
    cur = con.cursor()
    output = cur.execute(
        f"""SELECT DISTINCT(Patient_ID)
            FROM Lab
            WHERE Lab_Name = ?
            AND Lab_Value {gt_lt} {value}""",
        [lab],
    ).fetchall()

    patient_IDs: set[str] = set()  # O(1)
    for row in output:
        patient_IDs.add(row[0])

    return patient_IDs  # O(1)


def age_first_admission(patient_id: str) -> int:
    """Find patient age when first admitted"""
    cur = con.cursor()
    cache: dict[str, int] = {}
    if patient_id in cache:
        return cache[patient_id]

    age = cur.execute(
        """SELECT (JULIANDAY(Lab_Date) - JULIANDAY(Date_Of_Birth)) / ?
            FROM Lab l
            INNER JOIN Patient p ON l.Patient_ID = p.Patient_ID
            WHERE l.Patient_ID = ?
            AND Admission_ID = 1""",
        [DAYS_IN_YEAR, patient_id],
    ).fetchall()

    age_as_int = int(age[0][0])
    cache[patient_id] = age_as_int

    return age_as_int  # O(1)


def age(patient_id: str) -> int:
    """Find patient age."""
    cur = con.cursor()
    cache: dict[str, int] = {}
    if patient_id in cache:
        return cache[patient_id]

    age = cur.execute(
        """SELECT (JULIANDAY('now') - JULIANDAY(Date_Of_Birth)) / ?
            FROM Patient
            WHERE Patient_ID = ?""",
        [DAYS_IN_YEAR, patient_id],
    ).fetchall()

    age_as_int = int(age[0][0])
    cache[patient_id] = age_as_int

    return age_as_int  # O(1)
