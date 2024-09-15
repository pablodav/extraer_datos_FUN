
import os

def read_csv_files(directory):
    content = ""
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            with open(os.path.join(directory, filename), 'r') as file:
                content += file.read() + "\n"
    return content

# Replace 'your_directory_path' with the path to the directory containing your CSV files
script_path = os.path.dirname(__file__)
data_path = os.path.join(script_path, '..', 'data', "extract3/")
import pdb; pdb.set_trace()
data_content = read_csv_files(data_path)

with open("output.txt", "w") as file:
    file.write(data_content)
