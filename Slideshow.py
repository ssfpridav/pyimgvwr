
import wx
import os
from threading import *
import time

# Define notification event for thread
EVT_RESULT_ID = wx.NewId()
EVT_PROGRESS_ID = wx.NewId()

class ResultEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.data = data
#endclass


class ProgressEvent(wx.PyEvent):
    def __init__(self, direction):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_PROGRESS_ID)
        self.direction = direction


class SlideshowWorker(Thread):
    def __init__(self, direction, interval, notify_window):
        Thread.__init__(self)
        self.direction = direction
        self.interval = interval
        self.notifyWindow = notify_window
        self.stopFlag = False
        self.start()

    def run(self):
        while True:
            time.sleep(self.interval)
            if self.stopFlag:
                wx.PostEvent(self.notify_window, ResultEvent(None))
                return
            else:
                wx.PostEvent(self.notify_window, ProgressEvent(self.direction))
    
    def abort(self):
        self.stopFlag = True
