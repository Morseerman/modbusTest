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

def print_ascii_matrix(current_x, current_y, matrix_size):
    for y in range(matrix_size):
        for x in range(matrix_size):
            adjusted_x = x if y % 2 == 0 else matrix_size - 1 - x

            if adjusted_x == current_x and y == current_y:
                print('X', end=' ')
            else:
                print('-', end=' ')
        print()  # New line at the end of each row


def scan_matrix(repetitions=1, matrix_size=10, step_size=0.1, center_x_angle=get_motor_angle(14), center_y_angle=get_motor_angle(15)):
   
    max_strength = float('-inf')  # set to negative infinity initially
    max_position = (0, 0)

    # Calculate the starting position, offset from the center
    start_x_angle = center_x_angle - (matrix_size / 2 * step_size)
    start_y_angle = center_y_angle - (matrix_size / 2 * step_size)
    
    # Move to the new starting position
    move_motor(start_x_angle, 14)
    move_motor(start_y_angle, 15)
    time.sleep(2)  # Give the emitter some time to move to starting position
    
    for _ in range(repetitions):
        for y in range(matrix_size):
            for x in range(matrix_size):
                print(f"X: {get_motor_angle(14)}, Y: {get_motor_angle}")
                print_ascii_matrix(x, y, matrix_size)

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
                
                time.sleep(0.1)  # Give the emitter some time to move (modify as needed)
            
            # Move Y motor down one step after completing each row
            move_motor(start_y_angle + y * step_size, 15)
            time.sleep(0.1)  # Give the emitter some time to move (modify as needed)

    print("Scan complete")
    return max_strength, max_position



if __name__ == '__main__':
    # move_motor(90, 15)
    # print(f"angle: {get_motor_angle(15)}")

    # Start the scan with custom starting angles and get the results
    # start_x = 285  # example starting x-angle
    # start_y = 93   # example starting y-angle
    max_strength, max_position = scan_matrix()
    move_motor(max_position[0], 14)
    move_motor(max_position[1], 15)

    print(f"Strongest signal at position: {max_position} with strength: {max_strength}")

    # print(get_motor_angle(15))
    pass