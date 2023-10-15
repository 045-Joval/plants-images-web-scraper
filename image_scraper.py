import requests
from bs4 import BeautifulSoup
import os

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
def image_download(folder):
    global image_url
    url = 'https://commons.wikimedia.org/w/index.php?search={}&title=Special:MediaSearch&type=image&filemime=jpeg'.format(folder.replace(' ','+'))
    try:
        os.mkdir(os.path.join(os.getcwd(),"plants-images"))
    except:
        pass

    try:
        os.mkdir(os.path.join(os.getcwd(),"plants-images",folder))
    except:
        pass

    os.chdir(os.path.join(os.getcwd(),"plants-images",folder))
    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    images = soup.find_all('img')

    i = 0
    for image in images:
        i += 1
        name = folder + str(i) + '.jpg'
        try:
            image_url = image['src']
        except:
            pass
        if i==21:
            break
        with open(name, 'wb') as f:
            try:
                img = requests.get(image_url, headers=headers)
                f.write(img.content)
            except:
                pass
    os.chdir('..')
    os.chdir('..')

