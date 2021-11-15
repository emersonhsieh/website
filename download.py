# Downloads images, puts them in the images directory, replaces text in image
import re

import requests
import shutil

with open('trains/index.html') as f:
    lines = f.readlines()
    # print(lines)

# https://stackoverflow.com/a/169631

images_list = []

for line in lines:
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    urls = re.findall(regex, line)

    # trim two characters on end
    
    if len(urls) > 0:
        for tuple in urls:
            for url in tuple:
                url_temp = url.strip('"/')
                if url_temp.endswith('.png') or url_temp.endswith('.jpg'):
                    images_list.append(url_temp)
    

images_set_list = []
[images_set_list.append(x) for x in images_list if x not in images_set_list]

# https://towardsdatascience.com/how-to-download-an-image-using-python-38a75cfa21c

new_lines = lines

for i in range(0,len(images_set_list)):
    url = images_set_list[i]
    image_name = "trains/images/image_{}.png".format(str(i).zfill(5))

    r = requests.get(url, stream = True)

    if r.status_code == 200:
        r.raw.decode_content = True
        with open(image_name,'wb') as f:
            shutil.copyfileobj(r.raw, f)

    new_lines = [line.replace(url, image_name) for line in new_lines]

with open('trains/index2.html', 'w') as f:
    for line in new_lines:
        f.write(line)