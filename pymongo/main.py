#!/usr/bin/python3

"""
connects to mongoDB via pymongo

Author: Bradley Dillion Gilden
Date: 09-11-2023
"""
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
from os import environ
from crud import (insert_doc, insert_docs, find_all, find_by_name,  # noqa
                  find_by_id, count, age_range)

load_dotenv(find_dotenv())
password = environ.get("MONGODB_PWD")


if __name__ == "__main__":
    connection_str = ("mongodb+srv://bradleygilden:nanospartan117@cluster0."
                      "kwwgi0j.mongodb.net/?retryWrites=true&w=majority")
    client = MongoClient(connection_str)

    doclist = [
        {"name": "Timmy", "age": 2},
        {"name": "Carl", "age": 23},
        {"name": "Filch", "age": 46},
        {"name": "Minerva", "age": 75},
        {"name": "Conrad", "age": 14}
    ]

    """ returns a list of database names for a cluster
    client.list_database_names()
    """

    # reference school database
    schooldb = client.school

    """ To list collections for a database collection
    collections = schooldb.list_collection_names()
    """

    # reference student collection
    studentscol = schooldb.students

    # insert_doc(studentscol, {
    #     "name": "White Mamba",
    #     "Age": 14,
    #     "fullTime": True
    # })

    # insert_docs(studentscol, doclist)

    # find_all(studentscol, columns={"_id": False})

    # find_by_name(studentscol, "Constantine")
    # find_by_id(studentscol, "654254f7a25937783b1de1dc")
    # count(studentscol, {"age": {"$gt": 50}})
    # age_range(studentscol, 10, 20)
