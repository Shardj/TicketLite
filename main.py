import tkinter, json, os

class Main:
    file = './data.json'
    arr = []
    length = 20
    index = 0
    outputText1 = None
    outputText2 = None
    fontSize = 44
    fontFamily = "Arial Black"
    fontWeight = "bold"
    fullscreen = False

    # events
    def newNumber(self, num):
        self.ent.delete(0, 'end')
        try:
            self.arr[self.index] = int(num)
        except ValueError:
            if num == ",": # client wants comma to work as an alias for delete button
                self.removeNumber()
            return

        self.index = self.index+1 if self.index < (self.length -1) else 0
        self.writeCurrent()

    def removeNumber(self):
        self.index = self.index-1 if self.index > 0 else (self.length -1)
        self.arr[self.index] = ''
        self.writeCurrent()

    def writeCurrent(self, justFile = False):
        wr = open(self.file, 'w')
        wr.write(json.dumps({"arr": self.arr, "index": self.index}))
        if not justFile:
            self.valuesToOutputText()


    def valuesToOutputText(self):
        arrangedArr = self.arr[self.index:] + self.arr[:self.index]
        stringArr = [str(x) for x in arrangedArr if isinstance(x, int)]
        half = int(self.length/2)
        text1 = '\n'.join(stringArr[:half])
        text2 = '\n'.join(stringArr[half:])
        self.outputText1.set(text1)
        self.outputText2.set(text2)

    # init
    def __init__(self):
        self.arr = 20*['']
        if os.path.isfile(self.file):
            with open(self.file) as f:
                data = json.load(f)
                self.arr = data["arr"]
                self.index = data["index"]
        else:
            self.writeCurrent(True)

        self.startGui()

    # tkinter madness
    def startGui(self):
        # init window
        window = tkinter.Tk()
        window.geometry("200x200")
        window.title("Input")

        # init output text for use later
        self.outputText1 = tkinter.StringVar()
        self.outputText2 = tkinter.StringVar()
        self.valuesToOutputText()

        tkinter.Label(window, text="Enter next number:").pack(side=tkinter.TOP, anchor="w")
        self.ent = tkinter.Entry(window)
        self.ent.bind("<Return>", (lambda event: self.newNumber(self.ent.get())))
        self.ent.pack(side=tkinter.TOP, anchor="w")
        btn = tkinter.Button(window,text="Submit", command=(lambda: self.newNumber(self.ent.get())))
        btn.pack(side=tkinter.TOP, anchor="w")

        rmBtn = tkinter.Button(window,text="Remove Last Number", command=(lambda: self.removeNumber()))
        rmBtn.pack(side=tkinter.TOP, anchor="w")

        outputBtn = tkinter.Button(window, text="Open output window", command=(lambda: self.startOutputGui()))
        outputBtn.pack(side=tkinter.TOP, anchor="w")

        window.mainloop()

    def startOutputGui(self):
        window = tkinter.Toplevel()
        window.geometry("600x800")
        window.title("Output")
        window.configure(background="black")
        def toggleFullscreen(event):
            self.fullscreen = False if self.fullscreen else True
            window.attributes('-fullscreen', self.fullscreen)
        window.bind("<Escape>", toggleFullscreen)
        msg = tkinter.Label(window, text="Ready to pickup: ")
        msg.configure(foreground="#f5be0c", background="black", font=(self.fontFamily, self.fontSize, self.fontWeight))
        msg.grid(columnspan=2, sticky=tkinter.N)

        labels = [tkinter.Label(window, textvariable=self.outputText1), tkinter.Label(window, textvariable=self.outputText2)]
        for label in labels:
            label.configure(foreground="white", background="black", font=(self.fontFamily, self.fontSize, self.fontWeight))
        labels[0].grid(row=1, column=0, sticky=tkinter.NE, padx = 75)
        labels[1].grid(row=1, column=1, sticky=tkinter.NW, padx = 75)

        window.grid_columnconfigure(0, weight=1, uniform='match')
        window.grid_columnconfigure(1, weight=1, uniform='match')
        window.mainloop()

# call
Main()
