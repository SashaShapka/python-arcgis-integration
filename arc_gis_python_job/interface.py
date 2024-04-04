from arc_gis_python_job.checks.chain import NameCheck, PathCheck, ProjectCheck, TypeCheck
from arc_gis_python_job.manager.manager import Context
from arc_gis_python_job.models import Project, Object, Types
from arcgis_python_db.db import ArcGisPythonDB
from sqlalchemy.exc import DatabaseError
from arc_gis_python_job.manager.object_creation import create_poligon, create_polyline, create_point_layer

db = ArcGisPythonDB()


def session_job(committed_obj):
    with db.session_scope() as session:
        try:
            session.add(committed_obj)
            session.flush()
            session.commit()

        except DatabaseError as e:
            print(e.__str__())


def add_project(project_name: str, project_path: str):
    name_check = NameCheck()
    path_check = PathCheck()
    name_check.set_next(path_check)
    name_check.check(project_name=project_name, project_path=project_path)
    project = Project(name=project_name, path=project_path)

    session_job(committed_obj=project)
    return project.id


def add_object(project_id: str, object_type: str, input_file_path: str, object_name: str, coordinate_system:int):
    project_check = ProjectCheck()
    type_check = TypeCheck()
    path_check = PathCheck()
    project_check.set_next(type_check).set_next(path_check)
    project_check.check(project_id=project_id, object_type=object_type, input_file_path=input_file_path)
    object_instance = Object(
        project=project_id,
        name=object_name,
        type=object_type,
        coordinate_system=coordinate_system,
    )
    session_job(committed_obj=object_instance)

    context = Context(input_object_file=input_file_path, object_id=object_instance.id, project_id=project_id)
    context.do_some_business_logic()

    if object_type == Types.POLIGON.value:
        create_poligon(object_id=object_instance.id, project_id=project_id)
    elif object_type == Types.POLILINE.value:
        create_polyline(object_id=object_instance.id, project_id=project_id)
    else:
        create_point_layer(object_id=object_instance.id, project_id=project_id)


if __name__ == '__main__':
   # add_project(project_name='MyProject1.gdb', project_path=r"D:\test_project\MyProject1\MyProject1.gdb")
   add_object(project_id='efbda36c-8441-4be8-b041-1eb0f399bdfd', object_type="point", input_file_path=r"D:\arcgis_python_integration\arcgis_source_file\multipoint.shp", object_name='point_arcgis', coordinate_system=5563)


