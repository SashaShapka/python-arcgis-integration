from urllib.parse import quote_plus as urlquote
import arc_gis_python_job.config


class Singleton(type):
    """
    Singleton meta class.
    :see: http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def get_connection_string(db_name):
    host = "127.0.0.1"
    port = "5432"
    user = arc_gis_python_job.config.USER
    password = arc_gis_python_job.config.PASSWORD
    return f"postgresql://{urlquote(user)}:{urlquote(password)}@{urlquote(host)}:{urlquote(port)}/{urlquote(db_name)}"