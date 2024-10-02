def process_satellite_data(data, user_path, user_row):
    if data is None:
        return None

    lines = data.splitlines()
    for line in lines:
        # Assuming the columns are separated by commas
        parts = line.split(',')
        if len(parts) < 3:
            continue
        
        # Parse Path, Row, and Time from the line
        path = parts[0].strip()
        row = parts[1].strip()
        time_of_pass = parts[2].strip()

        # Check if path and row match
        if path == str(user_path) and row == str(user_row):
            return time_of_pass
    return None

# Example: User's path and row (You will need to set this dynamically based on your conversion)
user_path = 137
user_row = 43

# Process Landsat 8 and 9 data
landsat8_time = process_satellite_data(landsat8_data, user_path, user_row)
landsat9_time = process_satellite_data(landsat9_data, user_path, user_row)

print(f"Landsat 8 time: {landsat8_time}")
print(f"Landsat 9 time: {landsat9_time}")
