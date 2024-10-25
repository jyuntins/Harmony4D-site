import os

# Define the directory containing your config files and the base path
# CONFIG_DIR = '/home/rawalk/Desktop/egohumans/egohumans/configs/tagging/'
# CONFIG_DIR = '/home/rawalk/Desktop/egohumans/egohumans/configs/legoassemble/'
# CONFIG_DIR = '/home/rawalk/Desktop/egohumans/egohumans/configs/fencing/'
# CONFIG_DIR = '/home/rawalk/Desktop/egohumans/egohumans/configs/basketball/'
# CONFIG_DIR = '/home/rawalk/Desktop/egohumans/egohumans/configs/volleyball/'
# CONFIG_DIR = '/home/rawalk/Desktop/egohumans/egohumans/configs/badminton/'
CONFIG_DIR = '/home/rawalk/Desktop/egohumans/egohumans/configs/tennis/'

BASE_PATH = '/home/rawalk/Desktop/ego/'
RELATIVE_PATH = './external/'

def modify_file(file_path):
    """Modifies the paths in the config file"""
    
    with open(file_path, 'r') as file:
        content = file.read()

    # Replace the absolute path with the relative path
    content = content.replace(BASE_PATH, RELATIVE_PATH)
    
    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.write(content)

def process_all_files(directory):
    """Processes all YAML files in the provided directory"""
    
    # List all YAML files in the directory
    files = [f for f in os.listdir(directory) if f.endswith('.yaml')]

    for file in files:
        modify_file(os.path.join(directory, file))

process_all_files(CONFIG_DIR)
