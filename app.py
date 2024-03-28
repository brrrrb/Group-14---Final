import os
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# Personal and Business form directories and allowed extentions
Images = os.path.join("static", "images")
Extensions = {"png", "jpg", "jpeg"} 

@app.get('/')
def index():
    return render_template('index.html')

# Business form submission
@app.route("/business_post_form", methods=["GET", "POST"])
def business_post_form():
    # Collects information from user's submitted form
    if request.method == "POST":
        if not request.form.get("agreementCheck"):
            return redirect(url_for("business_post_form"))
        post = {
            "title": request.form.get("postTitle"),
            "country": request.form.get("countryVisited"),
            "category": request.form.get("eventCategory"),
            "description": request.form.get("postDescription"),
            "address_line_1": request.form.get("addressLine1"),
            "address_line_2": request.form.get("addressLine2"),
            "city": request.form.get("city"),
            "state": request.form.get("state"),
            "website_link": request.form.get("websiteLink"),
            "phone_number": request.form.get("phoneNumber"),
            "email": request.form.get("email"),
            "hours_of_operation": request.form.get("hoursOfOperation"),
            "agreement_check": request.form.get("agreementCheck"),
        }
        # Uploads image file
        file = request.files.get("addPictures")
        if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in Extensions: # Makes sure extention is correct
            filepath = os.path.join(Images, file.filename)
            file.save(filepath)
            post["image_filename"] = file.filename
            return render_template("view_business_post.html", post=post)

    return render_template("business_post_form.html")

# Personal form submission
@app.route("/personal_post_form", methods=["GET", "POST"])
def personal_post_form():
    # Collects information from user's submitted form
    if request.method == "POST":
        if not request.form.get("agreementCheck"):
            return redirect(url_for("personal_post_form"))
        post = {
            "title": request.form.get("postTitle"),
            "country": request.form.get("countryVisited"),
            "category": request.form.get("eventCategory"),
            "description": request.form.get("postDescription"),
            "rating": request.form.get("inlineRadioOptions"),
            "trip_purpose": request.form.get("purposeOfTrip"),
            "time_of_visit": request.form.get("timeOfVisit"),
            "agreement_check": request.form.get("agreementCheck"),
        }
        # Uploads image file
        file = request.files.get("addPictures")
        if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in Extensions:  # Makes sure extention is correct
            filepath = os.path.join(Images, file.filename)
            file.save(filepath)
            post["image_filename"] = file.filename
            return render_template("view_personal_post.html", post=post)



    return render_template("personal_post_form.html")

#Discover Page
@app.route('/DiscoverPage')
def discover_page():
    return render_template('discover_page.html')

#Different Countries
@app.route('/PuertoRico')
def puerto_rico():
    return render_template('countries/PuertoRico.html')
@app.route('/Italy')
def italy():
    return render_template('countries/Italy.html')
@app.route('/Greece')
def greece():
    return render_template('countries/Greece.html')
@app.route('/Hawaii')
def hawaii():
    return render_template('countries/Hawaii.html')
@app.route('/Jamaica')
def jamaica():
    return render_template('countries/Jamaica.html')
@app.route('/US')
def us():
    return render_template('countries/US.html')
@app.route('/Canada')
def canada():
    return render_template('countries/Canada.html')
@app.route('/Australia')
def australia():
    return render_template('countries/Australia.html')
@app.route('/Sweden')
def sweden():
    return render_template('countries/Sweden.html')
@app.route('/China')
def china():
    return render_template('countries/China.html')
@app.route('/Brazil')
def brazil():
    return render_template('countries/Brazil.html')
@app.route('/Germany')
def germany():
    return render_template('countries/Germany.html')
@app.route('/Russia')
def russia():
    return render_template('countries/Russia.html')
@app.route('/Turkey')
def turkey():
    return render_template('countries/Turkey.html')
@app.route('/Serbia')
def serbia():
    return render_template('countries/Serbia.html')

if __name__ == '__main__':
    app.run(debug=True)
