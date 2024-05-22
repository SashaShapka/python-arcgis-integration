from __future__ import annotations

import openpyxl
import subprocess
import re
from abc import ABC, abstractmethod

from sqlalchemy.exc import DatabaseError

from arc_gis_python_job.models import Project, Object, Coordinates, Types
from arcgis_python_db.db import ArcGisPythonDB


db = ArcGisPythonDB()


class Context:
    def __init__(self, input_object_file, object_id, project_id):
        self.input_object_file = input_object_file
        self.object = object_id,
        self.project_id = project_id
        self._strategy = ShapeStrategy() if input_object_file.endswith('.shp') else XLSXStrategy()

    @property
    def strategy(self) -> Strategy:
        return self._strategy

    def do_some_business_logic(
            self,
    ) -> None:
        print(f"Context: Saving data via {self.__repr__()}")
        self._strategy.do_algorithm(
            input_object_file=self.input_object_file,
            object=self.object,
            project=self.project_id
        )

    def __repr__(self):
        if "ShapeStrategy" in str(self._strategy):
            return "Shape Strategy"

        elif "XLSXStrategy" in str(self._strategy):
            return "XLSX Strategy"


class Strategy(ABC):
    @abstractmethod
    def do_algorithm(self, **kwargs):
        pass


class ShapeStrategy(Strategy):

    def do_algorithm(self, **kwargs):
            
        import arcpy

        file = kwargs.get("input_object_file")
        formatted_file_path = r'{}'.format(file)
        res = {}
        with arcpy.da.SearchCursor(formatted_file_path, ["SHAPE@"]) as cursor:
            for row in cursor:
                points = []
                shape = row[0]
                if isinstance(shape, arcpy.PointGeometry):
                    label = shape.labelPoint
                    points.append((label.X, label.Y))
                    res.update({shape.length: points})
                else:
                    for part in shape:
                        for point in part:
                            points.append((point.X, point.Y))
                    res.update({shape.length: points})

        with db.session_scope() as session:
            try:
                coordinates = Coordinates(
                    object=kwargs.get("object"),
                    project_id=kwargs.get("project"),
                    coordinate=res
                )
                session.add(coordinates)
                session.commit()
            except DatabaseError as e:
                print(e.__str__())


class XLSXStrategy(Strategy):

    @staticmethod
    def clean_and_convert(value):
        # Replace non-breaking space and comma, then convert to float
        cleaned_value = re.sub(r'[^\d.]', '', value)
        return int(cleaned_value)

    def do_algorithm(self, **kwargs):
        xlsx_file_path = kwargs.get("input_object_file")
        wb = openpyxl.load_workbook(xlsx_file_path)
        sheet = wb.active
        points = list()
        for row in sheet.iter_rows(min_row=2, values_only=True):
            points.append((self.clean_and_convert(row[1]), self.clean_and_convert(row[2])))

        #TODO: countinue