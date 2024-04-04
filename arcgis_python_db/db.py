import contextlib

import sqlalchemy.orm
import arcgis_python_db.manager_lib.lib as lib
from arc_gis_python_job import models
from arc_gis_python_job.config import DB_NAME


class ArcGisPythonDB(metaclass=lib.Singleton):

    def __init__(self, timeout=60, create_all=False):

        self.is_closed = False
        self.engine = sqlalchemy.create_engine(lib.get_connection_string(DB_NAME))
        self.engine.pool_timeout = timeout
        self.session = sqlalchemy.orm.sessionmaker(bind=self.engine)

        if create_all:
            models.Base.metadata.create_all(self.engine)

    def __del__(self):
        """
        Calls the close method
        """
        try:
            self.close()
        except Exception:
            pass

    def close(self):
        """
        Closes the connections and disposes the engine
        """
        if self.is_closed or self.engine is None:
            return

        self.engine.dispose()
        self.is_closed = True

    @contextlib.contextmanager
    def session_scope(self, to_commit=True):
        """
        Context manager for creating and using the SQL session
        :param to_commit: True if the session needs to be committed at the end
        :return: Session object
        """
        session = self.session(expire_on_commit=False)
        try:
            yield session
            if to_commit:
                session.commit()
        except Exception as err:
            session.rollback()
            raise
        finally:
            session.close()