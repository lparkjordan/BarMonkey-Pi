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
        
        self.drinkPrices = dict(zip(drinks,prices))
        self.drinkInstructions = dict(zip(drinks,instructions))
        
        label = Label(self, text="Welcome to BarMonkey")
        dispenseButton = Button(self, text="Dispense", command=self.dispense)
        self.drinkList = Listbox(self, selectmode="SINGLE")
        for drink in drinks:
            self.drinkList.insert(END, drink)
        self.drinkList.selection_set(0)
        
        label.grid(row=0, columnspan=3)
        dispenseButton.grid(row=1)
        self.drinkList.grid(row=1, column=2)
        # TODO switch back to inactive view after prespecified amount of time
        
        
    def dispense(self):
        item = self.drinkList.get(self.drinkList.curselection())
        value = self.drinkPrices[item]
        print "Dispensing " + item + " and charging " + str(value) + " to your account."
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
        
            
            
# Admin page - shown when an administrator is logged in.
#TODO add user, delete user, change admins, prime pumps, clean pumps, prices, ingredients, user dues
class AdminPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = Label(self, text="This is page 3")
        label.pack(side="top", fill="both", expand=True)

class App(Tk):
    def __init__(self,  *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        
        # inactive page
        self.inactive = Inactive(self)
        
        #user page
        self.userpage = UserPage(self)

        #admin page
        
        self.adminpage = AdminPage(self)

        #Data
        self.ID = ""
        self.userFile = "./Users.csv"
        self.adminFile = "./Admins.csv"
        
        container = Frame(self)
        
        container.pack(side="top", fill="both", expand=True)

        self.inactive.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.userpage.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.adminpage.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        # TODO should figure out how to change this when necessary
        self.bind("<Key>", self.keyPress)

        self.inactive.show()
        
    def keyPress(self, event):
        if event.char.isdigit():
            self.ID = self.ID + str(event.char)
            if (len(self.ID) == 10):
                self.changeUser()  

    def changeUser(self):
        userList = []
        with open(self.userFile) as f:
            for name, user, owed in csv.reader(f):
                userList += [user]
            if self.ID in userList:
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
