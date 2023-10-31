import time
import write

def degrees_to_steps(degrees):
    return round(degrees * 100)

def move_motor(angle, motor_id):   
    try:
        write.write_to_register(0x1803, degrees_to_steps(angle), motor_id)
        write.write_to_register(0x79, 8, motor_id) #This is the START command

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    write.close_server()

   

def test_small_increments():
    angle = 0
    increment = 0.01

    write.write_to_register(0x1803, write.degrees_to_steps(angle))
    write.write_to_register(0x79, 8) #This is the START command

    time.sleep(5)

    while angle < 90:
        angle = angle + increment
        write.write_to_register(0x1803, write.degrees_to_steps(angle))
        write.write_to_register(0x79, 8) #This is the START command
        time.sleep(0.2)

def read_signal_strength():
    # Implement this function to return the signal strength as a number.
    # For now, I'll just simulate it with a random number.
    import random
    return random.random()

def scan_matrix(repetitions=10, matrix_size=10, step_size=1, start_x_angle=0, start_y_angle=90):
    """
    Moves the emitter across a matrix multiple times.

    Parameters:
    - repetitions: The number of times the matrix will be scanned.
    - matrix_size: Size of the matrix (assuming it's a square matrix).
    - step_size: The angular size for a single step.
    - start_x_angle: Starting angle for the X axis.
    - start_y_angle: Starting angle for the Y axis.
    """
    max_strength = float('-inf')  # set to negative infinity initially
    max_position = (0, 0)
    
    # Move to starting position
    move_motor(start_x_angle, 15)
    move_motor(start_y_angle, 14)
    time.sleep(2)  # Give the emitter some time to move to starting position
    
    for _ in range(repetitions):
        for y in range(matrix_size):
            for x in range(matrix_size):
                # Use starting angles to adjust movement
                if y % 2 == 0:  # Move right during even rows
                    move_motor(start_x_angle + x * step_size, 15)
                else:  # Move left during odd rows
                    move_motor(start_x_angle + (matrix_size - x - 1) * step_size, 15)
                
                # Read the signal strength
                current_strength = read_signal_strength()
                
                # Update if this is the strongest signal seen so far
                if current_strength > max_strength:
                    max_strength = current_strength
                    max_position = (x, y)
                
                time.sleep(0.1)  # Give the emitter some time to move (modify as needed)
            
            if y < matrix_size - 1:  # If not on the last row, move down
                move_motor(start_y_angle + (y + 1) * step_size, 14)
                time.sleep(0.1)  # Give the emitter some time to move (modify as needed)

    return max_strength, max_position

def refined_scan(position, step_size=1, matrix_size=10):
    """
    Performs a refined scan centered around a given position.

    Parameters:
    - position: A tuple (x, y) indicating the position to center the refined scan around.
    - step_size: The angular size for a single step.
    - matrix_size: Size of the refined matrix.
    """
    # Calculate the start angles for the refined scan.
    # The math here assumes you're scanning a matrix centered at 'position'
    start_x_angle = position[0] * step_size - (matrix_size * step_size) / 2
    start_y_angle = position[1] * step_size - (matrix_size * step_size) / 2

    # Conduct the refined scan
    max_strength, max_position = scan_matrix(matrix_size=matrix_size, step_size=step_size/10,  # finer step size
                                             start_x_angle=start_x_angle, start_y_angle=start_y_angle)
    
    # Adjust the max_position to be relative to the larger matrix
    refined_x = start_x_angle / step_size + max_position[0] / 10
    refined_y = start_y_angle / step_size + max_position[1] / 10
    
    return max_strength, (refined_x, refined_y)

# Start the scan with custom starting angles and get the results
start_x = 10  # example starting x-angle
start_y = 5   # example starting y-angle
max_strength, max_position = scan_matrix(start_x_angle=start_x, start_y_angle=start_y)

print(f"Strongest signal at position: {max_position} with strength: {max_strength}")

max_strength_refined, max_position_refined = refined_scan(max_position)

print(f"Refined strongest signal at position: {max_position_refined} with strength: {max_strength_refined}")