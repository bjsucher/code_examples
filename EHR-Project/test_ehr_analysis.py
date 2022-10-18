"""Create tests to test ehr_analysis"""

from ehr_analysis import (
    parse_patient_data,
    parse_lab_data,
    num_older_than,
    sick_patients,
    age_first_admission,
    age,
)

import sqlite3

con = sqlite3.connect("ehr.db")
cur = con.cursor()
parse_patient_data("PatientsTest.txt")
parse_lab_data("LabsTest.txt")


def test_num_older_than():
    """Test num_older_than function"""
    assert num_older_than(40) == 1
    assert num_older_than(15) == 2
    assert num_older_than(70) == 0


def test_sick_patients():
    """Test sick_patients() function"""
    assert sick_patients("URINALYSIS: RED BLOOD CELLS", ">", 1.5) == {1}
    assert sick_patients("METABOLIC: GLUCOSE", "<", 120) == {2}
    assert sick_patients("METABOLIC: GLUCOSE", ">", 120) == set()


def test_age_first_admission():
    """Test age_first_admission() function"""
    assert age_first_admission("1") == 24
    assert age_first_admission("2") == 19


def test_age():
    """Test age property in the Patient class"""
    assert age("1") == 54
    assert age("2") == 29
