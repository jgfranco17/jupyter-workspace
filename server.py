import argparse
import os
import subprocess
from pathlib import Path


def start_jupyter_notebook(port: int) -> None:
    """Start a Jupyter Notebook server on the specified port and IP for remote access.

    :param port: Port number to run the notebook server on.
    :param ip: IP address to bind the server to. Defaults to "0.0.0.0" for remote access.
    :param password: Password for accessing the notebook server. If None, a token is used.

    Args:
        port (int): Port number to run the notebook server on
        ip (str, optional): IP address to bind the server to, defaults to "0.0.0.0"
    """
    # Check if jupyter is installed
    try:
        subprocess.run(["jupyter", "--version"], check=True)
    except subprocess.CalledProcessError:
        print(
            "Jupyter is not installed. Please install it using 'pip install jupyter' in terminal."
        )
        return

    # Create a Jupyter config directory if it doesn"t exist
    config_dir = os.path.expanduser("~/.jupyter")
    os.makedirs(config_dir, exist_ok=True)

    # Generate a config file if one doesn"t exist
    config_file = Path(config_dir, "jupyter_notebook_config.py")
    if not config_file.exists():
        subprocess.run(["jupyter", "notebook", "--generate-config"])

    # Set a password for the Jupyter Notebook
    password = os.getenv("JUPYTER_NOTEBOOK_PASSWORD")
    if password:
        from jupyter_server.auth import passwd

        hashed_password = passwd(password)

        with open(config_file, "a") as f:
            f.write(f"\nc.NotebookApp.password = u'{hashed_password}'\n")

    # Run the Jupyter notebook server
    ip = "0.0.0.0"
    print(f"Starting Jupyter Notebook on {ip}:{port}...")
    result = subprocess.run(
        [
            "jupyter",
            "notebook",
            "--no-browser",
            f"--port={port}",
            f"--ip={ip}",
            "--allow-root",
        ]
    )
    if result.returncode!= 0:
        print(f"Jupyter Notebook server was shut down: {result.stdout.decode('utf-8')}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Start a Jupyter Notebook server on a remote machine."
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="Port to run the Jupyter Notebook server on (default: 8080)",
    )
    args = parser.parse_args()
    start_jupyter_notebook(port=args.port)
