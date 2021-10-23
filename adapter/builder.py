from prefect.schedules.schedules import IntervalSchedule
from sodapy import Socrata
import pandas as pd
import dask.dataframe as dd
import os
from prefect import task, Flow, Parameter
from dotenv import load_dotenv
import datetime as dt

s3_bucket_path = os.getenv('S3_BASE_LOCATION')

@task
def extract():
    class Client:
        APP_TOKEN = "XNKZJVsscuBPRteOXyyM6G3yc"
        ROOT_URL = "data.cityofnewyork.us"
        # END_POINT_ONE - School_Location Dataset
        END_POINT_ONE = "8b6c-7uty" #"ahjc-fdu3" 
 
    
        def request_school_locs(self):
            client = Socrata(self.ROOT_URL, app_token = self.APP_TOKEN)
            data = client.get(self.END_POINT_ONE, content_type = "json")
            return data    

    school_loc_details = Client().request_school_locs()
    return school_loc_details

@task
def create_df(records):
    df = pd.DataFrame(records)
    ddf = dd.from_pandas(df, npartitions=2)
    return df

@task
def transform(df):
    columns = ['dbn','school_name','primary_address_line_1','city','postcode',
               'latitude','longitude','gradespan','subway','pct_stu_safe','graduation_rate',
               'attendance_rate','college_career_rate']
    transformed_df = df.loc[:, columns]
    return transformed_df

@task
def load(transformed_df):
    #s3_bucket_path,src_of_data
 
    loaded_object = transformed_df.to_csv('./out.csv', encoding='utf-8', index=False)
 
    # loaded_object = transformed_df.to_parquet(s3_bucket_path + f"/{src_of_data}.parquet" ,engine='fastparquet')
    return loaded_object


def build_flow(schedule=None):
    with Flow("my_etl",schedule=schedule) as flow:
        data = extract()
        df = create_df(data)
        tdata = transform(df)
        ldata = load(tdata)
    return flow



if __name__ == "__main__":
    schedule = IntervalSchedule(start_date=dt.datetime.now() + dt.timedelta(seconds=1),
                interval=dt.timedelta(seconds=5))
    flow = build_flow(schedule)
    flow.run()

