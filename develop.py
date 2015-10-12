#!/usr/bin/env python
from project import init_app
from project.config import DevelopmentConfig

application = init_app(DevelopmentConfig)


if __name__ == "__main__":
    application.run(port=5000, host="0.0.0.0", threaded=True)
