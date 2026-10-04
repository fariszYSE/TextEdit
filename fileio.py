import textedit
import os
import logging

logging.basicConfig(
    filename="debug.log",
    level=logging.DEBUG
)
def readfile():
    try:
        logging.info("file read")
        with open(textedit.file_name,"r") as f:
            textedit.file = f.read().splitlines()
    except:
        logging.warning("attempted to read, file not found so file written instead")
        writefile()
def writefile():
    with open(textedit.file_name,"w") as f:
        logging.info(f"wrote data to file\nnew file data is:\n{textedit.file}\n")
        textedit.testgrid = "".join(textedit.testgrid)
        f.write("\n".join(textedit.file))
