import typing

import pydantic


class CoaCity(pydantic.BaseModel):

    city_title: str = pydantic.Field(alias="title")
    coa_url: str = pydantic.Field(alias="crest_url")
    city_description: str = pydantic.Field(alias="description")
    coordinates: tuple[float, float]

    class Config:
        allow_population_by_field_name = True


class CoaRegion(pydantic.BaseModel):
    region_title: str = pydantic.Field(alias="title")
    coa_url: str = pydantic.Field(alias="crest_url")
    boards_img: str = pydantic.Field(alias="bordrs_img")
    state_description: str = pydantic.Field(alias="description")
    coordinates: tuple[float, float]

    class Config:
        allow_population_by_field_name = True


class CoaCollection(pydantic.BaseModel):

    cities: list[CoaCity]
    regions: list[CoaRegion]
