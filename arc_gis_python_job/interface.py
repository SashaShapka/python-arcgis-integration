from config import logging
from arc_gis_python_job.checks.chain import NameCheck, PathCheck, ProjectCheck, TypeCheck
from arc_gis_python_job.manager.deep_learning_analize_manager import AnaliseContext,\
    DetectTreeObjectStrategy, DetectBuildObjectsStrategy, DetectRoadObjectsStrategy, DetectWaterObjectsStrategy
from arc_gis_python_job.manager.export_training_data import export_training_data
from arc_gis_python_job.manager.manager import Context
from arc_gis_python_job.models import Project, Object, Types, AnalyseObjects, ExportTrainingDataObjects
from arcgis_python_db.db import ArcGisPythonDB
from sqlalchemy.exc import DatabaseError
from arc_gis_python_job.manager.object_creation import create_poligon, create_polyline, create_point_layer

db = ArcGisPythonDB()


def session_job(committed_obj, commit=True):
    with db.session_scope() as session:
        try:
            session.add(committed_obj)
            session.flush()
            session.commit()

        except DatabaseError as e:
            print(e.__str__())


def add_project(project_name: str, project_path: str):

    """Description:
    The add_project function is designed to add a new ArcGIS project by performing a series of checks on the provided project name and path, then registering the project within a session job. It logs the process of adding the project and confirms its successful addition.

    Parameters:
    project_name (str): The name of the project to be added. This name is checked for validity to ensure it meets specific criteria.
    project_path (str): The filesystem path where the project will be stored. This path is also validated to ensure it is accessible and appropriate for storing the project.
    Returns:
    project.id (int or similar identifier): Returns the unique identifier of the newly added project.
    Detailed Workflow:
    Logging Start: The function logs the initiation of the process to add an ArcGIS project with the specified project_name.
    Checks Initialization:
    NameCheck(): Initializes a name checking process to validate the project_name.
    PathCheck(): Initializes a path checking process to validate the project_path.
    Chain of Responsibility Setup:
    The name checking process is set to pass its result to the path checking process.
    Execution of Checks:
    The chained validation processes are executed with the provided project_name and project_path.
    Project Initialization:
    A new Project object is created with the validated name and path.
    Session Job Registration:
    The new project is registered within a session job, which may involve database interactions or other session-specific logic to commit the project data.
    Logging Completion: Logs the successful addition of the project, noting the project_path.
    Return Value: Returns the unique identifier of the newly added project, typically used for further reference or operations."""

    logging.info(f"Starting add the arcgis project {project_name}")
    name_check = NameCheck()
    path_check = PathCheck()
    name_check.set_next(path_check)
    name_check.check(project_name=project_name, project_path=project_path)
    project = Project(name=project_name, path=project_path)
    session_job(committed_obj=project)
    logging.info(f'Project {project_path} added successfully')
    return project.id


def add_object(project_id: str, object_type: str, input_file_path: str, object_name: str, coordinate_system: int):

    """Description:
    The add_object function is responsible for adding a new geospatial object to a specified project by conducting several checks on the project's validity, the object type, and the file path. It also logs various stages of the process and manages the integration of the object into the project's database and file system.

    Parameters:
    project_id (str): The identifier for the project to which the object is being added.
    object_type (str): Specifies the type of the object, such as "POLYGON", "POLYLINE", or "POINT".
    input_file_path (str): The file path where the input data for the object is located.
    object_name (str): The name given to the object.
    coordinate_system (int): The identifier for the coordinate system used by the object.
    Returns:
    This function does not explicitly return a value but performs several operations including logging the success of the operations and updating the database.
    Detailed Workflow:
    Logging Start: Logs the start of the object addition process, including the object's name and type.
    Checks Initialization:
    ProjectCheck(): Initializes a project validity check.
    TypeCheck(): Initializes a type check for the object.
    PathCheck(): Initializes a path check for the file location.
    Chain of Responsibility Setup:
    Chains the checking processes together, allowing for a streamlined validation flow.
    Execution of Checks:
    Executes the chained validation processes using the provided parameters.
    Object Instance Creation:
    Creates a new Object instance with the provided details, ready to be committed.
    Session Job Registration:
    Registers the new object within a session job, likely involving database transactions to save the object data.
    Logging Database Addition:
    Logs the successful addition of the object into the database.
    Shapefile Processing:
    Begins processing to convert the project data into a shapefile format, logging the start of this process.
    Depending on the object_type, calls the appropriate function to create the geometric representation (polygon, polyline, or point).
    Logging Completion:
    Logs the successful creation of the shapefile, indicating the end of the process."""

    logging.info(f"Starting add the object {object_name}:{object_type}")
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
    logging.info("Object added in to the DB")

    logging.info("Start adding the project as a shapefile")
    context = Context(input_object_file=input_file_path, object_id=object_instance.id, project_id=project_id)
    context.do_some_business_logic()

    if object_type == Types.POLIGON.value:
        create_poligon(object_id=object_instance.id, project_id=project_id)
    elif object_type == Types.POLILINE.value:
        create_polyline(object_id=object_instance.id, project_id=project_id)
    else:
        create_point_layer(object_id=object_instance.id, project_id=project_id)
    logging.info("Shapefile created successfully")


def deep_learning_scan(project_id: str,
                       in_raster_path: str,
                       out_feature_class_name: str,
                       in_model_definition_path: str,
                       in_features_path: str,
                       analyse_type: str):
    """Description:
    The deep_learning_scan function applies deep learning techniques to analyze geospatial raster data for specific features within a project. It checks the validity of the project and paths involved, manages database updates for the analysis, and applies different strategies based on the type of analysis requested.

    Parameters:
    project_id (str): Identifier for the project under which the analysis is performed.
    in_raster_path (str): File path to the input raster data that will be analyzed.
    out_feature_class_name (str): Name for the output feature class that will store the results of the analysis.
    in_model_definition_path (str): Path to the deep learning model definition used for analysis.
    in_features_path (str): Path to additional input features needed for the analysis.
    analyse_type (str): Type of analysis to be performed, such as "tree", "road", "water", or "building".
    Returns:
    This function does not return a value but logs significant steps and outcomes throughout its execution.
    Detailed Workflow:
    Logging Start: Logs the initiation of the deep learning scan on the specified raster path.
    Checks Initialization:
    ProjectCheck(): Ensures the project ID is valid and the project exists.
    PathCheck(): Ensures the paths for the raster, model definition, and feature inputs are valid.
    Chain of Responsibility Setup:
    Links the project check directly to the path check for streamlined validation.
    Validation Execution:
    Executes the project and path validations using the provided parameters.
    Analysis Object Initialization:
    Creates an AnalyseObjects instance configured with all necessary data for the analysis.
    Session Job Initiation:
    Registers the analysis object within a session job for later commitment to the database.
    Logging DB Addition:
    Logs that the analysis object has been staged for addition to the database.
    Strategy Selection:
    Selects an analysis strategy based on the analyse_type (e.g., tree detection, road detection, etc.).
    Context and Business Logic Execution:
    Configures and executes business logic specific to the chosen analysis strategy, using a context object designed for this purpose.
    Logging Completion:
    Logs the successful completion of the deep learning scan."""

    logging.info(f"Start to execute deep learning scan of {in_raster_path}")
    project_check = ProjectCheck()
    path_check = PathCheck()
    project_check.set_next(path_check)
    project_check.check(project_id=project_id, input_file_path=in_raster_path)
    path_check.check(input_file_path=in_model_definition_path)
    path_check.check(input_file_path=in_features_path)

    analyse_object = AnalyseObjects(
        project_id=project_id,
        in_raster_path=in_raster_path,
        out_feature_class_name=out_feature_class_name,
        analyse_type=analyse_type,
        in_model_definition_path=in_model_definition_path,
        in_features_path=in_features_path
    )
    session_job(analyse_object, commit=False)
    logging.info("Analyse object added in to the DB")

    if analyse_type == "tree":
        strategy = DetectTreeObjectStrategy()
    elif analyse_type == "road":
        strategy = DetectRoadObjectsStrategy()
    elif analyse_type == "water":
        strategy = DetectWaterObjectsStrategy()
    else:
        strategy = DetectBuildObjectsStrategy()
    context = AnaliseContext(strategy=strategy)
    context.do_some_business_logic(project_id, in_features_path, analyse_object.id)
    logging.info("Deep learning scan finished successfully")


def training_deep_learning_data(project_id: str, in_raster: str, out_folder: str, type_of_data_training: str, output_dpl_folder: str, in_training: str = None):

    """Description:
    The training_deep_learning_data function is designed to facilitate the preparation and export of training data for deep learning models within a geospatial context. It checks project and file path validity, handles conditional inputs, and manages the export process tailored to specific data training types.

    Parameters:
    project_id (str): Identifier for the project under which the training data will be prepared.
    in_raster (str): File path to the raster data that will be used for generating training data.
    out_folder (str): Directory path where the exported training data will be saved.
    type_of_data_training (str): Specifies the type of training data to be generated, such as "classification", "detection", or "segmentation".
    output_dpl_folder (str): Destination path for the deep learning packages generated during the training data export.
    in_training (str, optional): Path to the input training data that might be used to refine the training process.
    Returns:
    This function does not return a value but performs significant data processing and logging activities.
    Detailed Workflow:
    Logging Start: Logs the commencement of the deep learning model training data creation process, specifying the type of data training.
    Checks Initialization:
    ProjectCheck(): Ensures that the project exists and is valid.
    PathCheck(): Verifies the accessibility and validity of the paths provided for the raster data, output folder, and optionally the input training data.
    Chain of Responsibility Setup:
    Links the project check to the path check, ensuring streamlined validation.
    Validation Execution:
    Executes the validations for the project ID and paths involved.
    Training Data Object Initialization:
    Creates an ExportTrainingDataObjects instance, configuring it with all necessary parameters, including raster path, project ID, output folder, type of data training, and optional class data.
    Session Job Initiation:
    Registers the export training data object within a session job, preparing it for database transactions but initially setting it to not commit.
    Logging Export Initiation:
    Logs the start of the training data export process.
    Training Data Export Execution:
    Calls the export_training_data function, which handles the actual data export based on the prepared settings."""

    logging.info(f"Starting to create deep learning model of {type_of_data_training}")

    project_check = ProjectCheck()
    path_check = PathCheck()
    project_check.set_next(path_check)
    project_check.check(project_id=project_id, input_file_path=in_raster)
    path_check.check(input_file_path=out_folder)
    if in_training:
        path_check.check(in_training)

    export_training_data_object = ExportTrainingDataObjects(
        in_raster=in_raster,
        project_id=project_id,
        out_folder=out_folder,
        type_of_data_training=type_of_data_training,
        in_class_data=in_training,
        image_chip_format="TIFF",
        output_dpl_folder=output_dpl_folder
    )
    session_job(export_training_data_object, commit=False)
    logging.info("Exporting training data...")
    export_training_data(export_data_id=export_training_data_object.id)


if __name__ == '__main__':

   add_project(project_name='MyProject1.gdb',
               project_path=r"D:\deep_python_arcgis\MyProject1\MyProject1.gdb")
   add_object(project_id='4badb488-f913-4077-a0b2-80e87216ced5',
              object_type="poliline",
              input_file_path=r"D:\deep_python_arcgis\MyProject1\source_files\poliline.shp",
              object_name='poliline_arcgis',
              coordinate_system=5563)
   deep_learning_scan(project_id="e47ccefe-a89c-4c1e-b1bf-7c9ae2f688a9",
                      in_raster_path=r"D:\deep_python_arcgis\MyProject1\Layout5.tif",
                      out_feature_class_name=r"D:\deep_python_arcgis\MyProject1\MyProject1.gdb\TreeTrainModel",
                      in_features_path=r"D:\deep_python_arcgis\MyProject1\source_files\poligon.shp",
                      analyse_type="road",
                      in_model_definition_path=r"D:\deep_python_arcgis\MyProject1\PythonDeepModels\RodaModels\RodaModels.dlpk")
   training_deep_learning_data( project_id="e47ccefe-a89c-4c1e-b1bf-7c9ae2f688a9",
                                in_raster=r"D:\deep_python_arcgis\MyProject1\Layout5.tif",
                                out_folder=r"D:\deep_python_arcgis\MyProject1\TrainingPythonObjects\Layout_roads_2",
                                type_of_data_training="road",
                                output_dpl_folder=r"D:\deep_python_arcgis\MyProject1\PythonDeepModels\RodaModels",
                                in_training=None)


