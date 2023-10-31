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

def scan_matrix(repetitions=10, matrix_size=10, step_size=1):
    """
    Moves the emitter across a matrix multiple times.

    Parameters:
    - repetitions: The number of times the matrix will be scanned.
    - matrix_size: Size of the matrix (assuming it's a square matrix).
    - step_size: The angular size for a single step.
    """
    max_strength = float('-inf')  # set to negative infinity initially
    max_position = (0, 0)
    
    for _ in range(repetitions):
        for y in range(matrix_size):
            for x in range(matrix_size):
                if y % 2 == 0:  # Move right during even rows
                    move_motor(x * step_size, 15)
                else:  # Move left during odd rows
                    move_motor((matrix_size - x - 1) * step_size, 15)
                
                # Read the signal strength
                current_strength = read_signal_strength()
                
                # Update if this is the strongest signal seen so far
                if current_strength > max_strength:
                    max_strength = current_strength
                    max_position = (x, y)
                
                time.sleep(0.1)  # Give the emitter some time to move (modify as needed)
            
            if y < matrix_size - 1:  # If not on the last row, move down
                move_motor((y + 1) * step_size, 14)
                time.sleep(0.1)  # Give the emitter some time to move (modify as needed)

    return max_strength, max_position

# Start the scan and get the results
max_strength, max_position = scan_matrix()

print(f"Strongest signal at position: {max_position} with strength: {max_strength}")
