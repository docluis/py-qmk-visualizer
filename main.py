import sys
import keyboard
from keylogger import KeyLogger
from graphics import Overlay


def main(keyboard_f, width, height):
	overlay = Overlay(width=width, height=height, keyboard=keyboard_f, x_offset=50, y_offset=50)
	logger = KeyLogger(overlay.update_callback)
	keyboard.hook(logger.key_pressed)
	overlay.run()


if __name__ == '__main__':
	main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
