from typing import Optional, Annotated, List
from pydantic import BaseModel, ConfigDict, Field, BeforeValidator, field_validator


# Represents an ObjectId field in the database.
# It will be represented as a string in the model so that it can be serialized to JSON.

PyObjectId = Annotated[str, BeforeValidator(str)]


class CarModel(BaseModel):
    """
    Container for a single car document in the database
    """

    # The primary key for the CarModel, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses

    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    brand: str = Field(...)
    make: str = Field(...)
    year: int = Field(..., gt=1970, lt=2025)
    cm3: int = Field(..., gt=0, lt=5000)
    km: int = Field(..., gt=0, lt=500 * 1000)
    price: int = Field(..., gt=0, lt=100 * 1000)

    @field_validator("brand")
    @classmethod
    def check_brand_case(cls, v: str) -> str:
        return v.title()

    @field_validator("make")
    @classmethod
    def check_make_case(cls, v: str) -> str:
        return v.title()

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "brand": "Ford",
                "make": "Fiesta",
                "year": 2019,
                "cm3": 1500,
                "km": 120000,
                "price": 10000,
            }
        },
    )


# test_car = CarModel(
#     brand="ford", make="fiesta", year=2019, cm3=1500, km=120000, price=10000
# )

# print(test_car.model_dump())


class UpdateCarModel(BaseModel):
    """
    Optional updates
    """

    # The primary key for the CarModel, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses

    brand: str = Field(...)
    make: Optional[str] = Field(...)
    year: Optional[int] = Field(..., gt=1970, lt=2025)
    cm3: Optional[int] = Field(..., gt=0, lt=5000)
    km: Optional[int] = Field(..., gt=0, lt=500 * 1000)
    price: Optional[int] = Field(..., gt=0, lt=100 * 1000)

    @field_validator("brand")
    @classmethod
    def check_brand_case(cls, v: str) -> str:
        return v.title()

    @field_validator("make")
    @classmethod
    def check_make_case(cls, v: str) -> str:
        return v.title()

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "brand": "Ford",
                "make": "Fiesta",
                "year": 2019,
                "cm3": 1500,
                "km": 120000,
                "price": 10000,
            }
        },
    )


class CarCollection(BaseModel):
    """
    A container holding a list of cars
    """

    cars: List[CarModel]


# test_car_1 = CarModel(
#     brand="ford", make="fiesta", year=2019, cm3=1500, km=120000, price=10000
# )

# test_car_2 = CarModel(
#     brand="fiat", make="stilo", year=2003, cm3=1600, km=320000, price=3000
# )

# car_list = CarCollection(cars=[test_car_1, test_car_2])

# print(car_list.model_dump())
