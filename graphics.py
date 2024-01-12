import tkinter
import qmk

class Overlay:
	def __init__(self, width: int = 400, height: int = 300, x_offset: int = 0, y_offset: int = 0, keyboard=None, key_size=None): 
		self.root = tkinter.Tk()

		self.width = width
		self.collapsed_height = 60
		self.expanded_height = height
		self.anchor_x = self.root.winfo_screenwidth()-width-x_offset
		self.anchor_y = self.root.winfo_screenheight()-self.collapsed_height-x_offset
		self.keyboard = keyboard
		self.key_size = key_size

		self.update_callback = self.update
		self.char_lim = int(self.width // 20)

		self.expanded = False
		if self.keyboard:
			self.char_lim -= 3
			self.keyboard = qmk.Keyboard(self.keyboard)
		self.layer = tkinter.IntVar()
		self.layer_buttons = []
		self.setup_keyboard()
		self.setup_keylog()

		self.set_root_geometry(self.width, self.collapsed_height, self.anchor_x, self.anchor_y)
		self.root.overrideredirect(True)
		self.root.lift()
		self.root.overrideredirect(True)
		self.root.wm_attributes('-alpha', '0.75')
		self.root.wm_attributes("-topmost", True)
		self.root.configure(background='#26233a', border=2)
		

	def set_root_geometry(self, width, height, x, y):
		self.root.geometry(f"{width}x{height}+{x}+{y}")

	def setup_keylog(self):	
		self.log_frame = tkinter.Frame(self.root, width=self.width, height=self.collapsed_height, bg='#26233a')
		self.log_text = tkinter.StringVar()
		self.log_text_label = tkinter.Label(self.log_frame, textvariable=self.log_text, fg='#c4a7e7', bg='#26233a', font=('Courier', 16))
		self.log_text_label.place(anchor='w', x=10, y=int(self.collapsed_height/2)+5)
		if self.keyboard:
			self.expand_button_text = tkinter.StringVar()
			self.expand_button_text.set('^')
			self.expand_button = tkinter.Button(self.log_frame, 
												textvariable=self.expand_button_text, 
												command=self.expand_callback, 
												fg='#9ccfd8', 
												bg='#26233a',
												borderwidth=0,
												relief='raised',
												activeforeground='#f6c177',
												activebackground='#eb6f92')
			self.expand_button.place(anchor='w', x=self.width-50, y=int(self.collapsed_height/2))
		self.log_frame.pack(fill=tkinter.BOTH)

	def setup_keyboard(self):
		self.keyboard_frame = tkinter.Frame(self.root, width=self.width, height=self.expanded_height-self.collapsed_height, bg='#26233a')
		if not self.keyboard:
			return

		if len(self.keyboard.keymaps) > 1:
			self.layer_buttons = []
			button_frame = tkinter.Frame(self.keyboard_frame, bg='#26233a')
			for i in range(len(self.keyboard.keymaps)):
				b = tkinter.Radiobutton(button_frame, 
										text=f'{i}', 
										value=i, 
										variable=self.layer,	
										indicatoron=False, 
										width=3,
										fg='#9ccfd8',	
										bg='#26233a',
										borderwidth=0,
										relief='raised',
										activeforeground='#f6c177',
										activebackground='#eb6f92',
										highlightcolor='#191724',
										highlightbackground='#c4a7e7',
										selectcolor='#524f67',
										command=self.change_layer)
				b.grid(row=0, column=i, padx=5)
				self.layer_buttons.append(b)
			self.layer_buttons[0].select()
			
			self.key_vars = []
			keyboard_width = self.width * 0.9
			keyboard_height = self.expanded_height * 0.9
			if not self.key_size:
				key_size = min(keyboard_width/self.keyboard.max_x, keyboard_height/self.keyboard.max_y)
			else:
				key_size = self.key_size
			keyboard_width = key_size * self.keyboard.max_x
			keyboard_height = key_size * self.keyboard.max_y

			old_height = self.expanded_height
			old_width = self.width

			self.expanded_height = int(keyboard_height) + 150
			self.width = int(keyboard_width) + 50

			self.anchor_x += old_width - self.width
			self.keyboard_frame.configure(height=self.expanded_height-self.collapsed_height)
			button_frame.place(anchor='center', x=self.width / 2, y=self.expanded_height-(self.collapsed_height)-20)

			keyboard_xpad = (self.width - keyboard_width)/2
			keyboard_ypad = (self.expanded_height-100-keyboard_height)/2
			self.layout_frame = tkinter.Frame(self.keyboard_frame, width=keyboard_width, height=keyboard_height, bg='#26233a')
			self.layout_frame.place(anchor='nw', x=keyboard_xpad, y=keyboard_ypad)
			key_reduction = 2
			for i, key in enumerate(self.keyboard.keys):
				key_frame = tkinter.Frame(self.layout_frame, width=key.width*key_size-key_reduction, height=key.height*key_size-key_reduction, bg='#403d52') 
				key_var = tkinter.StringVar()
				key_var.set(self.keyboard.keymaps[0][i])
				key_lab = tkinter.Label(key_frame, textvariable=key_var, font=('Courier', 8), fg='#e0def4', bg='#403d52')
				key_lab.place(anchor='center', x=(key.width*key_size-key_reduction)/2, y=(key.height*key_size-key_reduction)/2)
				self.key_vars.append(key_var)
				key_frame.place(anchor='center', x=key.x*key_size+key.width*key_size/2, y=key.y*key_size+key.height*key_size/2)

	def change_layer(self):
		for label, key in zip(self.key_vars, self.keyboard.keymaps[self.layer.get()]):
			label.set(key)
	
	def expand_callback(self):
		if not self.expanded and self.keyboard:
			self.expand_button_text.set('v')
			self.expanded = True
			self.log_frame.pack_forget()
			self.set_root_geometry(self.width, self.expanded_height, self.anchor_x, self.anchor_y - (self.expanded_height-self.collapsed_height))
			self.keyboard_frame.pack(fill=tkinter.BOTH)
			self.log_frame.pack(fill=tkinter.BOTH)
		else:
			self.expand_button_text.set('^')
			self.expanded = False
			self.set_root_geometry(self.width, self.collapsed_height, self.anchor_x, self.anchor_y)
			self.log_frame.place(anchor='sw', y=self.collapsed_height)
			self.keyboard_frame.pack_forget()

	def update(self, text):
		if len(text) > self.char_lim:
			text = text[-self.char_lim:]
		self.log_text.set(text)

	def run(self):
		self.log_text.set("")
		self.root.mainloop()
