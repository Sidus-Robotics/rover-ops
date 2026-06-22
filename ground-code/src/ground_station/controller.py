import pygame
import serial
import struct
import os 
import math
import multiprocessing
import asyncio
import websockets


os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"

pygame.init()
pygame.joystick.init()
ser = serial.Serial('/dev/ttyUSB0')


def main():
    ser.write(b'1.0')
    # Used to manage how fast the screen updates.
    clock = pygame.time.Clock()


    # This dict can be left as-is, since pygame will generate a
    # pygame.JOYDEVICEADDED event for every joystick connected
    # at the start of the program.
    joysticks = {}

    done = False
    while not done:
        # Event processing step.
        # Possible joystick events: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
        # JOYBUTTONUP, JOYHATMOTION, JOYDEVICEADDED, JOYDEVICEREMOVED
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True  # Flag that we are done so we exit this loop.

            if event.type == pygame.JOYBUTTONDOWN:
                print("Joystick button pressed.")
                if event.button == 0: 
                    joystick = joysticks[event.instance_id]
                    if joystick.rumble(0, 0.7, 500):
                        print(f"Rumble effect played on joystick {event.instance_id}")

            if event.type == pygame.JOYBUTTONUP:
                print("Joystick button released.")

            # Handle hotplugging
            if event.type == pygame.JOYDEVICEADDED:
                # This event will be generated when the program starts for every
                # joystick, filling up the list without needing to create them manually.
                joy = pygame.joystick.Joystick(event.device_index)
                joysticks[joy.get_instance_id()] = joy
                print(f"Joystick {joy.get_instance_id()} connencted")

            if event.type == pygame.JOYDEVICEREMOVED:
                del joysticks[event.instance_id]
                print(f"Joystick {event.instance_id} disconnected")

        # For each joystick:
        for joystick in joysticks.values():
          
            x_axis = round(joystick.get_axis(0), 1) + 0.0
            y_axis = -1 * round(joystick.get_axis(1), 1) + 0.0

            """Pack each variable into a 4 byte float.
            Totoal 8 byte payload."""
            binary_payload = struct.pack('<ff', x_axis, y_axis) 

            print(f"Mag: {math.sqrt(pow(x_axis,2) + pow(y_axis,2))}\nX: {x_axis}\nY: {y_axis}\nbin: {binary_payload}")
            ser.write(binary_payload)

            axis = joystick.get_axis(0)
            button = joystick.get_button(0)
            hat = joystick.get_hat(0)

        # Go ahead and update the screen with what we've drawn.
        pygame.event.pump()
        # Limit to 30 frames per second.
        clock.tick(60)


if __name__ == "__main__":
    main()
    ser.close
    pygame.quit()