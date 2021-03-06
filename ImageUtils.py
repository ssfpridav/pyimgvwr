# this file largely borrowed from http://wiki.wxpython.org/WorkingWithImages

import wx
import Image             # PIL module. Only if you use the PIL library.

def WxBitmapToPilImage( myBitmap ) :
    return WxImageToPilImage( WxBitmapToWxImage( myBitmap ) )

def WxBitmapToWxImage( myBitmap ) :
    return wx.ImageFromBitmap( myBitmap )

#-----

def PilImageToWxBitmap( myPilImage ) :
    return WxImageToWxBitmap( PilImageToWxImage( myPilImage ) )

def PilImageToWxImage( myPilImage ):
    myWxImage = wx.EmptyImage( myPilImage.size[0], myPilImage.size[1] )
    myWxImage.SetData( myPilImage.convert( 'RGB' ).tostring() )
    return myWxImage

# Or, if you want to copy any alpha channel, too (available since wxPython 2.5)
# The source PIL image doesn't need to have alpha to use this routine.
# But, a PIL image with alpha is necessary to get a wx.Image with alpha.

def PilImageToWxImage( myPilImage, copyAlpha=True ) :

    hasAlpha = myPilImage.mode[ -1 ] == 'A'
    if copyAlpha and hasAlpha :  # Make sure there is an alpha layer copy.

        myWxImage = wx.EmptyImage( *myPilImage.size )
        myPilImageCopyRGBA = myPilImage.copy()
        myPilImageCopyRGB = myPilImageCopyRGBA.convert( 'RGB' )    # RGBA --> RGB
        myPilImageRgbData =myPilImageCopyRGB.tostring()
        myWxImage.SetData( myPilImageRgbData )
        myWxImage.SetAlphaData( myPilImageCopyRGBA.tostring()[3::4] )  # Create layer and insert alpha values.

    else :    # The resulting image will not have alpha.

        myWxImage = wx.EmptyImage( *myPilImage.size )
        myPilImageCopy = myPilImage.copy()
        myPilImageCopyRGB = myPilImageCopy.convert( 'RGB' )    # Discard any alpha from the PIL image.
        myPilImageRgbData =myPilImageCopyRGB.tostring()
        myWxImage.SetData( myPilImageRgbData )

    return myWxImage

#-----

def imageToPil( myWxImage ):
    myPilImage = Image.new( 'RGB', (myWxImage.GetWidth(), myWxImage.GetHeight()) )
    myPilImage.fromstring( myWxImage.GetData() )
    return myPilImage

def WxImageToWxBitmap( myWxImage ) :
    return myWxImage.ConvertToBitmap()

def GetPILResizedWxImage(filename, width, height):
    img = Image.open(filename)
    (imgWidth,  imgHeight) = img.size
    newSize = GetScaledSize(width, height, imgWidth, imgHeight)
    img = img.resize(newSize, Image.ANTIALIAS)
    return PilImageToWxImage(img)

def GetScaledSize(boxWidth, boxHeight, imgWidth, imgHeight):
    imgRatio = imgWidth / float(imgHeight)
    boxRatio = boxWidth / float(boxHeight)
    widthScale = boxWidth / float(imgWidth)
    heightScale = boxHeight / float(imgHeight)
    
    if imgRatio > boxRatio:
        return (boxWidth, int(imgHeight * widthScale))
    else:
        return (int(imgWidth * heightScale), boxHeight)


