import json
import os

KEYBOARD_DIR = './keyboards/'
LAYOUT_DIR = './layouts/'

keyboard2qmk={
	'space':'KC_SPC',
	'backspace':'KC_BSPC',
	'shift':'KC_LSFT',
	'alt':'KC_ALT',
	'ctrl':'KC_LCTL',
	'delete':'KC_DEL',
}

KC = {
	'SPC': '˽',
	'BSPC': '←',
	'LSFT': '⇧',
	'SFT': '⇧',
	'LCTL': 'CTRL',
	'COMM': '<\n,',
	'DOT': '>\n.',
	'SCLN': ':\n;',
	'PSLS': '/',
	'GRV': '~\n`',
	'AT': '@',
	'HASH': '#',
	'DLR': '$',
	'PERC': '%',
	'CIRC': '^',
	'AMPR': '&',
	'ASTR': '*',
	'ENT': '↵',
	'LBRC': '{\n[',
	'RBRC': '}\n]',
	'BSLS': '|\n\\',
	'QUOT': '"\n\'',
	'QUES': '?\n/',
	'EQL': '+\n=',
	'MINS': '_\n-',
	'EXLM': '!',
	'LPRN': '(',
	'RPRN': ')',
	'PPLS': '+',
	'PEQL': '=',
	'PMNS': '-',
	'PAST': '*',
	'P1': '1',
	'P2': '2',
	'P3': '3',
	'P4':'4',
	'P5':'5',
	'P6':'6',
	'P7':'7',
	'P8':'8',
	'P9':'9',
	'P0':'0',
	'BRID':'🔅',
	'BRIU':'🔆',
	'MSTP': '□',
	'MPLY':'▷',
	'MNXT':'⭲',
	'MPRV':'⭰',
	'VOLU':'🔊',
	'VOLD':'🔉',
	'MUTE':'🔇',
	'UP':'⮝',
	'DOWN':'⮟',
	'LEFT':'⮜',
	'RGHT':'⮞',
	'WBAK':'⮨',
	'WFWD':'⮩',
	'WREF':'⭮',
	# translate to layer below
	'TRNS':'',
	'NO':"🔴",
}

for key, value in KC.items():
	if '\n' in value:
		parts = value.split('\n')
		keyboard2qmk[parts[0]] = key
		keyboard2qmk[parts[1]] = key
	if value in '0123456789':
		keyboard2qmk[value] = key


class Key:
	def __init__(self, x, y, width=1, height=1):
		self.x = x
		self.y = y
		self.width = width
		self.height = height

	def __str__(self):
		return f'(x: {self.x}, y: {self.y}): {self.width}x{self.height}'

class KeymapEntry:
	def __init__(self, key, display):
		self.key = key
		self.display = key if display == None else display

	def __str__(self):
		return f'{self.display}'

class Keyboard:
	def __init__(self, keyboard_file = ''):
		self.keys = []
		self.keymaps = []
		self.max_x = 0
		self.max_y = 0
		
		self.__keyboard_file = keyboard_file
		self.__setup()

	def __setup(self):
		if not os.path.isfile(self.__keyboard_file):
			local_file = os.path.join(KEYBOARD_DIR, self.__keyboard_file, 'info.json')
			if not os.path.isfile(local_file):
				raise FileExistsError(f'couldn\'t find keyboard file {self.__keyboard_file} or local file {local_file}')
			self.__keyboard_file = local_file

		keyboard_data = None
		try:
			keyboard_data = json.load(open(self.__keyboard_file, 'r'))
		except:
			raise TypeError(f'couldn\'t parse {self.__keyboard_file} as json')

		self.name = keyboard_data['keyboard']
		self.__set_layout(keyboard_data['layout'])
		unprocessed_keymaps = [keymap for keymap in keyboard_data["layers"]]
		for i, keymap in enumerate(unprocessed_keymaps):
			assert len(keymap) == len(self.keys), f'layer {i+1} with {len(keymap)} keys does not match number of keys in layout ({len(self.keys)})'
		self.__process_keymaps(unprocessed_keymaps)

	def __process_keymaps(self, unprocessed_keymaps):
		for unprocessed in unprocessed_keymaps:
			processed = []
			for key in unprocessed:
				display = None
				# layer switching key like LT(6,KC_I)
				if key.startswith('LT('):
					layer = key.split(',')[0][3:]
					# print(f'layer: {layer}')
					main_key = key.split(',')[1].split(')')[0]
					main_key = self.process_key(main_key)
					display = f'{main_key}\n(🔵{layer})'
					# print(f"key: {key}, display: {display}, main_key: {main_key}")
					# print(f'key: {key}')
					processed.append(KeymapEntry(main_key, display))
				elif key.startswith('LT'):
					# alternative custom keys like LT1_S
					layer = key[2]
					main_key = key[4:]
					display = f'{main_key}\n(🔵{layer})'
					processed.append(KeymapEntry(main_key, display))
				elif key.startswith(("LSFT_T", "LCTL_T", "LALT_T", "LGUI_T", "RSFT_T", "RCTL_T", "RALT_T", "RGUI_T")):
					mode = key[1:4]
					main_key = key.split('(')[1].split(')')[0]
					main_key = self.process_key(main_key)
					display = f'{main_key}\n({mode})'
					processed.append(KeymapEntry(main_key, display))
				else:
					processed.append(KeymapEntry(self.process_key(key), display))
			self.keymaps.append(processed)
			# print(f'processed: {processed}')

	def process_key(self, key):
		if key.startswith('KC_'):
			key = key[3:]
			if key in KC.keys():
				return KC[key]
			else:
				return key
		elif key.startswith('LT('):
			# LT(5,KC_R) make this to R (5)
			# LT(7,KC_SPC) make this to KC[key] (7)
			layer = key.split(',')[0][3:]
			key = key.split(',')[1].split(')')[0]
			if key.startswith('KC_'):
				key = key[3:]
				if key in KC.keys():
					key = KC[key]
			return f'{key}\n({layer})'
		elif key.startswith(("LSFT_T", "LCTL_T", "LALT_T", "RSFT_T", "RCTL_T", "RALT_T")):
			# LALT_T(KC_C) make this to C (ALT)
			mode = key[:4]
			key = key.split('(')[1].split(')')[0]
			if key.startswith('KC_'):
				key = key[3:]
				if key in KC.keys():
					key = KC[key]
			return f'{key}\n({mode})'

		elif '(' in key and ')' in key:
			parts = key.split('(')
			wrapper = parts[0]
			inner = parts[1].split(')')[0]
			if inner.startswith('KC_'):
				inner = inner[3:]
				if inner in KC.keys():
					inner = KC[inner]
			return f'{wrapper}\n{inner}'
		else:
			return key

	def __set_layout(self, layout_file):
		if not os.path.isfile(layout_file):
			local_file = layout_file.split('LAYOUT_')[1]
			local_file = os.path.join(LAYOUT_DIR, local_file, 'info.json')
			if not os.path.isfile(local_file):
				raise FileExistsError(f'couldn\'t find layout file {layout_file} or local file {local_file}')
			layout_file = local_file

		layout_data = {}
		try:
			layout_data = json.load(open(layout_file, 'r'))
		except:
			raise TypeError(f'couldn\'t parse {layout_file} as json')
		
		for key in layout_data['layouts'][list(layout_data['layouts'].keys())[0]]['layout']:
			x = key['x']
			y = key['y']
			h = 1
			w = 1
			if 'h' in key.keys():
				h = key['h']
			if 'w' in key.keys():
				w = key['w']
			if x+w > self.max_x:
				self.max_x = x+w
			if y+h > self.max_y:
				self.max_y = y+h
			self.keys.append(Key(x,y,w,h))

	def __str__(self):
		return f'{self.name}:\n{",".join([str(key) for key in self.keys])}'


if __name__ == '__main__':
	test_keyboard = Keyboard('./test/split_3x5_2.json')
	print(test_keyboard)
