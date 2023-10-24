from bs4 import BeautifulSoup
import requests
import os 
from PIL import Image
from io import BytesIO

def is_valid_image(binary_data):
    try:
        # Create a BytesIO object and load the binary data into it
        image_data = BytesIO(binary_data)
        
        # Try to open the image
        with Image.open(image_data) as img:
            # If the image can be opened, it's a valid image
            return True
    except Exception as e:
        # If an exception occurs, it's not a valid image
        return False
    
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

def image_download(search_string):
    r = requests.get('https://www.bing.com/images/search?q={}'.format(search_string),headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    attribs = soup.findAll('a')
    image_urls=[]
    for items in attribs:
        try:
            data=eval(items['m'])
            image_urls.append(data['murl'])
        except:
            pass
    try:
        os.mkdir(os.path.join(os.getcwd(),'plants-images'))
        os.mkdir(os.path.join(os.getcwd(),'plants-images',search_string))
    except:
        pass
    os.chdir(os.path.join(os.getcwd(),'plants-images',search_string))
    i=0
    for image_url in image_urls:
        i+=1
        if i==21:
            break
        name = search_string + '_' + str(i) + '.jpg'
        try:
            img = requests.get(image_url, headers=headers)
            if is_valid_image(img.content):
                try:
                    with open(name, 'wb') as f:
                        f.write(img.content)
                except:
                    pass
            else:
                i-=1
                continue
                
        except:
            i-=1
            continue

    os.chdir('..')
    os.chdir('..')
