from dependecies import *

class captureWindow():
    

    def __init__(self,root,evidence,dirEvidence,filename,testDescription):
      self.evidence = evidence
      self.evidence.createDocument()
      self.dirEvidence = dirEvidence.get()
      self.filename = filename.get()
      self.testDescription = testDescription.get()
      self.secondary_window = tk.Toplevel(root)
      self.root = root
      setWindow(self.secondary_window,"Capture",370,70,"BOTTOM-LEFT")
      self.secondary_window.protocol("WM_DELETE_WINDOW",lambda:self.checkCloseOption())
      self.root.iconify()
      
      self.captureWindowFrame= tk.Frame(self.secondary_window,padx=10,pady=5)
      self.captureWindowFrame.grid(column=0,row=1)
      self.titleFrame = ttk.Frame(self.secondary_window)
      ttk.Label(self.titleFrame, text='Step #',anchor='w').grid(column=0, row=0,sticky='w') 
      self.stepsText = tk.StringVar()
      self.stepsText.set("1")
      ttk.Label(self.titleFrame, textvariable=self.stepsText,anchor='w').grid(column=1, row=0,sticky='w') 
      self.titleFrame.grid(column=0,row=0,pady=1)

      self.frame = ttk.Frame(self.captureWindowFrame) 
      self.frame.columnconfigure(0, weight=1,pad=1)
      self.frame.columnconfigure(1, weight=1,pad=1)
      self.frame.grid(column=0,row=0)

      ttk.Label(self.frame, text='Description:',anchor='w').grid(column=0, row=0,sticky='w',pady=5) 
      self.descriptionText= tk.StringVar() 
      self.description= ttk.Entry(self.frame, width=30,textvariable=self.descriptionText)
      self.description.grid(column=1, row=0,pady=5,sticky='w')

      self.buttonCapture= ttk.Button(
        self.frame,
        cursor="hand2",
        text="O",
        width=5,
        command=lambda:self.addStep()
      )
      self.buttonCapture.grid(column=2,row=0,padx=5)

      self.buttonCancel= ttk.Button(
        self.frame,
        cursor="hand2",
        text="X",
        width=5,
        command=lambda:self.checkCloseOption()
      )
      self.buttonCancel.grid(column=3,row=0,padx=5)
    def toString(self):
       print("dir: "+ self.dirEvidence)
       print("file: "+self.filename)
       print("descript: "+self.testDescription)


    def addStep(self):
      self.evidence.addPicture("Step # "+self.stepsText.get()+": "+self.descriptionText.get())
      self.descriptionText.set(" ") 
      current = int(self.stepsText.get())
      new_step = current + 1
      self.stepsText.set(str(new_step))

    def disableEvent(self):
       pass
    

    def closeCaptureWindow(self):
       self.secondary_window.destroy()
    
    def checkCloseOption(self):
      result = messagebox.askquestion("Stop Capture","¿Are you sure to stop de evidence capture?")
      if result == "yes":
        self.root.deiconify()
        self.closeCaptureWindow()

