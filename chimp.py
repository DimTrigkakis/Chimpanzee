# Event Workshop
import pythoncom
import pyHook
from threading import Thread, Lock

# Automation Workshop
import pymouse
import pyscreenshot
import pyautogui


class Chimp:

    __coded_mouse_actions = {}
    __coded_keyboard_actions = {}

    # For events, Chimp exposes only the function --reset_dictionaries--,
    # so that the user may redefine the functions mapped to certain events

    # The proper function call for a mapped event
    @staticmethod
    def custom(event=None):
        print "CUSTOM event:", event

    def __show(self, o):
        if self.debug:
            print(o)

    @staticmethod
    def __init_all_names():

        Chimp.__coded_mouse_actions['mouse_left_press'] = 513
        Chimp.__coded_mouse_actions['mouse_left_release'] = 514
        Chimp.__coded_mouse_actions['mouse_right_press'] = 516
        Chimp.__coded_mouse_actions['mouse_right_release'] = 517
        Chimp.__coded_mouse_actions['mouse_left_move'] = 512
        Chimp.__coded_mouse_actions['mouse_middle_press'] = 519
        Chimp.__coded_mouse_actions['mouse_middle_release'] = 520
        Chimp.__coded_mouse_actions['mouse_scroll'] = 522

        for i in range(26):
            key = ord('a') + i
            Chimp.__coded_keyboard_actions[str(chr(key))+"_press"] = (256, chr(key))

        for i in range(26):
            key = ord('a') + i
            Chimp.__coded_keyboard_actions[str(chr(key))+"_release"] = (257, chr(key))

        for i in range(26):
            key = ord('A') + i
            Chimp.__coded_keyboard_actions[str(chr(key))+"_press"] = (256, chr(key))

        for i in range(26):
            key = ord('A') + i
            Chimp.__coded_keyboard_actions[str(chr(key))+"_release"] = (257, chr(key))

    @staticmethod
    def get_all_names():
        Chimp.__init_all_names()
        return Chimp.__coded_mouse_actions, Chimp.__coded_keyboard_actions

    def __init__(self, event=False, dict_mouse={}, dict_keyboard={}):

        Chimp.__init_all_names()

        self.debug = False
        self.event = event

        # Mappings, defined as a dictionary between events and function calls
        self.tied_mouse_types = {}
        self.tied_keyboard_types = {}
        self.lock_hooks = Lock()

        # Main Core for Testing

        self.__custom_event_handler_init(dict_mouse=dict_mouse, dict_keyboard=dict_keyboard)
        self.reset_dictionaries(dict_mouse=dict_mouse, dict_keyboard=dict_keyboard)

        # self.grab_image()
        # self.grab_mouse_position()
        # self.move_mouse((512, 512))

    def __valid_keyboard_key(self, key):

        if key in self.tied_keyboard_types and self.tied_keyboard_types[key] is not None:
            return self.tied_keyboard_types[key]

        return None

    def __valid_mouse_key(self, key):

        if key in self.tied_mouse_types and self.tied_mouse_types[key] is not None:
            return self.tied_mouse_types[key]

        return None

    def __mouse_event(self, event):

        for iter_key in Chimp.__coded_mouse_actions:
            if event.Message == Chimp.__coded_mouse_actions[iter_key]:
                key = self.__valid_mouse_key(iter_key)
                if key is not None:
                    if self.event:
                        key(event=event)
                    else:
                        key()

        return True

    def __keyboard_event(self, event):

        for iter_key in Chimp.__coded_keyboard_actions:
            if event.Message == Chimp.__coded_keyboard_actions[iter_key][0]:
                if chr(event.Ascii) == Chimp.__coded_keyboard_actions[iter_key][1]:
                    key = self.__valid_keyboard_key(iter_key)
                    if key is not None:
                        if self.event:
                            key(event=event)
                        else:
                            key()

        return True

    def __custom_mouse_event_handler_asynchronous(self):

        self.__show("Custom Mouse Event Handler Initialized")
        hm = pyHook.HookManager()
        hm.MouseAll = self.__mouse_event
        hm.HookMouse()
        pythoncom.PumpMessages()

    def __custom_keyboard_event_handler_asynchronous(self):

        self.__show("Custom Keyboard Event Handler Initialized")
        hm = pyHook.HookManager()
        hm.KeyAll = self.__keyboard_event
        hm.HookKeyboard()
        pythoncom.PumpMessages()

    def __custom_event_handler_init(self, dict_mouse={}, dict_keyboard={}):

        self.lock_hooks.acquire()

        try:
            self.tied_mouse_types = {}
            self.tied_keyboard_types = {}

            for key in dict_mouse:
                if key not in self.__coded_mouse_actions:
                    self.__show("Invalid mouse action in suggested mapping")
                else:
                    self.tied_mouse_types[key] = dict_mouse[key]

            for key in dict_keyboard:
                if key not in self.__coded_keyboard_actions:
                    self.show("Invalid keyboard action in suggested mapping")
                else:
                    self.tied_keyboard_types[key] = dict_keyboard[key]

            thread = Thread(target=self.__custom_mouse_event_handler_asynchronous)
            thread.start()
            thread = Thread(target=self.__custom_keyboard_event_handler_asynchronous)
            thread.start()

        finally:
            self.lock_hooks.release()

        return

    def reset_dictionaries(self, dict_mouse, dict_keyboard):

        self.lock_hooks.acquire()

        try:
            self.tied_mouse_types = {}
            self.tied_keyboard_types = {}

            for key in dict_mouse:
                if key not in self.__coded_mouse_actions:
                    self.__show("Invalid mouse action in suggested mapping")
                else:
                    self.tied_mouse_types[key] = dict_mouse[key]

            for key in dict_keyboard:
                if key not in self.__coded_keyboard_actions:
                    self.__show("Invalid keyboard action in suggested mapping")
                else:
                    self.tied_keyboard_types[key] = dict_keyboard[key]

        finally:
            self.lock_hooks.release()

    @staticmethod
    def grab_image(bbox=(0, 0, 1920, 1080)):

        im = pyscreenshot.grab(bbox=bbox)

        return im

    @staticmethod
    def grab_mouse_position():

        mouse = pymouse.PyMouse()

        return mouse.position()

    @staticmethod
    def move_mouse(position):

        pyautogui.moveTo(position[0], position[1], duration=0.25)

        return


def construct_event_listener(event=True, dict_mouse={}, dict_keyboard={}):
    return Chimp(event=event, dict_mouse=dict_mouse, dict_keyboard=dict_keyboard)

# Signed ~ Bradley
