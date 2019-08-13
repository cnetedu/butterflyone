import bfly.server
import config
import os


if os.environ.get('GAE_INSTANCE'):
    app = bfly.server.create_app(config.AppEngineConfig)
else:
    app = bfly.server.create_app(config.DirectConfig)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
