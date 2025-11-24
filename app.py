from flask import Flask, request, jsonify, send_from_directory
from Weather import get_weather, get_forecast
from database import create_table, insert, fetch_all, fetch_one, update, delete
import json

app = Flask(__name__, static_folder='static')
create_table()

@app.get("/")
def home():
    return send_from_directory('static', 'index.html')

@app.get("/weather")
def weather_api():
    location = request.args.get("city")
    return jsonify(get_weather(location))

@app.get("/forecast")
def forecast_api():
    location = request.args.get("city")
    return jsonify(get_forecast(location))

# CREATE
@app.route('/create-record', methods=['POST'])
def create_record_route():
    data = request.json
    try:
        location = data['location']
        start_date = data['start_date']
        end_date = data['end_date']

        # Fetch weather data from API
        current_weather = get_weather(location)
        if "error" in current_weather:
            return jsonify({"error": "Invalid location. Please enter a real city name."}), 400
        forecast_data = get_forecast(location)

        # Prepare JSON string for DB
        temperature_json = json.dumps({
            "current_weather": current_weather,
            "forecast": forecast_data
        })

        # Save to database
        insert(location, start_date, end_date, temperature_json)
        return jsonify({"message": "Record created successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# READ (single record)
@app.route('/records/<int:record_id>', methods=['GET'])
def get_record_route(record_id):
    record = fetch_one(record_id)
    if record:
        return jsonify(dict(record))
    else:
        return jsonify({"error": "Record not found"}), 404

# READ (all records)
@app.route('/records', methods=['GET'])
def get_all_records_route():
    records = fetch_all()
    return jsonify([dict(r) for r in records])

# UPDATE
@app.route('/records/<int:record_id>', methods=['PUT'])
def update_record_route(record_id):
    data = request.json
    try:
        update(
            data['location'],
            data['start_date'],
            data['end_date'],
            data.get('temperature_data', ''),
            record_id
        )
        return jsonify({"message": "Record updated successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 404

# DELETE
@app.route('/records/<int:record_id>', methods=['DELETE'])
def delete_record_route(record_id):
    try:
        delete(record_id)
        return jsonify({"message": "Record deleted successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 404


if __name__ == "__main__":
    app.run(debug=True)
