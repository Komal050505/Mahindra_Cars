from flask import Flask, jsonify, request
from apps.constants import CARS_DATA
from email_setup.email_operations import notify_failure, notify_success
from logging_activity.logging_utils import *

"""
This Module contains the main apis code
"""
app = Flask(__name__)


@app.route('/cars/<car_type>', methods=['POST'])
def add_car(car_type):
    """
    Adds a new car to the specified car type.

    :param car_type: Type of the car (e.g., petrol_cars_with_gear).
    :return: JSON response with the added car or error message.
    """
    log_info(f"Add car function started with {car_type} details")
    try:
        log_info(f'Received request to add car to type: {car_type}')
        car_data = CARS_DATA.get(car_type)
        if car_data is None:
            error_message = f'Car type {car_type} not found'
            log_error(error_message)
            notify_failure("Car Addition Failed", error_message)
            return jsonify({"error": error_message}), 404
        new_car = request.get_json()
        car_data.append(new_car)
        log_info(f'Added new car: {new_car} to type: {car_type}')
        notify_success("Car Addition Successful", f'Added new car: {new_car} to type: {car_type}')
        return jsonify(new_car), 201
    except Exception as e:
        error_message = f'Error adding car to type {car_type}: {e}'
        log_error(error_message)
        notify_failure("Car Addition Failed", error_message)
        return jsonify({"error": "Internal server error"}), 500


log_info(f" Add car function ended")


@app.route('/cars/<car_type>/<car_number>', methods=['PATCH'])
def update_car(car_type, car_number):
    """
    Updates an existing car identified by its car number in the specified car type.

    :param car_type: Type of the car (e.g., petrol_cars_with_gear).
    :param car_number: Unique identifier for the car.
    :return: JSON response with the updated car or error message.
    """
    log_info(f"Update car method started with {car_type}, {car_number}")
    try:
        log_info(f'Received request to update car number: {car_number} in type: {car_type}')
        car_data = CARS_DATA.get(car_type)
        if car_data is None:
            error_message = f'Car type {car_type} not found'
            log_error(error_message)
            notify_failure("Car Update Failed", error_message)
            return jsonify({"error": error_message}), 404
        car_found = None
        for car in car_data:
            if car["car_number"] == car_number:
                car_found = car
                break

        if car_found is None:
            error_message = f'Car number {car_number} not found in type: {car_type}'
            log_error(error_message)
            notify_failure("Car Update Failed", error_message)
            return jsonify({"error": error_message}), 404
        updated_car = request.get_json()
        car_found.update(updated_car)
        log_info(f'Updated car number: {car_number} in type: {car_type} with updates: {updated_car}')
        notify_success("Car Update Successful",
                       f'Updated car number: {car_number} in type: {car_type} with updates: {updated_car}')
        return jsonify(car_found), 200
    except Exception as e:
        error_message = f'Error updating car number {car_number} in type {car_type}: {e}'
        log_error(error_message)
        notify_failure("Car Update Failed", error_message)
        return jsonify({"error": "Internal server error"}), 500


log_info(f"Update car function ended")


@app.route('/cars/<car_type>/<car_number>', methods=['DELETE'])
def delete_car(car_type, car_number):
    """
    Deletes an existing car identified by its car number from the specified car type.

    :param car_type: Type of the car (e.g., petrol_cars_with_gear).
    :param car_number: Unique identifier for the car.
    :return: HTTP status code indicating success or failure.
    """
    log_info(f"Delete car function entered with {car_type}, {car_number} details")
    try:
        log_info(f'Received request to delete car number: {car_number} from type: {car_type}')
        car_data = CARS_DATA.get(car_type)
        if car_data is None:
            error_message = f'Car type {car_type} not found'
            log_error(error_message)
            notify_failure("Car Deletion Failed", error_message)
            return jsonify({"error": error_message}), 404
        car_found = None
        for car in car_data:
            if car["car_number"] == car_number:
                car_found = car
                break
        if car_found is None:
            error_message = f'Car number {car_number} not found in type: {car_type}'
            log_error(error_message)
            notify_failure("Car Deletion Failed", error_message)
            return jsonify({"error": error_message}), 404
        car_data.remove(car_found)
        log_info(f'Deleted car number: {car_number} from type: {car_type}')
        notify_success(f"Car {car_found} Deletion Successful",
                       f'Deleted car number: {car_number} from type: {car_type}')
        return jsonify({"Deletion Successful for the car ": car_found}), 200
    except Exception as e:
        error_message = f'Error deleting car number {car_number} from type {car_type}: {e}'
        log_error(error_message)
        notify_failure("Car Deletion Failed", error_message)
        return jsonify({"error": "Internal server error"}), 500


log_info(f"Delete function ended")


@app.route('/cars/<car_type>', methods=['GET'])
def get_all_cars(car_type):
    """
    Retrieves all cars of the specified type.

    :param car_type: Type of the car (e.g., petrol_cars_with_gear).
    :return: JSON response with the list of cars or error message.
    """
    log_info(f"Get all car function started with {car_type} details")
    try:
        log_info(f'Received request for car type: {car_type}')
        car_data = CARS_DATA.get(car_type)
        if car_data is None:
            error_message = f'Car type {car_type} not found'
            log_error(error_message)
            notify_failure("Car Retrieval Failed", error_message)
            return jsonify({"error": error_message}), 404
        log_info(f'Successfully retrieved car type: {car_type}')
        notify_success(f"Cars {car_data} Retrieval Successful",
                       f'Successfully retrieved car type: {car_type}'), 200
        return jsonify(car_data)
    except Exception as e:
        error_message = f'Error retrieving cars for type {car_type}: {e}'
        log_error(error_message)
        notify_failure("Car Retrieval Failed", error_message)
        return jsonify({"error": "Internal server error"}), 500


log_info(f"Get all cars function ended")


@app.route('/car/<car_number>', methods=['GET'])
def get_single_car(car_number):
    """
    Retrieves a single car identified by its car number from any type.

    :param car_number: Unique identifier for the car.
    :return: JSON response with the car details or error message.
    """
    log_info(f"Get single car function started with {car_number} details")
    try:
        log_info(f'Received request for car number: {car_number}')
        car_found = None
        for car_type, cars in CARS_DATA.items():
            for car in cars:
                if car["car_number"] == car_number:
                    car_found = car
                    break
            if car_found:
                log_debug(f'Found car number: {car_number} in type: {car_type}')
                notify_success(f"Single Car {car_found} Retrieval Successful",
                               f'Found car number: {car_number} in type: {car_type}')
                return jsonify(car_found), 200
        error_message = f'Car number {car_number} not found'
        log_error(error_message)
        notify_failure("Single Car Retrieval Failed", error_message)
        return jsonify({"error": error_message}), 404
    except Exception as e:
        error_message = f'Error retrieving car number {car_number}: {e}'
        log_error(error_message)
        notify_failure("Single Car Retrieval Failed", error_message)
        return jsonify({"error": "Internal server error"}), 500


log_info(f"Get single car function ended")


@app.route('/cars/by_year/<int:year>', methods=['GET'])
def get_cars_by_year(year):
    log_info(f"Get cars by year function started for year {year}")
    try:
        result = []
        for car_type, cars in CARS_DATA.items():
            for car in cars:
                if car.get('year_of_manufacturing') == year:
                    result.append(car)
        if not result:
            error_message = f'No cars found for the year {year}'
            log_error(error_message)
            notify_failure("Car Retrieval Failed", error_message)
            return jsonify({"error": error_message}), 404
        log_info(f'Successfully retrieved cars for year: {year}')
        notify_success(f"Cars Retrieval Successful", f'Successfully retrieved cars for year: {year}')
        return jsonify(result)
    except Exception as e:
        error_message = f'Error retrieving cars for year {year}: {e}'
        log_error(error_message)
        notify_failure("Car Retrieval Failed", error_message)
        return jsonify({"error": "Internal server error"}), 500


log_info(f" Get cars by year function ended")


@app.route('/cars/by_cost', methods=['GET'])
def get_cars_by_cost():
    min_cost = request.args.get('min_cost', type=float)
    max_cost = request.args.get('max_cost', type=float)
    log_info(f"Get cars by cost range function started with min_cost {min_cost} and max_cost {max_cost}")
    try:
        result = []
        for car_type, cars in CARS_DATA.items():
            for car in cars:
                if min_cost <= car.get('cost', float('inf')) <= max_cost:
                    result.append(car)
        if not result:
            error_message = f'No cars found in the cost range {min_cost} - {max_cost}'
            log_error(error_message)
            notify_failure("Car Retrieval Failed", error_message)
            return jsonify({"error": error_message}), 404
        log_info(f'Successfully retrieved cars in cost range: {min_cost} - {max_cost}')
        notify_success(f"Cars Retrieval Successful",
                       f'Successfully retrieved cars in cost range: {min_cost} - {max_cost}')
        return jsonify(result)
    except Exception as e:
        error_message = f'Error retrieving cars in cost range {min_cost} - {max_cost}: {e}'
        log_error(error_message)
        notify_failure("Car Retrieval Failed", error_message)
        return jsonify({"error": "Internal server error"}), 500


log_info(f"Get cars by cost function ended")

if __name__ == '__main__':
    app.run(debug=True)
