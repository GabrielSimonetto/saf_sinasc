import os

def count_lines_in_directory(directory_path):
    total_lines = 0

    # Traverse the directory tree
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            # Open the file and count lines
            with open(file_path, 'r', encoding='latin1') as file:
                line_count = sum(1 for line in file)
                total_lines += line_count

    return total_lines

# Usage example
directory = '/home/gabriel/tcc/code/saf_sinasc/data/raw'
line_count = count_lines_in_directory(directory)
print(f"Total lines in directory: {line_count}")
