import datetime
import pandas as pd
from airflow.decorators import dag, task


DATA_PATH = (
    "/Users/rqobist/Documents/airflow/mentally-stability-of-the-person/train.csv"
)
CLEANED_DATA_PATH = "/Users/rqobist/Documents/airflow/train_cleaned.csv"


@dag(
    dag_id="playground_cleaning_dag",
    start_date=datetime.datetime(2025, 2, 26),
    schedule_interval="@daily",
)
def cleaning_dag():

    @task
    def load_data():
        df = pd.read_csv(
            DATA_PATH,
        )
        return df.to_json()  # Convert DataFrame to JSON string for XCom

    @task
    def merged_satisfaction(df_json):
        df = pd.read_json(df_json)  # Convert JSON back to DataFrame
        df["Satisfaction"] = df.apply(
            lambda row: (
                row["Study Satisfaction"]
                if not pd.isna(row["Study Satisfaction"])
                else row["Job Satisfaction"]
            ),
            axis=1,
        )
        df = df.drop(columns=["Study Satisfaction", "Job Satisfaction"])
        return df.to_json()

    @task
    def merged_pressure(df_json):
        df = pd.read_json(df_json)
        df["pressure"] = df.apply(
            lambda row: (
                row["Academic Pressure"]
                if not pd.isna(row["Academic Pressure"])
                else row["Work Pressure"]
            ),
            axis=1,
        )
        df = df.drop(columns=["Academic Pressure", "Work Pressure"])
        return df.to_json()

    @task
    def merged_profession(df_json):
        df = pd.read_json(df_json)
        df.loc[df["Working Professional or Student"] == "Student", "Profession"] = (
            "Student"
        )
        df["Profession"] = df["Profession"].fillna("Unemployed")
        df = df.drop(columns=["Working Professional or Student"])
        return df.to_json()

    @task
    def fill_CGPA(df_json):
        df = pd.read_json(df_json)
        df["CGPA"] = df["CGPA"].fillna(-1)
        return df.to_json()

    @task
    def save_data(df_json):
        df = pd.read_json(df_json)
        df.to_csv(
            CLEANED_DATA_PATH,
            index=False,
        )

    # Define DAG Task Dependencies
    load_data_task = load_data()
    merged_satisfaction_task = merged_satisfaction(load_data_task)
    merged_pressure_task = merged_pressure(merged_satisfaction_task)
    merged_profession_task = merged_profession(merged_pressure_task)
    fill_CGPA_task = fill_CGPA(merged_profession_task)
    save_data_task = save_data(fill_CGPA_task)

    (
        load_data_task
        >> merged_satisfaction_task
        >> merged_pressure_task
        >> merged_profession_task
        >> fill_CGPA_task
        >> save_data_task
    )


cleaning_dag_instance = cleaning_dag()
