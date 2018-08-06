from tkinter import *
import time

thours = 0
tminutes = 0
tseconds = 0
clockTime = ''
run = 0
timer = 1
t1 = time.localtime()
flag = 1
tickTime = ''
base_time = 0
refresh_time = 0
total_time = 0

class Master:
        def __init__(self, master):
            global t1
            self.master = master
            master.title("Time Card 1.1")

            self.label = Label(master, font="Helvetica 12", text="Time Card 1.1", background='#aaf0d1')
            self.label.pack()

            self.clock = Label(master, font="Helvetica 18 bold", background='#aaf0d1', textvariable = clockTime)
            self.clock.pack()


            self.clockInButton = Button(master, text="Clock In", command=self.clockIn)
            self.clockInButton.pack()

            self.clockOutButton = Button(master, text="Clock Out", command=self.clockOut)
            self.clockOutButton.pack()

            self.ticker = Label(master, font="Helvetica 18 bold", background='#aaf0d1', textvariable = tickTime)
            self.ticker.pack()
            
            self.Clock()

        def Clock(self):
                global timer
                if timer == 1:
                        global clockTime
                        # get the current local time from the PC
                        newTime = time.strftime('%I:%M:%S %p')
                        # if time string has changed, update it
                        if newTime != clockTime:
                                clockTime = newTime
                        
                        self.clock.config(text="Current Time: " + clockTime)
                        self.clock.after(200,self.Clock)

        def tick(self):
                global run
                global flag
                global base_time
                global total_time
                global period
                if flag == 1:
                        base_time = time.time()
                        print("Base time: " + str(base_time))
                        flag = 0
                if run == 1:
                        global thours
                        global tminutes
                        global tseconds
                        tdelta = time.time() - base_time + total_time
                        thours = int((tdelta % 86400) / 3600)
                        tminutes = int(((tdelta % 86400) % 3600) / 60)
                        tseconds = int((((tdelta % 86400) % 3600) % 60))

                        if thours >= 0 and thours <= 9:
                                strhours = "0" + str(thours)
                        else:
                                strhours = str(thours)
                        if tminutes >= 0 and tminutes <= 9:
                                strminutes = "0" + str(tminutes)
                        else:
                                strminutes = str(tminutes)
                        if tseconds >= 0 and tseconds <= 9:
                                strseconds = "0" + str(tseconds)
                        else:
                                strseconds = str(tseconds)
                        tickTime = strhours + ":" + strminutes + ":" + strseconds
                        self.ticker.config(text="Worked Time: " + tickTime)
                        self.ticker.after(200,self.tick)
                        
        def clockIn(self):
            global run
            global flag
            flag = 1
            run = 1
            self.tick()

        def clockOut(self):
            global run
            global base_time
            global total_time
            total_time += time.time() - base_time
            run = 0

root = Tk()
masterWindow = Master(root)
root.geometry("400x300")
root['background'] = '#aaf0d1'
root.mainloop()
