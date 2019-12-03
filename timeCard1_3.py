from tkinter import *
import time
import math
import csv

### GLOBALS
thours = 0
tminutes = 0
tseconds = 0
last_time = [0, 0, 0]
clockTime = ''
run = 0
timer = 1
t1 = time.localtime()
flag = 1
taskTickTime = ''
tickTime = ''
base_time = 0
refresh_time = 0
total_time = 0
history_counter = 0
entry_field = ''
global_background = '#AED6F1'
start_time = ''
end_time = ''

def formatTime(hours, minutes, seconds):
   if hours >= 0 and hours <= 9:
           strhours = "0" + str(hours)
   else:
           strhours = str(hours)
   if minutes >= 0 and minutes <= 9:
           strminutes = "0" + str(minutes)
   else:
           strminutes = str(minutes)
   if seconds >= 0 and seconds <= 9:
           strseconds = "0" + str(seconds)
   else:
           strseconds = str(seconds)
   return strhours + ":" + strminutes + ":" + strseconds

def calculateTimeDifference(lastTimeVector, currentTimeVector):
        lastTimeTotalSeconds = lastTimeVector[0] * 3600 + lastTimeVector[1] * 60 + lastTimeVector[2]
        currentTimeTotalSeconds = currentTimeVector[0] * 3600 + currentTimeVector[1] * 60 + currentTimeVector[2]
        diffTimeTotalSeconds = currentTimeTotalSeconds - lastTimeTotalSeconds
        retHours = math.floor(diffTimeTotalSeconds/3600)
        retMinutes = math.floor(diffTimeTotalSeconds/60) % 60
        retSeconds = diffTimeTotalSeconds % 60
        return [retHours, retMinutes, retSeconds]

class Master:
        def __init__(self, master):
            global t1, history_counter
            self.master = master
            master.title("Time Card 1.1")

            midHorzFrame = Frame(master, bg=global_background)
            topVertFrame = Frame(master, bg=global_background)
            bottomVertFrame = Frame(master, bg=global_background)

            topVertFrame.pack(side="top")
            midHorzFrame.pack(side="top")
            bottomVertFrame.pack(side="bottom")
            
            self.label = Label(topVertFrame, font="Helvetica 12", text="Time Card 1.1", bg=global_background)
            self.label.pack()

            self.clock = Label(topVertFrame, font="Helvetica 18 bold", bg=global_background, textvariable = clockTime)
            self.clock.pack()

            self.clockInButton = Button(midHorzFrame, text="Clock In", command=self.clockIn)
            self.clockInButton.pack(side="left", padx=10)

        
            self.clockOutButton = Button(midHorzFrame, state=DISABLED, text="Clock Out", command=self.clockOut)
            self.clockOutButton.pack(side="left", padx=10)

            self.entryField = Entry(bottomVertFrame, width=75)
            self.entryField.pack()

            self.ticker = Label(bottomVertFrame, font="Helvetica 18 bold", bg=global_background, textvariable = tickTime)
            self.ticker.pack()

            self.history = Listbox(bottomVertFrame, width=75, height=15)
            #self.history.insert(1, "Rouvem Pishchik")
            self.history.pack(side="top",pady=10)

            #self.resetHistory = Listbox(master)
            #self.resetHistory.pack(side="left");

            self.resetButton = Button(bottomVertFrame, state=DISABLED, text="Reset Worked Time", command=self.reset)
            self.resetButton.pack(side=BOTTOM, pady=10)


            topText = "   Start Time    |    End Time    |    Duration    |    Description"
            self.history.insert(history_counter, topText)
            self.history.pack()
            history_counter += 1
                                
            self.Clock()

        ## Current Time
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

        ## Timer for Clocked In Hours
        def tick(self):
                global run, flag, base_time, total_time, period, tickTime
                if flag == 1:
                        base_time = time.time()
                        print("Base time: " + str(base_time))
                        flag = 0
                if run == 1:
                        global thours, tminutes, tseconds
                        tdelta = time.time() - base_time + total_time
                        thours = int((tdelta % 86400) / 3600)
                        tminutes = int(((tdelta % 86400) % 3600) / 60)
                        tseconds = int((((tdelta % 86400) % 3600) % 60))
                        tickTime = formatTime(thours,tminutes,tseconds)
                        #tickTime = strhours + ":" + strminutes + ":" + strseconds
                        self.ticker.config(text="Worked Time: " + tickTime)
                        self.ticker.after(200,self.tick)
                        
         ## Activates timer for Clocking In               
        def clockIn(self):
            global run, flag, entry_field, last_time, clockTime, start_time
            flag = 1
            run = 1
            last_time = [thours, tminutes, tseconds]
            entry_field = self.entryField.get()
            start_time = clockTime
            self.tick()
            self.clockOutButton.config(state=NORMAL)
            self.resetButton.config(state=DISABLED)
            self.clockInButton.config(state=DISABLED)
            self.entryField.config(state=DISABLED)
        
        ## Deactivates timer for Clocking In    
        def clockOut(self):
                global run, base_time, total_time, history_counter, tickTime, entry_field, clockTime, start_time, end_time
                total_time += time.time() - base_time
                run = 0
                history_counter += 1
                end_time = clockTime
                current_time = calculateTimeDifference(last_time, [thours, tminutes, tseconds])
                taskTime = formatTime(current_time[0], current_time[1], current_time[2])
                listBoxEntry = "  " + start_time +"     " + end_time + "       " + taskTime + "       " + entry_field
                self.history.insert(history_counter, listBoxEntry)
                self.history.pack()
                self.clockOutButton.config(state=DISABLED)
                self.clockInButton.config(state=NORMAL)
                self.resetButton.config(state=NORMAL)
                self.entryField.config(state=NORMAL)

        ## Resets the timer
        def reset(self):
                global run, tminutes, thours, tseconds, history_counter, last_time, tickTime, base_time, total_time, flag
                thours = 0
                tminutes = 0
                tseconds = 0
                total_time = 0
                last_time = [0, 0, 0]
                self.clockOutButton.config(state=DISABLED)
                self.clockInButton.config(state=NORMAL)
                self.history.insert(history_counter+1, tickTime)
                self.history.pack()
                self.history.delete(1,'end')
                history_counter = 1
                tickTime = ''
                run = 0
                self.ticker.config(text="Worked Time: 00:00:00")
                
root = Tk()
masterWindow = Master(root)
root.geometry("600x500")
root['background'] = global_background
root.mainloop()
