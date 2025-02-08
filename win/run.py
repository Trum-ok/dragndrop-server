import os
import threading

from dotenv import load_dotenv
from server import run_server
from app import run_app

load_dotenv(override=True)


def main():
    PC_PORT = os.getenv("PC_PORT")
    if not PC_PORT:
        raise ValueError("PC_PORT isn`t set")
    server_thread = threading.Thread(target=run_server, args=(PC_PORT, False))

    server_thread.start()
    run_app()

    server_thread.join()


if __name__ == "__main__":
    main()
