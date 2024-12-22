import reflex as rx
from typing import Union, List
import csv
import pandas as pd
import networkx as nx
import sqlmodel
import sqlalchemy
from sqlalchemy import create_engine, Column, String, JSON, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func


class isnads(rx.Model, table=True): 
    source: int
    destination: int 
    hadith_count: int
    taraf_count: int 
    book_count: int 


class QueryIsnads(rx.State):
    hadith: str 
    taraf: int
    edges: list[isnads]

    @rx.event
    def get_isnads_hadith(self):
        with rx.session() as session:
            results = session.execute(sqlalchemy.text('select source, destination, hadith_count, taraf_count, book_count from isnads, json_each(taraf) where json_each.value=:hadith_select'), {'hadith_select':self.hadith}).all()
            keys = ['source', 'destination', 'hadith_count', 'taraf_count', 'book_count']
            results = [dict(zip(keys, list(value))) for value in results]
            self.edges = [isnads(**row) for row in results]
    
    @rx.event
    def get_isnads_taraf(self):
        with rx.session() as session:
            results = session.execute(sqlalchemy.text('select source, destination, hadith_count, taraf_count, book_count from isnads, json_each(taraf) where json_each.value=:taraf_select'), {'taraf_select':self.taraf}).all()
            keys = ['source', 'destination', 'hadith_count', 'taraf_count', 'book_count']
            results = [dict(zip(keys, list(value))) for value in results]
            self.edges = [isnads(**row) for row in results]