from Tkinter import *

class Page(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class Inactive(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = Label(self, text="Please swipe card to log in")
        label.pack(side="top", fill="both", expand=True)

class UserPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.drinks = dict([("Rum and Coke", 1),
                            ("Vodka Cranberry", 2),
                            ("Tequila Sunrise", 3)]);
       
        label = Label(self, text="Welcome to BarMonkey")
        dispenseButton = Button(self, text="Dispense", command=self.dispense)
        self.drinkList = Listbox(self, selectmode="SINGLE")
        for drink in self.drinks.keys():
            self.drinkList.insert(self.drinks.keys().index(drink), drink)
        self.drinkList.selection_set(0)
        
        label.grid(row=0, columnspan=3)
        dispenseButton.grid(row=1)
        self.drinkList.grid(row=1, column=2)
        
        
    def dispense(self):
        item = self.drinkList.get(self.drinkList.curselection())
        value = self.drinks[item]
        print "Dispensing " + item + " and charging " + str(value) + " to your account."
        with open(self.master.userFile) as f:
            print "derp"
            

class AdminPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = Label(self, text="This is page 3")
        label.pack(side="top", fill="both", expand=True)

class App(Tk):
    def __init__(self,  *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        
        #inactive page
        self.inactive = Inactive(self)
        
        #user page
        #TODO drink selection interface
        self.userpage = UserPage(self)

        #admin page
        #TODO add user, delete user, change admins, prime pumps, clean pumps, prices, ingredients, user dues
        self.adminpage = AdminPage(self)

        #Data
        self.ID = ""
        self.userFile = "./Users.txt"
        self.adminFile = "./Admins.txt"
        
        #buttonframe = Frame(self)
        container = Frame(self)
        self.bind("<Key>", self.keyPress)
        #buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        self.inactive.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.userpage.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.adminpage.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        #b1 = Button(buttonframe, text="Page 1", command=lambda: inactive.lift())
        #b2 = Button(buttonframe, text="Page 2", command=lambda: userpage.lift())
        #b3 = Button(buttonframe, text="Page 3", command=lambda: adminpage.lift())

        #b1.pack(side="left")
        #b2.pack(side="left")
        #b3.pack(side="left")

        self.inactive.show()
        
    def keyPress(self, event):
        if event.char.isdigit():
            self.ID = self.ID + str(event.char)
            print event.char
            if (len(self.ID) == 10):
                print "ID hit 10 chars"
                self.changeUser()  

    def changeUser(self):
        with open(self.userFile) as f:
            lines = f.read().splitlines()
        newlines = []
        for s in lines:
            s = s.split(',')
            newlines = newlines + s
        print self.ID
        if self.ID in newlines:
            print "AUTHENTICATION SUCCESSFUL"
            self.userpage.show()
        else:
            print "AUTHENTICATION FAILED"
            self.ID = ""
        

if __name__ == "__main__":
    root = App()
    root.wm_geometry("400x400")
    root.mainloop()
    root.destroy()
