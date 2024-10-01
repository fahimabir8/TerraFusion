function getPathRow(lat, lng) {
    fetch('/convert', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            latitude: lat,
            longitude: lng
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.path && data.row) {
            console.log('Converted Path/Row:', data);
            alert("Path: " + data.path + ", Row: " + data.row);
            
            // Now call the function to check the satellite passing time
            checkSatellitePassingTime(data.path, data.row);
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
