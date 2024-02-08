import subprocess

def execute_backend():
    try:
        subprocess.run(["python", "-m", "backend"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing backend: {e}")

if __name__ == "__main__":
    execute_backend()