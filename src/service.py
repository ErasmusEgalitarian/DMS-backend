import datetime

from src.mongo_connector import MongoConnector
from src.schemas import MeasurementSchema, WastePriceSchema, UserSchema

mongo_connector = MongoConnector()


def get_measurements(user_id: str):
    measurements = mongo_connector.get_documents('measurements', query={'user_id': user_id})

    measurements = [MeasurementSchema(
        id=str(measurement.get('_id')),
        device_id=str(measurement.get('device_id')),
        user_id=str(measurement.get('user_id')),
        cooperative_id=str(measurement.get('cooperative_id')),
        weight=float(measurement.get('weight')),
        waste_type=measurement.get('waste_type'),
        timestamp=int(measurement.get('timestamp'))
    ) for measurement in measurements]

    # Fetch all waste prices and organize them by waste_type
    waste_prices = mongo_connector.get_documents('waste_prices')
    price_lookup = {}

    for price in waste_prices:
        waste_type = price['waste_type']
        if waste_type not in price_lookup:
            price_lookup[waste_type] = []
        price_lookup[waste_type].append({
            "id": str(price.get('_id')),
            "price_per_kg": price.get('price_per_kg'),
            "date": price.get('date')
        })

    # Sort prices by date for each waste type
    for waste_type in price_lookup:
        price_lookup[waste_type].sort(key=lambda x: x['date'])

    # Combine measurements with the most recent price for the corresponding waste type and date
    results = []
    for measurement in measurements:
        measurement_date = datetime.datetime.fromtimestamp(measurement.timestamp)

        # Get prices for the measurement's waste type
        prices_for_type = price_lookup.get(measurement.waste_type, [])

        # Find the most recent price on or before the measurement date
        matching_price = None
        for price in reversed(prices_for_type):
            if price['date'] <= measurement_date:
                matching_price = price
                break

        waste_price = WastePriceSchema(
            id=matching_price['id'],
            waste_type=measurement.waste_type,
            price_per_kg=matching_price['price_per_kg'],
            date=matching_price['date']
        ) if matching_price else None

        total_price = round(measurement.weight * waste_price.price_per_kg, 2) if waste_price else None

        # Add price details to the measurement
        results.append({
            "measurement": measurement,
            "waste_price": waste_price,
            "total_price": total_price,
        })

    return results


def get_waste_pickers():
    waste_pickers = mongo_connector.get_documents('users', query={'role': 'waste_picker'})

    waste_pickers = [UserSchema(
        id=str(waste_picker.get('_id')),
        name=waste_picker.get('name'),
        email=waste_picker.get('email'),
        role=waste_picker.get('role')
    ) for waste_picker in waste_pickers]

    return waste_pickers


def get_waste_picker(waste_picker_id: str):
    waste_picker = mongo_connector.get_by_id('users', waste_picker_id)

    if not waste_picker:
        return None

    return UserSchema(
        id=str(waste_picker.get('_id')),
        name=waste_picker.get('name'),
        email=waste_picker.get('email'),
        role=waste_picker.get('role')
    )
