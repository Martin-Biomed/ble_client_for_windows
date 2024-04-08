from flask import Flask, jsonify, request
from ble_request_handler import main, generic_exception_handler
import asyncio

from field_format_funcs import (ble_msg_fields_dict, field_names, check_if_valid_field_value, ble_device_name,
								ble_device_addr, ble_msg_str, ble_gatt_read_uuid, ble_gatt_write_uuid,
								ble_msg_result_str_dict, ble_msg_result_str)

api = Flask("BLE Client Access API")

# API Server Constants
server_ip = '127.0.0.1'
server_port = 5900

# Initialize all dictionary terms as empty strings
ble_msg_fields_dict[ble_device_addr] = ''
ble_msg_fields_dict[ble_device_name] = ''
ble_msg_fields_dict[ble_gatt_read_uuid] = ''
ble_msg_fields_dict[ble_gatt_write_uuid] = ''
ble_msg_fields_dict[ble_msg_str] = ''

ble_msg_result_str_dict[ble_msg_result_str] = ''

# This function is accessible using a PUT request to endpoint: http://127.0.0.1:5900/device/name/<name>
# Note: If the device name contains spaces, URL encoding normally encodes spaces with either a (+) or %20
@api.route('/device/name/<name>', methods=['PUT'])
def update_ble_device_name(name):
	is_string = isinstance(name, str)
	if is_string == 1:
		print("Received: " + name)
		if check_if_valid_field_value(ble_device_name, name) == 0:
			ble_msg_fields_dict[ble_device_name] = name
			return 'Value Updated', 200
		else:
			print("Received string exceeds char limit")
			return 'Received string exceeds char limit', 400
	else:
		print("Received data is not a UTF-8 string")
		return 'Received data is not a UTF-8 string', 417


# This function is accessible using a PUT request to endpoint: http://127.0.0.1:5900/device/address/<address>
@api.route('/device/address/<address>', methods=['PUT'])
def update_ble_device_address(address):
	is_string = isinstance(address, str)
	if is_string == 1:
		print("Received: " + address)
		if check_if_valid_field_value(ble_device_addr, address) == 0:
			ble_msg_fields_dict[ble_device_addr] = address
			return 'Value Updated', 200
		else:
			print("MAC address did not match format: xx:xx:xx:xx:xx:xx (Note: F is highest Hex value allowed)")
			return 'MAC address did not match format: xx:xx:xx:xx:xx:xx (Note: F is highest Hex value allowed)', 400
	else:
		print("Received data is not a UTF-8 string")
		return 'Received data is not a UTF-8 string', 417


# This function is accessible using a PUT request to endpoint: http://127.0.0.1:5900/gatt/write/<uuid>
@api.route('/gatt/write/<uuid>', methods=['PUT'])
def update_gatt_write_uuid(uuid):
	is_string = isinstance(uuid, str)
	if is_string == 1:
		print("Received: " + uuid)
		if check_if_valid_field_value(ble_gatt_write_uuid, uuid) == 0:
			ble_msg_fields_dict[ble_gatt_write_uuid] = uuid
			return 'Value Updated', 200
		else:
			print("Received string is not in correct format (xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)")
			return 'Received string is not in correct format (xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)', 400
	else:
		print("Received data is not a UTF-8 string")
		return 'Received data is not a UTF-8 string', 417


# This function is accessible using a PUT request to endpoint: http://127.0.0.1:5900/gatt/read/<uuid>
@api.route('/gatt/read/<uuid>', methods=['PUT'])
def update_gatt_read_uuid(uuid):
	is_string = isinstance(uuid, str)
	if is_string == 1:
		print("Received: " + uuid)
		if check_if_valid_field_value(ble_gatt_read_uuid, uuid) == 0:
			ble_msg_fields_dict[ble_gatt_read_uuid] = uuid
			return 'Value Updated', 200
		else:
			print("Received string is not in correct format (xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)")
			return 'Received string is not in correct format (xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)', 400
	else:
		print("Received data is not a string")
		return 'Received data is not a string', 417


# This function is accessible using a PUT request to endpoint: http://127.0.0.1:5900/msg/<message>
@api.route('/msg/<message>', methods=['PUT'])
def update_ble_msg(message):
	is_string = isinstance(message, str)
	if is_string == 1:
		print("Received: " + message)
		if check_if_valid_field_value(ble_msg_str, message) == 0:
			ble_msg_fields_dict[ble_msg_str] = message
			return 'Value Updated', 200
		else:
			print("Received string exceeds char limit")
			return 'Received string exceeds char limit', 400
	else:
		print("Received data is not a string")
		return 'Received data is not a string', 417


# This function is accessible using a POST request to endpoint: http://127.0.0.1:5900/send_msg
@api.route('/send_msg', methods=['POST'])
def send_msg():
	# To send a message over GATT, a device name or a device MAC address is needed
	if (check_if_valid_field_value(ble_device_name, ble_msg_fields_dict[ble_device_name]) == 0 and len(
			ble_msg_fields_dict[ble_device_name]) > 0):
		ready_to_send = 1
	elif (check_if_valid_field_value(ble_device_addr, ble_msg_fields_dict[ble_device_addr]) == 0 and len(
			ble_msg_fields_dict[ble_device_addr]) > 0):
		ready_to_send = 1
	else:
		ready_to_send = 0

	# We check if the provided data is ready for sending a message and receiving the reply over BLE GATT
	for field in field_names:
		# If one of the fields does not have valid data (except for Name and Address), then the msg is not ready to send
		if check_if_valid_field_value(field, ble_msg_fields_dict[field]) != 0 and field != (
				ble_device_name or ble_device_addr):
			ready_to_send = 0

	if ready_to_send == 1:
		try:
			result_str = asyncio.run(main(ble_msg_fields_dict[ble_device_name], ble_msg_fields_dict[ble_device_addr],
										  ble_msg_fields_dict[ble_msg_str], ble_msg_fields_dict[ble_gatt_read_uuid],
										  ble_msg_fields_dict[ble_gatt_write_uuid]))

			ble_msg_result_str_dict[ble_msg_result_str] = result_str
			return result_str, 200

		except Exception as e:
			error_str = generic_exception_handler(e)
			print("Error String: " + error_str)
			return error_str, 500
	else:
		return 'One (or more) data fields are missing or wrongly formatted', 400


# This function returns all fields to their blank state: http://127.0.0.1:5900/clear_fields
@api.route('/clear_fields', methods=['POST'])
def clear_fields():
	ble_msg_fields_dict[ble_device_name] = ""
	ble_msg_fields_dict[ble_device_addr] = ""
	ble_msg_fields_dict[ble_gatt_read_uuid] = ""
	ble_msg_fields_dict[ble_gatt_write_uuid] = ""
	ble_msg_fields_dict[ble_msg_str] = ""

	return 'All fields values are blank', 200


# This function returns all fields to their blank state: http://127.0.0.1:5900/clear_fields
@api.route('/result_str', methods=['GET'])
def return_result_str():
	return ble_msg_result_str_dict[ble_msg_result_str], 200



#api.run(host='127.0.0.1', port=5900, debug=True)
