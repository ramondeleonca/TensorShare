from PIL import Image, ExifTags
import json
import os
import datetime
import io
import base64
import colorthief
import imghdr
import uuid

from werkzeug.user_agent import UserAgent
class config:
    class encoding:
        fmt: str = "ISO-8859-1"
class sys:
    endpoint: str = "http://localhost:5000"
    maxSize: int = 5242880
class image:
    def getColorData(fn: str | bytes, cols: int = 3) -> str:
        if isinstance(fn, str):
            ct = colorthief.ColorThief(fn)
        else:
            ct = colorthief.ColorThief(Image.open(fn))
        pl = "".join(f'{col[0]},{col[1]},{col[2]};' for col in ct.get_palette(cols))
        cl = str(ct.get_color()).replace("(", "").replace(")", "").replace(" ", "")
        return pl+":"+cl
    def getData(data: bytes, ub: str="Unknown", uid: str=None):
        """Returns all image data **modularly**"""
        if not uid:
            uid = new.image_id()
        ed = data.decode(config.encoding.fmt)
        fmt = imghdr.what(None, data)
        with open(f"./temp/{uid}.{fmt}", "x"):
            with open(f"./temp/{uid}.{fmt}", "wb") as f:
                f.write(data)
        w, h = Image.open(f"./temp/{uid}.{fmt}").size
        exif = json.dumps({ExifTags.TAGS[k]: v for k, v in Image.open(f"./temp/{uid}.{fmt}").getexif().items() if k in ExifTags.TAGS})
        colData = image.getColorData(f"./temp/{uid}.{fmt}")
        os.remove(f"./temp/{uid}.{fmt}")
        return {
                "data": ed,
                "fmt": fmt,
                "uploadedBy": ub,
                "iat": str(datetime.datetime.now()),
                "size": str(io.BytesIO(data).getbuffer().nbytes),
                "b64": str(base64.b64encode(data))[2:-1],
                "colData": colData,
                "dimen": f'{str(w)},{str(h)}',
                "exif": exif
            }
class email:
    def getFormated(email: str) -> str:
        """Returns an email formatted as a database key"""
        return email.replace(".", "!DOT").replace("@", "!AT")
    def unFormated(email: str) -> str:
        """Returns an email formatted from a database key"""
        return email.replace("!DOT", ".").replace("!AT", "@")
    class auth:
        mail: str = "tensorshare@gmail.com"
        pwd: str = "Cryonixyoutube1TensorSpark"
class new:
    def image_id() -> str:
        return str(uuid.uuid4()).split("-")[0]
class request:
    def is_from_browser(user_agent: UserAgent) -> bool:
        return user_agent.browser in [
            "camino",
            "chrome",
            "firefox",
            "galeon",
            "kmeleon",
            "konqueror",
            "links",
            "lynx",
            "msie",
            "msn",
            "netscape",
            "opera",
            "safari",
            "seamonkey",
            "webkit",
            "vivaldi",
            "brave"
        ] 