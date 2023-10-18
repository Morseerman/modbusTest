function fetchPosition() {
    $.ajax({
        url: '/get_position',
        method: 'GET',
        success: function(data) {
            if (data.motor_14_position !== undefined && data.motor_14_position !== null) {
                $('#positionMotor14').text(`Motor 14 Position: ${data.motor_14_position}`);
            }
            if (data.motor_15_position !== undefined && data.motor_15_position !== null) {
                $('#positionMotor15').text(`Motor 15 Position: ${data.motor_15_position}`);
            }
        }
    });
}

// Fetch the position every 2 seconds
setInterval(fetchPosition, 2000);

// Function to set the motor position using a POST request
$('#setAngleButton').click(function() {
    const angle = $('#angleInput').val();
    const motorId = $('#motorSelect').val();
    
    $.post('/set_position', { position: angle, motor_id: motorId }, function(data) {
        if (data.status === 'success') {
            alert(data.message);
            fetchPosition();
        } else {
            alert(`Error: ${data.message}`);
        }
    });
});

function fetchCompassData() {
    $.ajax({
        url: '/get_compass_data',
        method: 'GET',
        success: function(data) {
            if (data.compass_data !== undefined && data.compass_data !== null) {
                $('#compassData').text(`Compass Data: ${data.compass_data}`);
            }
        },
        error: function() {
            $('#compassData').text(`Failed to fetch compass data.`);
        }
    });
}

// Fetch the compass data every 2 seconds
setInterval(fetchCompassData, 2000);


// Fetch the compass data every 2 seconds
setInterval(fetchCompassData, 500);
