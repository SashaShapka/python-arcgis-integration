from __future__ import annotations

from abc import ABC, abstractmethod

from arc_gis_python_job.manager.deep_learning_analize import detect_objects_using_deep_learning
from arc_gis_python_job.models import AnalyseObjects
from arcgis_python_db.db import ArcGisPythonDB

db = ArcGisPythonDB()


class AnaliseContext:
    """The Context defines the interface of interest to clients.
    """

    def __init__(self, strategy: Strategy):
        self._strategy = strategy

    @property
    def strategy(self) -> Strategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        self._strategy = strategy

    def do_some_business_logic(self, project_id, in_features_path, analyse_obj_id) -> None:
        self._strategy.do_algorithm(project_id=project_id, in_features_path=in_features_path,
                                    analyse_obj_id=analyse_obj_id)


class Strategy(ABC):

    @abstractmethod
    def do_algorithm(self, project_id: str, in_features_path: str, analyse_obj_id: str):
        pass


class DetectTreeObjectStrategy(Strategy):
    def do_algorithm(self, project_id: str, in_features_path: str, analyse_obj_id: str):
        with db.session_scope() as session:
            analise_object_data = session.query(AnalyseObjects).filter_by(id=analyse_obj_id).one()
            detect_objects_using_deep_learning(input_raster=analise_object_data.in_raster_path,
                                               out_detected_objects=analise_object_data.out_feature_class_name,
                                               in_model_definition=analise_object_data.in_model_definition_path,
                                               in_feature_path=analise_object_data.in_features_path)


class DetectRoadObjectsStrategy(Strategy):
    def do_algorithm(self, project_id: str, in_features_path: str, analyse_obj_id: str):
        with db.session_scope() as session:
            analise_object_data = session.query(AnalyseObjects).filter_by(id=analyse_obj_id).one()
            detect_objects_using_deep_learning(input_raster=analise_object_data.in_raster_path,
                                               out_detected_objects=analise_object_data.out_feature_class_name,
                                               in_model_definition=analise_object_data.in_model_definition_path,
                                               in_feature_path=analise_object_data.in_features_path)


class DetectBuildObjectsStrategy(Strategy):
    def do_algorithm(self, project_id: str, in_features_path: str, analyse_obj_id: str):
        with db.session_scope() as session:
            analise_object_data = session.query(AnalyseObjects).filter_by(id=analyse_obj_id).one()
            detect_objects_using_deep_learning(input_raster=analise_object_data.in_raster_path,
                                               out_detected_objects=analise_object_data.out_feature_class_name,
                                               in_model_definition=analise_object_data.in_model_definition_path,
                                               in_feature_path=analise_object_data.in_features_path)


class DetectWaterObjectsStrategy(Strategy):
    def do_algorithm(self, project_id: str, in_features_path: str, analyse_obj_id: str):
        with db.session_scope() as session:
            analise_object_data = session.query(AnalyseObjects).filter_by(id=analyse_obj_id).one()
            detect_objects_using_deep_learning(input_raster=analise_object_data.in_raster_path,
                                               out_detected_objects=analise_object_data.out_feature_class_name,
                                               in_model_definition=analise_object_data.in_model_definition_path,
                                               in_feature_path=analise_object_data.in_features_path)