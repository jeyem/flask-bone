import os


class MainConfig:
    """
    Project Main config
    """

    SECRET_KEY = 'this must change'
    MEDIA = "%s/project/media/temp/" % os.path.abspath(os.curdir)
    TEMPLATES = MEDIA + "Templates/"
    STATICS = MEDIA + "Statics/"

    # Registering Blueprints
    APPS_LIST = ()

    SESSION_COOKIE_NAME = 'project'
    LOGGER_NAME = 'bfl'
    LOG_PATH = 'log/'  # '/var/log/project/'
    DEBUG_LOG = LOG_PATH + "debug.log"
    ERROR_LOG = LOG_PATH + "error.log"
    LOG_FORMAT = '\033[1;35m[%(asctime)s]\033[1;m [\033[1;31m %(levelname)s \033[1;m] \033[1;32m[%(logger_name)s]\033[1;m: \
        \033[1;33m %(message)s \033[1;m'



class DeploymentConfig(MainConfig):

    """
    Deployment mode config
    """

    DEBUG = False

class DevelopmentConfig(MainConfig):

    """
    Development mode config
    """

    DEBUG = True
