import requests, re, json, os
from PIL import Image
from io import BytesIO

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36",
}


def resize_image(binary_data, image_path, new_size):
    try:
        image_data = BytesIO(binary_data)
        with Image.open(image_data) as img:
            resized_img = img.resize(new_size)
            resized_img.save(image_path)
            return True
    except Exception as e:
        return False


def image_download(search_string, license_type, num_of_images, image_size):
    search_string = search_string.lower()
    params = {
        "q": search_string,  # search query
        "tbm": "isch",  # image results
        "hl": "en",  # language of the search
        "gl": "us",  # country where search comes from
    }
    if license_type == 1:
        params.update({"tbs": "il:cl"})
    elif license_type == 2:
        params.update({"tbs": "il:ol"})
    html = requests.get("https://google.com/search", params=params, headers=headers, timeout=30)
    matched_images_data = "".join(re.findall(r"AF_initDataCallback\(([^<]+)\);", html.text))
    param = matched_images_data.encode().decode('unicode_escape')
    image_info_pattern = re.compile(r'\[\[{\"\d+\":.*?}\]\]')
    image_info = image_info_pattern.findall(param)
    images_url = []
    image_license_details = []
    return_data = []
    for test in image_info:
        try:
            json_data_needed = list(json.loads(test)[0][0].values())[0][1]
            images_url.append(json_data_needed[3][0])
            license_data = max(json_data_needed[25].values(),key=len)
            filtered_data = [x for x in license_data if x not in (None, False, True)]
            image_license_details.append(filtered_data)
        except:
            pass

    try:
        os.mkdir(os.path.join(os.getcwd(), 'plants-images'))
    except:
        pass
    try:
        os.mkdir(os.path.join(os.getcwd(), 'plants-images', search_string))
    except:
        pass
    os.chdir(os.path.join(os.getcwd(), 'plants-images', search_string))
    i = 0
    for image_url, image_info in zip(images_url, image_license_details):
        i += 1
        if i == num_of_images + 1:
            break
        name = search_string + '_' + str(i)
        try:
            img = requests.get(image_url, headers=headers, timeout=30)
            if resize_image(img.content, name + '.jpg', image_size):
                with open(name + '.json', 'w') as f:
                    f.write(json.dumps(image_info, indent=2))
                image_path = os.path.join('plants-images', search_string, name + '.jpg')
                json_path = os.path.join('plants-images', search_string, name + '.json')
                return_data.append((image_path, json_path))
            else:
                i -= 1
                continue
        except:
            i -= 1
            continue

    os.chdir('..')
    os.chdir('..')
    print(return_data)
    return return_data
