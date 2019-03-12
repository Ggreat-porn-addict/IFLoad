# -*- coding: cp1252 -*-

### ImageFap Gallery Downloader
### image gallery processing

import config
import urlqueue
import download
import request
import sys
import time

def GetGalleryId(url, gidtype = 1):
    ### gidtype: 1=imagefap1, 2=imagefap2, 3=xhamster, 4=imagefap3
    
    if (gidtype==1):
        gid_index = url.find('gid=')
        gid = url[gid_index+4:]
        
    if (gidtype==2):
        n = url.find(config.GalleryLink2)
        l = len(config.GalleryLink2)
        gid = url[n+l:url.find('/',n+l)]
        
    if (gidtype==3):
        start = url.find('gallery')+8
        end = url.find('/',start)
        gid = url[start:end]

    if (gidtype==4):
        start = url.find("gallery/")
        gid = url[start+len("gallery/"):]
        
    return gid

def RemoveBlank(string):
    Str = string
    while True:
        if (Str.startswith(' ')):
            Str = Str[1:]
        else: break

    while True:
        if (Str.endswith(' ')):
            Str = Str[:len(Str)-1]
        else: break

    return Str

def GetGalleryTitle(data,gallerytype):
    title_start = data.find('<title>')
    title_end = data.find('</title>',title_start)
    PageTitle = data[title_start+7:title_end]

    ### format the gallery title 
    if (gallerytype==3):
        _galtitle = PageTitle[:len(PageTitle)-15]
    else:
        q = PageTitle.find(' (Page')
        if (q!=-1):
            _galtitle = PageTitle[13:q]
        else:
            _galtitle = PageTitle

    ### remove forbidden characters so the title can be
    ### used as folder name
    gallerytitle=''

    char_allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789ÄÖÜäöü#+~.,-_^!§$%&()={}[]@ "
    
    for char in _galtitle:
        if char in char_allowed: gallerytitle+=char

    ### remove blank characters from start and end of title string
    gallerytitle = RemoveBlank(gallerytitle)
    
    return gallerytitle

def NextPage_IF(PageContent,gid,currentpage):
    ### check for a link to the next page of an ImageFap gallery.
    ### returns 0 if no link is found, otherwise returns
    ### a string containing the url.
    np_index_start = PageContent.find('page='+str(currentpage+1))
    if (np_index_start==-1):
        return 0
    else:
        np_index_start = PageContent.find(config.GalleryLink2)
        np_index_end = PageContent.find("'",np_index_start)
        url1 = PageContent[np_index_start:np_index_end]
        url2 = '?gid='+str(gid)+'&page='+str(currentpage+1)+'&view=0'
        return url1+url2

def GetImageList_IF(url,gid):
    ### returns list of images in ImageFap gallery page content
    UrlList=[]

    PageContent = request.ReqUrl(url, 'utf-8')

    p = 0
    
    while True:
        ### iterate through gallery pages
        index_begin=0
        index_end=0
        pics = []
        while True:
            ### find html entries with 'idx=' string indicating image link
            index_begin = PageContent.find('idx=',index_end)
            if (index_begin==-1): break
            
            index_end = PageContent.find('"',index_begin)
            i = index_begin
            while (PageContent[i]!='"'):
                i=i-1
            pic = PageContent[i+1:index_end]
            if (len(pic)>1): pics+=[str(config.baseurl)+pic]
        UrlList+=pics
        
        np_url = NextPage_IF(PageContent,gid,p)
        
        if (np_url==0):
            break
        else:
            url = np_url
            #print url
            p+=1
            PageContent = request.ReqUrl(url, 'utf-8')
    return UrlList

def GetImageList_xH(url,gid):
    ### returns list of images in xhamster gallery
    UrlList=[]
    PageContent = request.ReqUrl(url, 'utf-8')

    imglink_begin=0
    imglink_end=0
    pics = []

    while True:
        ### find location of image page link
        index_link = PageContent.find("photo-container photo-thumb",imglink_end)
        if (index_link==-1): break 
        imglink_begin = PageContent.find("href=",index_link)+6
        imglink_end = PageContent.find("\"",imglink_begin)
        pic = PageContent[imglink_begin:imglink_end]
        if (len(pic)>1): pics+=[pic]
    UrlList+=pics
    return UrlList

def GetImageUrl_IF(UrlList, UrlNum):
    ### get image source url (ImageFap)
    PageContent = request.ReqUrl(UrlList[UrlNum], 'utf-8')
    url_index = PageContent.find('contentUrl')
    url_start = PageContent.find('https://',url_index)
    url_end = PageContent.find('"',url_start)
    return PageContent[url_start:url_end]

def GetImageUrl_xH(UrlList, UrlNum, session):
    ### get image source url (xHamster)
    #PageContent = request.ReqUrl(UrlList[UrlNum], 'utf-8')
    r = session.get(UrlList[UrlNum])
    r.html.render(timeout=90)
    PageContent = r.html.html
    url_index = PageContent.find("fotorama__loaded--img")
    url_start = PageContent.find("https://",url_index)
    url_end = PageContent.find("\"",url_start)
    return PageContent[url_start:url_end]
    
def OpenGallery(Gal_Url, urltype):
    ### get gallery title and list of image urls
    url = Gal_Url
    gid = GetGalleryId(url,urltype)
    PageContent = request.ReqUrl(url, 'utf-8')
    
    ### read gallery title from html content
    GalTitle = GetGalleryTitle(PageContent,urltype)

    ### get image list from gallery page
    if (urltype==3):
        UrlList = GetImageList_xH(url,gid)
    else:
        UrlList = GetImageList_IF(url,gid)    
    
    return GalTitle, UrlList

def DownloadGallery():
    from requests_html import HTMLSession
    session = HTMLSession()
    while (len(urlqueue.queue)>0):
        ### get first element from url queue
        Gal_Url = urlqueue.queue[0][0]
        urltype = urlqueue.queue[0][1]
        destination_folder = urlqueue.queue[0][2]
        GalTitle, UrlList = OpenGallery(Gal_Url, urltype)
        output_dir = destination_folder+"/"+GalTitle
        
        urlqueue.CheckClipboard()

        N = len(UrlList)
        print("Downloading "+str(N)+" images from "+Gal_Url)
        
        for j in range(N):
            if (urltype==3):
                url = GetImageUrl_xH(UrlList,j,session)
            else:
                url = GetImageUrl_IF(UrlList,j)
                
            if download.DownloadImage(url,output_dir):
                sys.stdout.write(".")
            else:
                sys.stdout.write("x")
                
            sys.stdout.flush()
            urlqueue.CheckClipboard()

        ### remove first element from url queue after download
        urlqueue.RemoveFromQueue()
        print("\n"+"Done"+"\n")

