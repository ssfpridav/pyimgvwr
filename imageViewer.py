#!/usr/bin/env python

import os
import wx
import sys 
from MainFrame import *

class PhotoCtrl(wx.App):
    def __init__(self, filepath, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename, True)
        self.frame = MainFrame(None, 'PhotoViewer1', filepath)
 
        self.frame.Bind(wx.EVT_CHAR_HOOK, self.OnCharPress)
        self.frame.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.frame.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
        
        self.frame.Show()

    def OnCharPress(self, event):
        keycode = event.GetKeyCode()
        print 'Charpress: {0}'.format(keycode)
        event.Skip()

    def OnKeyDown(self, event):
        keycode = event.GetKeyCode()
        print 'Keydown: {0}'.format(keycode)
        event.Skip()

    def OnKeyUp(self, event):
        keycode = event.GetKeyCode()
        print 'KeyUp: {0}'.format(keycode)
        event.Skip()

#endClass

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage {0} <firstImageFile>".format(sys.argv[0])
    else:
        app = PhotoCtrl(sys.argv[1])
        app.MainLoop()
