'''
Author: William Zhizhuo Yin
Data: 07/04/2023
'''

import argparse
import os
import time

def skybox_generator(apikey, prompt, literature):
    import urllib.parse
    import urllib.request
    from urllib.request import urlretrieve
    import requests
    import json

    url = "https://backend.blockadelabs.com/api/v1/skybox"
    request = {'prompt': prompt, 'skybox_style_id':5}
    header = {"x-api-key": apikey}
    post_param = urllib.parse.urlencode(request).encode('UTF-8')
    req = urllib.request.Request(url, post_param, header)
    styles = requests.get("https://backend.blockadelabs.com/api/v1/skybox/styles", headers=header)
    response = urllib.request.urlopen(req)

    response = json.loads(response.read().decode())
    time.sleep(30)
    download_url = "https://backend.blockadelabs.com/api/v1/imagine/requests/"+str(response['id'])
    contents = requests.get(download_url, headers=header).content.decode()#urllib.request.urlopen(download_url).read()
    file_url = json.loads(contents)['request']['file_url']
    skybox_file = "/skybox.jpg"
    skybox_filepath = "./tmp_file/resource/images"
    if not os.path.exists(skybox_filepath):
        os.makedirs(skybox_filepath)
    output_filepath = "./tmp_file/resource/images/" + literature + ".jpg"
    indiv_filepath = "./tmp_file/" + str(literature) + "/resource/images"
    if not os.path.exists(indiv_filepath):
        os.makedirs(indiv_filepath)

    urlretrieve(file_url, skybox_filepath+skybox_file)

    os.system("cp " + skybox_filepath+skybox_file + " " + output_filepath)
    os.system("cp " + skybox_filepath+skybox_file + " " + indiv_filepath+skybox_file)

    return True

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--apikey",
        type=str,
        nargs="?",
        default="<apikey>",
        help="apikey of skybox generation"
    )
    parser.add_argument(
        "--prompt",
        type=str,
        nargs="?",
        default="a professional photograph of an astronaut riding a triceratops",
        help="the prompt to render"
    )
    opt = parser.parse_args()
    opt.prompt = "In the middle of dissert with shiny sun"
    skybox_generator(opt.apikey, opt.prompt, "madmax")


