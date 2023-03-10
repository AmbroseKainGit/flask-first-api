from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema
from models import StoreModel
from db import db
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
blp = Blueprint("Stores", "store", description="Operations on stores")


@blp.route("/store/<string:store_id>", methods=['GET', 'DELETE'])
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        # store = StoreModel.query.get_or_404(store_id)
        return StoreModel.query.get_or_404(store_id)
        # try:
        #     return stores[store_id]
        # except KeyError:
        #     abort(404, message="Store not found.")

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted"}
        # try:
        #     del stores[store_id]
        #     return {"message": "Store deleted"}
        # except KeyError:
        #     abort(404, message="Store not found.")


@blp.route("/store", methods=['GET', 'POST'])
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(400, message="A store with that name already exists.")
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="An Error ocurred while creating the store.")
        # for store in stores.values():
        #     if store_data["name"] == store["name"]:
        #         abort(400, message=f"Store already exists: {store['name']}")
        # store_id = uuid.uuid4().hex
        # store = {**store_data, "id": store_id}
        # stores[store_id] = store
        return store, 201
