import pandas as pd 
from sodapy import Socrata
from pymongo import MongoClient


def pull_data():
    results = client.get("9fxf-t2tr", limit=2000)
    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)
    results_df['date'] = pd.to_datetime(results_df['date'], dayfirst = True)
    return results_df

client = MongoClient()
client.DallasPD_DB
db  = client['DallasPD_DB']
running_data = db.running_db

client = Socrata('www.dallasopendata.com',
                 'KfIrXaHOglxeS3ELKoScuOmr8',
                 username="bryce_ka@hotmail.com",
                 password="Bantho750451580!")

pulled_data = pull_data()
running = pd.DataFrame(list(running_data.find())).drop('_id', axis = 1)
# print("current number of incidents: ", len(running))

# update the constant db for the application or program 
# 1. identify new rows using incident number date time unit number 
updated_df = pd.concat([running, pulled_data], axis=0).drop_duplicates()
running = pd.DataFrame(list(running_data.find()))
new_documents = updated_df.merge(running, how='left', on=['incident_number', 'date', 'time', 'unit_number'], suffixes=('', '_y'))
new_documents = new_documents[new_documents['_id'].isnull()][['incident_number', 'division', 'nature_of_call', 'priority', 'date', 'time', 'unit_number', 'location', 'beat', 'reporting_area', 'status', 'block']]
print(f"found {len(new_documents)} new incident(s)")
if len(new_documents)!= 0:
    running_data.insert_many(new_documents.to_dict('records'))

