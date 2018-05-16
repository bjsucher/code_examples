*ods html file = "C:\Users\brand\OneDrive\Documents\My SAS Files\9.4\Final.html";
ods html; /* ods html not working */
/* Extract data from Downloads folder */
filename final 'C:\Users\brand\Downloads\Final_Data\*.txt';

/* Report 1 */

/* Set Weighted value for each grade letter */
proc format;
	invalue mysweetformat
	"A" = 4.0
	"A-" = 3.7
	"B+" = 3.4
	"B" = 3.0
	"B-" = 2.7
	"C+" = 2.4
	"C" = 2.0
	"C-" = 1.7
	"D+" = 1.4
	"D" = 1.0
	"D-" = 0.7
	other = 0
	;
run; 

/* Read in data from files */
data finalData;
	infile final dlm="@";
	length ID $ 5 Course $ 10;
	input ID $ Date Course $ Credits Grade $;
	Weight = input(Grade, mysweetformat.);
	/* Create variables for different types of credits earned */
	if Grade in ("A" "A-" "B+" "B" "B-" "C+" "C" "C-" "D+" "D" "D-" "P") then EarnedCredits = Credits;
	else EarnedCredits = 0;
	if Grade in ("A" "A-" "B+" "B" "B-" "C+" "C" "C-" "D+" "D" "D-" "E" "IE" "WE" "UW") then CredsForCalcGPA = Credits;
	else CredsForCalcGPA = 0;
	if Grade in ("A" "A-" "B+" "B" "B-" "C+" "C" "C-" "D+" "D" "D-") then GradedCreds = Credits;
	else GradedCreds = 0;
	/* Create date field and switch so that it prints year then semester */
	Date = substrn(Date, 2, 2) || substrn(Date, 1, 1);
	if substr(reverse(trim(Course)), 1, 1) = "R" then Rs = 1; /* Count courses with R for repeated classes */
	else Rs = 0;
run;

/* Create first half of Report 1 that shows information by student and semester */
proc sql;
	create table report1a as
	select ID, Date,
		sum(Weight*CredsForCalcGPA) as Numerator, /* Calculates Numerator of GPA */
		round(sum(Weight*CredsForCalcGPA)/sum(CredsForCalcGPA), .01) as GPA, /* Rounds GPA to nearest hundredth */
		sum(CredsForCalcGPA) as Denom, /* Calculates Denominator of GPA */
		sum(EarnedCredits) as TotalCredits,sum(GradedCreds) as GradedCredits
	from finalData
	group by ID, Date
	;
quit;

/* Calculates cumulative GPA over semesters and finds class standing for each student */
data cumGPA;
	set report1a;
	by ID Date;
	if ID ne lag(ID) then do;
		CumGPAScore = 0;
		CumDenom = 0;
		CreditHoursEarned = 0;
	end;
	CumGPAScore + Numerator;
	CumDenom + Denom;
	CreditHoursEarned + TotalCredits;
	CumGPA = CumGPAScore/CumDenom;
	length Class $ 10; /* Set length to 10 characters so "Sophomore" does not get cut off */
	format CumGPA 4.3; 
	/* Determines class standing of student */
	if CreditHoursEarned < 30 then Class = "Freshman";
	else if CreditHoursEarned < 60 then Class = "Sophomore";
	else if CreditHoursEarned < 90 then Class = "Junior";
	else Class = "Senior";
	drop Numerator Denom CumGPAScore CumDenom; /* Drops unnecessary variables */
run;

/* Creates macro to show overall grades and credits for each student at end of college */
%macro final(source, table);

proc sql;
	create table &table as
	select ID,
		round(sum(Weight*CredsForCalcGPA)/sum(CredsForCalcGPA), .01) as OverallGPA,
		sum(EarnedCredits) as TotCredits,sum(GradedCreds) as TotGradedCredits,
		count(*) - count(distinct Course) - sum(Rs) as repeats, /* Counts number of repeat courses */
		/* Count the number of letter grades each student receives */
		sum(Grade in ("A", "A-")) as A,
		sum(Grade in ("B+", "B", "B-")) as B,
		sum(Grade in ("C+", "C", "C-")) as C,
		sum(Grade in ("D+", "D", "D-")) as D,
		sum(Grade="E", Grade="IE", Grade="WE", Grade="UW") as E,
		sum(Grade="W") as W
	from &source
	group by ID
	;
quit;

%mend; /* End of macro */

%final(finalData, report1b); /* Call macro to create report of overall grades and credits for each student */

/* Clean up overall report, getting rid of a negative number of repeat classes and showing only one observation
	for each student */
data report1b;
	set report1b;
	by ID;
	if repeats < 0 then repeats = 0; 
	if last.ID then output;
run;

/* Merge the top half of report with overall student results to create Report 1 */
data report1;
	merge cumGPA report1b;
	by ID;
run;

proc print data=report1 (drop=CreditHoursEarned);
run;

/* Report 2 */

/* Create a subset of Math and Statistics courses */
data mathStat;
	set finalData;
	if substr(Course, 1, 4) in ("MATH" "STAT");
run;

%final(mathStat, mathReport); /* Find Overall results for each student in math and statistics classes */

/* Rename variables to be able to distinguish from results from all classes */
data mathReport (rename=(GPA=GPA_S TotalCredits=TotalCredits_S GradedCredits=GradedCredits_S repeats=repeats_S
						A=A_S B=B_S C=C_S D=D_S E=E_S W=W_S));
	set mathReport;
	by ID;
	if last.ID then output;
run;

/* Merge results for all classes with subset of just math and statistics classes */
data report2;
	merge report1b mathReport;
	by ID;
run;

proc print data=report2; 
run;

/* Report 3 */

proc sql;
	create table report3 as
	select ID, CumGPA, CreditHoursEarned 
	from cumGPA
	where CreditHoursEarned > 60 and CreditHoursEarned < 130 /* Subset to students with 60-130 overall credits */ 
	order by CumGPA desc /* Change to descending order of cumulative GPA */
	;
quit;

data report3;
	set report3;
	if _n_ / &sqlobs < .1; /* Subsets to output only Top 10% of students */
run;

proc print data=report3;
run;

/* Report 4 */

proc sql;
	create table report4 as
	select ID, GPA_S, GradedCredits_S
	from mathReport
	where GradedCredits_S > 20 /* Subset to students who completed over 20 credits of math or stats classes */
	order by GPA_S desc
	;
quit;

data report4;
	set report4;
	if _n_ / &sqlobs < .1; /* Subsets to output only Top 10% of students */
run;

proc report data=report4;
run;

*ods html close;
