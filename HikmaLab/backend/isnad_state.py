import reflex as rx
import csv
import pandas as pd
import networkx as nx
import sqlalchemy
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
    multi_hadith: list[str] 
    edges: list[isnads]
    sort_value: str = ""
    sort_reverse: bool = False

    total_items: int = 0
    offset: int = 0
    limit: int = 12  # Number of rows per page
    search_value: str = ""


    @rx.event
    def get_isnads_hadith(self):
        with rx.session() as session:
            results = session.execute(sqlalchemy.text('select source, destination, hadith_count, taraf_count, book_count from isnads, json_each(hadith) where json_each.value=:hadith_select'), {'hadith_select':self.hadith}).all()
        keys = ['source', 'destination', 'hadith_count', 'taraf_count', 'book_count']
        results = [dict(zip(keys, list(value))) for value in results]
        self.edges = [isnads(**row) for row in results]
        self.total_items = len(self.edges)
    
    @rx.event
    def get_isnads_taraf(self):
        with rx.session() as session:
            results = session.execute(sqlalchemy.text('select source, destination, hadith_count, taraf_count, book_count from isnads, json_each(taraf) where json_each.value=:taraf_select'), {'taraf_select':self.taraf}).all()
        keys = ['source', 'destination', 'hadith_count', 'taraf_count', 'book_count']
        results = [dict(zip(keys, list(value))) for value in results]
        self.edges = [isnads(**row) for row in results]
        self.total_items = len(self.edges)
    
    @rx.event
    def get_isnads_hadiths(self):
        '''
        queries multiple hadith
        '''
        query = """
        SELECT source, destination, hadith_count, taraf_count, book_count
        FROM isnads
        WHERE EXISTS (
        SELECT 1
        FROM json_each(hadith) AS elem
        WHERE elem.value IN ({}));""".format(', '.join(f"'{item}'" for item in self.multi_hadith))
        with rx.session as session:
            results = session.execute(sqlalchemy.text(query)).all()
        keys = ['source', 'destination', 'hadith_count', 'taraf_count', 'book_count']
        results = [dict(zip(keys, list(value))) for value in results]
        self.edges = [isnads(**row) for row in results]
        self.total_items = len(self.edges)
        

    @rx.var(cache=True)
    def filtered_sorted_items(self) -> list[isnads]:
        items = self.edges

        # Filter items based on selected item
        if self.sort_value:
            items = sorted(
                items,
                key=lambda item: str(getattr(item, self.sort_value)).lower(),
                reverse=self.sort_reverse,
            )

        # Filter items based on search value
        if self.search_value:
            search_value = self.search_value.lower()
            items = [
                item
                for item in items
                if any(
                    search_value in str(getattr(item, attr)).lower()
                    for attr in ['source', 'destination', 'hadith_count', 'taraf_count', 'book_count']
                )
            ]

        return items

    @rx.var(cache=True)
    def page_number(self) -> int:
        return (self.offset // self.limit) + 1

    @rx.var(cache=True)
    def total_pages(self) -> int:
        return (self.total_items // self.limit) + (
            1 if self.total_items % self.limit else 0
        )

    @rx.var(cache=True, initial_value=[])
    def get_current_page(self) -> list[isnads]:
        start_index = self.offset
        end_index = start_index + self.limit
        return self.filtered_sorted_items[start_index:end_index]

    def prev_page(self):
        if self.page_number > 1:
            self.offset -= self.limit

    def next_page(self):
        if self.page_number < self.total_pages:
            self.offset += self.limit

    def first_page(self):
        self.offset = 0

    def last_page(self):
        self.offset = (self.total_pages - 1) * self.limit

    def load_entries(self):
        self.total_items = len(self.edges)

    def toggle_sort(self):
        self.sort_reverse = not self.sort_reverse