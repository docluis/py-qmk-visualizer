import tkinter


class Overlay:
	def __init__(self): 
		self.root = tkinter.Tk()
		self.frame = tkinter.Frame(self.root, width=350, height=60, bg='#26233a')
		self.text = tkinter.StringVar()
		self.textLabel = tkinter.Label(self.frame, textvariable=self.text, fg='#c4a7e7', bg='#26233a', font=('Courier', 16))
		self.textLabel.place(anchor='center', x=175, y=30)
		self.frame.pack()
		self.root.overrideredirect(True)
		self.root.geometry("350x60+1850+1390")
		self.root.lift()
		self.root.overrideredirect(True)
		self.root.wm_attributes('-alpha', '0.75')
		self.root.wm_attributes("-topmost", True)
		self.update_callback = self.update

	def update(self, text):
		if len(text) > 18:
			text = text[-18:]
		self.text.set(text)

	def run(self):
		self.text.set("")
		self.root.mainloop()
