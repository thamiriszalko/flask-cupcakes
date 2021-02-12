"""Flask app for Cupcakes"""
from flask import Flask, jsonify, request, render_template

from models import connect_db, db, Cupcake
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost:5433/cupcake_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "123-456"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)


def serialize(cupcake):
    """Serialize a cupcake SQLAlchemy object to dictionary."""

    return {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image,
    }


@app.route('/')
def index_page():
    cupcakes = Cupcake.query.all()
    return render_template('landing_page.html', cupcakes=cupcakes)


@app.route('/api/cupcakes')
def listing():
    cupcakes = Cupcake.query.all()

    serialized = [serialize(cupcake) for cupcake in cupcakes]

    return jsonify(cupcakes=serialized)


@app.route('/api/cupcakes/<int:cupcake_id>')
def retrieve(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    return jsonify(cupcake=serialize(cupcake))


@app.route('/api/cupcakes', methods=["POST"])
def create():
    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json.get("image")
    instance = Cupcake(
        flavor=flavor,
        size=size,
        rating=rating,
        image=image,
    )

    db.session.add(instance)
    db.session.commit()

    return jsonify(cupcake=serialize(instance))


@app.route('/api/cupcakes/<int:cupcake_id>', methods=["PUT"])
def update_todo(cupcake_id):
    """Updates a particular cupcake and
    responds w/ JSON of that updated instance"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)

    db.session.commit()

    return jsonify(cupcake=serialize(cupcake))


@app.route('/api/cupcakes/<int:cupcake_id>', methods=["DELETE"])
def delete_todo(cupcake_id):
    """Deletes a particular cupcake"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="deleted")
