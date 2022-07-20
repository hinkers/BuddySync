import requests
from sqlalchemy import create_engine
from dataclasses import dataclass
from sqlalchemy.orm import sessionmaker

@dataclass
class SQL:

    connection_string: str
    _engine = None
    _session = None

    def __init__(self, connectionstring):
        self.connection_string = connectionstring
    
    def engine(self):
        if self._engine is None:
            self._engine = create_engine(self.connection_string, echo=False)
            self._session = sessionmaker(bind=self.engine())
        return self._engine

    def session(self):
        if self._session is None:
            self._session = sessionmaker(bind=self.engine())
        return self._session
