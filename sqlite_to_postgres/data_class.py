import uuid
import dataclasses
from dataclasses import dataclass, field
from datetime import date, datetime
from const import FORMAT_TIME


@dataclass
class MainMix:
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def to_tuple(self, ) -> tuple:
        return dataclasses.astuple(self)

    def to_dict(self, ) -> dict:
        return dataclasses.asdict(self)


@dataclass
class Filmwork(MainMix):
    title: str = field(default='')
    description: str = field(default='')
    creation_date: date = field(default=None)
    file_path: str = field(default='')
    rating: float = field(default=None)
    type: str = field(default='')
    created: datetime = field(default=None)
    modified: datetime = field(default=None)

    def __post_init__(self) -> None:
        if isinstance(self.created, str):
            self.created = datetime.strptime(self.created, FORMAT_TIME)
        if isinstance(self.modified, str):
            self.modified = datetime.strptime(self.modified, FORMAT_TIME)

    @staticmethod
    def TableName() -> str:
        return 'film_work'


@dataclass
class Genre(MainMix):
    name: str = field(default='')
    description: str = field(default='')
    created: datetime = field(default=None)
    modified: datetime = field(default=None)

    def __post_init__(self) -> None:
        if isinstance(self.created, str):
            self.created = datetime.strptime(self.created, FORMAT_TIME)
        if isinstance(self.modified, str):
            self.modified = datetime.strptime(self.modified, FORMAT_TIME)

    @staticmethod
    def TableName() -> str:
        return 'genre'


@dataclass
class Person(MainMix):
    full_name: str = field(default='')
    created: datetime = field(default=None)
    modified: datetime = field(default=None)

    def __post_init__(self) -> None:
        if isinstance(self.created, str):
            self.created = datetime.strptime(self.created, FORMAT_TIME)
        if isinstance(self.modified, str):
            self.modified = datetime.strptime(self.modified, FORMAT_TIME)

    @staticmethod
    def TableName() -> str:
        return 'person'


@dataclass
class GenreFilmwork(MainMix):
    genre_id: uuid.UUID = field(default_factory=uuid.uuid4)
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)
    created: datetime = field(default=None)

    def __post_init__(self) -> None:
        if isinstance(self.created, str):
            self.created = datetime.strptime(self.created, FORMAT_TIME)

        self.genre_id, self.film_work_id = self.film_work_id, self.genre_id

    @staticmethod
    def TableName() -> str:
        return 'genre_film_work'


@dataclass
class PersonFilmwork(MainMix):
    person_id: uuid.UUID = field(default_factory=uuid.uuid4)
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)
    role: str = field(default='')
    created: datetime = field(default=None)

    def __post_init__(self) -> None:
        if isinstance(self.created, str):
            self.created = datetime.strptime(self.created, FORMAT_TIME)

        self.person_id, self.film_work_id = self.film_work_id, self.person_id

    @staticmethod
    def TableName() -> str:
        return 'person_film_work'
