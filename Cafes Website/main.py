from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os


google_map_api_key = os.getenv("google_maps_api_key")

app = Flask(__name__)

# Connessione al database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)


# Configurazione della tabella
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(250))
    coffee_price = db.Column(db.String(250))
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")  # Homepage
def home():
    cafes_list = []  # creo la lista da passare all'html
    all_cafes = db.session.query(Cafe)  # carico i dati del db
    for cafe in all_cafes:  # preparo tutte le variabili da inserire dentro la lista da passare all'html
        url = cafe.map_url
        id = cafe.id - 1
        lat = cafe.latitude
        lng = cafe.longitude
        img = cafe.img_url
        name = cafe.name
        location = cafe.location
        if cafe.has_sockets:
            sockets = "⚡"
        else:
            sockets = "✘"
        if cafe.has_toilet:
            toilets = "🚽"
        else:
            toilets = "✘"
        if cafe.has_wifi:
            wifi = "📶"
        else:
            wifi = "✘"
        if cafe.can_take_calls:
            calls = "📞"
        else:
            calls = "✘"
        seats = f"🪑: {cafe.seats}"
        price = f"☕️: {cafe.coffee_price}"
        cafes_list.append([url, id, lat, lng, img, name, location, sockets, toilets, wifi, calls, seats, price])
    return render_template("index.html", cafes_list=cafes_list, google_api=google_map_api_key)


@app.route("/all")
def get_all_cafes():  # GET Api per ottenere la lista di tutti i cafes in formato json
    all_cafes = db.session.query(Cafe)
    cafes_json = {"cafes": []}
    for cafe in all_cafes:
        cafes_json["cafes"].append({
            "id": cafe.id,
            "name": cafe.name,
            "map_url": cafe.map_url,
            "img_url": cafe.img_url,
            "location": cafe.location,
            "has_sockets": cafe.has_sockets,
            "has_toilet": cafe.has_toilet,
            "has_wifi": cafe.has_wifi,
            "can_take_calls": cafe.can_take_calls,
            "seats": cafe.seats,
            "coffee_price": cafe.coffee_price,
            "latitude": cafe.latitude,
            "longitude": cafe.longitude})
    return jsonify(cafes_json)


@app.route("/search")
def search():  # GET Api con funzione cerca by location
    query_location = request.args.get("location")
    all_cafes = Cafe.query.filter_by(location=query_location).all()
    if all_cafes:
        cafes_json = {"cafes": []}
        for cafe in all_cafes:
            cafes_json["cafes"].append({
                "id": cafe.id,
                "name": cafe.name,
                "map_url": cafe.map_url,
                "img_url": cafe.img_url,
                "location": cafe.location,
                "has_sockets": cafe.has_sockets,
                "has_toilet": cafe.has_toilet,
                "has_wifi": cafe.has_wifi,
                "can_take_calls": cafe.can_take_calls,
                "seats": cafe.seats,
                "coffee_price": cafe.coffee_price,
                "latitude": cafe.latitude,
                "longitude": cafe.longitude})
        return jsonify(cafes_json)
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."})


@app.route("/add", methods=["POST"])
def add_new_cafe():  # POST Api per aggiungere un nuovo cafe
    json = request.get_json()
    print(json)
    new_cafe = Cafe(
        name=json["name"],
        map_url=json["map_url"],
        img_url=json["img_url"],
        location=json["location"],
        has_sockets=bool(json["has_sockets"]),
        has_toilet=bool(json["has_toilet"]),
        has_wifi=bool(json["has_wifi"]),
        can_take_calls=bool(json["can_take_calls"]),
        seats=json["seats"],
        coffee_price=json["coffee_price"],
        latitude=json["latitude"],
        longitude=json["longitude"]
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"Success": "Successfully added the new cafe."})


@app.route("/update-price", methods=["PATCH"])
def update_price():  # PATCH Api per modificare il prezo del cafe di un cafe
    cafe_name = request.args.get("cafe_name")
    new_price = request.args.get("new_price")
    cafe = db.session.query(Cafe).where(Cafe.name == cafe_name).first()
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price."})
    else:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."})


@app.route("/report-closed", methods=["DELETE"])
def delete_cafe():  # DELETE Api per cancellare un cafe dal db
    # api_key = request.args.get("api-key")
    cafe_name = request.args.get("cafe_name")
    cafe = db.session.query(Cafe).where(Cafe.name == cafe_name).first()
    if cafe:
        db.session.delete(cafe)
        db.session.commit()
        return jsonify(response={"success": "Successfully deleted the cafe from the database."})
    else:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."})


if __name__ == "__main__":
    app.run()
