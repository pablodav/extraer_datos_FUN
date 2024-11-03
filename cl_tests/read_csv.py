
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

def write_output(file_name, data):
    """
    This function writes the content of CSV files into a single output file.

    Args:
        file_name (str): The name of the output file.
        data (str): The content of CSV files to be written in the output file.

    Returns:
        None
    """
    with open(file_name, "w") as output_file:
        output_file.write(data)

write_output("output.txt", data_content)
