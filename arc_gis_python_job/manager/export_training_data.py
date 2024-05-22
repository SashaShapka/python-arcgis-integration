import arcpy
from arcpy.ia import *

from arc_gis_python_job.models import ExportTrainingDataObjects
from arcgis_python_db.db import ArcGisPythonDB
from arc_gis_python_job.config import logging

db = ArcGisPythonDB()


def export_training_data(export_data_id: str):

    logging.info("Starting export training data...")

    with db.session_scope() as session:
        export_propagation = session.query(ExportTrainingDataObjects).filter_by(id=export_data_id).one()
        in_raster = export_propagation.in_raster
        out_folder = export_propagation.out_folder
        in_training = export_propagation.in_class_data
        image_chip_format = export_propagation.image_chip_format
        output_dpl_folder = export_propagation.output_dpl_folder
        metadata_format = "RCNN_Masks"
        buffer_radius = None
        if export_propagation.type_of_data_training == "road":
            buffer_radius = 1

        ExportTrainingDataForDeepLearning(in_raster=in_raster, out_folder=out_folder, in_class_data=in_training,
                                          image_chip_format=image_chip_format, metadata_format=metadata_format,
                                          buffer_radius=buffer_radius)

        arcpy.env.processorType = "CPU"

        TrainDeepLearningModel(in_folder=out_folder, out_folder=output_dpl_folder, model_type="MASKRCNN")


