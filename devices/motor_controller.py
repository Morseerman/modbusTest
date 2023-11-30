import math
import time
import write
import read
from VoltMeter import volt_meter


def degrees_to_steps(degrees):
    return round(degrees * 200)

def steps_to_degrees(degrees):
    return degrees / 200

def get_motor_angle(motor_id):
    return steps_to_degrees(read.read_motor_position(motor_id))

# soft limit currently 327.67
def move_motor(angle, motor_id):  
    max_number_for_register = 327.67 
    try:
        
        upper_register_value = math.floor(angle / max_number_for_register)
        lower_register_value = degrees_to_steps(angle % max_number_for_register)
        write.write_to_register(0x1802, upper_register_value, motor_id)
        write.write_to_register(0x1803, lower_register_value, motor_id)

        
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

def print_ascii_matrix(current_x, current_y, matrix_size, scan_mode):
    for y in range(matrix_size):
        for x in range(matrix_size):
            # Adjust position based on the scanning mode
            if scan_mode == 'y':
                adjusted_y = y if x % 2 == 0 else matrix_size - 1 - y
                is_current_position = x == current_x and adjusted_y == current_y
            elif scan_mode == 'x':
                adjusted_x = x if y % 2 == 0 else matrix_size - 1 - x
                is_current_position = adjusted_x == current_x and y == current_y

            if is_current_position:
                print('X', end=' ')
            else:
                print('-', end=' ')
        print()  # New line at the end of each row


def scan_matrix_rows(repetitions=1, matrix_size=10, step_size=0.1, center_x_angle=get_motor_angle(14), center_y_angle=get_motor_angle(15)):
   
    max_strength = float('-inf')  # set to negative infinity initially
    max_position = (0, 0)
    max_x = None
    max_y = None

    # Calculate the starting position, offset from the center
    start_x_angle = center_x_angle - (matrix_size / 2 * step_size)
    start_y_angle = center_y_angle - (matrix_size / 2 * step_size)
    
    print(f"X: {get_motor_angle(14)}, Y: {get_motor_angle(15)}")

    # Move to the new starting position
    move_motor(start_x_angle, 14)
    move_motor(start_y_angle, 15)
    time.sleep(5)  # Give the emitter some time to move to starting position
    
    for _ in range(repetitions):
        for y in range(matrix_size):
            for x in range(matrix_size):
                print(f"X: {get_motor_angle(14)}, Y: {get_motor_angle(15)}")
                print_ascii_matrix(x, y, matrix_size, 'x')

                time.sleep(1)
                # Read the signal strength
                current_strength = volt_meter.get_voltage_once()

                # Adjust motor movements based on row (Y) and column (X)
                if y % 2 == 0:  # Move right during even rows
                    move_motor(start_x_angle + x * step_size, 14)
                else:  # Move left during odd rows
                    move_motor(start_x_angle + (matrix_size - x - 1) * step_size, 14)
            
                # Update if this is the strongest signal seen so far
                if current_strength > max_strength:
                    max_strength = current_strength
                    max_position = (get_motor_angle(14), get_motor_angle(15))
                    max_x = x
                    max_y = y
                
                time.sleep(0.1)  # Give the emitter some time to move (modify as needed)
            
            # Move Y motor down one step after completing each row
            move_motor(start_y_angle + y * step_size, 15)

    print("Scan complete")

    if max_strength < 0.1:
        print("No signal Found")
        return None
    else:
        print(f"Strongest signal at position: {max_position} with strength: {max_strength}")
        print_ascii_matrix(max_x, max_y, matrix_size, 'x')
        return max_position

def scan_matrix_columns(repetitions=1, matrix_size=10, step_size=0.1, center_x_angle=get_motor_angle(14), center_y_angle=get_motor_angle(15)):
   
    max_strength = float('-inf')  # set to negative infinity initially
    max_position = (0, 0)
    max_x = None
    max_y = None

    # Calculate the starting position, offset from the center
    start_x_angle = center_x_angle - (matrix_size / 2 * step_size)
    start_y_angle = center_y_angle - (matrix_size / 2 * step_size)
    
    print(f"X: {get_motor_angle(14)}, Y: {get_motor_angle(15)}")

    # Move to the new starting position
    move_motor(start_x_angle, 14)
    move_motor(start_y_angle, 15)
    time.sleep(5)  # Give the emitter some time to move to starting position
    
    for _ in range(repetitions):
        for x in range(matrix_size):
            for y in range(matrix_size):
                print(f"X: {get_motor_angle(14)}, Y: {get_motor_angle(15)}")
                print_ascii_matrix(x, y, matrix_size, 'y')

                time.sleep(0.2)
                # Read the signal strength
                current_strength = volt_meter.get_voltage_once()

                # Adjust motor movements based on column (X) and row (Y)
                if x % 2 == 0:  # Move down during even columns
                    move_motor(start_y_angle + y * step_size, 15)
                else:  # Move up during odd columns
                    move_motor(start_y_angle + (matrix_size - y - 1) * step_size, 15)
            
                # Update if this is the strongest signal seen so far
                if current_strength > max_strength:
                    max_strength = current_strength
                    max_position = (get_motor_angle(14), get_motor_angle(15))
                    max_x = x
                    max_y = y
                
            
            # Move X motor to the side one step after completing each column
            move_motor(start_x_angle + x * step_size, 14)
            time.sleep(0.1)  # Give the emitter some time to move (modify as needed)

    print("Scan complete")

    if max_strength < 0.1:
        print("No signal Found")
        return None
    else:
        print(f"Strongest signal at position: {max_position} with strength: {max_strength}")
        print_ascii_matrix(max_x, max_y, matrix_size, 'y')
        return max_position


if __name__ == '__main__':
    move_motor(360, 15)
    print(get_motor_angle(15))

    # Start the scan with custom starting angles and get the results
    # max_position = scan_matrix_columns(step_size=0.01)
    # move_motor(max_position[0], 14)
    # move_motor(max_position[1], 15)

    # print(get_motor_angle(15))
    pass