from backend.server import Server
from backend.api.task import update_random_task

def main():
    update_random_task()
    server = Server()
    server.run(host='0.0.0.0', port=210, debug=True)

if __name__ == '__main__':
    main()