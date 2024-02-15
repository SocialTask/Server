from backend.server import Server
from backend.api.task import update_random_task
import backend.config

def main():
    update_random_task()
    server = Server()
    server.run(host=backend.config.HOST, port=backend.config.PORT, debug=True)

if __name__ == '__main__':
    main()