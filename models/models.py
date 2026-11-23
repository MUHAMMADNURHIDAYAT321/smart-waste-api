
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()


# Tabel pengguna
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(30), nullable=False)

    devices = db.relationship("Device", backref="user")


# Tabel perangkat IoT
class Device(db.Model):
    __tablename__ = "devices"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(20), default="offline")

    sensors = db.relationship("Sensor", backref="device")
    alerts = db.relationship("Alert", backref="device")


# Tabel sensor
class Sensor(db.Model):
    __tablename__ = "sensors"

    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(
        db.Integer,
        db.ForeignKey("devices.id"),
        nullable=False
    )

    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    unit = db.Column(db.String(20), nullable=False)

    telemetries = db.relationship(
        "Telemetry",
        backref="sensor"
    )


# Tabel pembacaan sensor
class Telemetry(db.Model):
    __tablename__ = "telemetries"

    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(
        db.Integer,
        db.ForeignKey("sensors.id"),
        nullable=False
    )

    value = db.Column(db.Float, nullable=False)

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )


# Tabel peringatan
class Alert(db.Model):
    __tablename__ = "alerts"

    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(
        db.Integer,
        db.ForeignKey("devices.id"),
        nullable=False
    )

    message = db.Column(db.String(255), nullable=False)
    severity = db.Column(db.String(20), nullable=False)

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )