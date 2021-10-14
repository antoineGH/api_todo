# import logging
from __init__ import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
    # gunicorn_logger = logging.getLogger('gunicorn.error')
    # app.logger.handlers = gunicorn_logger.handlers
    # app.logger.setLevel(gunicorn_logger.level)

