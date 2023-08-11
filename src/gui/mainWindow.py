from dependecies import *

jsonFilepath = os.getcwd()+"\src\config\settings.json"

class mainWindow():

  def __init__(self,root):
    self.root = root
    self.evidence = ""
    self.weStart = False
    setWindow(self.root,"Fast Evidence",400,180,"CENTER")
    self.file = Menu(self.menuBar,tearoff = 0)
    self.menuBar.add_cascade(label ='File', menu = self.file)
    self.file.add_command(label ='New Evidence', command = None)
    self.file.add_command(label ='Generate', command = lambda:self.generateEvidence())
    self.file.add_command(label ='Reset',command=lambda:self.resetEvidence())
    self.file.add_separator()
    self.file.add_command(label ='Exit', command = lambda:self.askCloseProgram())
    self.file.config(cursor="hand2")

    self.settings = Menu(self.menuBar,tearoff=0)
    self.menuBar.add_cascade(label="Settings",menu=self.settings)
    self.settings.add_command(label ='Test Data', command =lambda:self.openTestDataWindow())
    self.settings.add_command(label ='Language', command = None)

    self.root.config(menu = self.menuBar)
    

    self.mainFrame = ttk.Frame(root)
    self.mainFrame.columnconfigure(0, weight=1,pad=10)
    self.mainFrame.columnconfigure(1, weight=3,pad=10)

    self.mainFrame.rowconfigure(0,weight=1,pad=10)
    self.mainFrame.rowconfigure(1,weight=1,pad=10)
    self.mainFrame.rowconfigure(2,weight=1,pad=10)


    #Path Entry
    ttk.Label(self.mainFrame, text='* Directory:',anchor='w').grid(column=0, row=0,sticky='w')
    self.dirPathText= tk.StringVar()
    self.dirPath= ttk.Entry(self.mainFrame, width=30,textvariable=self.dirPathText)
    self.dirPath.focus()
    self.dirPath.grid(column=1, row=0)
    self.fileExploreButton = ttk.Button(self.mainFrame,text="...",width=3,command = lambda:self.selectDir())    
    self.fileExploreButton.grid(column=2,row=0)

    #FilenameEntry
    ttk.Label(self.mainFrame, text='* Filename:',anchor='w').grid(column=0, row=1,sticky='w') 
    self.replacementText= tk.StringVar()
    self.replacement = ttk.Entry(self.mainFrame, width=30,textvariable=self.replacementText)
    self.replacement.grid(column=1, row=1)

    #FilenameEntry
    ttk.Label(self.mainFrame, text='Description:',anchor='w').grid(column=0, row=2,sticky='w') 
    self.descriptionText = tk.StringVar()
    self.description= ttk.Entry(self.mainFrame, width=30,textvariable=self.descriptionText)
    self.description.grid(column=1, row=2)

    self.mainFrame.grid(column=0, row=0)


    ##Button Frame 
    self.buttonFrame = ttk.Frame(root)
    self.buttonFrame.columnconfigure(0, weight=1)

    self.buttonStart = ttk.Button(self.buttonFrame, text='Start',command=lambda:self.startCaptureProcess(),cursor="hand2").grid(column=0, row=0)
    self.buttonTestData = ttk.Button(self.buttonFrame, text='Reset',cursor="hand2",command=lambda:self.resetEvidence()).grid(column=0, row=1)
    self.buttonOpenDirStyle = ttk.Style()
    self.buttonOpenDir = ttk.Button(self.buttonFrame, text='Open Dir',cursor="hand2",command=lambda:self.openWorkingDirectory()).grid(column=0, row=2)
    self.buttonGenerate = ttk.Button(self.buttonFrame, text='Generate',cursor="hand2",command=lambda:self.generateEvidence()).grid(column=0, row=3)

    for widget in self.buttonFrame.winfo_children():
      widget.grid(padx=3, pady=3)

    self.buttonFrame.grid(column=1, row=0)


  def openTestDataWindow(self):
    td = testDataWindow(self.root)

  def selectDir(self):
    dirSelected = fd.askdirectory()
    self.dirPathText.set(dirSelected) 


  def startCaptureProcess(self):
    if not self.weStart:
      if self.validInputData():
        res = boxmessage.askquestion("New Evidence","¿Do you want to create a new test case evidence?")
        if res == "yes":
          self.setTestExecutionData()
          testData = self.getMetadata()
          self.evidence = Evidence(self.dirPathText.get(),self.replacementText.get(),testData,self.descriptionText.get())
          cap = captureWindow(self.root,self.evidence,self.dirPathText,self.replacementText,self.descriptionText) 
          if cap != None:
            self.weStart = True
          self.buttonStart.config(text="Continue")
      else:
        boxmessage.showerror("Input Data","The filename or Directory is not valid to store the evidence")
    else:
        boxmessage.showerror("Start Error","You have already a evidence in process, to start again press RESET")



  def setTestExecutionData(self):
    status = self.setStatusTest()
    try:
      with open(jsonFilepath,'r') as f :
        config = json.load(f)
        config['Status'] = status
        config['TestCase'] = self.replacementText.get()
      with open(jsonFilepath,'w') as fi:
        json.dump(config,fi,indent=4)
    except FileNotFoundError as e:
      config = {}
      boxmessage.showerror(e)
    filename = self.replacementText.get()
    # filename_Status = "["+status+"] "+filename
    self.replacementText.set(filename)

  def validInputData(self):
    if not self.dirPathText.get().isspace() and self.dirPathText.get() != '' :
      if os.path.exists(self.dirPath.get()):
        if not self.replacementText.get().isspace() and self.replacementText.get() != '':
          return True
    return False

  def getMetadata(self):
    metadata = []
    try:
      with open(jsonFilepath,'r') as f:
        config = json.load(f)
        for key in config:
          metadata.append(config[key])
    except FileNotFoundError as e:
      config = {}
      boxmessage.showerror("Error",e)

    return metadata
  
  def setStatusTest(self):
    result = messagebox.askquestion("Test Status","¿The test case had passed?")
    if result == "yes":
      return "PASSED" 
    else:
      return "FAILED"
    
  def custom_dialog(self):
    result = simpledialog.askstring("Test Status","¿The test case had passed?",show=False,buttons=["Passed","Failed"])
    return result

  def generateEvidence(self):
    if self.weStart:
      result = messagebox.askquestion("Generate Doc","¿You are sure to generate the document?")
      if result == "yes":
        self.evidence.closeDocument()
        messagebox.showinfo("Generate Doc","Document as been created successfully")
        self.openWorkingDirectory()
        self.replacementText.set("")
        self.dirPathText.set("")
        self.descriptionText.set("")
        self.weStart = False

    else:
      boxmessage.showerror("We don´t start","First you must click Start button to capture the evidences")
      self.dirPath.focus()


  def openWorkingDirectory(self):
    if self.weStart:
      subprocess.run(["explorer",os.path.realpath(self.dirPathText.get())])
    else:
      boxmessage.showerror("We don´t start","First you must click Start button to capture the evidences")
      self.dirPath.focus()

  def askCloseProgram(self):
    res = boxmessage.askquestion("Close Program","¿Are you sure to close the program?")
    if res == "yes":
      self.root.destroy()

  def resetEvidence(self):
    if self.weStart:
      res = boxmessage.askquestion("Reset Evidence","¿Are you sure to reset all the evidences?")
      if res == "yes":
        self.dirPathText.set("")
        self.descriptionText.set("")
        self.replacementText.set("")
        self.weStart = False

        ##Using os module we delete de directories that create at the creation of evidence object
        realpath = os.path.realpath(self.evidence.dir)
        shutil.rmtree(realpath)
        self.evidence = None
        boxmessage.showinfo("Reset Successfully","The reset of the information was successfull")
    else:
      boxmessage.showerror("We don´t start","First you must click Start button to capture the evidences")
