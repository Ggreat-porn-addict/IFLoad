ImageFap Gallery Downloader

Usage: 
Launch the .py script (or .exe if you are using the "compiled" version) 
and let it run in the background. When you copy the gallery link to the 
clipboard, the download will start automatically. The default download 
directory is named 'Galleries' and is created in the ImageFap Gallery 
Downloader main folder. The downloader will recognize the gallery title 
and save the gallery in the main download directory. When you are done, 
just close the console window.

In order to download user folders in v0.4, open the user profile, follow 
the 'Galleries' link and copy the folder link from the sidebar to the 
clipboard. Download everything from a user by copying the user profile link.

The main download directory can be specified in "IFLoad.config" by 
setting MainDirectory="path to directory".


Version history:

v0.4 - 11/15/2015

added:
+ download entire user collections or specific user folders

v0.3 - 9/17/2015

added:
+ xHamster gallery support
+ handling of failed downloads


v0.22 - 9/16/2015

fixed:
- incorrect usage of Tk().clipboard_get leading to 
"unable to realloc x bytes" crash after a few thousand calls
- second download request is ignored if the time interval 
between the first and the second request is too short


v0.21 - 9/16/2015

fixed:
- crash if gallery title starts or ends with a blank character


v0.2 - 9/16/2015

added:
+ external config file
+ now the user can specify the main download directory in the config file
+ new download requests are enqueued while the downloader is busy


v0.11 - 9/14/2015

fixed:
- TclError crash when clipboard is empty
- Output directory naming

added:
+ now also working with url from the browser address bar (via select&copy)


v0.1 - first release 9/13/2015

Downloader will watch the clipboard content and download a gallery when 
the url is copied to the clipboard.

gallery url must be of the format
_http://www.imagefap.com/gallery.php?gid=<gallery id number>_

known bugs:
- downloader will crash with a TclError when clipboard is empty
- download of a gallery will not start if the url has been copied 
to the clipboard prior to the execution of the downloader
- problem with the creation of the target directory. sometimes, 
subdirectories are created in the main gallery dir and files are 
placed in the subdirectory