import os 
import sys

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"

import pygame
from pygame.event import Event
from pygame.joystick import JoystickType
from typing import Dict, List
import logging
import time
from serial import Serial
import struct
import math
import platform

from multiprocessing import Process, Queue
import itertools
import json

from websockets.sync.client import ClientConnection, connect
# from websockets.exceptions import ConnectionClosedOK, ConnectionClosed

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

operating_sys = platform.system().lower()
if operating_sys == 'linux':
    config: Dict = {
        'sync': 255,
        'x_axis': 0,
        'y_axis' :1,
        'port': '/dev/ttyUSB0',
        'baud': 115200,
    }
elif operating_sys == 'windows':
    pass
elif operating_sys == 'darwin':
    pass

class ControllerProcess(Process):
    _joysticks: Dict
    _done = False
    _events: List[Event]
    _controller: JoystickType
    _controller_event: Event
    _controller_x_axis: int 
    _controller_y_axis: int
    _sync: int
    _binary_payload: bytes
    _x: int
    _y: int
    _serial_bus: Serial

    _out_queue : Queue

    _testing: bool

    def __init__(self, joysticks: Dict = {}, 
                 controller = None, config: Dict = config, 
                 testing: str = False,
                 queue: Queue = None) -> None:
        super().__init__()
        if not pygame.joystick.get_init:
            pygame.joystick.init()
        
        if testing:
            self._serial_bus = Serial(port=config['port'], baudrate=config['baud'])

        self._joysticks = joysticks
        self._controller = controller
        self._controller_event = None
        self._controller_x_axis = config['x_axis']
        self._controller_y_axis = config['y_axis']
        self._sync =  config['sync']
        self._out_queue = queue
        self._testing = testing

        self._clock = pygame.time.Clock()
        pygame.init()
    
    def __exit__(self, exc_type, exc, tb):
        self._serial_bus.close()
        pygame.quit()
        sys.exit()
        return False
    
    """Pivate methods used by this class."""
    def _find_events(self) -> None:
        events: List[Event] = pygame.event.get()
        self._events = events
    
    def _get_controller(self) -> None:
        for event in self._events:
            if event.type == pygame.JOYDEVICEADDED:
                self._controller_event = event
                logger.info(f"Got Controller: {self._controller_event}")

    def _set_controller(self) -> None:
        """Gets the device index and saves it in a dict."""
        joy = pygame.joystick.Joystick(
            self._controller_event.device_index
            )
        self._joysticks[joy.get_instance_id()] = joy
        self._controller = self._joysticks[joy.get_instance_id()]
        logger.info(f"Set Controller: {self._controller}")
        
    def _get_payload(self) -> int:
        """Pack each variable into a 4 byte float.
            With 1 byte Sync. Total 9 byte payload."""
        dead_zone = 0.15
        x = round(self._controller.get_axis(self._controller_x_axis), 2) + 0.0
        y = -1 * round(self._controller.get_axis(self._controller_y_axis), 2) + 0.0

        if abs(x) < dead_zone:
            x = 0
        if abs(y) < dead_zone:
            y = 0
        
        self._x = x
        self._y = y
        self._binary_payload = struct.pack('<Bff', self._sync, self._x, self._y)

        if self._testing:
            logger.info(f"Mag: {math.sqrt(pow(self._x,2) + pow(self._y,2))}\nX: {self._x}\nY: {self._y}\nbin: {self._binary_payload}")
    
    def _send_payload(self):
        """Writes the packet to the bus."""
        if self._testing:
            self._serial_bus.write(self._binary_payload)
        else:
            self._out_queue.put(self._binary_payload)
        


    def _time_step(self):
        pygame.event.pump()
        self._clock.tick(120)

    """Public methods to be used outside."""
    def run(self):
        """Runs in an loop. Overies BaseProcess run()."""
        try:
            while True:
                self._find_events()

                if self._controller == None:
                    self._get_controller()
                    self._set_controller()

                if self._controller != None:
                    self._get_payload()
                    self._send_payload()
                self._time_step()

        except Exception as e:
            self.__exit__()
            logging.warning(
                f"{e}: ATTEMPTING RECONNECT."
            )
            time.sleep(1)
            self.run()

class WebsocketProcess(Process):
    _in_queue: Queue
    def __init__(self, queue: Queue):
        super().__init__()
        self._uri = 'ws://127.0.0.1:8000/controller-node'  
        self._in_queue = queue
    
    def test(self):
        print("Test")

    def run(self):
        with connect(self._uri) as websocket:
            while True:
                try:
                    msg = self._in_queue.get()
                    print(msg)
                    websocket.send(msg)
                except Exception as e:
                    print(e)

def test_joy():
    ground = ControllerProcess(config=config)  
    try:
        while True:
            ground._find_events()

            if ground._controller == None:
                ground._get_controller()
                ground._set_controller()

            if ground._controller != None:
                ground._get_payload()
                ground._send_payload()

            ground._time_step()
    except Exception as e:
        ground.__exit__
        logging.warning(
            f"{e}: ATTEMPTING RECONNECT."
        )
        time.sleep(1)
        test_joy()

if __name__ == "__main__":
     

    controller_queue = Queue()

    controller_worker = ControllerProcess(config=config, queue=controller_queue)
    web_client_worker = WebsocketProcess(queue=controller_queue) 
 
    
    controller_worker.start()
    web_client_worker.start()

    controller_worker.join()
    web_client_worker.join()