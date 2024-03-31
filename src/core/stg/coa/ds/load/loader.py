import json
import typing

from pydantic import TypeAdapter

from src.core.unit.coa.ds.model import CoaCity, CoaCollection, CoaRegion


class CoaLoader:
    def __init__(
        self,
        cities_collection_path: str,
        states_collection_path: str,
    ):

        self.cities_path = cities_collection_path
        self.states_path = states_collection_path

    def load_coa_collection(self) -> CoaCollection:

        return CoaCollection(
            cities=self.load_coa_cities_collection(),
            regions=self.load_coa_states_collection(),
        )

    def load_coa_cities_collection(self) -> typing.List[CoaCity]:
        with open(self.cities_path, "r") as r_file:
            data = json.load(r_file)

        cities = TypeAdapter(typing.List[CoaCity]).validate_python(data)

        return cities

    def load_coa_states_collection(self) -> typing.List[CoaRegion]:
        with open(self.states_path, "r") as r_file:
            data = json.load(r_file)

        states = TypeAdapter(typing.List[CoaRegion]).validate_python(data)

        return states
