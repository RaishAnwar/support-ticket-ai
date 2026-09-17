import subprocess
import sys


def main():
    api = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "main:app",
            "--reload",
        ]
    )

    ui = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "ui.py",
        ]
    )

    try:
        api.wait()
        ui.wait()
    except KeyboardInterrupt:
        api.terminate()
        ui.terminate()


if __name__ == "__main__":
    main()