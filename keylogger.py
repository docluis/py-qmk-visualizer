import time
import keyboard

REMAPS = {
	'space':' ',
	'caps lock':'<CAPS>',
	#'backspace':'\u0008'
}
ENCLOSE = ['delete', 'backspace', 'enter', 'up', 'down', 'left', 'right', 'esc', 'tab', 'home', 'end', 'page up', 'page down', 'insert']

class KeyLogger:
	def __init__(self, update_callback, keyevent_callback, layerswitch_callback, buf_len: int = 100, collapse: bool = True, collapse_threshold: int = 3, timeout: int = 2):
		super().__init__()
		self.__buf_len = buf_len
		self.__collapse = collapse
		self.__collapse_threshold = collapse_threshold
		self.__queue = []
		self.__mod_list = []
		self.__update_callback = update_callback
		self.__keyevent_callback = keyevent_callback
		self.__layerswitch_callback = layerswitch_callback
		self.__most_recent = time.time()
		self.__timeout = timeout

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
		return outstr

	def key_pressed(self, e):
		print(e.name)
		self.__keyevent_callback(e.name, e.event_type)
		if not self.__most_recent:
			self.__most_recent = time.time()
		else:
			if time.time() - self.__most_recent > self.__timeout:
				self.__queue = []
			self.__most_recent = time.time()
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
					mod_plus_name = f'<{"-".join(self.__mod_list + [name])}>'
					if mod_plus_name == '<alt-f1>':
						self.__layerswitch_callback(1)
					elif mod_plus_name == '<alt-f2>':
						self.__layerswitch_callback(2)
					elif mod_plus_name == '<alt-f3>':
						self.__layerswitch_callback(3)
					elif mod_plus_name == '<alt-f4>':
						self.__layerswitch_callback(4)
					elif mod_plus_name == '<alt-f5>':
						self.__layerswitch_callback(5)
					elif mod_plus_name == '<alt-f6>':
						self.__layerswitch_callback(6)
					elif mod_plus_name == '<alt-f7>':
						self.__layerswitch_callback(7)
					elif mod_plus_name == '<alt-f12>':
						self.__layerswitch_callback(0)
					self.enqueue(mod_plus_name)				
				else:
					self.enqueue(name)
				# print('\r' + str(self) + ' '*40, end='')
				self.__update_callback(str(self))
		elif e.event_type == keyboard.KEY_UP and e.name in self.__mod_list:
			self.__mod_list.remove(e.name)

