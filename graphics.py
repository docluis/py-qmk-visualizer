import tkinter


class Overlay:
	def __init__(self, width: int = 400, anchor_x: int = 1800, anchor_y: int = 1390): 
		self.root = tkinter.Tk()
		self.width = width
		self.collapsed_height = 60
		self.expanded_height = 300
		self.anchor_x = anchor_x
		self.anchor_y = anchor_y
		self.set_root_geometry(self.width, self.collapsed_height, self.anchor_x, self.anchor_y)
		self.setup_keylog()
		self.setup_keyboard()
		self.root.overrideredirect(True)
		self.root.lift()
		self.root.overrideredirect(True)
		self.root.wm_attributes('-alpha', '0.75')
		self.root.wm_attributes("-topmost", True)
		self.root.configure(background='#26233a')
		self.update_callback = self.update
		self.expanded = False

	def set_root_geometry(self, width, height, x, y):
		self.root.geometry(f"{width}x{height}+{x}+{y}")

	def setup_keylog(self):	
		self.log_frame = tkinter.Frame(self.root, width=self.width, height=self.collapsed_height, bg='#26233a')
		self.log_text = tkinter.StringVar()
		self.log_text_label = tkinter.Label(self.log_frame, textvariable=self.log_text, fg='#c4a7e7', bg='#26233a', font=('Courier', 16))
		self.log_text_label.place(anchor='w', x=5, y=int(self.collapsed_height/2)+5)
		self.expand_button_text = tkinter.StringVar()
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

	def expand_callback(self):
		if self.expanded:
			self.expand_button_text.set('^')
			self.expanded = False
			self.set_root_geometry(self.width, self.collapsed_height, self.anchor_x, self.anchor_y)
			self.log_frame.place(anchor='sw', y=self.collapsed_height)
			self.keyboard_frame.pack_forget()
		else:
			self.expand_button_text.set('v')
			self.expanded = True
			self.log_frame.pack_forget()
			self.set_root_geometry(self.width, self.expanded_height, self.anchor_x, self.anchor_y - (self.expanded_height - self.collapsed_height))
			self.keyboard_frame.pack(fill=tkinter.BOTH)
			self.log_frame.pack(fill=tkinter.BOTH)

	def update(self, text):
		if len(text) > 17:
			text = text[-17:]
		self.log_text.set(text)

	def run(self):
		self.log_text.set("")
		self.expand_button_text.set('^')
		self.root.mainloop()
