from bs4 import *
import requests
import os

def create_folder(images):
    try:
        folder_name = input('Enter Folder Name: ')
        
        if os.path.exists(folder_name):
            os.remove(folder_name)
        
        os.mkdir(folder_name)
        
        download_images(images,folder_name)
    except:
        print(f'Folder {folder_name} already exists')
        create_folder(images)
        
def download_images(images,folder_name):
    print(f'Total {len(images)} Images')
    try:
        count = 0
        if len(images) != 0:

            image_link = None
            imageTag = ['data-srcset','data-src','data-fallback-src','src']
            for i,image in enumerate(images):
                for key in imageTag:
                    
                    if key in image.attrs:
                        image_link = image[key] if image[key] != '' else None
                        break
                    
                if image_link is not None:
                    ext = image_link.split('.')[3]
                    r = requests.get(image_link)
                    if r.status_code == 200:
                        with open(f'{folder_name}/images{i+1}.jpg','wb+') as file:
                            file.write(r.content)

                        count +=1

            if count == len(images):
                print('All images Downloaded')
            else:
                print(f'Total {count} images downloaded out of {len(images)} Images')
    except Exception as error:
        print(error)
                           

def main(url):
    r = requests.get(url)
    
    soup = BeautifulSoup(r.text,'html.parser')
    
    images = soup.findAll('img')
    
    create_folder(images)