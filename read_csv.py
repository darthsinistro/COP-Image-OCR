import csv

def read_csv_column(csv_file, column_name):
    values = []

    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            value = row.get(column_name)
            if value:
                values.append(value)

    return values

# Example usage
csv_file = 'drone_images.csv'  # Replace with the path to your CSV file
column_name = 'Img URL'

url_list = read_csv_column(csv_file, column_name)