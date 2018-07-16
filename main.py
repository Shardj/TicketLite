import tkinter, json, os

class Main:
    file = './data.json'
    arr = ['','','','','','','','','','']
    index = 0
    outputText = None
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

        self.index = self.index+1 if self.index < 9 else 0
        self.writeCurrent()

    def removeNumber(self):
        self.index = self.index-1 if self.index > 0 else 9
        self.arr[self.index] = ''
        self.writeCurrent()

    def writeCurrent(self, justFile = False):
        wr = open(self.file, 'w')
        wr.write(json.dumps({"arr": self.arr, "index": self.index}))
        if not justFile:
            self.valuesToOutputText()


    def valuesToOutputText(self):
        arrangedArr = self.arr[self.index:] + self.arr[:self.index]
        text = '\n'.join(str(x) for x in arrangedArr if isinstance(x, int) )
        self.outputText.set(text)

    # init
    def __init__(self):
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
        window.geometry("400x400")
        window.title("Input")

        # init output text for use later
        self.outputText = tkinter.StringVar()
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
        window.geometry("400x400")
        window.title("Output")
        window.configure(background="black")
        def toggleFullscreen(event):
            self.fullscreen = False if self.fullscreen else True
            window.attributes('-fullscreen', self.fullscreen)
        window.bind("<Escape>", toggleFullscreen)
        msg = tkinter.Label(window, text="Ready to pickup: ")
        msg.configure(foreground="white", background="black", font=(self.fontFamily, self.fontSize, self.fontWeight))
        msg.grid(sticky=tkinter.NE)

        label = tkinter.Label(window, textvariable=self.outputText)
        label.configure(foreground="white", background="black", font=(self.fontFamily, self.fontSize, self.fontWeight))
        label.grid(row=0, column=1, sticky=tkinter.N)

        window.grid_columnconfigure(0, weight=1, uniform='match')
        window.grid_columnconfigure(1, weight=1)
        window.grid_columnconfigure(2, weight=1, uniform='match')
        window.mainloop()

# call
Main()
