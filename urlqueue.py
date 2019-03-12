### ImageFap Gallery Downloader
### download queue management

import config
import IFUser
#from Tkinter import Tk
from shelve import open as dbmopen

queue = []

def CheckUrl(url):
    ### check if url looks like a gallery url
    if (url.find(config.GalleryLink1)!=-1):
        return 1 #IF1
    elif (url.find(config.GalleryLink2)!=-1):
        return 2 #IF2
    elif (url.find(config.GalleryLink3)!=-1):
        return 3 #XH
    elif (url.find(config.GalleryLink4)!=-1):
        return 4 #IF3
    elif (url.find(config.IFFolder1)!=-1):
        return 5 #IFFolder1
    elif (url.find(config.IFFolder2)!=-1):
        return 6 #IFFolder2
    elif (url.find(config.IFUserLink)!=-1):
        return 7 #IFUser
    else:
        return 0

def PollClipboard():
    ### retrieve the current clipboard content
    clipb = []
    maxk = config.stamp[0]
    with dbmopen(config.clipboard, 'r') as clip:
        for k in clip:
            t = int(k) 
            if t > config.stamp[0]:
                clipb.append(clip[k])
                if t > maxk:
                    maxk = t
        config.stamp[0] = maxk
#    try:
#        clip = Tk()
#        clip.withdraw()
#        clipb = clip.clipboard_get()
#        clip.destroy()
#    except:
#        clipb = ''
    return clipb

def AddToQueue(url,urltype,destination_folder):
    global queue
    queue+=[[url,urltype,destination_folder]]

def RemoveFromQueue():
    global queue
    queue.remove(queue[0])

def AddFolder(FolderUrl):
    UserName, FolderName, Galleries = IFUser.ListFolderGalleries(FolderUrl)
    for Gal in Galleries:
        AddToQueue(Gal,4,config.MainDirectory+"/"+config.UserDirectory+"/"+UserName+"/"+FolderName)

def enqeue(url):    
        urltype = CheckUrl(url)
        if urltype:
            if urltype<5:
                ### add url to queue
                if urltype==3:
                    AddToQueue(url,urltype,config.MainDirectory+"/xHamster")
                else:
                    AddToQueue(url,urltype,config.MainDirectory+"/ImageFap")
            elif urltype<7:
                AddFolder(url)
            elif urltype==7:
                Username, Folders = IFUser.ListUserFolders(url)
                for Folder in Folders:
                    AddFolder(Folder[1])

def CheckClipboard():
    ### check if clipboard content has changed
    ### check if the new content is a valid url and add to queue
#    global last_clipboard
    
#    clipboard = PollClipboard()
            
#    if (clipboard!=last_clipboard):
#        last_clipboard=clipboard
    for clipboard in PollClipboard():
        enqeue(clipboard)        
#last_clipboard = PollClipboard()
