#!/usr/bin/env python3

import os
import requests
from sys import argv
import shutil
import urllib.request
from posixpath import join as urljoin

# Constants
DL_LOC = os.path.join(os.path.dirname(os.path.realpath(__file__)), "dl/")

# Input
if len(argv) < 2:
    print("Usage: {} <yiffer.xyz comic url>".format(argv[0]))
    exit(1)

url = argv[1]
#dl = argv[2]

def download_comic(url, DL_LOC):
    # Vars
    img_id = 1
    err = None

    # Get comic name and create dir in dl/
    cname = url.split("/")[-1].replace("%20", "_")
    try:
        os.mkdir(DL_LOC + "/" + cname)
    except:
        print("Comic directory already exists: '{}'".format(cname))

    # Iterate until error (not graceful but works TM)
    while err is None:
        err = download_image(url, DL_LOC, cname, img_id)
        img_id = img_id + 1

def download_image(url, DL_LOC, cname, img_id):
    # Parse URL
    # format: ../comics/<comic name>/xxx.jpg
    img_url = urljoin(
        "comics/", 
        url.split("/")[-1], 
        "{0:03d}.jpg".format(img_id))
    url_parsed = urllib.parse.urlparse(url)
    base_url = '{uri.scheme}://static.{uri.netloc}/'.format(uri=url_parsed)
    dl_url = urljoin(base_url, img_url)

    # Check image exists
    if os.path.isfile(os.path.join(DL_LOC + "/" + cname + "/" + '{}'.format(img_id) + ".jpg")):
        print("Image already exists: {}".format(img_id) + ".jpg")
        return None

    # Download image
    res = requests.get(dl_url, stream = True)

    # Save if res is OK
    if res.status_code == 200:
        # Save image
        with open(DL_LOC + "{}".format(img_id) + ".jpg", 'wb') as f:
            res.raw.decode_content = True
            shutil.copyfileobj(res.raw, f)
        print('Downloaded image ' + '{}'.format(img_id))
    else:
        print('Error: Image ' + '{}'.format(img_id) + ' could not be retrieved')
        return res.status_code

if __name__ == "__main__":
    # Make sure the dl directory exists
    try: os.mkdir(DL_LOC)
    except: pass

    # Run script
    download_comic(url, DL_LOC)
