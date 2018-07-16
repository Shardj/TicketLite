import tkinter, json, os

class Main:
    file = './data.json'
    arr = ['','','','','','','','','','']
    index = 0
    outputText = None

    # events
    def newNumber(self, num):
        try:
            self.arr[self.index] = int(num)
        except ValueError:
            self.arr[self.index] = ""

        self.index = self.index+1 if self.index < 9 else 0
        self.writeCurrent()

    def removeNumber(self):
        self.index = self.index-1 if self.index > 0 else 9
        self.arr[self.index] = ''
        self.writeCurrent()

    def writeCurrent(self):
        wr = open(self.file, 'w')
        wr.write(json.dumps({"arr": self.arr, "index": self.index}))
        self.valuesToOutputText()

    def valuesToOutputText(self):
        arrangedArr = self.arr[self.index:] + self.arr[:self.index]
        text = ', '.join(str(x) for x in arrangedArr)
        self.outputText.set(text)

    # init
    def __init__(self):
        if os.path.isfile(self.file):
            with open(self.file) as f:
                data = json.load(f)
                self.arr = data["arr"]
                self.index = data["index"]
        else:
            self.writeCurrent()

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
        ent = tkinter.Entry(window)
        ent.bind("<Return>", (lambda event: self.newNumber(ent.get())))
        ent.pack(side=tkinter.TOP, anchor="w")
        btn = tkinter.Button(window,text="Submit", command=(lambda: self.newNumber(ent.get())))
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
        tkinter.Label(window, textvariable=self.outputText).pack(side=tkinter.TOP, anchor="w")
        window.mainloop()

# call
Main()
