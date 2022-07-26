import datetime
from dataclasses import dataclass, field
from serialize import *


@dataclass(slots=True)
class Record(ISerializable):
    mapped_word: str
    contents: list[str] = field(default_factory=list)
    last_update_date: datetime.date = field(default_factory=datetime.date.today)
    repeated_times: int = 0
