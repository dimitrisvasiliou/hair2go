# build.py
import os
import subprocess

def main():
    # Install dependencies into current project (Vercel's Python path)
    subprocess.check_call(["pip", "install", "-r", "requirements.txt"])
    print("Dependencies installed.")

if __name__ == "__main__":
    main()