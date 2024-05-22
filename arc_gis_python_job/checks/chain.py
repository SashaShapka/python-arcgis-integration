from abc import ABC, abstractmethod
from arc_gis_python_job.config import logging
import os

from arcgis_python_db.db import ArcGisPythonDB
from arc_gis_python_job.models import Project, Types

db = ArcGisPythonDB()


class Check(ABC):
    @abstractmethod
    def set_next(self, check):
        pass

    @abstractmethod
    def check(self, db=db, project_name=None, project_path=None, project_id=None, object_type=None, input_file_path=None):
        pass

    @staticmethod
    def project_name_check(project_name):
        if len(project_name) <= 36 and project_name.endswith('.gdb'):
            return
        raise Exception

    @staticmethod
    def is_path(project_path):
        if os.path.isabs(project_path) or os.path.isabs(os.path.expanduser(project_path)):
            return
        raise Exception


class AbstractCheck(Check):
    _next_check = None

    def set_next(self, check: Check):
        self._next_check = check
        return check

    @abstractmethod
    def check(self, db=db, project_name=None, project_path=None, project_id=None, object_type=None, input_file_path=None):
        if self._next_check:
            return self._next_check.check(db=db, project_name=project_name, project_path=project_path, project_id=project_id,
                                          object_type=object_type, input_file_path=input_file_path)


class NameCheck(AbstractCheck):
    def check(self, db=db, project_name=None, project_path=None, project_id=None, object_type=None, input_file_path=None):
        try:
            self.project_name_check(project_name=project_name)
        except:
            raise Exception("Name is incorrect ")
        logging.info('Successfully validation - project_name')
        super().check(project_name=project_name, project_path=project_path, project_id=project_id, object_type=object_type, input_file_path=input_file_path)


class PathCheck(AbstractCheck):
    def check(self, db=db, project_name=None, project_path=None, project_id=None, object_type=None, input_file_path=None):
        try:
            self.is_path(project_path if project_path else input_file_path)
        except:
            raise Exception("Path is incorrect")
        logging.info('successfully validation - path_check')


class ProjectCheck(AbstractCheck):
    def check(self, db=db, project_name=None, project_path=None, project_id=None, object_type=None, input_file_path=None):
        with db.session_scope() as session:
            try:
                session.query(Project).filter_by(id=project_id).one()
            except:
                raise Exception("Project does not exist")

        logging.info("successfully validation - project_id")
        super().check(project_name=project_name, project_path=project_path, project_id=project_id, object_type=object_type, input_file_path=input_file_path)


class TypeCheck(AbstractCheck):

    def check(self, db=db, project_name=None, project_path=None, project_id=None, object_type=None, input_file_path=None):
        if Types.has_value(object_type):
            logging.info("successfully validation - object_type")
        else:
            raise Exception("Type is invalid")

        super().check(project_name=project_name, project_path=project_path, project_id=project_id, object_type=object_type, input_file_path=input_file_path)


