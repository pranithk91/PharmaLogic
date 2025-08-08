import asyncio
from database_lib import (
    select_table as async_select_table,
    insert_into_table as async_insert_into_table,
    get_client_id as async_get_client_id,
    run_query as async_run_query,
    to_dataframe as async_to_dataframe
)

#Define new functions
def selectTable(table_name, column_names = '*', condition= "1=1", Limit=None):
    return asyncio.run(async_select_table(table_name, column_names, condition, Limit))

def insertIntoTable(table_name, values, column_names ):
    return asyncio.run(async_insert_into_table(table_name, values, column_names))

def getClientID(currentName):
    return asyncio.run(async_get_client_id(currentName))

def runQuery(query, condition):
    return asyncio.run(async_run_query(query, condition))

def to_dataframe(query):
    return asyncio.run(async_to_dataframe(query))



