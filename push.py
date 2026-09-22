#!/usr/bin/env python3

import hashlib
import sys
import shutil
from pathlib import Path
from debian.deb822 import Deb822

REPO_PATH = Path("/home/build/repo/")
IMAGES_PATH = REPO_PATH / "images" / sys.argv[2]

with open("dab.conf") as f:
    dab_conf = Deb822(f)

target = f"{dab_conf['Name']}_{dab_conf['Version']}_{dab_conf['Architecture']}"

# TODO: detect compressor
tarball = target + ".tar.zst"

aplinfo = target + ".aplinfo"

with open(tarball, "rb") as f:
    data = f.read()
    md5sum = hashlib.md5(data).hexdigest()
    sha512sum = hashlib.sha512(data).hexdigest()

aplinfo_str = """Package: {Name}
Version: {Version}
Type: lxc
OS: """ + sys.argv[1] + """
Section: {Section}
Maintainer: {Maintainer}
Architecture: {Architecture}
Location: {Section}/""" + tarball + """
md5sum: """ + md5sum + """
sha512sum: """ + sha512sum + """
Infopage: {Infopage}
Description: {Description}

"""
aplinfo_str = aplinfo_str.format_map(dab_conf)

with open(IMAGES_PATH / aplinfo, "w") as f:
    f.write(aplinfo_str)

shutil.copy(tarball, IMAGES_PATH)
