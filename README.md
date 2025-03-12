#CPE393-Machine Learning Operations
## Group: Super AIops Engineer

- Keetawan Limaroon 64070501005
- Punnawat Namwongsa 64070501032
- Patcharaphon Santhitikul 64070501037
- Pakawat Phasook 65070503430
- Rapepong Pitijaroonpong 65070503434

## Dataset
Mentally stability of the person
source: https://www.kaggle.com/competitions/mentally-stability-of-the-person/data?select=train.csv
## to test this code
1. clone this repo
2. cd to the folder
3. docker-compose up
4. go to localhost:8080
- username: airflow
- password: airflow
5. go to desired dags (eg. playground_cleaning_dag)
6. view result
### note
- you can get out put file via result folder and you can get your data via data folder
- for adding more folder please edit volumns mapping in docker compose file
## EDA and Feature engineering
![image](https://github.com/user-attachments/assets/f233f6ed-4b2b-4552-95c2-e1ed4ccbe853)

Figure1 : visualize null values inside the dataset

### Null columns are: 
Profession                             104070 non-null  object
Academic Pressure                      27897 non-null   float64
 Work Pressure                          112782 non-null  float64
 CGPA                                   27898 non-null   float64
 Study Satisfaction                     27897 non-null   float64
 Job Satisfaction                       112790 non-null  float64
 Dietary Habits                         140696 non-null  object 
 Degree        			140698 non-null  object

### questions

Q1: Why are there missing data in the profession?
Ans: because students are not graduated and do not obtain a profession.
 	34 Students have a profession. We think they might misunderstand that they should put their major in there. And with the small amount of data compared to the majority of the group, we think this data should be ignored.
To address this, we decided to fill the null in the profession column with “Student” as profession, then erase “Working Professional or Student”


Q2: Why are there missing data in many columns with similar volume such as work pressure, academic pressure, CGPA, study satisfaction, and job satisfaction?
Ans: 
	because there are columns specifically for student and employed like CGPA, study, satisfaction, etc.
Students will have null values in profession because they have not worked yet, and work pressure will also be null. If they are company employees, they will have null values in academic pressure and CGPA. Job satisfaction and study satisfaction show how much they are satisfied with their work and studies.
	To address this, We filled missing values as follows:
Profession: If  Working Professional or Student is 'Student', we set Profession to 'Student'. Otherwise, we filled NaN values in Profession with 'Unemployed'.
Pressure Level: We merged Academic Pressure (for students) and Work Pressure (for professionals) into a new column called pressure.
Satisfaction: We combined Study Satisfaction (for students) and Job Satisfaction (for employees) into a single column called Satisfaction.
CGPA: Since CGPA is only relevant for students, we filled missing values with -1 to indicate "Not Applicable" for working professionals.

