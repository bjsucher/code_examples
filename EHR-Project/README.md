# EHR-cumulative-project

This project pulls in patient and lab data to look at different features of the data. It expects two input files: a .txt file with patient data and a .txt file with lab data. The patient data file should have 7 columns: Patient ID, Gender, Date Of Birth, Race, Marital Status, Language, Percent Below Poverty. The lab data file should have 6 columns: Patient ID, Admission ID, Lab Name, Value, Units, Date and Time. The columns should be in this specific order for each file and the lab data file should be in chronological order but does not necessarily need to be.  


## Functions and Database
There are five functions that can be used from the project although it should be noted that the parse_patient_data function must be used to read in the patient data while the parse_lab_data function must be used to read in the lab data files that are needed for the other functions. A SQLite database is created to store the data for patients and labs in tables. These tables are then used in the functions. Each section below contains the class or function's purpose, arguments, and an example.

### parse_patient_data
Purpose: This function creates the Patient table in the SQLite database and parses the data from a patient data text file, storing it in the newly created table.

Arguments: The file path of the patient data, written inside quotation marks.

Example: 
```
parse_patient_data("FilePath/patient_data.txt")
```

### parse_lab_data
Purpose: This function creates the Lab table in the SQLite database and parses the data from a lab data text file, storing it in the newly created table.

Arguments: The file path of the lab data, written inside quotation marks.

Example: 
```
parse_lab_data("FilePath/lab_data.txt")
```

### num_older_than
Purpose: This function looks at the patient data and counts how many patients are above a certain age input by the user.

Argument: The age threshold determined by the user. This can be written as a decimal and must be written as a number. 

Example: 
```
num_older_than(42.2)
```


### sick_patients
Purpose: In this function, the user inputs a certain lab name, a numerical value to compare it to, and if the function should look for patients with measures greater than or equal to that value for the certain lab. The function looks through each patient to see if during any visit, the patient meets the user-defined criteria for the measure. The function then outputs a set of patient IDs for the patients who met the criteria.

Arguments: 
1. Lab name (i.e. Urinalysis: Red blood cells), 
2. Greater than or less than sign in quotation marks (equals sign is not accepted in this argument)
3. Value to compare to (must be numeric)

Example: 
```
sick_patients("CBC: RED BLODD CELL COUNT", ">", 6.9)
```

### age_first_admission
Purpose: This function looks at the first visit of a certain patient and outputs the age of the patient at that visit.

Argument: Patient ID, written in quotation marks

Example: 
```
age_first_admission("1")
```


## Testing Instructions for Contributors
To add a new test case, open the test_ehr_analysis.py file. There is a function that tests each function in the ehr_analysis.py file and test cases for each file are found within each function. To add a test case, use the assert command to assert whether the function is equal to the expected output. When calling the function, put in unique values into the function arguments to test different features of the function. 

Here is an example to illustrate how to create a test case:
Suppose I want to test the age at first admission of the patient with patient ID #2. I look in the patient and lab data test files and see that the patient should be 19 years old at the first admission. So, I create the following test case inside the function "test_age_first_admission()":
```
assert (age_first_admission("1") == 24)
```
Normally the assert statement can be done on one line, but when the function arguments run longer, it is acceptable to put the statement on multiple lines using parentheses as shown above.

When we run pytest on our file (code for terminal: pytest .\test_ehr_analysis.py), we should get a green "Passed" line that shows the test case successfully passes.
