#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import os
import subprocess
import platform
import shutil

from os.path import exists

CWD=os.getcwd()
DRAWIO="drawio --export"
if platform.system() == "Darwin":
    DRAWIO="/Applications/draw.io.app/Contents/MacOS/draw.io --export"
elif ("DISPLAY" not in os.environ or len(os.environ["DISPLAY"].strip()) == 0):
    DRAWIO=f"docker run -w /data -v {CWD}/drawings:/data rlespinasse/drawio-desktop-headless --export"

tree = ET.parse("drawings/firewall demo.drawio")
page_index = 0
for e in tree.findall("diagram"):
    try:
        options = f"--page-index {page_index} --output \"/data/{e.attrib['name']}.png\" --transparent \"/data/firewall demo.drawio\""
        subprocess.run(f"{DRAWIO} {options}", shell=True, check=True, capture_output=True)
        if exists(f"drawings/{e.attrib['name']}.png"):
            shutil.copy(f"drawings/{e.attrib['name']}.png", f"drawings/{e.attrib['name']}.png.new")
            os.remove(f"drawings/{e.attrib['name']}.png")
            os.rename(f"drawings/{e.attrib['name']}.png.new", f"drawings/{e.attrib['name']}.png")
        page_index+=1
    except subprocess.CalledProcessError as e:
        print("Process failed")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        raise e
