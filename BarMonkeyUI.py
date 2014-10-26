from Tkinter import *
import csv
# TODO add wiringpi import


# Page superclass
class Page(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

# Inactive page - shown when no user is logged in. 
class Inactive(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = Label(self, text="Please swipe card to log in")
        label.pack(side="top", fill="both", expand=True)

# User page - shown when a basic user is logged in.
class UserPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        # Drinks list. TODO Could probably make this a file.
        drinks = ["Rum and Coke",
                  "Vodka Cranberry",
                  "Tequila Sunrise",
                  "Screwdriver",
                  "White Russian"]
        # Prices list, in cents, in the same order.
        prices = [1,
                  2,
                  3,
                  4,
                  5]
        # Instructions are stored as a list of (pump, numshots) pairs.
        instructions = [[(1,1),(5,10)],
                        [(2,1),(6,10)],
                        [(3,1),(6,5),(7,5)],
                        [(2,1),(7,10)],
                        [(2,1),(4,1),(8,1)]]
        # Descriptions of each drink
        descriptions = ["The Frosh Special",
                        "Self-explanatory",
                        "Tequila and some fruit crap",
                        "OJ and Vodka.",
                        "DAVAI DAVAI DAVAI"]
        
        self.drinkPrices = dict(zip(drinks,prices))
        self.drinkInstructions = dict(zip(drinks,instructions))
        self.drinkDescriptions = dict(zip(drinks,descriptions))

        # Define widgets
        label = Label(self, text="Welcome to BarMonkey! Choose a drink.")
        self.description = Label(self, text="Description will appear here.", height=2)
        dispenseButton = Button(self, text="DISPENSE", command=self.dispense, bg="#006600")
        doneButton = Button(self, text="DONE", command=self.logOut, bg="#880000")
        drinkScrollbar = Scrollbar(self, orient=VERTICAL)
        self.drinkList = Listbox(self, selectmode="SINGLE", yscrollcommand=drinkScrollbar.set)
        self.drinkList.bind("<<ListboxSelect>>", self.setDescription)
        drinkScrollbar.config(command=self.drinkList.yview)
        for drink in drinks:
            self.drinkList.insert(END, drink)
        self.drinkList.selection_set(0)
        

        # Place objects in the frame
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        label.grid(row=0, columnspan=3)
        self.description.grid(row=3, columnspan=3)
        self.drinkList.grid(row=1, rowspan=2, sticky=W+E+N+S)
        drinkScrollbar.grid(row=1, column=1, rowspan=2, sticky=W+N+S)
        dispenseButton.grid(row=1, column=2, padx=30, pady=10, sticky=N+S+E+W)
        doneButton.grid(row=2, column=2, padx=30, pady=10, sticky=N+S+E+W)
        
    def dispense(self):
        item = self.drinkList.get(self.drinkList.curselection())
        value = self.drinkPrices[item]
        print "Dispensing " + item + " and charging " + str(value) + " cents to your account."
        usersList = []

        # Currently, to charge the user for their drink, the device loads the
        # entire list of users and changes the current user's line, then writes
        # the whole list back.
        with open(self.master.userFile) as f:
            for name,user,owed in csv.reader(f):
                if user == self.master.ID:
                    usersList += [(name,user,int(owed)+value)]
                else:
                    usersList += [(name,user,owed)]
        with open(self.master.userFile, 'w') as f:
            w = csv.writer(f)
            for line in usersList:
                w.writerow(line)

        # Dispense the drink by activating pumps.
        instructions = self.drinkInstructions[item]
        for ingredient in instructions:
            # TODO use wiringpi here
            print "Activating pump " + str(ingredient[0]) + " for " + str(ingredient[1]) + " shots"
    def logOut(self):
        self.master.ID = ""
        self.master.inactive.show()
    def setDescription(self, event):
        item = self.drinkList.get(self.drinkList.curselection())
        self.description.config(text=self.drinkDescriptions[item])
            
            
# Admin page - shown when an administrator is logged in.
#TODO add user, delete user, change admins, prime pumps, clean pumps, prices, ingredients, user dues
class AdminPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        # Define widgets
        nameLabel = Label(self, text="Name: ")
        IDLabel = Label(self, text="ID Number: ")
        self.balanceResult = Label(self, text="Balance goes here")
        userButton = Button(self, text="User Page", command=self.master.userpage.show)
        doneButton = Button(self, text="DONE", bg="#880000", command=self.logOut)
        addUserButton = Button(self, text="Add User", command=self.addUser)
        balanceButton = Button(self, text="Check User Balance", command=self.checkBalance)
        primeButton = Button(self, text="Prime Pumps", command=self.primePumps)
        cleanButton = Button(self, text="Clean Pumps", command=self.cleanPumps)
        nameEntry = Entry(self)
        IDEntry = Entry(self)

        # Place in the grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=2)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        
        userButton.grid(row=0, column=0, columnspan=2, sticky=NSEW)
        doneButton.grid(row=0, column=2, columnspan=2, sticky=NSEW)
        nameLabel.grid(row=1, column=0, sticky=NSEW)
        nameEntry.grid(row=1, column=1, columnspan=2, sticky=NSEW)
        IDLabel.grid(row=2, column=0, sticky=NSEW)
        IDEntry.grid(row=2, column=1, columnspan=2, sticky=NSEW)
        addUserButton.grid(row=1, column=3, sticky=NSEW)
        balanceButton.grid(row=2, column=3, sticky=NSEW)
        self.balanceResult.grid(row=3, column=0, columnspan=4, sticky=NSEW)
        primeButton.grid(row=0, column=4, rowspan=2, sticky=NSEW, padx=30, pady=30)
        cleanButton.grid(row=2, column=4, rowspan=2, sticky=NSEW, padx=30, pady=30)
        
    def logOut(self):
        self.master.ID = ""
        self.master.inactive.show()
    def addUser(self):
        return
    def checkBalance(self):
        return
    def primePumps(self):
        return
    def cleanPumps(self):
        return
        

class App(Tk):
    def __init__(self,  *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        #Pages
        self.inactive = Inactive(self)
        self.userpage = UserPage(self)
        self.adminpage = AdminPage(self)

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        self.inactive.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.userpage.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.adminpage.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.inactive.show()

        #Data
        self.ID = ""
        self.userFile = "./Users.csv"
        self.adminFile = "./Admins.csv"

        # Callbacks 
        # TODO should figure out how to change this when necessary
        self.bind("<Key>", self.keyPress)

    # TODO stop reading numbers after ID is full
    def keyPress(self, event):
        if event.char.isdigit():
            self.ID = self.ID + str(event.char)
            if (len(self.ID) == 10):
                self.changeUser()

    def changeUser(self):
        userList = []
        adminList = []
        with open(self.userFile) as f:
            for name, user, owed in csv.reader(f):
                userList += [user]
        with open(self.adminFile) as f:
            for name, admin in csv.reader(f):
                adminList += [admin]
        if self.ID in userList:
            print "AUTHENTICATION SUCCESSFUL"
            self.userpage.show()
            self.after(60*1000, self.userpage.logOut) #TODO make this time reset with user activity
        elif self.ID in adminList:
            print "ADMINISTRATOR AUTHENTICATION SUCCESSFUL"
            self.adminpage.show()
        else:
            print "AUTHENTICATION FAILED"
            self.ID = ""
        

if __name__ == "__main__":
    root = App()
    root.wm_geometry("800x480")
    root.mainloop()
    try:
        root.destroy()
    except:
        pass
