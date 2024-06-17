import os

def print_directory_structure(directory, indent=0):
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        print('    ' * indent + '- ' + item)
        if os.path.isdir(item_path):
            print_directory_structure(item_path, indent + 1)

if __name__ == '__main__':
    base_directory = 'source_images'
    print(f'Structure of {base_directory}:')
    print_directory_structure(base_directory)
