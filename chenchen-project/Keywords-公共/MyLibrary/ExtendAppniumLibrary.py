# -*- coding:utf-8 -*-

import sys

from AppiumLibrary import *

reload(sys)
sys.setdefaultencoding('utf8')


class ExtendAppniumLibrary(AppiumLibrary):
    ROBOT_LIBRARY_SCOPE = 'Global'#在调用这个类是在全局实例化一次

    def __init__(self):
        AppiumLibrary.__init__(self, timeout=5, run_on_failure='ExtendAppniumLibrary.Capture Page Screenshot')

    def available_ime_engines(self):
        """Get the available input methods for an Android device. Package and
        activity are returned (e.g., ['com.android.inputmethod.latin/.LatinIME'])

        Android only.
        """
        driver = self._current_application()
        available_ime_engines = driver.available_ime_engines
        self._info("the available input methods is:  '%s'." % available_ime_engines)
        return available_ime_engines

    def is_ime_active(self):
        """Checks whether the device has IME service active. Returns True/False.

        Android only.
        """
        driver = self._current_application()
        is_ime_active = driver.is_ime_active()
        self._info("is the device has IME service active:  '%s'." % is_ime_active)
        return is_ime_active

    def activate_ime_engine(self, engine):
        """Activates the given IME engine on the device.

        Android only.

        :Args:
         - engine - the package and activity of the IME engine to activate (e.g.,
            'com.android.inputmethod.latin/.LatinIME')
        """
        driver = self._current_application()
        driver.activate_ime_engine(engine)
        self._info("activate the given IME engine on the device.")

    def deactivate_ime_engine(self):
        """Deactivates the currently active IME engine on the device.

        Android only.
        """
        driver = self._current_application()
        driver.deactivate_ime_engine()
        self._info("deactivate the given IME engine on the device.")

    def get_mobile_key(self):
        key = {'0': 7, '1': 8, '2': 9, '3': 10, '4': 11, '5': 12, '6': 13, '7': 14, '8': 15, '9': 16,
               'A': 29, 'B': 30, 'C': 31, 'D': 32, 'E': 33, 'F': 34, 'G': 35, 'H': 36, 'I': 37, 'J': 38,
               'K': 39, 'L': 40, 'M': 41, 'N': 42, 'O': 43, 'P': 44, 'Q': 45, 'R': 46, 'S': 47, 'T': 48,
               'U': 49, 'V': 50, 'W': 51, 'X': 52, 'Y': 53, 'Z': 54,
               'a': 29, 'b': 30, 'c': 31, 'd': 32, 'e': 33, 'f': 34, 'g': 35, 'h': 36, 'i': 37, 'j': 38,
               'k': 39, 'l': 40, 'm': 41, 'n': 42, 'o': 43, 'p': 44, 'q': 45, 'r': 46, 's': 47, 't': 48,
               'u': 49, 'v': 50, 'w': 51, 'x': 52, 'y': 53, 'z': 54,
               'META_ALT_LEFT_ON': 16,
               'META_ALT_MASK': 50,
               'META_ALT_ON': 2,
               'META_ALT_RIGHT_ON': 32,
               'META_CAPS_LOCK_ON': 1048576,
               'META_CTRL_LEFT_ON': 8192,
               'META_CTRL_MASK': 28672,
               'META_CTRL_ON': 4096,
               'META_CTRL_RIGHT_ON': 16384,
               'META_FUNCTION_ON': 8,
               'META_META_LEFT_ON': 131072,
               'META_META_MASK': 458752,
               'META_META_ON': 65536,
               'META_META_RIGHT_ON': 262144,
               'META_NUM_LOCK_ON': 2097152,
               'META_SCROLL_LOCK_ON': 4194304,
               'META_SHIFT_LEFT_ON': 64,
               'META_SHIFT_MASK': 193,
               'META_SHIFT_ON': 1,
               'META_SHIFT_RIGHT_ON': 128,
               'META_SYM_ON': 4,
               'KEYCODE_APOSTROPHE': 75,
               'KEYCODE_AT': 77,
               'KEYCODE_BACKSLASH': 73,
               'KEYCODE_COMMA': 55,
               'KEYCODE_EQUALS': 70,
               'KEYCODE_GRAVE': 68,
               'KEYCODE_LEFT_BRACKET': 71,
               'KEYCODE_MINUS': 69,
               'KEYCODE_PERIOD': 56,
               'KEYCODE_PLUS': 81,
               'KEYCODE_POUND': 18,
               'KEYCODE_RIGHT_BRACKET': 72,
               'KEYCODE_SEMICOLON': 74,
               'KEYCODE_SLASH': 76,
               'KEYCODE_STAR': 17,
               'KEYCODE_SPACE': 62,
               'KEYCODE_TAB': 61,
               'KEYCODE_ENTER': 66,
               'KEYCODE_ESCAPE': 111,
               'KEYCODE_CAPS_LOCK': 115,
               'KEYCODE_CLEAR': 28,
               'KEYCODE_PAGE_DOWN': 93,
               'KEYCODE_PAGE_UP': 92,
               'KEYCODE_SCROLL_LOCK': 116,
               'KEYCODE_MOVE_END': 123,
               'KEYCODE_MOVE_HOME': 122,
               'KEYCODE_INSERT': 124,
               'KEYCODE_SHIFT_LEFT': 59,
               'KEYCODE_SHIFT_RIGHT': 60,
               'KEYCODE_F1': 131,
               'KEYCODE_F2': 132,
               'KEYCODE_F3': 133,
               'KEYCODE_F4': 134,
               'KEYCODE_F5': 135,
               'KEYCODE_F6': 136,
               'KEYCODE_F7': 137,
               'KEYCODE_F8': 138,
               'KEYCODE_F9': 139,
               'KEYCODE_F10': 140,
               'KEYCODE_F11': 141,
               'KEYCODE_F12': 142,
               'KEYCODE_BACK': 4,
               'KEYCODE_CALL': 5,
               'KEYCODE_ENDCALL': 6,
               'KEYCODE_CAMERA': 27,
               'KEYCODE_FOCUS': 80,
               'KEYCODE_VOLUME_UP': 24,
               'KEYCODE_VOLUME_DOWN': 25,
               'KEYCODE_VOLUME_MUTE': 164,
               'KEYCODE_MENU': 82,
               'KEYCODE_HOME': 3,
               'KEYCODE_POWER': 26,
               'KEYCODE_SEARCH': 84,
               'KEYCODE_NOTIFICATION': 83,
               'KEYCODE_NUM': 78,
               'KEYCODE_SYM': 63,
               'KEYCODE_SETTINGS': 176,
               'KEYCODE_DEL': 67,
               'KEYCODE_FORWARD_DEL': 112,
               'KEYCODE_NUMPAD_0': 144,
               'KEYCODE_NUMPAD_1': 145,
               'KEYCODE_NUMPAD_2': 146,
               'KEYCODE_NUMPAD_3': 147,
               'KEYCODE_NUMPAD_4': 148,
               'KEYCODE_NUMPAD_5': 149,
               'KEYCODE_NUMPAD_6': 150,
               'KEYCODE_NUMPAD_7': 151,
               'KEYCODE_NUMPAD_8': 152,
               'KEYCODE_NUMPAD_9': 153,
               'KEYCODE_NUMPAD_ADD': 157,
               'KEYCODE_NUMPAD_COMMA': 159,
               'KEYCODE_NUMPAD_DIVIDE': 154,
               'KEYCODE_NUMPAD_DOT': 158,
               'KEYCODE_NUMPAD_EQUALS': 161,
               'KEYCODE_NUMPAD_LEFT_PAREN': 162,
               'KEYCODE_NUMPAD_MULTIPLY': 155,
               'KEYCODE_NUMPAD_RIGHT_PAREN': 163,
               'KEYCODE_NUMPAD_SUBTRACT': 156,
               'KEYCODE_NUMPAD_ENTER': 160,
               'KEYCODE_NUM_LOCK': 143,
               'KEYCODE_MEDIA_FAST_FORWARD': 90,
               'KEYCODE_MEDIA_NEXT': 87,
               'KEYCODE_MEDIA_PAUSE': 127,
               'KEYCODE_MEDIA_PLAY': 126,
               'KEYCODE_MEDIA_PLAY_PAUSE': 85,
               'KEYCODE_MEDIA_PREVIOUS': 88,
               'KEYCODE_MEDIA_RECORD': 130,
               'KEYCODE_MEDIA_REWIND': 89,
               'KEYCODE_MEDIA_STOP': 86
               }
        return key
