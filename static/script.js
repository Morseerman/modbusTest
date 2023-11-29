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
            console.log(data.compass_data)
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


function fetchInclinometerData() {
    $.ajax({
        url: '/get_inclinometer_data',
        method: 'GET',
        success: function(data) {
            if (data.inclinometer_angle_data !== undefined && data.inclinometer_angle_data !== null) {
                $('#inclinometerData').text(`Inclinometer Data: ${data.inclinometer_angle_data}`);
            }
            if (data.inclinometer_air_pressure_data !== undefined && data.inclinometer_air_pressure_data !== null) {
                $('#inclinometerAirPressure').text(`Inclinometer Air Pressure: ${data.inclinometer_air_pressure_data} Pa`);
            }
        },
        error: function() {
            $('#inclinometerData').text(`Failed to fetch inclinometer data.`);
        }
    });
}
// Fetch the inclinometer data every 2 seconds
setInterval(fetchInclinometerData, 2000);

// Function to set the motor position using a POST request
$('#inclonometer0').click(function() {
    $.post('/set_0', function(data) {
       
    });
});