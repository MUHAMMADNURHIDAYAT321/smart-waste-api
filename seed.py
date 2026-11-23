
from app import app
from models import db, User, Device, Sensor, Telemetry, Alert


with app.app_context():

    if User.query.first() is not None:
        print("Database sudah berisi data.")
        raise SystemExit

    user = User(
        name="Administrator",
        email="admin@example.com",
        role="admin"
    )

    db.session.add(user)
    db.session.flush()

    device = Device(
        user_id=user.id,
        name="Smart Bin 01",
        location="Kampus Amikom",
        status="online"
    )

    db.session.add(device)
    db.session.flush()

    sensor = Sensor(
        device_id=device.id,
        name="Sensor Kapasitas",
        type="Ultrasonic",
        unit="%"
    )

    db.session.add(sensor)
    db.session.flush()

    telemetry = Telemetry(
        sensor_id=sensor.id,
        value=85.5
    )

    alert = Alert(
        device_id=device.id,
        message="Tempat sampah hampir penuh",
        severity="high"
    )

    db.session.add_all([telemetry, alert])
    db.session.commit()

    print("Seed data berhasil ditambahkan!")