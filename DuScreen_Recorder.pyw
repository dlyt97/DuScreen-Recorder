import sys
import os
import time

try:
    import numpy
except:
    os.system('py -m pip install numpy')
   
try:
    from screen_recorder_sdk import screen_recorder
except:
    os.system('py -m pip install screen-recorder-sdk')

import win32gui, win32con

from tkinter.filedialog import askdirectory
    
import time
from tkinter import *
import tkinter as tk

from screeninfo import get_monitors

import threading

class DuRec(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        #self.__hide_console__()
        
        def __start__():
            screen_recorder.enable_dev_log ()
            
            pid = int (0) # PID - System IDLE Process
            
            screen_recorder.init_resources (pid)
        __start__()

        self.__controls__()
        self.__style__()
        self.__commands__()

        def __disabled_control__():
            self.btn_stop['state'] = 'disabled'
        __disabled_control__()


    def __minimize_window__(self):
        Minimize = win32gui.GetForegroundWindow()
        win32gui.ShowWindow(Minimize, win32con.SW_MINIMIZE)


    def __hide_console__(self):
        HIDE_PROGRAM = win32gui.GetForegroundWindow()
        win32gui.ShowWindow(HIDE_PROGRAM , win32con.SW_HIDE)  
    

    def __start_rec__(self):
        self.btn_stop['state'] = 'normal'
        self.input_name['state'] = 'disabled'
        self.btn_start['state'] = 'disabled'
        self.btn_output['state'] = 'disabled'

        # self.__minimize_window__()
        
        try:
            def rec():
                screen_recorder.start_video_recording (self.path + '/' + str(self.var_name.get()) + '.mp4', 60, 100 * pow(10,6), True)
            threadObj = threading.Thread(target=lambda:rec())
            threadObj.start()
        except:
            def rec():
                screen_recorder.start_video_recording(str(self.var_name.get()) + '.mp4', 60, 100 * pow(10,6), True)
            threadObj = threading.Thread(target=lambda: rec())
            threadObj.start()
        
        print('START Recorder')
        
        def stop_watch(vreme = 1):
            for sat in range(24)[::vreme]:
                for minut in range(60)[::vreme]:
                    for sekunda in range(60)[::vreme]:
                        h = int
                        m = int
                        s = int
                        
                        if sat < 10:
                            h = '0' + str(sat)
                        else:
                            h = str(sat)
                            
                        if minut < 10:
                            m = '0' + str(minut)
                        else:
                            m = str(minut)
                            
                        if sekunda < 10:
                            s = '0' + str(sekunda)
                        else:
                            s = str(sekunda)

                        self.total = '{0}:{1}:{2}'.format(h,m,s)
                        self.stopwatch['text'] = str(self.total)
                        self.stopwatch.update()
                        
                        time.sleep(1)
                        
        def timer_thread():
            threadObj = threading.Thread(target=lambda: stop_watch())
            threadObj.start()
        timer_thread()
          
    def __stop_rec__(self):
        
        self.destroy()
        
        screen_recorder.stop_video_recording ()
        screen_recorder.free_resources()
       
        try:
            os.system('taskkill /F /IM DuScreen_Recorder.exe')
        except:
            print(end='')
       
        quit()
       
    def __choose_path__(self):
        self.path = askdirectory(title = 'Path?',initialdir = os.path.expanduser('./'))
        

    def __get_current_resolution__(self):
        for x in get_monitors():
            self.screen = str(x).split(',')
            
            self.width = self.screen[2].replace(' ','').replace('width=','')
            self.height = self.screen[3].replace(' ','').replace('height=','')

            print(self.width,self.height)

            resolution = str(self.width) + 'x' + str(self.height)
            self.lbl_resolution['text'] = resolution
            self.lbl_resolution.update()

    def __commands__(self):
        try:
            self.btn_start['command'] = lambda : self.__start_rec__()
        except:
            print(end='')

        try:
            self.btn_stop['command'] = lambda : self.__stop_rec__()
        except:
            print(end='')

        try:
            self.btn_output['command'] = lambda: self.__choose_path__()
        except:
            print(end='')

        self.__get_current_resolution__()


    def __style__(self):
        self.input_name['font'] = ('Calibri',20,'bold')
        self.input_name['bg'] = 'gray90'
        self.input_name['fg'] = 'black'
        self.input_name['width'] = 10
        
        self.stopwatch['font'] = ('Calibri',20,'bold')
        self.stopwatch['bg'] = 'gray90'
        self.stopwatch['fg'] = 'black'
        self.stopwatch['width'] = 10
        
        self.btn_start['font'] = ('Calibri',20,'bold')
        self.btn_start['bg'] = 'deepskyblue'
        self.btn_start['fg'] = 'white'
        self.btn_start['width'] = 10

        self.btn_stop['font'] = ('Calibri',20,'bold')
        self.btn_stop['bg'] = 'red'
        self.btn_stop['fg'] = 'white'
        self.btn_stop['width'] = 10
        
        self.btn_output['font'] = ('Verdana',15,'bold')
        self.btn_output['bg'] = 'Green'
        self.btn_output['fg'] = 'white'
        self.btn_output['width'] = 10
        
        self.lbl_resolution['font'] = ('Verdana',15,'bold')
        self.lbl_resolution['bg'] = 'gray12'
        self.lbl_resolution['fg'] = 'gray90'
        self.lbl_resolution['width'] = 10
        

    def __controls__(self):
        self.stopwatch = Label(self)
        self.stopwatch.grid(row = 0,column = 1,padx = 10,pady = 10)

        self.var_name = StringVar()
        self.input_name = Entry(self,textvariable = self.var_name)
        self.input_name.grid(row = 0,column = 0,padx = 10,pady = 10)
        self.input_name.insert(0, 'video1')
        
        self.btn_start = Button(self,text='START')
        self.btn_start.grid(row = 1,column = 0,padx = 10,pady = 10)

        self.btn_stop = Button(self,text='STOP')
        self.btn_stop.grid(row = 1,column = 1,padx = 10,pady = 10)

        self.btn_output = Button(self,text = 'Browse')
        self.btn_output.grid(row = 2,column = 0,padx = 10, pady = 10)

        self.lbl_resolution = Label(self)
        self.lbl_resolution.grid(row = 2, column = 1,padx = 10, pady = 10)


def gui():
    app = DuRec()
    try:
        app.title('DuScreen Recorder 1.1')
    except:
        print(end='')
    try:
        app.geometry('350x200')
    except:
        print(end='')
    try:
        app.configure(bg = 'gray12')
    except:
        print(end='')
    try:
        app.resizable(False,False)
    except:
        print(end='')
    app.mainloop()
gui()
