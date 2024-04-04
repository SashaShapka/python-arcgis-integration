import sqlalchemy
import enum
from sqlalchemy.ext.declarative import declarative_base
from arcgis_python_db.allocator import UUID_F
from sqlalchemy import Enum


Base = declarative_base()


class Types(enum.Enum):
    POLILINE = "poliline"
    POLIGON = "poligon"
    POINT = "point"

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)


class Project(Base):
    __tablename__ = "project"

    id = sqlalchemy.Column(UUID_F(), default=UUID_F.uuid_allocator, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(36), nullable=False)
    path = sqlalchemy.Column(sqlalchemy.String(), nullable=False)

    def __init__(self, name, path):
        self.name = name
        self.path = path


class Object(Base):
    __tablename__ = "object"
    id = sqlalchemy.Column(UUID_F(), default=UUID_F.uuid_allocator, primary_key=True)
    project = sqlalchemy.Column(
        sqlalchemy.String(36), sqlalchemy.ForeignKey("project.id"), nullable=False
    )
    name = sqlalchemy.Column(sqlalchemy.String(), nullable=False)
    type = sqlalchemy.Column(sqlalchemy.String(), nullable=False)
    coordinate_system = sqlalchemy.Column(sqlalchemy.INTEGER(), nullable=False)

    def __init__(self, project, name, type, coordinate_system):
        self.project = project
        self.name = name
        self.type = type
        self.coordinate_system = coordinate_system


class Coordinates(Base):
    __tablename__ = "coordinates"
    id = sqlalchemy.Column(UUID_F(), default=UUID_F.uuid_allocator, primary_key=True)
    project_id = sqlalchemy.Column(
        sqlalchemy.String(36), sqlalchemy.ForeignKey("project.id"), nullable=False
    )
    object = sqlalchemy.Column(
        sqlalchemy.String(36), sqlalchemy.ForeignKey("object.id"), nullable=False
    )
    coordinate = sqlalchemy.Column(sqlalchemy.JSON())

    def __init__(self, object, coordinate, project_id):
        self.object = object
        self.project_id=project_id
        self.coordinate = coordinate