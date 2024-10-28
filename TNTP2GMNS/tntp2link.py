import csv

# File paths
net_file_path = 'net/net.tntp'
flow_file_path = 'net/flow.tntp'
node_file_path = 'net/node.tntp'
output_file_path = 'net/link.csv'

# Initialize list to store data extracted from net file
net_data = []

# Parse net.tntp to extract link network data
with open(net_file_path, 'r') as net_file:
    for line in net_file:
        # Skip metadata or header lines by looking for lines that start with known non-numeric indicators
        if line.startswith("~") or line.startswith("<") or line.strip() == "" or line.strip().split()[0].isdigit() is False:
            continue
        parts = line.strip().split()

        from_node_id = int(parts[0])
        to_node_id = int(parts[1])
        dir_flag = 1
        length = float(parts[3])
        lanes = 1
        capacity = float(parts[2])
        ffft = float(parts[4])
       
        free_speed = float(parts[7]) 
        
        
        if ffft == 0:  
          length = 0
          if free_speed == 0 : 
              free_speed = 60 # set default values 
        else : # with postiive value 
           free_speed = length / ffft * 60
        

        toll = float(parts[8])
        link_type = float(parts[9])
        allowed_uses = ''
        VDF_alpha = float(parts[5])
        VDF_beta = float(parts[6])
        VDF_plf = 1

        VDF_fftt = length / max(1,free_speed) *60  # FFTT's unit is min  

        # Add data to net_data list
        net_data.append([from_node_id, to_node_id, dir_flag, length, lanes, capacity, free_speed, toll, link_type, allowed_uses, VDF_alpha, VDF_beta, VDF_plf, VDF_fftt])

# Initialize dictionary to store data extracted from flow file
flow_data = {}
with open(flow_file_path, 'r') as flow_file:
    for line in flow_file:
        # Skip metadata or header lines
        if line.startswith("~") or line.startswith("<") or line.startswith("From"):
            continue
        parts = line.strip().split()
        if len(parts) >= 3:
            ref_volume = float(parts[2])
            ref_cost = float(parts[3])
            from_node_id = int(parts[0])
            to_node_id = int(parts[1])
            # Store flow data using (source_node, target_node) as the key
            flow_data[(from_node_id, to_node_id)] = ref_volume

# Initialize dictionary to store data extracted from node file
node_data = {}
with open(node_file_path, 'r') as node_file:
    for line in node_file:
        # Skip metadata or header lines
        if line.startswith("~") or line.startswith("<") or line.startswith("node"):
            continue
        parts = line.strip().split()
        if len(parts) >= 3:
            from_node_id = int(parts[0])
            x_coord = float(parts[1]) * (3 / 839108) - (87823395 / 974261)
            y_coord = float(parts[2]) * (2 / 739817) + (31680191 / 863933)
            geometry = str(x_coord) + ' ' + str(y_coord)  # Generate LINESTRING format
            # Store flow data using (source_node, target_node) as the key
            node_data[from_node_id] = geometry

# Write data to a new CSV file
with open(output_file_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write the complete header
    writer.writerow(["link_id", "from_node_id", "to_node_id", "dir_flag", "length", "lanes", "capacity", "free_speed","toll", "link_type", "allowed_uses", "VDF_alpha", "VDF_beta", "VDF_plf", "ref_volume", "ref_cost", "VDF_fftt", "geometry"])

    # Merge net data and flow data, and write to CSV
    for idx, row in enumerate(net_data):
        from_node_id, to_node_id, dir_flag, length, lanes, capacity, free_speed,toll, link_type, allowed_uses, VDF_alpha, VDF_beta, VDF_plf, VDF_fftt = row
        # Get flow data from flow_data; default to 0 if not present
        ref_volume = flow_data.get((from_node_id, to_node_id), 0)
        # Get geometry data from node_data; default to 0 if not present
        geometry1 = node_data.get(from_node_id, 0)
        geometry2 = node_data.get(to_node_id, 0)
        geometry = 'LINESTRING (' + str(geometry1) + ', ' + str(geometry2) + ')'
        # Generate link_id, starting from 1
        link_id = idx + 1
        # Write data
        writer.writerow([link_id, from_node_id, to_node_id, dir_flag, length, lanes, capacity, free_speed, toll, link_type, allowed_uses, VDF_alpha, VDF_beta, VDF_plf, ref_volume, ref_cost, VDF_fftt, geometry])

print(f"Data successfully written to {output_file_path}")
