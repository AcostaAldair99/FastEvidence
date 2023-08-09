from dependecies import *
jsonFilepath = os.getcwd()+"\src\config\settings.json"

class testDataWindow():

    def __init__(self,root):
      self.secondary_window = tk.Toplevel(root)
      setWindow(self.secondary_window,"Test Cycle Information",300,235,"CENTER")
      self.secondary_window.grab_set()

      self.settingsContainerFrame= tk.Frame(self.secondary_window,padx=10,pady=5)
      self.settingsContainerFrame.grid(column=0,row=1)

      self.titleFrame = ttk.Frame(self.secondary_window)
      ttk.Label(self.titleFrame, text='Add the information about the test execution').grid(column=0, row=0) 
      self.titleFrame.grid(column=0,row=0,pady=3)

      self.frame = ttk.Frame(self.settingsContainerFrame) 
      self.frame.columnconfigure(0, weight=1,pad=10)
      self.frame.columnconfigure(1, weight=3,pad=10)
      self.frame.grid(column=0,row=1)


      ttk.Label(self.settingsContainerFrame, text='dRequest:',anchor='w').grid(column=0, row=1,sticky='w',pady=5) 
      self.dRequestText = tk.StringVar()
      self.dRequest= ttk.Entry(self.settingsContainerFrame, width=30,textvariable=self.dRequestText)
      self.dRequest.grid(column=1, row=1,pady=10)
      self.dRequest.focus()

      ttk.Label(self.settingsContainerFrame, text='Request:',anchor='w').grid(column=0, row=2,sticky='w',pady=10) 
      self.requestText = tk.StringVar() 
      self.request= ttk.Entry(self.settingsContainerFrame, width=30,textvariable=self.requestText)
      self.request.grid(column=1, row=2,pady=10)

      ttk.Label(self.settingsContainerFrame, text='Tester:',anchor='w').grid(column=0, row=3,sticky='w',pady=10) 
      self.testerText = tk.StringVar()
      tester= ttk.Entry(self.settingsContainerFrame, width=30,textvariable=self.testerText)
      tester.grid(column=1, row=3,pady=10)

      ttk.Label(self.settingsContainerFrame, text='Defect:',anchor='w').grid(column=0, row=4,sticky='w',pady=10) 
      self.defectText= tk.StringVar() 
      self.defect= ttk.Entry(self.settingsContainerFrame, width=30,textvariable=self.defectText)
      self.defect.grid(column=1, row=4,pady=10,sticky='w')

      self.showSettings()

      buttonAccept= ttk.Button(
        self.settingsContainerFrame,
        text="Accept",
        cursor="hand2",
        command=lambda:self.saveTestSettings()
      )
      buttonAccept.grid(column=1,row=5,pady=10)

      buttonCancel= ttk.Button(
        self.settingsContainerFrame,
        cursor="hand2",
        text="Cancel",
        command=self.secondary_window.destroy
    )
      buttonCancel.grid(column=0,row=5,pady=10)

    def saveTestSettings(self):
      try:
        with open(jsonFilepath,'r') as f:
          config = json.load(f)
          config['dRequest'] = self.dRequestText.get()
          config['Request'] = self.requestText.get()
          config['Tester'] = self.testerText.get()
          config['Defect'] = self.defectText.get() 
        with open(jsonFilepath,'w') as fi:
          json.dump(config,fi,indent=4)
          self.secondary_window.destroy()
          boxmessage.showinfo("Saved Settings","The settings of the test are saved successfully")

      except FileNotFoundError as e:
        config = {}
        boxmessage.showerror(e) 

    def showSettings(self):
        try:
          with open(jsonFilepath,'r') as f:
            config = json.load(f)
            self.dRequestText.set(config['dRequest'])
            self.requestText.set(config['Request'])
            self.testerText.set(config['Tester'])
            self.defectText.set(config['Defect'])
        except FileNotFoundError as e:
            config={}
            print(e)
