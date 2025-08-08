import configparser
import pandas as pd
from datetime import date
from libsql_client import create_client

#Read config
config = configparser.ConfigParser()
config.read("config.ini")

db_url = config.get("TURSO", "url")
auth_token = config.get("TURSO", "auth_token")

async def get_client():
    return create_client(url=db_url, auth_token=auth_token)

async def select_table(table_name, column_names='*', condition="1=1", limit=None):
    client = await get_client()
    query = f"SELECT {column_names} FROM {table_name} WHERE {condition}"
    if limit:
        query += f" LIMIT {limit}"

    try:
        print(query)
        result = await client.execute(query)
        return [row._values for row in result.rows]
    except Exception as e:
        print(f"Error executing query: {e}")
        return []

async def insert_into_table(table_name, values, column_names):
    client = await get_client()
    query = f"INSERT INTO {table_name} ({column_names}) VALUES {values}"
    try:
        print(query)
        await client.execute(query)
    except Exception as e:
        print(f"Error inserting data: {e}")

async def get_client_id(current_name):
    initial = current_name[0].upper()
    query = f"SELECT last_id FROM vw_Name_Counter WHERE starting_letter = '{initial}'"
    result = await select_table(f"( {query} )", column_names='last_id')
    if not result:
        count = 1
    else:
        count = int(result[0][0]) + 1
    formatted_id = f"{date.today():%y%m}{initial}{count:03}"
    return formatted_id

async def run_query(query, condition="1=1"):
    client = await get_client()
    query = f"{query} WHERE {condition}"
    try:
        print(query)
        result = await client.execute(query)
        return [row.values() for row in result.rows]
    except Exception as e:
        print(f"Error running query: {e}")
        return []

async def to_dataframe(query):
    client = await get_client()
    result = await client.execute(query)
    return pd.DataFrame([row.values() for row in result.rows], columns=result.columns)
