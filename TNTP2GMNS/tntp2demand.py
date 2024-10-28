import csv

# Read the contents of the tntp file
file_path_tntp = 'net/trips.tntp'

# Open and read the tntp file
with open(file_path_tntp, 'r') as file:
    tntp_content = file.readlines()

# Initialize a list to store OD data and a variable to sum the total volume
od_data = []
total_volume = 0  # Initialize total volume counter

# Parse the tntp file
origin_zone = None
for line in tntp_content:
    line = line.strip()

    # Detect "Origin" block
    if line.startswith("Origin"):
        origin_zone = int(line.split()[1])  # Get the origin zone

    # Parse lines with destination data
    elif origin_zone is not None and ":" in line:
        # Split each destination pair by ';'
        destinations = line.split(";")
        for destination in destinations:
            if ":" in destination:
                # Extract destination zone and volume
                d_zone_id, volume = destination.split(":")
                volume = float(volume.strip())
                
                # Only add non-zero volumes to the OD data and accumulate the total volume
                if volume > 0:
                    od_data.append([origin_zone, int(d_zone_id.strip()), volume])
                    total_volume += volume  # Accumulate total volume

# Write the parsed OD data to a new CSV file, skipping zero-value OD pairs
output_file_path = 'net/demand.csv'
with open(output_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["o_zone_id", "d_zone_id", "volume"])  # Write header
    writer.writerows(od_data)  # Write OD data

# Output the total volume
print(f"Total volume across all OD pairs: {total_volume}")
print(f"File has been successfully converted and saved to: {output_file_path}")
