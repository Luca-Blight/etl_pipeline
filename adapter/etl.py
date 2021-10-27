from prefect import task, Flow
from prefect.schedules.schedules import IntervalSchedule
from prefect.engine.executors import DaskExecutor
from dask.distributed import Client
from sodapy import Socrata
import pandas as pd
import datetime as dt
import os


s3_bucket_path = os.getenv('S3_BASE_LOCATION')

@task(nout=2)
def extract():
    class Client:
        APP_TOKEN = os.getenviron('APP_TOKEN')
        ROOT_URL = os.getenviron('ROOT_URL')       
        END_POINT_ONE = os.getenviron('END_POINT_ONE')
        END_POINT_TWO = os.getenviron('END_POINT_TWO')

    
        def request_school_info(self):
            sub_client = Socrata(self.ROOT_URL, app_token = self.APP_TOKEN)
            data = sub_client.get(self.END_POINT_ONE, content_type = "json")
            return data    
        
        def request_school_results(self):
            sub_client = Socrata(self.ROOT_URL, app_token = self.APP_TOKEN)
            data = sub_client.get(self.END_POINT_TWO, content_type = "json")
            return data 
            

    school_loc_details = Client().request_school_locs()
    school_results = Client().request_school_locs()

    return school_loc_details, school_results

@task
def create_transform_df(records):
    df = pd.DataFrame(records)
    columns = ['dbn','school_name','primary_address_line_1','city','postcode',
               'latitude','longitude','gradespan','subway','pct_stu_safe','graduation_rate',
               'attendance_rate','college_career_rate']
    transformed_df = df.loc[:, columns]
    return transformed_df

@task
def create_transform_df_two(records):
    df = pd.DataFrame(records)
    return df

@task
def merge(df_one,df_two):
    merged_df = pd.merge(left=df_one,right=df_two,on='dbn')
    return merged_df

@task
def load(transformed_df):
    #s3_bucket_path,src_of_data
    loaded_object = transformed_df.to_csv('./out.csv', encoding='utf-8', index=False)
    # loaded_object = transformed_df.to_parquet(s3_bucket_path + f"/{src_of_data}.parquet" ,engine='fastparquet')
    return loaded_object

def build_flow(schedule=None):
    with Flow("my_etl",schedule=schedule) as flow:
        data1,data2 = extract()
        df_1 = create_transform_df(data1)
        df_2 = create_transform_df_two(data2)
        merged_df = merge(df_1,df_2)
        tdata = load(merged_df)
    return flow



if __name__ == "__main__":
    schedule = IntervalSchedule(start_date=dt.datetime.now() + dt.timedelta(hours=11),
                interval=dt.timedelta(hours=12))
    flow = build_flow(schedule)
    flow.visualize()
    flow.run()


