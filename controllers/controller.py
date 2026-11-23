
from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from math import isfinite
from models import db, User, Device, Sensor, Telemetry, Alert


MODELS = {
    "users": User,
    "devices": Device,
    "sensors": Sensor,
    "telemetries": Telemetry,
    "alerts": Alert
}

FIELDS = {
    "users": ["name", "email", "role"],
    "devices": ["user_id", "name", "location", "status"],
    "sensors": ["device_id", "name", "type", "unit"],
    "telemetries": ["sensor_id", "value"],
    "alerts": ["device_id", "message", "severity"]
}


def serialize(item):
    result = {}

    for column in item.__table__.columns:
        value = getattr(item, column.name)

        if hasattr(value, "isoformat"):
            value = value.isoformat()

        result[column.name] = value

    return result


def error(message, status=400):
    return jsonify({
        "success": False,
        "message": message
    }), status


def validate(resource, data):
    if not isinstance(data, dict):
        return "Body harus berupa objek JSON"

    model = MODELS[resource]

    for field in FIELDS[resource]:
        if field not in data:
            return f"{field} wajib diisi"

        value = data[field]
        column = model.__table__.columns[field]
        expected = column.type.python_type

        if expected == str:
            if not isinstance(value, str) or not value.strip():
                return f"{field} harus berupa teks"

            if len(value) > column.type.length:
                return f"{field} terlalu panjang"

        elif expected == int:
            if type(value) is not int or value < 1:
                return f"{field} harus berupa ID yang valid"

        elif expected == float:
            if type(value) not in (int, float):
                return f"{field} harus berupa angka"

            if not isfinite(value):
                return f"{field} harus berupa angka terbatas"

    foreign_keys = {
        "user_id": User,
        "device_id": Device,
        "sensor_id": Sensor
    }

    for field, parent in foreign_keys.items():
        if field in FIELDS[resource]:
            if db.session.get(parent, data[field]) is None:
                return f"{field} tidak ditemukan"

    if resource == "users":
        if "@" not in data["email"]:
            return "Email tidak valid"

        if data["role"] not in ["admin", "operator"]:
            return "Role harus admin atau operator"

    if resource == "devices":
        if data["status"] not in ["online", "offline"]:
            return "Status harus online atau offline"

    if resource == "alerts":
        if data["severity"] not in ["low", "medium", "high"]:
            return "Severity tidak valid"

    return None


# READ ALL
def get_all(resource):
    model = MODELS[resource]
    query = model.query

    search = request.args.get("search", "")
    sort = request.args.get("sort", "asc")

    if search and hasattr(model, "name"):
        query = query.filter(
            model.name.ilike(f"%{search}%")
        )

    status = request.args.get("status")

    if status and resource == "devices":
        query = query.filter_by(status=status)

    if sort == "desc":
        query = query.order_by(model.id.desc())
    else:
        query = query.order_by(model.id.asc())

    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)

    if page < 1 or limit < 1 or limit > 100:
        return error("Pagination tidak valid")

    pagination = query.paginate(
        page=page,
        per_page=limit,
        error_out=False
    )

    return jsonify({
        "success": True,
        "data": [
            serialize(item)
            for item in pagination.items
        ],
        "pagination": {
            "page": page,
            "limit": limit,
            "total": pagination.total,
            "pages": pagination.pages
        }
    }), 200


# READ BY ID
def get_one(resource, item_id):
    item = db.session.get(MODELS[resource], item_id)

    if item is None:
        return error("Data tidak ditemukan", 404)

    return jsonify({
        "success": True,
        "data": serialize(item)
    }), 200


# CREATE
def create(resource):
    data = request.get_json(silent=True)

    message = validate(resource, data)

    if message:
        return error(message)

    try:
        item = MODELS[resource](**{
            field: data[field]
            for field in FIELDS[resource]
        })

        db.session.add(item)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Data berhasil ditambahkan",
            "data": serialize(item)
        }), 201

    except IntegrityError:
        db.session.rollback()
        return error("Data duplikat atau konflik database", 409)


# UPDATE
def update(resource, item_id):
    item = db.session.get(MODELS[resource], item_id)

    if item is None:
        return error("Data tidak ditemukan", 404)

    data = request.get_json(silent=True)

    message = validate(resource, data)

    if message:
        return error(message)

    try:
        for field in FIELDS[resource]:
            setattr(item, field, data[field])

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Data berhasil diperbarui",
            "data": serialize(item)
        }), 200

    except IntegrityError:
        db.session.rollback()
        return error("Konflik database", 409)


# DELETE
def delete(resource, item_id):
    item = db.session.get(MODELS[resource], item_id)

    if item is None:
        return error("Data tidak ditemukan", 404)

    try:
        db.session.delete(item)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Data berhasil dihapus"
        }), 200

    except IntegrityError:
        db.session.rollback()
        return error(
            "Data masih memiliki relasi dengan tabel lain",
            409
        )