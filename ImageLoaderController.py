import objc
from Cocoa import *
from Foundation import *
from AppKit import *
from PyObjCTools import AppHelper
from ImageLoader import ImageLoader
from Alert import alert
from threading import Thread

class ImageLoaderWorker(Thread):
   def __init__(self, imageLoader):
       Thread.__init__(self)
       self.imageLoader = imageLoader

   def run(self):
       self.imageLoader.loadImages()


class Delegate (NSObject):
    def applicationDidFinishLaunching_(self, aNotification):
        pass

    def applicationShouldTerminateAfterLastWindowClosed_(self, application):
        return True

class ImageLoaderController(NSWindowController):
    startLoadingButton = objc.IBOutlet()
    destinationLabel = objc.IBOutlet()
    setNameTextField = objc.IBOutlet()
    groupByColorCheckbox = objc.IBOutlet()
    statusLabel = objc.IBOutlet()

    def windowDidLoad(self):
        NSWindowController.windowDidLoad(self)
        self.startLoadingButton.setEnabled_(False)
        self.setNameTextField.setDelegate_(self)

    @objc.IBAction
    def setDestination_(self, sender):
        panel = NSOpenPanel.openPanel()
        panel.setCanChooseDirectories_(YES)
        panel.setAllowsMultipleSelection_(NO)
        panel.setCanChooseFiles_(NO)
        result = panel.runModal()

        # Save selected URL as an output directory.
        if (result == NSFileHandlingPanelOKButton):
            url = panel.URL()
            self.selectedPath = url.path()
            self.destinationLabel.setStringValue_(self.selectedPath)
    
    @objc.IBAction
    def startLoading_(self, sender):
        self.startLoadingButton.setEnabled_(False)
        loader = ImageLoader(self.selectedPath, self.setNameTextField.stringValue(), self.groupByColorCheckbox.state() == NSOnState, self)
        self.worker = ImageLoaderWorker(loader)
        self.worker.daemon = True
        self.worker.start();

    def controlTextDidChange_(self, notification):
        if (self.setNameTextField.stringValue().length() > 0):
            self.startLoadingButton.setEnabled_(True)
        else:
            self.startLoadingButton.setEnabled_(False)

    def updateStatus(self, cardName):
        self.statusLabel.setStringValue_("Downloading " + cardName)

    def downloadFinished(self):
        self.statusLabel.setStringValue_("Finished downloading")
        self.startLoadingButton.setEnabled_(True)


if __name__ == "__main__":
    app = NSApplication.sharedApplication()
    delegate = Delegate.alloc().init()
    app.setDelegate_(delegate)

    viewController = ImageLoaderController.alloc().initWithWindowNibName_("ImageLoaderWindow")
    viewController.showWindow_(viewController)
    NSApp.activateIgnoringOtherApps_(True)

    from PyObjCTools import AppHelper
    AppHelper.runEventLoop()
