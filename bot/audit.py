## Disclaimer - This code was written by ChatGPT

import os
import re
import shutil

# Step 1: Read packages from requirements.txt
def read_requirements(file_path):
    with open(file_path, 'r') as f:
        packages = [line.strip() for line in f if line.strip()]
    return packages

# Step 2: Collect all Python files in the project directory
def collect_python_files(directory):
    python_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files

# Step 3: Extract imported modules from a Python file
def extract_imports(file_path):
    imports = set()
    with open(file_path, 'r') as f:
        for line in f:
            # Handle 'import module'
            match = re.match(r'^import\s+(\S+)', line)
            if match:
                imports.add(match.group(1).split('.')[0])
            # Handle 'from module import ...'
            match = re.match(r'^from\s+(\S+)\s+import', line)
            if match:
                imports.add(match.group(1).split('.')[0])
    return imports

# Step 4: Find unused packages
def find_unused_packages(requirements_file, project_directory):
    required_packages = read_requirements(requirements_file)
    python_files = collect_python_files(project_directory)
    
    used_packages = set()
    for file in python_files:
        used_packages.update(extract_imports(file))
    
    unused_packages = {pkg.split('==')[0] for pkg in required_packages} - used_packages
    return unused_packages

# Step 5: Remove unneeded packages from requirements.txt
def remove_unused_packages(requirements_file, unused_packages):
    backup_file = requirements_file + '.backup'
    shutil.copyfile(requirements_file, backup_file)
    
    with open(requirements_file, 'r') as f:
        lines = f.readlines()
    
    with open(requirements_file, 'w') as f:
        for line in lines:
            package = line.strip().split('==')[0]
            if package not in unused_packages:
                f.write(line)
    
    print(f"Unused packages removed. Backup saved as {backup_file}")

# Run the analysis and clean up
requirements_file = 'requirements.txt'
project_directory = '.'

unused_packages = find_unused_packages(requirements_file, project_directory)

if unused_packages:
    print("Unused packages:")
    for package in unused_packages:
        print(package)
    remove_unused_packages(requirements_file, unused_packages)
else:
    print("No unused packages found.")
