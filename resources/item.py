from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from schemas import ItemSchema, ItemUpdateSchema, ResponseSchema
from models import ItemModel
from db import db
from sqlalchemy.exc import SQLAlchemyError
blp = Blueprint("Items", __name__, description="Operations on items")

@blp.before_request
@jwt_required()
def authenticate():
    pass

@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            # item = ItemModel.query.get_or_404(item_id)
            return ItemModel.query.get_or_404(item_id)
        except KeyError:
            abort(404, message="Item not found.")

    def delete(self, item_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin Privileges Required.")
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted"}
        # raise NotImplementedError("Deleting an item is not implemented.")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ResponseSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        message = ""
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
            message = "Item updated"
        else:
            item = ItemModel(id=item_id, **item_data)
            message = "Item created"
        db.session.add(item)
        db.session.commit()
        return {"message": message, "data": item}
        # try:
        #     item = items[item_id]
        #     item |= item_data
        #     return {"message": "Item updated", "data": item}
        # except KeyError:
        #     abort(404, message="Item not found.")


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    # @blp.response(200, ResponseSchema)
    def get(self):
        return ItemModel.query.all()
        # return items.values()
        # return {"message": "Items", "data": list(items.values())}

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="An Error ocurred while inserting the item.")
        return item, 201
        # for item in items.values():
        #     if (
        #         item_data["name"] == item["name"]
        #         and item_data["store_id"] == item["store_id"]
        #     ):
        #         abort(400, message=f"Item already exists: {item['name']}")
        # if item_data["store_id"] not in stores:
        #     abort(404, message="Store not found.")
        # item_id = uuid.uuid4().hex
        # item = {**item_data, "id": item_id}
        # items[item_id] = item
