import tkinter, json, os

class Main:
    file = './data.json'
    arr = []
    length = 20
    index = 0
    outputText = []
    labels = []
    windowOpen = False
    fontSize = 44
    fontFamily = "Arial Black"
    fontWeight = "bold"
    fullscreen = False # escape key will toggle
    bg = 'black'
    fg = 'white'
    alt = "#f5be0c" # main text colour and flash colour

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
        self.writeCurrent(True)

    def removeNumber(self):
        self.index = self.index-1 if self.index > 0 else (self.length -1)
        self.arr[self.index] = ''
        self.writeCurrent()

    def writeCurrent(self, flash = False):
        wr = open(self.file, 'w')
        wr.write(json.dumps({"arr": self.arr, "index": self.index}))
        if self.windowOpen:
            self.valuesToOutputText(flash)


    def valuesToOutputText(self, flash = False):
        arrangedArr = self.arr[self.index:] + self.arr[:self.index]
        stringArr = [str(x) for x in arrangedArr if isinstance(x, int)]
        finalIndex = len(stringArr) - 1 # if we don't have a full array this finds the index of the last used cell so we know which index to flash
        while len(stringArr) < self.length:
            stringArr.append("") # so removed values are cleared by replacing them with empty string
        for index, text in enumerate(stringArr):
            self.outputText[index].set(text)

        if flash:
            self.labels[finalIndex].configure(foreground=self.alt)
            # reset colours after delay, doesn't matter which tk object after is called on
            self.labels[finalIndex].after(500, lambda: self.labels[finalIndex].configure(foreground=self.fg))


    # init
    def __init__(self):
        self.arr = 20*['']
        if os.path.isfile(self.file):
            with open(self.file) as f:
                data = json.load(f)
                self.arr = data["arr"]
                self.index = data["index"]

        self.startGui()

    # tkinter madness
    def startGui(self):
        # init window
        window = tkinter.Tk()
        window.geometry("200x200")
        window.title("Input")

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
        self.windowOpen = True
        window = tkinter.Toplevel()
        window.geometry("600x800")
        window.title("Output")
        window.configure(background=self.bg)

        def windowClosed():
            self.windowOpen = False
            window.destroy()
        window.protocol("WM_DELETE_WINDOW", windowClosed)

        def toggleFullscreen(event):
            self.fullscreen = False if self.fullscreen else True
            window.attributes('-fullscreen', self.fullscreen)
        window.bind("<Escape>", toggleFullscreen)
        msg = tkinter.Label(window, text="Ready to pickup: ")
        msg.configure(foreground=self.alt, background=self.bg, font=(self.fontFamily, self.fontSize, self.fontWeight))
        msg.grid(columnspan=2, sticky=tkinter.N)

        # set output text variables
        for i in range(0,self.length):
            self.outputText.append(tkinter.StringVar())
        self.labels = [tkinter.Label(window, textvariable=self.outputText[x]) for x in range(0,self.length)]
        half = int(self.length/2)
        for idx, label in enumerate(self.labels):
            label.configure(foreground=self.fg, background=self.bg, font=(self.fontFamily, self.fontSize, self.fontWeight))
            row = 1 + idx
            if idx < half:
                label.grid(row=row, column=0, sticky=tkinter.NE, padx = 75)
            else:
                row -= half
                label.grid(row=row, column=1, sticky=tkinter.NW, padx = 75)

        # create and write output text to screen
        self.valuesToOutputText()

        window.grid_columnconfigure(0, weight=1, uniform='match')
        window.grid_columnconfigure(1, weight=1, uniform='match')
        window.mainloop()

# call
Main()
