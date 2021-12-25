import io
import TS
import uuid
import json
import flask
import base64
import imghdr
import datetime
import yagmail
import firebase_admin
from flask_cors import CORS
from firebase_admin import db
from flask import request, render_template, url_for
firebase_admin.initialize_app(firebase_admin.credentials.Certificate("./auth.json"), {"databaseURL": "https://tensorshareio-default-rtdb.firebaseio.com/"})
app = flask.Flask(__name__)
mac = yagmail.SMTP(user=TS.email.auth.mail, password=TS.email.auth.pwd)
CORS(app, resources={"/*": {"origins": "*"}})
def get_tokens():
    return db.reference("/tokens").get()

@app.route("/waitlist", methods=["GET"])
def waitlist():
    return render_template("waitlist.html", endpoint=TS.sys.endpoint)

@app.route("/waitlist/add_user", methods=["PUT"])
def waitlist_add_user():  # sourcery skip: remove-unnecessary-else, simplify-fstring-formatting, swap-if-else-branches
    if TS.email.getFormated(request.args.get("email")) in db.reference("/waitlist/emails").get():
        return json.dumps({"error": "Email already in waitlist", "code": 32})
    email = request.args.get("email")
    femail = TS.email.getFormated(email)
    name = request.args.get("name")
    utk = str(uuid.uuid4()).replace("-", ".")
    html = f"""
        <img src="{TS.sys.endpoint}/waitlist/thanks/image" alt="Thank you, {name}">
        <h1>Hello, {name}, you've been added to the waitlist.</h1>
        <p>We sent you this email as a confirmation for your subscription to the TensorShare waitlist!</p>
        <p>If you did not wish to be added to the waitlist, you may click <a href="{TS.sys.endpoint}/waitlist/unsubscribe/?utk={utk}&email={email}">here</a> to unsubscribe</p>
    """
    mac.send(to=email, subject=f"Hello, {name}, you've been added to the waitlist.", contents=[html])
    db.reference(f"/waitlist/emails/{femail}").set({
        "confirmed": "true",
        "utk": utk,
        "email": email,
        "name": name
    })
    return json.dumps({"success": True})

@app.route("/waitlist/remove_user", methods=["DELETE"])
def waitlist_remove_user():
    if TS.email.getFormated(request.args.get("email")) in db.reference("/waitlist/emails").get():
        if db.reference("/waitlist/emails/"+TS.email.getFormated(request.args.get("email"))).get()["utk"] == request.args.get("utk"):
            data = db.reference("/waitlist/emails/"+TS.email.getFormated(request.args.get("email"))).get()
            db.reference("/waitlist/emails/"+TS.email.getFormated(request.args.get("email"))).delete()
            return json.dumps({"success": True, "name": data["name"], "email": data["email"]})
    return json.dumps({"error": "Email not in database", "success": False, "code": 404})

@app.route("/waitlist/unsubscribe/", methods=["GET"])
def waitlist_unsubscribe():
    email = request.args.get("email")
    femail = TS.email.getFormated(email)
    if TS.email.getFormated(email) in db.reference("/waitlist/emails").get():
        data = db.reference(f"/waitlist/emails/{femail}").get()
        return flask.render_template("unsubscribe.html", name=data["name"].split(" ")[0])
    return flask.redirect("/waitlist")

@app.route("/waitlist/thanks", methods=["GET"])
def waitlist_thanks():
    email = request.args.get("email")
    emailProvider = email.split("@")[-1]
    return render_template("thanks.html", name=request.args.get("name", db.reference("/waitlist/emails/"+TS.email.getFormated(email)).get()["name"]) , email=email, emailProvider=f"https://{emailProvider}")

@app.route("/waitlist/sorry")
def waitlist_sorry():
    email = request.args.get("email")
    return render_template("sorry.html", email=email, name=request.args.get("name", "Unknown user"))

@app.route("/waitlist/thanks/image", methods=["GET"])
def waitlist_thanks_image():
    return flask.send_file("./static/thanks.png")

@app.route("/post/image/", methods=["GET", "POST"])
def post_image():  # sourcery skip: simplify-fstring-formatting
    if request.args.get("token") not in get_tokens().keys():
        return json.dumps({"error": "Unauthorized"})

    if request.data and ";base64," not in str(request.data) and ";base64," not in request.args.get("data", ""):
        data = request.data
    elif not request.data and ";base64," in request.args.get("data"):
        try:
            data = base64.b64decode(request.args.get("data",  "").split(";base64,")[-1].replace(" ", "+"))
        except:
            return json.dumps({"error": "Couldn't decode base64 string"})
    elif ";base64," in str(request.data):
        try:
            data = base64.b64decode(str(request.data).split(";base64,", "")[-1].replace(" ", "+"))
        except:
            return json.dumps({"error": "Couldn't decode base64 string"})
    else:
        data = None

    if io.BytesIO(data).getbuffer().nbytes > TS.sys.maxSize and request.args.get("token") != db.reference("/tokens/master").get():
        return json.dumps({"error": "Data exceeds size limit."})

    uid = TS.new.image_id()
    fmt = imghdr.what(None, data)
    
    if fmt:
        if request.args.get("by") not in {"anon", "anonymous"} and request.args.get("anon") != "true":
            ub = (
                request.args.get("by")
                or get_tokens()[request.args.get("token")]["belongsTo"]
            )
        else:
            ub = "an Anonymous user"

        if data:
            finalData = TS.image.getData(data, ub, uid)
        else:
            return json.dumps({"error": "Invalid data URL or body (data URL must be in base64 or body must be in binary)."})
        db.reference(f"/images/{uid}").set(finalData)
        return json.dumps({"success": True, "url": f"{TS.sys.endpoint}/{uid}.{fmt}"})

    else:
        return json.dumps({"error": "Media type not supported"})

@app.route("/<img>/", methods=["GET"])
def view(img: str): # sourcery skip: collection-builtin-to-comprehension, remove-redundant-if, remove-unnecessary-else, swap-if-else-branches
    image = img.split(".")[0]
    got = db.reference(f"/images/{image}").get()
    
    if got:
        if TS.request.is_from_browser(request.user_agent):
            if "b64" not in got:
                b64im = str(base64.b64encode(got["data"].encode(TS.config.encoding.fmt)))[2:-1]
            else:
                b64im = got["b64"]
            return render_template(
                "main.html",
                name=image,
                nameU=image.upper(),
                data=b64im,
                fmt=got["fmt"],
                fmtU=got["fmt"].upper(),
                uploadedBy=got["uploadedBy"]["name"],
                iat=str(datetime.datetime.now()) if "iat" not in got else got["iat"],
                size="0" if "size" not in got else got["size"],
                colData="0,0,0;0,0,0;0,0,0;0,0,0;:0,0,0" if "colData" not in got else got["colData"],
                dimen="0,0" if "dimen" not in got else got["dimen"],
                exif="{}" if "exif" not in got else got["exif"],
                endpoint=TS.sys.endpoint
            )
        else:
            return flask.send_file(io.BytesIO(got["data"].encode(TS.config.encoding.fmt)), mimetype="image/"+str(got["fmt"]))
    else:
        return flask.send_file("./static/404.png")

@app.route("/<img>/file/", methods=["GET"])
def img_file(img: str):
    image = img.split(".")[0]
    got = db.reference(f"/images/{image}").get()
    if got:
        return flask.send_file(io.BytesIO(got["data"].encode(TS.config.encoding.fmt)), mimetype="image/"+str(got["fmt"]))
    else:
        return flask.send_file("./static/404.png")

@app.route("/<img>/data/") 
def image_data(img: str):
    return json.dumps(db.reference(f"/images/{img}").get())

@app.route("/404", methods=["GET"])
def _404():
    return flask.send_file("./static/404.png")

@app.route("/favicon.ico/", methods=["GET"])
def icon():
    return flask.send_file("favicon.ico")

if __name__ == '__main__':
    app.run()