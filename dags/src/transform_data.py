import pandas as pd
import datetime,pytz
from src.scrape_file import tgl

tz = pytz.timezone('Asia/Jakarta')        
tl = tgl
def dates(tgl_):
    tgl_datetime = tz.localize(datetime.datetime.strptime(tgl_[:-4], '%d/%m/%Y %H:%M'))
    timestamp = tgl_datetime.strftime('%Y-%m-%d %H:%M:%S')
    return timestamp

def transform_news():
    df_kompas = pd.read_csv('/home/milim/airflow/dags_folder/data_result/ress_kompas.csv')
    df_detik = pd.read_csv('/home/milim/airflow/dags_folder/data_result/ress_detik.csv',delimiter='|')
    for i in range(len(df_detik)):
        df_detik.at[i, 'released'] = dates(df_detik.at[i, 'released'])

    for i in range(len(df_kompas)):
        df_kompas.at[i, 'released'] = dates(df_kompas.at[i,'released'])

    df_detik = df_detik.replace('\n', '', regex=True)
    df_result = pd.concat([df_kompas,df_detik])

    df_result = df_result.dropna()
    df_result = df_result.astype(str)

    cleaned_content = []
    for content in df_result['content']:
        lines = content.split(' ')
        lines = [line.strip() for line in lines]
        text = ' '.join(lines)
        cleaned_content.append(text)

    df_result['content'] = cleaned_content
    df_result.to_csv(f"/home/milim/airflow/dags_folder/data_result/result{tl}.csv",index=False)
