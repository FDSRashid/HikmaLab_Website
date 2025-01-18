import reflex as rx
import csv
import pandas as pd
import networkx as nx
import sqlalchemy
from sqlalchemy import func
from .isnad_state import QueryIsnads
from sqlmodel import select, or_
from typing import Dict, Any
import sqlmodel

class narrators(rx.Model, table=True):
    """The narrator model."""
    rawi_id: int = sqlmodel.Field(primary_key=True)

    gender: str
    official_name: str
    famous_name: str
    title_name: str
    kunya: str
    laqab: str
    occupation: str
    wasf: str
    madhhab: str
    nasab: str
    narrator_rank: str
    generation: int
    birth_date: str
    death_date: str
    age: str
    place_of_stay: str
    place_of_death: str
    mawla_relation: str
    famous_relatives: str
    number_of_narrations: int
    avg_death_date: str
    whole_number_death: str
     

class NetworkState(QueryIsnads):
    # Backend-only networkx graph (use underscore prefix for helper attributes)
    _graph: nx.Graph = nx.DiGraph()
    
    # Frontend state vars need proper initialization
    nodes: list = []  # Initialize empty list
    node_ids: list[int] = []  # Initialize empty list
    edges_network: list[tuple[int, int]] = []  # Initialize empty list
    node_positions: dict = {}  # Initialize empty dict

    def update_frontend_data(self):
        self.node_ids = list(self._graph.nodes())
        self.edges_network = list(self._graph.edges())

    @rx.event
    def retrieve_node_attributes(self):
        with rx.session() as session:
            query = select(narrators)
            if self.node_ids:
                query = query.where(narrators.rawi_id.in_(self.node_ids))
            found_nodes = session.exec(query).all()
            
            # Create a dictionary of found nodes by ID
            found_node_dict = {node.rawi_id: node for node in found_nodes}
            
            # Create default nodes for missing IDs
            all_nodes = []
            for node_id in self.node_ids:
                if node_id in found_node_dict:
                    all_nodes.append(found_node_dict[node_id])
                else:
                    # Create default narrator for missing node
                    default_node = narrators(
                        rawi_id=node_id,
                        gender="Unknown",
                        official_name=f"Unknown Narrator {node_id}",
                        famous_name=f"Unknown Narrator {node_id}",
                        title_name="",
                        kunya="",
                        laqab="",
                        occupation="",
                        wasf="",
                        madhhab="",
                        nasab="",
                        narrator_rank="Unknown",
                        generation=-1,
                        birth_date="",
                        death_date="",
                        age="",
                        place_of_stay="",
                        place_of_death="",
                        mawla_relation="",
                        famous_relatives="",
                        number_of_narrations=0,
                        avg_death_date="",
                        whole_number_death=""
                    )
                    all_nodes.append(default_node)
            
            self.nodes = all_nodes     
    
    @rx.event
    def update_node_positions(self):
        # Store positions in state var
        positions = nx.nx_agraph.graphviz_layout(self._graph, prog='dot')
        self.node_positions = positions  # This updates the state var

    
    @rx.event
    def retrieve_isnad_network(self):
        edges = [(obj.source, obj.destination) for obj in self.edges] 
        self._graph.add_edges_from(edges)
        self.update_node_positions()
        self.update_frontend_data()
        self.retrieve_node_attributes()

    @rx.event
    def get_hadith_network(self):
        self._graph = nx.DiGraph()
        self.get_isnads_hadith()
        self.retrieve_isnad_network()


    @rx.event
    def get_taraf_network(self):
        self._graph = nx.DiGraph()
        self.get_isnads_taraf()
        self.retrieve_isnad_network()

    @rx.var
    def processed_nodes(self):
        return [{
            'id': node.rawi_id,
            'name': node.famous_name,
            'x': self.node_positions[node.rawi_id][0],
            'y': -self.node_positions[node.rawi_id][1],
            'fontsize': 200
        } for node in self.nodes]

    @rx.var
    def processed_edges(self):
        return [{'source': source, 'target': target} 
                for source, target in self.edges_network]

