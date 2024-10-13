import os
import subprocess


def analyze_code(directory):  # type: ignore
    # List Python files in the directory
    python_files = [file for file in os.listdir(directory) if file.endswith(".py")]
    if not python_files:
        print("No Python files found in the specified directory.")
        return

    # Analyze each Python file using pylint and flake8
    for file in python_files:
        print(f"Analyzing file: {file}")
        file_path = os.path.join(directory, file)

        # Run pylint
        print("\nRunning pylint...")
        pylint_command = f"pylint {file_path}"
        subprocess.run(pylint_command, shell=True)

        # Run flake8
        print("\nRunning flake8...")
        flake8_command = f"flake8 {file_path}"
        subprocess.run(flake8_command, shell=True)

        # Run ruff
        print("\nRunning ruff...")
        ruff_command = f"ruff check {file_path}"
        subprocess.run(ruff_command, shell=True)

        # Run isort
        print("\nRunning isort...")
        isort_command = f"isort --profile black --diff {file_path}"
        subprocess.run(isort_command, shell=True)

        # Run mypy
        print("\nRunning mypy...")
        mypy_command = f"mypy {file_path}"
        subprocess.run(mypy_command, shell=True)

        # Run bandit
        print("\nRunning bandit...")
        bandit_command = f"bandit -r {file_path}"
        subprocess.run(bandit_command, shell=True)

        
analyze_code("/Users/frankserrao/MyStuff/TestAndPlay/Click2Mail/c2m-generative-ai-marketing-portal/assets/layers/factory_module/python")
