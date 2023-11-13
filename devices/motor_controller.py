import time
import write
import read
from VoltMeter import volt_meter


def degrees_to_steps(degrees):
    return round(degrees * 200)

def steps_to_degrees(degrees):
    return round(degrees / 200)

def get_motor_angle(motor_id):
    return steps_to_degrees(read.read_motor_position(motor_id))

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


def scan_matrix(repetitions=1, matrix_size=10, step_size=0.1, start_x_angle=read.read_motor_position(14)/100, start_y_angle=read.read_motor_position(15)/100):
   
    max_strength = float('-inf')  # set to negative infinity initially
    max_position = (0, 0)
    
    # Move to starting position
    move_motor(start_x_angle, 14)
    move_motor(start_y_angle, 15)
    time.sleep(2)  # Give the emitter some time to move to starting position
    
    for _ in range(repetitions):
        for y in range(matrix_size):
            for x in range(matrix_size):
                time.sleep(1.5)
                # Read the signal strength
                current_strength = volt_meter.get_voltage_once()

                # Use starting angles to adjust movement
                if y % 2 == 0:  # Move right during even rows
                    move_motor(start_x_angle + x * step_size, 14)
                else:  # Move left during odd rows
                    move_motor(start_x_angle + (matrix_size - x - 1) * step_size, 14)
            
                
                # Update if this is the strongest signal seen so far
                if current_strength > max_strength:
                    max_strength = current_strength
                    max_position = (read.read_motor_position(14), read.read_motor_position(15))
                
                time.sleep(0.1)  # Give the emitter some time to move (modify as needed)
            
            if y < matrix_size - 1:  # If not on the last row, move down
                move_motor(start_y_angle + (y + 1) * step_size, 15)
                time.sleep(0.1)  # Give the emitter some time to move (modify as needed)

    print("Scan complete")
    return max_strength, max_position

def refined_scan(position, start_x_angle=0, start_y_angle=90, step_size=1, matrix_size=10):
    """
    Performs a refined scan centered around a given position.

    Parameters:
    - position: A tuple (x, y) indicating the position to center the refined scan around (in terms of matrix indices).
    - original_start_angles: A tuple (x, y) indicating the starting angles of the original scan.
    - step_size: The angular size for a single step.
    - matrix_size: Size of the refined matrix.
    """
    # Calculate the start angles for the refined scan.
    start_x_angle = start_x_angle + position[0] * step_size
    start_y_angle = start_y_angle + position[1] * step_size

    # Conduct the refined scan
    max_strength, max_position = scan_matrix(matrix_size=matrix_size, step_size=step_size/10,  # finer step size
                                             start_x_angle=start_x_angle, start_y_angle=start_y_angle)
    
    # Adjust the max_position to be relative to the original matrix
    # refined_x = start_x_angle / step_size + max_position[0] / 10
    # refined_y = start_y_angle / step_size + max_position[1] / 10
    refined_position_x = position[0] + max_position[0] / 10
    refined_position_y = position[1] + max_position[1] / 10
    
    return max_strength, (refined_position_x, refined_position_y)


if __name__ == '__main__':
    move_motor(90, 15)
    print(f"angle: {get_motor_angle(15)}")

    # Start the scan with custom starting angles and get the results
    # start_x = 285  # example starting x-angle
    # start_y = 93   # example starting y-angle
    # max_strength, max_position = scan_matrix()
    # move_motor(max_position[0]/100, 14)
    # move_motor(max_position[1]/100, 15)

    # print(f"Strongest signal at position: {max_position} with strength: {max_strength}")

    # max_strength_refined, max_position_refined = refined_scan(max_position, start_x_angle=start_x, start_y_angle=start_y)

    # print(f"Refined strongest signal at position: {max_position_refined} with strength: {max_strength_refined}")
