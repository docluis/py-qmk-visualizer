import keyboard
from keylogger import KeyLogger
from graphics import Overlay


overlay = Overlay()
logger = KeyLogger(overlay.update_callback, buf_len=15)
keyboard.hook(logger.key_pressed)
overlay.run()
