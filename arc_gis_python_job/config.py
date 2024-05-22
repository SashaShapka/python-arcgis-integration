import logging
logging = logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


DB_NAME = "arcgis_python_int"
# TEST_DB_NAME = "passport_office_test"
USER = "arcgissysadmin"
# TEST_USER = "test_sysadmin"
PASSWORD = "arcgispython"
HOST = "127.0.0.1"
PORT = "5432"

DB_SCRIPT = f'D:/arcgis_python_integration/arc_gis_python_db/create_db.sh'
# TEST_DB_SCRIPT = f'/home/{os.getenv("USER")}/passport_office/Passport_Office/passport_db/test_db.sh'
DROP_DB_SCRIPT = f'D:/arcgis_python_integration/arc_gis_python_db/drop_db.sh'
# DROP_TEST_DB_SCRIPT = f'/home/{os.getenv("USER")}/passport_office/Passport_Office/passport_db/test_db_drop.sh'