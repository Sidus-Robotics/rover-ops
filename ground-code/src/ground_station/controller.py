import pygame
from pygame.event import Event
from pygame.joystick import JoystickType
from typing import Dict
import logging
import time
import serial
import struct
import os 
import math
import multiprocessing
import asyncio
import websockets
logger = logging.getLogger(__name__)

config: Dict = {
    'sync': 255,
    'x_axis': 0,
    "y_axis" :1,
}

class ControllerProcess:
    _joysticks: Dict
    _done = False
    _event: Event
    _controller: JoystickType
    _x_axis: int 
    _y_axis: int

    def __init__(self, joysticks: Dict = {}, controller = None, config: Dict = config) -> None:
        pygame.init()
        pygame.joystick.init()
        self._joysticks = joysticks
        self._controller = controller
        self._x_axis = config['x_axis']
        self._y_axis = config['y_axis']
        self._sync =  config['sync']
        self._clock = pygame.time.Clock()
    
    def set_event(self) -> None:
        event: Event = pygame.event.get()
        if event is not None:
            self._event = event
    
    def set_controller(self) -> None:
        joy = pygame.joystick.Joystick(self._event.device_index)
        self._controller = joy.get_instance_id()
    
    def get_payload(self) -> int:
        sync = 255
        x = round(self._controller.get_axis(self._x_axis),1 ) + 0.0
        y = -1 * round(self._controller.get_axis(self._y_axis), 1) + 0.0
        return sync, x, y
    
def joy():
    ground = ControllerProcess(config=config)  
    try:
        with serial.Serial(port='/dev/ttyUSB0', baudrate=115200) as usb:
            print("CONNECTED.")
            while True:
                ground.set_event()
                if ground._event == pygame.JOYDEVICEADDED:
                    ground.set_controller()
                
                if ground._controller is not None:
                    # sync = 255
                    # x_axis = round(ground._controller.get_axis(0), 1) + 0.0
                    # y_axis = -1 * round(ground._controller.get_axis(1), 1) + 0.0
                    sync, x_axis, y_axis = ground.get_payload()

                    """Pack each variable into a 4 byte float.
                    With 1 byte Sync. Total 9 byte payload."""
                    binary_payload = struct.pack('<Bff', sync, x_axis, y_axis) 

                    print(f"Mag: {math.sqrt(pow(x_axis,2) + pow(y_axis,2))}\nX: {x_axis}\nY: {y_axis}\nbin: {binary_payload}")
                    usb.write(binary_payload)

                    axis = ground._controller.get_axis(0)
                    button = ground._controller.get_button(0)
                    hat = ground._controller.get_hat(0)

                    pygame.event.pump()

                    ground._clock.tick(120)
    except Exception as e:
        pygame.quit()
        logging.warning(
            f"{e}: ATTEMPTING RECONNECT."
        )
        time.sleep(1)
        joy()

def main():
    # Used to manage how fast the screen updates.
    clock = pygame.time.Clock()


    # This dict can be left as-is, since pygame will generate a
    # pygame.JOYDEVICEADDED event for every joystick connected
    # at the start of the program.
    joysticks: Dict = {}

    done = False
    with serial.Serial(port='/dev/ttyUSB0', baudrate=115200) as usb:
        while not done:
            # Event processing step.
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
                
                sync = 255
                x_axis = round(joystick.get_axis(0), 1) + 0.0
                y_axis = -1 * round(joystick.get_axis(1), 1) + 0.0
                current_motor_speed = 0

                """Pack each variable into a 4 byte float.
                With 1 byte Sync. Total 9 byte payload."""
                binary_payload = struct.pack('<Bff', sync, x_axis, y_axis) 

                print(f"Mag: {math.sqrt(pow(x_axis,2) + pow(y_axis,2))}\nX: {x_axis}\nY: {y_axis}\nbin: {binary_payload}")
                usb.write(binary_payload)

                axis = joystick.get_axis(0)
                button = joystick.get_button(0)
                hat = joystick.get_hat(0)

            # Go ahead and update the screen with what we've drawn.
            pygame.event.pump()
            # Limit to 30 frames per second.
            clock.tick(120)


if __name__ == "__main__":
    os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"
    joy()
    pygame.quit()