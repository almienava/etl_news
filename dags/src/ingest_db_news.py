import csv
import psycopg2
from airflow.models import Variable
from src.scrape_file import tgl


tl = tgl

def load_to_dwh():
    conn_params = {
        "host": Variable.get("dwh_host"),
        "port": Variable.get("dwh_port"),
        "database": Variable.get("dwh_database"),
        "user": Variable.get("dwh_user"),
        "password": Variable.get("dwh_password")
    }
    path_csv = f"/home/milim/airflow/dags_folder/data_result/result{tl}.csv"

    conn = psycopg2.connect(**conn_params)
    cur = conn.cursor()
    with open(path_csv, "r") as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                judul,tanggal,author,url,content,platform = row[0],row[1],row[2],row[3],row[4],row[5]

                quer = """insert into "public"."news"(judul,tanggal,author,url,content,platform) values (%s,%s,%s,%s,%s,%s)"""
                val = (judul,tanggal,author,url,content,platform,)

                cur.execute(quer,val)
            conn.commit()
            cur.close()
            conn.close()
            print("Data loaded successfully!")
