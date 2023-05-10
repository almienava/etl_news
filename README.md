# etl_news
This project is a simple job of processing and scheduling ETL using Apache AirFlow. I set the running schedule to be every hour 23:00 utc+7 for news data retrieval every day according to the current server date.

Below is an overview of the flow of this project:

![image](https://github.com/almienava/etl_news/assets/61896664/20df195b-12cb-4416-a246-ebe2930d68bc)

## Flow

- Task Starts

- Scraping data from Indonesian news sites (Kompas.com and Detik.com)

- Transform the resulting data from the scrapping process

- Load data into postgresql database

- Task Finish


## Installation

Please read the documentation for the airflow install process [here](https://airflow.apache.org/docs/apache-airflow/stable/installation/index.html)

```bash
  git clone https://github.com/almienava/etl_news
  cd etl_news
  pip install -r requirements.txt
```
Move the dags file into $AIRFLOW_HOME

Setting the airflow.cfg file in $AIRFLOW_HOME,adjust the path to yours
```bash
  dags_folder = /home/user/airflow/dags
```
And lastly run apache airflow according to the [Documentation](https://airflow.apache.org/docs/) instructions from Apache Airflow

## Notes

Please adjust the output csv file location path in each py file.

## Feedback

If you have any feedback, please reach out to us at haldad.almi@gmail.com

