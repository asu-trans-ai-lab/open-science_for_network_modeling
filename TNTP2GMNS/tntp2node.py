import csv


# Define the file path
meta_file_path = 'net/meta.tntp'

# Initialize a dictionary to store the metadata values
metadata = {}

# Open and read the meta.tntp file
with open(meta_file_path, 'r') as file:
    for line in file:
        # Extract the number of zones
        if line.startswith("<NUMBER OF ZONES>"):
            metadata["number_of_zones"] = int(line.split()[-1])
        
        # Extract the number of nodes
        elif line.startswith("<NUMBER OF NODES>"):
            metadata["number_of_nodes"] = int(line.split()[-1])
        
        # Extract the first thru node
        elif line.startswith("<FIRST THRU NODE>"):
            metadata["first_thru_node"] = int(line.split()[-1])
        
        # Extract the number of links
        elif line.startswith("<NUMBER OF LINKS>"):
            metadata["number_of_links"] = int(line.split()[-1])
        
        # Stop reading when the end of metadata is reached
        elif line.startswith("<END OF METADATA>"):
            break

# Print the extracted metadata
print("Extracted Metadata:")
for key, value in metadata.items():
    print(f"{key}: {value}")



# Read the contents of the tntp file
file_path_node_tntp = 'net/node.tntp'

# Open and read the tntp file
with open(file_path_node_tntp, 'r') as file:
    node_tntp_content = file.readlines()

# Prepare an output data list
output_data = []

# Skip the header row and process the remaining rows
for line in node_tntp_content[1:]:  # Skip the header
    # Split each line using tab and extract values
    parts = line.strip().split('\t')
    if len(parts) >= 3:
        node_id = int(parts[0])
        x_coord = float(parts[1]) * (3 / 839108) - (87823395 / 974261)
        y_coord = float(parts[2]) * (2 / 739817) + (31680191 / 863933)
        zone_id = -1 
        if node_id < metadata["first_thru_node"]:
            zone_id = node_id
            
        output_data.append([node_id, zone_id, x_coord, y_coord])

# Write the data to a CSV file
output_file_path_nodes = 'net/node.csv'
with open(output_file_path_nodes, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["node_id", "zone_id", "x_coord", "y_coord"])  # Write the header
    writer.writerows(output_data)  # Write node data

print(f"File has been converted and saved to: {output_file_path_nodes}")
