from dataclasses import asdict
from datetime import datetime
from typing import Optional
from pydantic.dataclasses import dataclass

from services.case_converter import to_camel_case_mapper


@dataclass
class MachineInputDTO:
    name: str
    manufacturer_id: int
    purchased_at: datetime
    year_of_manufacture: int
    status: str  # optional values are '0', or '1'
    capacity_in_percent: float


@dataclass
class Machine(MachineInputDTO):
    id: int
    created_at: datetime
    updated_at: datetime
    image_url: Optional[str] = None

    def to_json(self):
        data_dict = asdict(self)
        return to_camel_case_mapper(data_dict)


@dataclass
class MachineUpdateDTO(MachineInputDTO):
    id: int


@dataclass
class Machines:
    machines: list[Machine]
