import csv, os

def write_csv(file_name, data):
    fieldnames = data[0].keys()
    folder_path = os.path.join(os.getcwd(), "history")
    file_path = os.path.join(folder_path, file_name )
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    

def read_csv(file_name):
    folder_path = os.path.join(os.getcwd(), "history")
    file_path = os.path.join(folder_path, file_name )
    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]

    return data
