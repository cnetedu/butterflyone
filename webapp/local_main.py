import bfly.users.models
import bfly.job_match.models
import bfly.server
import config
import os
import tempfile


if __name__ == '__main__':
    try:
        db_file_descriptor, path = tempfile.mkstemp()
        app = bfly.server.create_app(config.LocalConfig(path), True, True)
        with app.app_context():
            bfly.users.models.create_tables()
            bfly.users.models.initialize_data()

        app.run(host='127.0.0.1', port=8080, debug=True)
    finally:
        os.close(db_file_descriptor)
        os.unlink(path)
