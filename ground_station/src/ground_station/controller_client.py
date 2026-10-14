import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"

# from multiprocessing import Process, Queue
import logging
import math
import platform
import struct
import time
from queue import Queue
from threading import Thread

import pygame
from pygame.event import Event
from pygame.joystick import JoystickType
from serial import Serial
from websockets.exceptions import ConnectionClosed
from websockets.sync.client import ClientConnection, connect

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

operating_sys = platform.system().lower()
if operating_sys == "linux" or operating_sys == "windows" or operating_sys == "darwin":
    config: dict = {
        "sync": 255,
        "x_axis": 0,
        "y_axis": 1,
        "port": "/dev/ttyUSB0",
        "baud": 115200,
    }


class ControllerProcess(Thread):
    _joysticks: dict
    _done = False
    _events: list[Event]
    _controller: JoystickType
    _controller_event: Event
    _controller_x_axis: int
    _controller_y_axis: int
    _sync: int
    _payload: bytes
    _x: int
    _y: int
    _serial_bus: Serial

    _out_queue: Queue

    _testing: bool

    def __init__(
        self,
        joysticks: dict = {},
        controller=None,
        config: dict = config,
        testing: bool = False,
        queue: Queue = None,
    ) -> None:
        super().__init__()
        pygame.init()
        if not pygame.joystick.get_init:
            pygame.joystick.init()

        if testing:
            self._serial_bus = Serial(port=config["port"], baudrate=config["baud"])
        else:
            self._serial_bus = None

        self._joysticks = joysticks
        self._controller = controller
        self._controller_event = None
        self._controller_x_axis = config["x_axis"]
        self._controller_y_axis = config["y_axis"]
        self._sync = config["sync"]
        self._out_queue = queue
        self._testing = testing

        self._clock = pygame.time.Clock()

    def __del__(self):
        if self._testing:
            self._serial_bus.close()

        if self._out_queue.full():
            self._out_queue.task_done()

        pygame.quit()
        return False

    """Pivate methods used by this class."""

    def _find_events(self) -> None:
        events: list[Event] = pygame.event.get()
        self._events = events

    def _get_controller(self) -> None:
        for event in self._events:
            if event.type == pygame.JOYDEVICEADDED:
                self._controller_event = event
                logger.info(f"Got Controller: {self._controller_event}")

    def _set_controller(self) -> None:
        """Gets the device index and saves it in a dict."""
        joy = pygame.joystick.Joystick(self._controller_event.device_index)
        self._joysticks[joy.get_instance_id()] = joy
        self._controller = self._joysticks[joy.get_instance_id()]
        logger.info(f"Set Controller: {self._controller}")

    def _get_payload(self) -> int:
        """Pack each variable into a 4 byte float.
        With 1 byte Sync. Total 9 byte payload."""
        dead_zone = 0.20
        x = round(self._controller.get_axis(self._controller_x_axis), 2) + 0.0
        y = -1 * round(self._controller.get_axis(self._controller_y_axis), 2) + 0.0

        if abs(x) < dead_zone:
            x = 0
        if abs(y) < dead_zone:
            y = 0

        self._x = x
        self._y = y
        self._payload = struct.pack("<Bff", self._sync, self._x, self._y)

        # if self._testing:
        logger.info(
            f"Mag: {math.sqrt(pow(self._x, 2) + pow(self._y, 2))}\nX: {self._x}\nY: {self._y}\nbin: {self._payload}"
        )

    def _send_payload(self):
        """Writes the packet to the bus."""
        if self._testing:
            self._serial_bus.write(self._payload)
        else:
            self._out_queue.put(self._payload)

    def _time_step(self):
        pygame.event.pump()
        self._clock.tick(120)

    """Public methods to be used outside."""

    def run(self):
        """Runs in an loop. Overrides BaseProcess run()."""
        try:
            while True:
                self._find_events()

                if self._controller == None:
                    logger.debug("CONTROLLER NEEDS CONNECT.")
                    self._get_controller()
                    self._set_controller()

                if self._controller != None:
                    self._get_payload()
                    self._send_payload()
                self._time_step()

        except Exception:
            self.__del__()
            time.sleep(1)
            self.run()


class WebsocketProcess(Thread):
    _in_queue: Queue
    _uri: str
    _websocket: ClientConnection

    def __init__(self, queue: Queue):
        super().__init__()
        self._uri = "ws://127.0.0.1:8000/controller-node"
        self._in_queue = queue
        self._websocket = None

    def __del__(self):
        if self._in_queue.full():
            self._in_queue.task_done()
        self._websocket.close()
        pygame.quit()

        return False

    def _connect(self):
        self._websocket = connect(self._uri)

    def run(self):
        while True:
            try:
                if self._websocket == None:
                    self._connect()

                msg: bytes = self._in_queue.get()
                self._websocket.send(msg)
            except ConnectionRefusedError:
                logging.warning("ATTEMPTING RECONNECT.")
                # self._connect()
                # time.sleep(1)
                # self.run()
                time.sleep(1)
            except ConnectionClosed:
                logging.warning("CONNECTION CLOSED: ATTEMPTING RECONNECT.")
                self._connect()
                time.sleep(1)
            except KeyboardInterrupt:
                self.__del__()
                self._websocket.close()
                time.sleep(1)


def test_joy(queue: Queue):
    ground = ControllerProcess(config=config, queue=queue, testing=True)
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
        ground.__del__()
        logging.warning(f"{e}: ATTEMPTING RECONNECT.")
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
    # test_joy(controller_queue)
