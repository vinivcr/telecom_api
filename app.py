from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from call_pricing import calculate_call_duration, calculate_call_price
from connection_db import get_connection

app = Flask(__name__)


@app.route('/')
def home():
    return 'Welcome to the Call Pricing API!'


@app.route('/call_records', methods=['POST'])
def receive_call_record():
    data = request.get_json()
    required_fields = ["id", "type", "timestamp", "call_id"]

    if data["type"] == "start":
        required_fields.extend(["source", "destination"])
    elif data["type"] == "end":
        pass
    else:
        return jsonify({"error": "Invalid record type"}), 400

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    record_id = data["id"]
    record_type = data["type"]
    timestamp = data["timestamp"].replace("Z", "")  # Remove "Z" do timestamp
    call_id = data["call_id"]
    source = data.get("source", None)
    destination = data.get("destination", None)

    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO call_records (record_id, type, timestamp, call_id, source, destination)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
            cursor.execute(sql, (record_id, record_type, timestamp, call_id,
                                 source, destination))
        connection.commit()
    finally:
        connection.close()

    return jsonify({"message": "Record received successfully"}), 200


@app.route('/billing', methods=['GET'])
def get_phone_bill():
    phone_number = request.args.get("phone_number")
    period = request.args.get("period")

    if not phone_number:
        return jsonify({"error": "Phone number is required"}), 400

    if not period:
        today = datetime.today()
        first_day_of_last_month = today.replace(day=1) - timedelta(days=1)
        period_month = first_day_of_last_month.month
        period_year = first_day_of_last_month.year
    else:
        try:
            period_year, period_month = map(int, period.split('-'))
        except ValueError:
            return jsonify({"error":
                            "Invalid period format. Use YYYY-MM"}), 400

    phone_bill = {
        "phone_number": phone_number,
        "period": f"{period_year}-{period_month:02d}",
        "call_records": []
    }

    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = """
                SELECT * FROM call_records
                WHERE (source = %s OR destination = %s)
                AND type = 'end'
                AND YEAR(timestamp) = %s
                AND MONTH(timestamp) = %s
                """
            cursor.execute(
                sql, (phone_number, phone_number, period_year, period_month))
            calls = cursor.fetchall()

        for record in calls:
            call_id = record['call_id']
            end_time = record['timestamp']

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM call_records WHERE call_id = %s AND type = 'start'",
                    (call_id, ))
                start_record = cursor.fetchone()

            if start_record:
                start_time = start_record["timestamp"]
                duration_str, duration_seconds = calculate_call_duration(
                    start_time, end_time)
                price = calculate_call_price(start_time, end_time)

                phone_bill["call_records"].append({
                    "destination":
                    start_record["destination"],
                    "start_date":
                    start_time.date().isoformat(),
                    "start_time":
                    start_time.time().isoformat(),
                    "end_time":
                    end_time.time().isoformat(),
                    "duration":
                    duration_str,
                    "price":
                    f"R$ {price:.2f}"
                })

    finally:
        connection.close()

    return jsonify(phone_bill), 200


if __name__ == '__main__':
    app.run(debug=True)
