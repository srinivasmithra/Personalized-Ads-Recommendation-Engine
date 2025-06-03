from app.db.mongo_connection import db


def insert_single_document(collection, data):
    # data will be dictionary
    db_collection = db[collection]
    response = db_collection.insert_one(data)
    return response.inserted_id


def insert_multiple_documents(collection, data):
    # data will be array of dictionary
    db_collection = db[collection]
    response = db_collection.insert_many(data)
    return response.inserted_ids


def fetch_documents(collection, query={}):
    response = db[collection].find(query)
    return response

def update_by_key(select_key, val_key, col_to_update, val_to_update, collection):
    db[collection].find_one_and_update({ select_key: val_key}, {'$addToSet': {col_to_update: val_to_update}})

def update_document(collection, query, update_doc, options={}):
    db_collection = db[collection]
    response = db_collection.update_one(
        query,
        update_doc,
        upsert = True
    )
    return response


