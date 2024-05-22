#!D:\arcgis_pro\bin\Python\envs\arcgispro-py3\python.exe
from arcgis_python_db.db import ArcGisPythonDB
from arc_gis_python_job.models import Project, Object, Coordinates
from arc_gis_python_job.config import logging

db = ArcGisPythonDB()


def get_prework_arguments(project_id, object_id):
    with db.session_scope() as session:
        project_path = session.query(Project).filter_by(id=project_id).one().path
        object_name = session.query(Object).filter_by(id=object_id).one().name
        coordinate_system = session.query(Object).filter_by(id=object_id).one().coordinate_system
        points = session.query(Coordinates).filter_by(project_id=project_id, object=object_id).one().coordinate

    return project_path, object_name, coordinate_system, points


def create_poligon(project_id, object_id):

    logging.info("Starting creating POLIGON object")

    import arcpy
    magick_name = False

    project_path, object_name, coordinate_system, points = get_prework_arguments(project_id=project_id,
                                                                                 object_id=object_id)
    if len(points.keys()) > 1:
        magick_name = True

    index = 1
    for point_key, point_value in points.items():
        array = []
        name = object_name + str(index) if magick_name else object_name
        for points in point_value:
            arc_point = arcpy.Point(*points)
            array.append(arc_point)

        arcpy_array = arcpy.Array(array)

        spatial_reference = arcpy.SpatialReference(int(coordinate_system))
        polygon_fc = arcpy.management.CreateFeatureclass(
            project_path, name, "POLYGON", spatial_reference=spatial_reference)
        cursor = arcpy.da.InsertCursor(polygon_fc, ["SHAPE@"])
        polygon = arcpy.Polygon(arcpy_array)
        cursor.insertRow([polygon])
        index += 1


def create_polyline(project_id, object_id):

    logging.info("Starting creating POLILINE object")

    import arcpy

    project_path, object_name, coordinate_system, points = get_prework_arguments(project_id=project_id,
                                                                                 object_id=object_id)
    magick_name = False
    if len(points.keys()) > 1:
        magick_name = True

    index = 1
    for point_key, point_value in points.items():
        array = []
        name = object_name + str(index) if magick_name else object_name
        for points in point_value:
            arc_point = arcpy.Point(*points)
            array.append(arc_point)

        arcpy_array = arcpy.Array(array)
        spatial_reference = arcpy.SpatialReference(int(coordinate_system))
        polyline_fc = arcpy.management.CreateFeatureclass(project_path, name,
                        "POLYLINE", spatial_reference=spatial_reference)

        cursor = arcpy.da.InsertCursor(polyline_fc, ["SHAPE@"])

        polyline = arcpy.Polyline(arcpy_array)
        cursor.insertRow([polyline])
        index += 1


def create_point_layer(project_id, object_id):

    logging.info("Starting creating POINT object")

    import arcpy

    project_path, object_name, coordinate_system, points = get_prework_arguments(project_id=project_id,
                                                                                 object_id=object_id)
    magick_name = False
    if len(points.keys()) > 1:
        magick_name = True

    index = 1
    for point_key, point_value in points.items():
        name = object_name + str(index) if magick_name else object_name
        for points in point_value:
            arc_point = arcpy.Point(*points)
            spatial_reference = arcpy.SpatialReference(int(coordinate_system))
            point_fc = arcpy.management.CreateFeatureclass(project_path, name,
                            "POINT", spatial_reference=spatial_reference)

            cursor = arcpy.da.InsertCursor(point_fc, ["SHAPE@"])
            cursor.insertRow([arc_point])
            index += 1