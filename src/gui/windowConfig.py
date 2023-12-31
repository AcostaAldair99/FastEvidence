from dependecies import *
import os
from tkinter import Menu

def setWindow(root,title,width,height,position):

  root.title(title)
   # get the screen dimension
  screen_width = root.winfo_screenwidth()
  screen_height = root.winfo_screenheight()
  
  if position == "CENTER":
  # find the center point
    center_x = int(screen_width/2 - width / 2)
    center_y = int(screen_height/2 - height / 2)

  # set the position of the window to the center of the screen
    root.geometry(f'{width}x{height}+{center_x}+{center_y}')
  else:
    root.geometry(f'{width}x{height}+{screen_width-(width+30)}+{screen_height-(height+90)}') 
    root.attributes("-topmost",True)
  root.resizable(False,False)
  root.columnconfigure(0, weight=4)
  root.columnconfigure(1, weight=1)
  ##Check this shit someday 
  try:
    filepath = os.getcwd()+"\src\\assets\icon.ico"
    root.iconbitmap(filepath)
  except tk.TclError as e:
    print(e)
    pass

