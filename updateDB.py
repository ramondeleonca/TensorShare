# sourcery skip: simplify-fstring-formatting
from PIL import Image, ExifTags
import io
import firebase_admin
import datetime
import json
import base64
import TS
import os
from firebase_admin import db
firebase_admin.initialize_app(firebase_admin.credentials.Certificate("./auth.json"), {"databaseURL": "https://tensorshareio-default-rtdb.firebaseio.com/"})
imgs = db.reference("/images/").get()
for im in imgs:
    curr = imgs[im]
    fmt = curr["fmt"]
    with open(f"./temp/{im}.{fmt}", "x"):
        with open(f"./temp/{im}.{fmt}", "wb") as f:
            f.write(curr["data"].encode(TS.config.encoding.fmt))

    # w, h = Image.open(f"./temp/{im}.{fmt}").size
    db.reference(f"/images/{im}").update({
        # "iat": str(datetime.datetime.now()),
        # "size": str(io.BytesIO(curr["data"].encode(TS.config.encoding.fmt)).getbuffer().nbytes),
        # "b64": str(base64.b64encode(curr["data"].encode(TS.config.encoding.fmt)))[2:-1],
        # "colData": TS.image.getColorData(f"./temp/{im}.{fmt}"),
        # "dimen": f'{str(w)},{str(h)}',
        "exif": json.dumps({ExifTags.TAGS[k]: v for k, v in Image.open(f"./temp/{im}.{fmt}").getexif().items() if k in ExifTags.TAGS})
    })
    os.remove(f"./temp/{im}.{fmt}")