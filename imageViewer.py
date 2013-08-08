#!/usr/bin/env python

import os
import wx
import sys 

class MainFrame(wx.Frame):
    def __init__(self, parent, title, filepath):
        wx.Frame.__init__(self, parent, title=title, size=(400,400))

        self.registerEvents()
        self.initialize(filepath)

    def registerEvents(self):
        self.Bind(wx.EVT_KEY_UP, self.onKeyPress)
        self.Bind(wx.EVT_SIZE, self.onReSize)
        self.Bind(wx.EVT_MOVE, self.onMove)
        self.Bind(wx.EVT_SET_FOCUS, self.onGetFocus)
        self.Bind(wx.EVT_KILL_FOCUS, self.onLoseFocus)

    def initialize(self, filepath):
        # initialize some ui stuff
        self.panel = wx.Panel(parent=self)
        self.panel.SetFocus()
        self.panel.SetBackgroundColour('#000000')
        #self.vbox = wx.BoxSizer(wx.VERTICAL)
        #self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        #self.panel.SetSizer(self.vbox)

        # other variables
        self.filepath = filepath
        self.imageCtrl = None
        self.fullScreen = False

        # actual setup
        self.setupFileList()
        self.createMenuBar()
        self.loadImage()

    def setupFileList(self):
        self.dirname = os.path.dirname(self.filepath)
        filename = os.path.basename(self.filepath)
        self.getFileList()        
        self.filePosition = -1
        for i in xrange(0, len(self.fileList)):
            if (self.fileList[i] == filename):
                self.filePosition = i
                break
            #else:
                #print '{0}th file: {1} is not a match to {2}'.format(i, self.fileList[i], self.filepath)
        
        print 'viewing {0}th file of {1}'.format(self.filePosition, len(self.fileList))

    def getFileList(self):
        filteredList = []
        rawlist = os.listdir(self.dirname)
        for i in xrange(0, len(rawlist)):
            if rawlist[i].endswith((".png",".jpg",".gif",".tif",".jpeg")):
                filteredList.append(rawlist[i])

        self.fileList = sorted(filteredList)
        print "first: {0} and last: {1}".format(self.fileList[0], self.fileList[len(self.fileList)-1])
        return self.fileList

    def createMenuBar(self):
        menubar = wx.MenuBar()

        filemenu = wx.Menu()
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About", "Info about program")
        filemenu.AppendSeparator()
        menuExit = filemenu.Append(wx.ID_EXIT, "E&xit", "Terminate the program")
        self.Bind(wx.EVT_MENU, self.onAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.onExit, menuExit)

        menubar.Append(filemenu, "&File")
        self.SetMenuBar(menubar)

    def loadImage(self):
        print 'Loading {0}'.format(self.filepath)
        self.removeOldControls()
        self.rawimg = wx.Image(self.filepath, wx.BITMAP_TYPE_ANY)
        self.imgWidth = self.rawimg.GetWidth()
        self.imgHeight = self.rawimg.GetHeight()
        self.img = self.rawimg
        self.imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY, 
                                         wx.BitmapFromImage(self.rawimg))
        #self.vbox.Add(self.imageCtrl, proportion = 0, flag = wx.ALIGN_CENTER, border = 40)
        self.scaleAndPositionImage()

    def removeOldControls(self):
        if not self.imageCtrl == None:
            self.imageCtrl.Destroy()

    def scaleAndPositionImage(self):
        self.scaleImage()
        self.positionImage()
        self.Refresh()

    def scaleImage(self):
        frmWidth,  frmHeight = self.GetSize()
        #print 'scaling image {0},{1} to {2},{3}'.format(self.imgWidth, self.imgHeight, frmWidth, frmHeight)

        imgRatio = self.imgWidth / float(self.imgHeight)
        frmRatio = frmWidth / float(frmHeight)
        heightScale = frmHeight / float(self.imgHeight)
        widthScale = frmWidth / float(self.imgWidth)
        
        if imgRatio > frmRatio:
            NewW = frmWidth
            NewH = self.imgHeight * widthScale
        else:
            NewW = self.imgWidth * heightScale
            NewH = frmHeight

        self.img = self.rawimg.Scale(NewW,NewH, quality = wx.IMAGE_QUALITY_HIGH)
        self.imageCtrl.SetBitmap(wx.BitmapFromImage(self.img))

    def positionImage(self):
        frmWidth, frmHeight = self.GetSize()
        imgWidth, imgHeight = self.imageCtrl.GetSize()
        newX = 0
        newY = 0
        if not frmWidth == imgWidth:
            newX = (frmWidth - imgWidth) / 2

        if not frmHeight == imgHeight:
            newY = (frmHeight - imgHeight) / 2

        print "trying to move the image to {0},{1}".format(newX, newY)
        self.imageCtrl.SetPosition((newX, newY))

    def loadPreviousImage(self):
        if self.filePosition >= 1:
            self.filePosition = self.filePosition - 1
            self.filepath = os.path.normpath('{0}/{1}'.format(self.dirname, self.fileList[self.filePosition]))
            self.loadImage()
        else: #loop around
            self.filePosition = len(self.fileList)-1
            self.filepath = os.path.normpath('{0}/{1}'.format(self.dirname, self.fileList[self.filePosition]))
            self.loadImage()

    def loadNextImage(self):
        if self.filePosition <= len(self.fileList)-2:
            self.filePosition = self.filePosition + 1
            self.filepath = os.path.normpath('{0}/{1}'.format(self.dirname, self.fileList[self.filePosition]))
            self.loadImage()
        else: #loop around
            self.filePosition = 0
            self.filepath = os.path.normpath('{0}/{1}'.format(self.dirname, self.fileList[self.filePosition]))
            self.loadImage()

    def toggleFullScreen(self):
        if not self.fullScreen:
            self.fullScreen = True
            self.ShowFullScreen(True)
        else:
            self.fullScreen = False
            self.ShowFullScreen(False)
            
    def onReSize(self, event):
        self.scaleAndPositionImage()
        event.Skip()

    def onMove(self, event):
        x, y = event.GetPosition()
        #print 'Moved to {0},{1}'.format(x,y)
        event.Skip()

    def onGetFocus(self, event):
        print 'Got focus :)'
        event.Skip()

    def onLoseFocus(self, event):
        print 'Lost focus :('
        event.Skip()

    def onKeyPress(self, event):
        keycode = event.GetKeyCode()
        print 'Keypress: {0}'.format(keycode)
        if keycode == wx.WXK_ESCAPE:
            self.Close(True)
        elif keycode == wx.WXK_LEFT or keycode == wx.WXK_PAGEUP or keycode == wx.WXK_UP:
            self.loadPreviousImage()
        elif keycode == wx.WXK_RIGHT or keycode == wx.WXK_PAGEDOWN or keycode == wx.WXK_DOWN:
            self.loadNextImage()
        elif keycode == wx.WXK_F11:
            self.toggleFullScreen()

        event.Skip()

    def onAbout(self, e):
        print 'About: This is a super-simple image viewer'

    def onExit(self, e):
        self.Close(True)

    def onBrowse(self, event):
        """ 
        Browse for file
        """
        wildcard = "JPEG files (*.jpg)|*.jpg"
        dialog = wx.FileDialog(None, "Choose a file",
                               wildcard=wildcard,
                               style=wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.filepath = dialog.GetPath()
            self.photoTxt.SetValue(self.filepath)

        dialog.Destroy() 
        self.loadImage()

#endClass

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
