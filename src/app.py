from dataclasses import dataclass
from database import DatabasesView
from testmethod import ITestmethod
from serialize import ISerializer


@dataclass(slots=True)
class Model:
    serializer: ISerializer
    testmethod: ITestmethod
    databases: DatabasesView
