import json

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import dicts


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///memory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String)
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone
        }


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String)
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    address = db.Column(db.String)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "price": self.price,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id
        }


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id
        }
# db.drop_all()
db.create_all()


for dict_1 in dicts.users:
    new_user = User(
        id=dict_1["id"],
        first_name=dict_1["first_name"],
        last_name=dict_1["last_name"],
        age=dict_1["age"],
        email=dict_1["email"],
        role=dict_1["role"],
        phone=dict_1["phone"],
    )

    db.session.add(new_user)
    db.session.commit()


for dict_2 in dicts.orders:
    new_order = Order(
        id=dict_2["id"],
        name=dict_2["name"],
        description=dict_2["description"],
        start_date=dict_2["start_date"],
        end_date=dict_2["end_date"],
        address=dict_2["address"],
        price=dict_2["price"],
        customer_id=dict_2["customer_id"],
        executor_id=dict_2["executor_id"],
    )

    db.session.add(new_order)
    db.session.commit()


for dict_3 in dicts.offers:
    new_offer = Offer(
        id=dict_3["id"],
        order_id=dict_3["order_id"],
        executor_id=dict_3["executor_id"]
    )

    db.session.add(new_offer)
    db.session.commit()


#users
@app.route("/users", methods=['GET', 'POST'])
def users():
    if request.method == "GET":
        res = []
        for u in User.query.all():
            res.append(u.to_dict())
        return json.dumps(res), 200, {'Content-Type':'application/json; charset=utf-8'}
    elif request.method == "POST":
        user_data = json.load(request.data)
        new_user = User(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            age=user_data["age"],
            email=user_data["email"],
            role=user_data["role"],
            phone=user_data["phone"]
        )
        db.session.add(new_user)
        db.session.commit()
        return "", 201


@app.route("/users/<int:uid>", methods=['GET', 'POST', 'DELETE'])
def get_user(uid: int):
    if request.method == "GET":
        return json.dumps(User.query.get(uid).to_dict()), 200, {'Content-Type': 'application/json; charset=utf-8'}
    elif request.method == "DELETE":
        u = User.query.get(uid)
        db.session.delete(u)
        db.session.commit()
        return "", 204
    elif request.method == "POST":
        user_data = json.loads(request.data)
        u = User.query.get(uid)
        u.first_name = user_data["first_name"]
        u.last_name = user_data["last_name"]
        u.age = user_data["age"]
        u.email = user_data["email"]
        u.role = user_data["role"]
        u.phone = user_data["phone"]
        db.session.delete(u)
        db.session.commit()
        return "", 204


#orders
@app.route("/orders", methods=['GET', 'POST'])
def orders():
    if request.method == "GET":
        res = []
        for o in Order.query.all():
            res.append(o.to_dict())
        return json.dumps(res), 200, {'Content-Type':'application/json; charset=utf-8'}
    elif request.method == "POST":
        order_data = json.load(request.data)
        new_order = Order(
            name=order_data["name"],
            description=order_data["description"],
            start_date=order_data["start_date"],
            end_date=order_data["end_date"],
            address=order_data["address"],
            price=order_data["price"],
            customer_id=order_data["customer_id"],
            executor_id=order_data["executor_id"]
        )
        db.session.add(new_order)
        db.session.commit()
        return "", 201


@app.route("/orders/<int:oid>", methods=['GET', 'POST', 'DELETE'])
def get_order(oid: int):
    if request.method == "GET":
        return json.dumps(Order.query.get(oid).to_dict()), 200, {'Content-Type': 'application/json; charset=utf-8'}
    elif request.method == "DELETE":
        o = Order.query.get(oid)
        db.session.delete(o)
        db.session.commit()
        return "", 204
    elif request.method == "POST":
        order_data = json.loads(request.data)
        o = User.query.get(oid)
        o.name = order_data["name"]
        o.description = order_data["description"]
        o.start_date = order_data["start_date"]
        o.end_date = order_data["end_date"]
        o.address = order_data["address"]
        o.price = order_data["price"]
        o.customer_id = order_data["customer_id"]
        o.executor_id = order_data["executor_id"]
        db.session.delete(o)
        db.session.commit()
        return "", 204


#offers
@app.route("/offers", methods=['GET', 'POST'])
def offers():
    if request.method == "GET":
        res = []
        for of in Offer.query.all():
            res.append(of.to_dict())
        return json.dumps(res), 200, {'Content-Type':'application/json; charset=utf-8'}
    elif request.method == "POST":
        offer_data = json.load(request.data)
        new_offer = Offer(
            order_id=offer_data["order_id"],
            executor_id=offer_data["executor_id"]
        )
        db.session.add(new_offer)
        db.session.commit()
        return "", 201


@app.route("/offers/<int:ofid>", methods=['GET', 'POST', 'DELETE'])
def get_offer(ofid: int):
    if request.method == "GET":
        return json.dumps(Offer.query.get(ofid).to_dict()), 200, {'Content-Type': 'application/json; charset=utf-8'}
    elif request.method == "DELETE":
        of = Offer.query.get(ofid)
        db.session.delete(of)
        db.session.commit()
        return "", 204
    elif request.method == "POST":
        offer_data = json.loads(request.data)
        of = User.query.get(ofid)
        of.order_id = offer_data["order_id"]
        of.executor_id = offer_data["executor_id"]
        db.session.delete(of)
        db.session.commit()
        return "", 204


if __name__ == '__main__':
    app.run()