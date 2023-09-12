from dataclasses import asdict
from pydantic.dataclasses import dataclass

from services.case_converter import to_camel_case_mapper


@dataclass
class Manufacturer:
    id: int
    name: str

    def to_json(self):
        data_dict = asdict(self)
        return to_camel_case_mapper(data_dict)

