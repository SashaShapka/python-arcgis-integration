import sqlalchemy
import enum
from sqlalchemy.ext.declarative import declarative_base
from arcgis_python_db.allocator import UUID_F


Base = declarative_base()

IN_TRAINING_BUILDINGS = r"D:\deep_python_arcgis\MyProject1\MyProject1.gdb\training_buildings"
IN_TRAINING_WATER = r"D:\deep_python_arcgis\MyProject1\MyProject1.gdb\water_training"
IN_TRAINING_ROAD = r"D:\deep_python_arcgis\MyProject1\MyProject1.gdb\training_road"


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
        self.project_id = project_id
        self.coordinate = coordinate


class AnalyseObjects(Base):
    __tablename__ = "analyse_objects"
    id = sqlalchemy.Column(UUID_F(), default=UUID_F.uuid_allocator, primary_key=True)
    project_id = sqlalchemy.Column(
        sqlalchemy.String(36), sqlalchemy.ForeignKey("project.id"), nullable=False
    )
    in_raster_path = sqlalchemy.Column(sqlalchemy.String(), nullable=False)
    out_feature_class_name = sqlalchemy.Column(sqlalchemy.String(), nullable=False)
    in_model_definition_path = sqlalchemy.Column(sqlalchemy.String(), nullable=False)
    in_features_path = sqlalchemy.Column(sqlalchemy.String(), nullable=False)
    analyse_type = sqlalchemy.Column(sqlalchemy.String(), nullable=False)

    def __init__(self, project_id, in_raster_path, out_feature_class_name, in_model_definition_path, analyse_type, in_features_path):
        self.project_id = project_id
        self.in_raster_path = in_raster_path
        self.out_feature_class_name = out_feature_class_name
        self.in_model_definition_path = in_model_definition_path
        self.analyse_type = analyse_type
        self.in_features_path = in_features_path


class ExportTrainingDataObjects(Base):
    __tablename__ = "export_training_data_objects"

    id = sqlalchemy.Column(UUID_F(), default=UUID_F.uuid_allocator, primary_key=True)
    project_id = sqlalchemy.Column(
        sqlalchemy.String(36), sqlalchemy.ForeignKey("project.id"), nullable=False
    )
    in_raster = sqlalchemy.Column(sqlalchemy.String(), nullable=False)
    out_folder = sqlalchemy.Column(sqlalchemy.String(), nullable=False)
    in_class_data = sqlalchemy.Column(sqlalchemy.String(), nullable=False, default=lambda context: context.get_current_parameters()['type_of_data_training'])
    image_chip_format = sqlalchemy.Column(sqlalchemy.String(), nullable=False)
    output_dpl_folder = sqlalchemy.Column(sqlalchemy.String(), nullable=False)
    type_of_data_training = sqlalchemy.Column(sqlalchemy.String(), nullable=False)

    def __init__(self, project_id, in_raster, out_folder, image_chip_format, type_of_data_training, output_dpl_folder, in_class_data=None):
        self.project_id = project_id
        self.in_raster = in_raster
        self.out_folder = out_folder
        self.image_chip_format = image_chip_format
        self.output_dpl_folder = output_dpl_folder
        self.type_of_data_training = type_of_data_training
        if in_class_data is None:
            self.in_class_data = self._set_in_class_data()
        else:
            self.in_class_data = in_class_data

    def _set_in_class_data(self):
        data_mapping = {
            "road": IN_TRAINING_ROAD,
            "water": IN_TRAINING_WATER,
            "buildings": IN_TRAINING_BUILDINGS
        }
        return data_mapping.get(self.type_of_data_training)
