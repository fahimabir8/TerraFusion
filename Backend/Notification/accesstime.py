import pandas as pd

# Load the CSV file containing satellite passing data (Path, Row, Time)
satellite_data = pd.read_csv('satellite_passing_times.csv')

def get_satellite_passing_time(path, row):
    # Filter the data to find the corresponding Path/Row entry
    result = satellite_data[(satellite_data['Path'] == path) & (satellite_data['Row'] == row)]
    
    if not result.empty:
        return result.iloc[0]['Time']  # Return the passing time
    else:
        return None

@app.route('/satellite_pass_time', methods=['POST'])
def satellite_pass_time():
    data = request.json
    path = data['path']
    row = data['row']
    
    passing_time = get_satellite_passing_time(path, row)
    
    if passing_time:
        return jsonify({'time': passing_time})
    else:
        return jsonify({'error': 'No satellite passing time found'}), 404

