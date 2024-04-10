import os
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# Personal and Business form directories and allowed extentions
Images = os.path.join("static", "images")
Extensions = {"png", "jpg", "jpeg"} 

itineraries = [
    {'id': 1, 'name': 'Trip to Paris', 'destination': 'France', 'disembark_date': '2024-04-01'},
    {'id': 2, 'name': 'Beach vacation', 'destination': 'Maldives', 'disembark_date': '2024-07-15'}
]
days = 0
day_number = 1 

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
@app.get('/DiscoverPage')
def discover_page():
    return render_template('discover_page.html')

@app.get('/discover_page_selected')
def discover_page_selected():
    selected_country = request.args.get('country')
    if selected_country is None:
        selected_country = "None" 
    return render_template('discover_page_selected.html', selected_country=selected_country)

@app.route("/all_itineraries_page")
def all_itineraries():

    return render_template("all_itineraries_page.html", itineraries=itineraries)

@app.route("/edit_itinerary/<int:id>")
def edit_itinerary(id):
    
    return render_template("edit_itinerary.html")

@app.route("/delete_itinerary/<int:id>")
def delete_itinerary(id):

    return render_template("delete_itinerary.html")

@app.route('/itinerary_creation', methods=['GET', 'POST'])
def itinerary_creation():
    global days
    if request.method == 'POST':
        name = request.form['name']
        destination = request.form['destination']
        disembark_date = request.form['disembark_date']
        days = int(request.form['days'])

        day_number = 1 

        itinerary = {'id': len(itineraries) + 1, 'name': name, 'destination': destination, 'disembark_date': disembark_date}
        itineraries.append(itinerary)

        return redirect(url_for("itinerary_creation_step_2", day_number=day_number))

    return render_template('itinerary_creation_page.html', itineraries=itineraries)


@app.route('/itinerary_creation_step_2/<int:day_number>', methods=['GET', 'POST'])
def itinerary_creation_step_2(day_number):
    global days
    activities = []  # Initialize empty list for activities
    descriptions = []  # Initialize empty list for descriptions

    if day_number > days:
        #return "Error: Invalid day number"
        #Go to the all itineraries page.
        return redirect(url_for('all_itineraries'))
    
    if len(activities) != len(descriptions):
            return "Error: Number of activities and descriptions don't match"
    
    for activity, description in zip(activities, descriptions):
        #Process each activity and description here (temporary print statements for now)
        print("Activity: ", activity)
        print("Description: ", description)

    if request.method == 'POST':
        activities = request.form.getlist('activity')
        descriptions = request.form.getlist('description')

        if 'add_another' in request.form and len(activities) < 3:
            if day_number < days:

                return redirect(url_for('itinerary_creation_step_2', day_number=day_number + 1))
            else:
                return "It's the last day"
            
        else:
            return redirect(url_for('next_day', day_number=day_number))
    
    return render_template('itinerary_creation_step2.html', day_number=day_number)

@app.route('/next_day/<int:day_number>')
def next_day(day_number):
    next_day_number = day_number + 1
    return redirect(url_for("itinerary_creation_step_2", day_number=next_day_number))

if __name__ == '__main__':
    app.run(debug=True)
