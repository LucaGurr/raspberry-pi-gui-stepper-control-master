import sys
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

# Initialize the MotorHATs
kit1 = MotorKit(address=0x60)
kit2 = MotorKit(address=0x61)

# Mapping of motors to the MotorHATs
motors = {
    0: kit1.stepper1,
    1: kit1.stepper2,
    2: kit2.stepper1,
    3: kit2.stepper2
}

# Function to rotate the motor
def rotate_motor(motor_id, direction, degrees):
    steps_per_revolution = 200
    steps = int((degrees / 360) * steps_per_revolution)

    motor = motors.get(motor_id)
    if not motor:
        print(f"Motor {motor_id} does not exist.")
        return

    if direction == "cw":
        for _ in range(steps):
            motor.onestep(direction=stepper.FORWARD)
    elif direction == "ccw":
        for _ in range(steps):
            motor.onestep(direction=stepper.BACKWARD)
    else:
        print(f"Invalid direction: {direction}")

# Function to handle serial commands
def handle_serial_command(command):
    parts = command.split()
    if len(parts) != 4:
        print("Usage: <motor_id> <command> <direction> <degrees>")
        return

    motor_id = int(parts[0].replace("motor", ""))
    command = parts[1]
    direction = parts[2]
    degrees = int(parts[3])

    if command == "rotate":
        rotate_motor(motor_id, direction, degrees)
    else:
        print(f"Invalid command: {command}")