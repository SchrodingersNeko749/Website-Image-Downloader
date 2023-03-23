#!/usr/bin/env python3
import os 
import argparse
import requests
from bs4 import BeautifulSoup
import re

def print_options():
    print("\nUsage: imgd [-p,--path <path>] [-u,--url <url>] \nExample \nimgd -p /path/ -u https://mydomain.com/directory/")


# grab the input  

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url", help="the url of the images you want to download")
parser.add_argument("-p","--path", help="the download path")

# # parse the arguments
args = parser.parse_args()

path_name = args.path
url = args.url
if path_name and url:
    try:
        # make get request
         response = requests.get(url)
         # parse html and get image tags
         if response:
             soup = BeautifulSoup(response.text, "html.parser")
             img_tags = soup.find_all("img")

             #make folder and download all images in it
             try:
                 os.mkdir(path_name)
             except FileExistsError:
                 print(path_name,"already exists. skipping folder creation")
             image_counter = 0 # for file naming
             for img in img_tags:
                src = img.get("src")
                if src and re.search(r"\.(jpg|jpeg|png)$", src):
                    filename = re.search(r"/([\w\.-]+)$", src)
                    print(filename.group(1))

                    response = requests.get(src)

                    with open(path_name+filename.group(1), "wb") as f:
                        f.write(response.content)
                    

    except TimeoutError:
        print("didnt get any requests. check if url is correct")

else:
    print("specify a url and a path")
    print_options()

