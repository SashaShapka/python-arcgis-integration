import arcpy
from arc_gis_python_job.config import logging


def detect_objects_using_deep_learning(input_raster, out_detected_objects, in_model_definition, in_feature_path):
    """
    Detect objects in an input raster using a deep learning model with arcpy.

    Args:
    input_raster (str): Path to the input raster.
    model (str): Path to the deep learning model.
    output (str): Path to save the output.
    config_file (str): Path to the configuration file.
    """
    # Set local variables
    in_raster = input_raster
    out_detected_objects = out_detected_objects
    in_model_definition = in_model_definition

    # Specify the processing environment to use CPU (if supported in your environment setup)
    arcpy.env.processorType = "CPU"
    desc = arcpy.Describe(in_feature_path)
    arcpy.env.extent = desc.extent

    # Execute Detect Objects Using Deep Learning
    arcpy.ia.DetectObjectsUsingDeepLearning(
        in_raster,
        out_detected_objects,
        in_model_definition,
        run_nms=True,
        confidence_score_field="Confidence",
        class_value_field="Class",
        processing_mode="PROCESS_ITEMS_SEPARATELY"
    )
    logging.info(f"Detection completed. Results saved to: {out_detected_objects}")






