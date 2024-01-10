import keyboard

REMAPS = {
	'space':' ',
	'caps lock':'<CAPS>'
}
ENCLOSE = ['delete', 'backspace', 'enter', 'up', 'down', 'left', 'right', 'esc', 'tab', 'home', 'end', 'page up', 'page down', 'insert']

class KeyLogger:
	def __init__(self, buf_len: int = 10, collapse: bool = True, collapse_threshold: int = 3):
		super().__init__()
		self.__buf_len = buf_len
		self.__collapse = collapse
		self.__collapse_threshold = collapse_threshold
		self.__queue = []
		self.__mod_list = []

	def enqueue(self, item):
		if not self.__queue or self.__queue[-1][0] != item:
			item = [item, 1]
			self.__queue.append(item)
		else:
			self.__queue[-1][1] += 1
		if self.size() > self.__buf_len:
			self.dequeue()

	def dequeue(self):
		return self.__queue.pop(0)

	def size(self):
		return len(self.__queue)

	def __str__(self) -> str:
		outstr = ''
		for item in self.__queue:
			if item[1] == 1:
				outstr += item[0]
			elif not self.__collapse or item[1] < self.__collapse_threshold:
				outstr += item[0]*item[1]
			else:
				outstr += f'{item[0]}x{item[1]}'
		return f'[{outstr}]'

	def key_pressed(self, e):
		if e.event_type == keyboard.KEY_DOWN:
			name = e.name
			if name in REMAPS.keys():
				name = REMAPS[name]
			elif name in ENCLOSE:
				name = f'<{name}>'
			if name in keyboard.all_modifiers:
				if name not in self.__mod_list:
					self.__mod_list.append(name)
			else:
				if self.__mod_list:
					self.enqueue(f'<{"-".join(self.__mod_list + [name])}>')
				else:
					self.enqueue(name)
				print('\r' + str(self) + ' '*40, end='')
		elif e.event_type == keyboard.KEY_UP and e.name in self.__mod_list:
			self.__mod_list.remove(e.name)
