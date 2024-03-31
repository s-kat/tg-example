import random

from src.core.stg.coa.ds.load.loader import CoaLoader
from src.core.unit.coa.ds.model import CoaCity, CoaCollection, CoaRegion
from src.settings.settings import Settings


class CoaCollectionStorage:

    def __init__(self, coa_collection: CoaCollection, settings: Settings):

        self.coa_collection = coa_collection
        self.settings = settings

    @classmethod
    def create(cls, settings: Settings) -> "CoaCollectionStorage":

        loader = CoaLoader(
            cities_collection_path=settings.COA_CITIES_COLLECTION_LOCATION,
            states_collection_path=settings.COA_STATES_COLLECTION_LOCATION,
        )

        coa_collection = loader.load_coa_collection()

        mng = cls(coa_collection=coa_collection, settings=settings)

        return mng

    def get_random_city(self) -> CoaCity:
        random_city = random.choice(self.coa_collection.cities)

        print(f"RANDOM CITY: {random_city}")

        return random_city

    def get_random_region(self) -> CoaRegion:
        random_region = random.choice(self.coa_collection.regions)

        print(f"RANDOM REGION: {random_region}")


        return random_region

    def find_city(self, city_name: str) -> CoaCity | None:

        cities = [
            city
            for city in self.coa_collection.cities
            if city_name.lower() == city.city_title.lower()
        ]

        if len(cities) == 0:
            return None

        return cities[0]

    def find_region(self, region_name: str) -> CoaRegion | None:

        regions = [
            state
            for state in self.coa_collection.regions
            if region_name.lower() == state.region_title.lower()
        ]

        if len(regions) == 0:
            return None

        return regions[0]
