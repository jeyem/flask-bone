from project import init_app
from project.config import DeploymentConfig


application = init_app(DeploymentConfig, 'starter')
