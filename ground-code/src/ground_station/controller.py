import pygame
from pygame.event import Event
from pygame.joystick import JoystickType
from typing import Dict, List
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
    _events: List[Event]
    _controller: JoystickType
    _x_axis: int 
    _y_axis: int

    def __init__(self, joysticks: Dict = {}, controller = None, config: Dict = config) -> None:
        if not pygame.joystick.get_init:
            pygame.joystick.init()

        self._joysticks = joysticks
        self._controller = controller
        self._x_axis = config['x_axis']
        self._y_axis = config['y_axis']
        self._sync =  config['sync']
        self._clock = pygame.time.Clock()
        pygame.init()
    
    def __exit__(self, exc_type, exc, tb):
        pygame.quit()
        return False
    
    def set_events(self) -> None:
        events: List[Event] = pygame.event.get()
        self._events = events
    
    def set_controller(self, event: Event) -> None:
        joy = pygame.joystick.Joystick(event.device_index)
        self._joysticks[joy.get_instance_id()] = joy
        self._controller = self._joysticks[joy.get_instance_id()]
        
    def get_payload(self) -> int:
        dead_zone = 0.15
        sync = 255
        x = round(self._controller.get_axis(self._x_axis),1 ) + 0.0
        y = -1 * round(self._controller.get_axis(self._y_axis), 1) + 0.0

        if abs(x) < dead_zone:
            x = 0
        if abs(y) < dead_zone:
            y = 0
        return sync, x, y
    
def joy():
    ground = ControllerProcess(config=config)  
    try:
        with serial.Serial(port='/dev/ttyUSB0', baudrate=115200) as usb:
            while True:
                ground.set_events()
                for event in ground._events:
                    if event.type == pygame.JOYDEVICEADDED:
                        ground.set_controller(event)

                if ground._controller is not None:
                    sync, x_axis, y_axis = ground.get_payload()
                    
                    """Pack each variable into a 4 byte float.
                    With 1 byte Sync. Total 9 byte payload."""
                    binary_payload = struct.pack('<Bff', sync, x_axis, y_axis) 

                    logger.info(f"Mag: {math.sqrt(pow(x_axis,2) + pow(y_axis,2))}\n \
                                X: {x_axis}\n \
                                Y: {y_axis}\nbin: {binary_payload}")
                    usb.write(binary_payload)

                pygame.event.pump()

                ground._clock.tick(120)
    except Exception as e:
        pygame.quit()
        logging.warning(
            f"{e}: ATTEMPTING RECONNECT."
        )
        time.sleep(1)
        joy()


if __name__ == "__main__":
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"
    joy()
    pygame.quit()