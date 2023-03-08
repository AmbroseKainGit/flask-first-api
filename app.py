import uuid
from flask import Flask, request
from flask_smorest import abort
from db import items, stores

app = Flask(__name__)


@app.get("/store")
def get_stores():
    return {"data": list(stores.values())}


@app.post("/store")
def create_store():
    store_data = request.get_json()
    if "name" not in store_data:
        abort(400, message="Bad request. Ensure name field is present.")
    for store in stores.values():
        if store_data["name"] == store["name"]:
            abort(400, message=f"Store already exists: {store['name']}")
    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    return store, 201
    # request_data = request.get_json()
    # new_store = {"name": request_data["name"], "items": []}
    # stores.append(new_store)
    # return new_store, 201


@app.post("/item")
def create_item():
    item_data = request.get_json()
    if (
        "price" not in item_data
        or "store_id" not in item_data
        or "name" not in item_data
    ):
        abort(
            400,
            message="Bad request, Ensure all required fields are present"
        )
    for item in items.values():
        if (
            item_data["name"] == item["name"]
            and item_data["store_id"] == item["store_id"]
        ):
            abort(400, message=f"Item already exists: {item['name']}")
    if item_data["store_id"] not in stores:
        abort(404, message="Store not found.")
        # return {"message": "Store not found"}, 404
    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item
    return item, 201
    # store = next((store for store in stores if store["name"] == name), None)
    # if store == None:
    #     return {"message": "Store not found"}, 404
    # new_item = {"name": request_data["name"], "price": request_data["price"]}
    # store["items"].append(new_item)
    # return new_item, 201


@app.get("/item")
def get_all_items():
    return {"data": list(items.values())}


@app.get("/store/<string:store_id>")
def get_specific_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="Store not found.")
        # return {"message": "Store not found"}, 404
    # store = next((store for store in stores if store["name"] == name), None)
    # if store == None:
    #     return {"message": "Store not found"}, 404
    # return {"data": store}


@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="Item not found.")
        # return {"message": "Item not found"}, 404
    # store = next((store for store in stores if store["name"] == name), None)
    # if store == None:
    #     return {"message": "Store not found"}, 404
    # return {"items": store["items"]}
