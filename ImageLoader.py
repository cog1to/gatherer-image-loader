from lxml import html
from lxml import etree
import requests
import os
import sys
from StringIO import StringIO

ColorSelectors = [ ('Gold and Colorless','&color=+[C]'),
                   ('W','&color=+%40(+%5bW%5d)'),
                   ('U','&color=+%40(+%5bU%5d)'),
                   ('B','&color=+%40(+%5bB%5d)'),
                   ('R','&color=+%40(+%5bR%5d)'),
                   ('G','&color=+%40(+%5bG%5d)'),
                   ('Gold and Colorless','&color=+^(|[W]|[U]|[B]|[R]|[G])')
                    ]

class ImageLoader:
    def __init__(self, outputDir, setName, separateByColor = True, delegate = None):
        self.delegate = delegate
        self.separateByColor = separateByColor
        self.setName = setName
        self.url_set_name = setName.replace(' ','+')
        self.template_url = "http://gatherer.wizards.com/Pages/Search/Default.aspx?page={page}&output=spoiler&method=visual&set=%5b{mtgset}%5d"
        self.color_template_url = "http://gatherer.wizards.com/Pages/Search/Default.aspx?output=spoiler&method=visual&action=advanced{color}&set=+%5b\"{mtgset}\"%5d"
        self.url_base = 'http://gatherer.wizards.com'
        self.image_directory_base = outputDir + '/' + setName + ' ' + 'Card Images'

    def createDirs(self):
        if not os.path.exists(self.image_directory_base):
            os.makedirs(self.image_directory_base)
        if self.separateByColor:
            for color in ColorSelectors:
                color_directory = self.image_directory_base + '/' + color[0]
                if not os.path.exists(color_directory):
                    os.makedirs(color_directory)

    def extractCardImagesFromPage(self, url, image_directory):
        card_page = requests.get(url, stream = True)
        card_page.raw.decode_content = True
        card_tree = html.parse(card_page.raw)
        card_images = card_tree.xpath("//img[contains(@src,'multiverseid=')]")
        for image in  card_images:
            imageName = (image.get('alt').replace('!','').replace('//','and').replace('/',''))
            path = image_directory + "/" + imageName + ".png"
            card_url = image.get('src').replace('../..', self.url_base)
            if (self.delegate is not None):
                self.delegate.updateStatus(imageName)
            img_data = requests.get(card_url, stream=True)
            if img_data.status_code == 200:
                with open(path, 'wb') as f:
                    for chunk in img_data.iter_content(1024):
                        f.write(chunk)

    def loadImages(self):
        self.createDirs()
        for color in ColorSelectors:
            page_url = self.color_template_url.format(page=0,mtgset=self.url_set_name,color=color[1])
            image_dir = (self.image_directory_base + '/' + color[0]) if self.separateByColor else self.image_directory_base
            page = requests.get(page_url, stream=True)
            page.raw.decode_content = True
            tree = html.parse(page.raw)
            page_links = tree.xpath("//div[@class='paging']/a")
            if page_links == []:
                self.extractCardImagesFromPage(page_url,image_dir)
            else:                
                for page in page_links:
                    page_url = self.url_base + page.get('href')
                    self.extractCardImagesFromPage(page_url, image_dir)
        if (self.delegate is not None):
                self.delegate.downloadfinished()
