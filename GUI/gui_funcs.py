from PyQt5 import QtWidgets
from ble_request_handler import main
from result_str_class import Result_String
import asyncio
import re

# Each field has a max number of chars allowed
max_uuid_str_len = 36
max_mac_addr_len = 18
max_device_name_len = 100
max_msg_len = 100

ble_msg_fields_dict = {}

# BLE Field names required to send a message to the BLE GATT Client
ble_device_name = "ble_device_name"
ble_device_addr = "ble_device_addr"
ble_gatt_write_uuid = "ble_gatt_write_uuid"
ble_gatt_read_uuid = "ble_gatt_read_uuid"
ble_msg_str = "ble_msg_str"

field_names = [ble_device_name, ble_device_addr, ble_gatt_write_uuid, ble_gatt_read_uuid, ble_msg_str]

def help_button_clicked():
	print("Help Button clicked")


# There is a specific set of criteria for each field value to determine if the value is valid
def check_if_valid_field_value(usr_field_name: str, qt_text_str: str) -> int:
	# Valid Value -> Return 0

	# Check the BLE Device Name is valid
	if usr_field_name == ble_device_name:
		if len(qt_text_str) <= max_device_name_len:
			return 0
		else:
			print("Device Name with length " + str(len(qt_text_str)) + " exceeds char limit.")
			return -1

	# Check the BLE Device Address is valid
	elif usr_field_name == ble_device_addr:
		if 0 < len(qt_text_str) <= max_mac_addr_len:
			# Check if the entered MAC address matches the format for a MAC address
			if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", qt_text_str):
				return 0
			else:
				print(
					"Provided MAC address did not match format: xx:xx:xx:xx:xx:xx (Note: F is highest Hex value allowed)")
				return -1

		elif len(qt_text_str) == 0:
			return 0

		else:
			print("Device MAC Address with length " + str(len(qt_text_str)) + " exceeds char limit.")
			return -1

	# Check the BLE GATT Write Characteristic UUID is valid
	elif usr_field_name == ble_gatt_write_uuid:
		if max_uuid_str_len >= len(qt_text_str) > 0:
			# [\x00-\x7F]{4} = (x4) ASCII characters
			if re.match("[\x00-\x7F]{8}-[\x00-\x7F]{4}-[\x00-\x7F]{4}-[\x00-\x7F]{4}-[\x00-\x7F]{12}", qt_text_str):
				return 0
			else:
				print("Provided GATT Write UUID did not match format: xxxxxxxx-xxxx-xxxxx-xxxx-xxxxxxxxxxxx")
				return -1

		elif len(qt_text_str) == 0:
			print("GATT Write UUID is required to receive replies from BLE GATT Server")
			return -1

		else:
			print("BLE GATT Write UUID with length " + str(len(qt_text_str)) + " exceeds char limit.")
			return -1

	# Check the BLE GATT Read Characteristic UUID is valid
	elif usr_field_name == ble_gatt_read_uuid:
		if max_uuid_str_len >= len(qt_text_str) > 0:
			# [\x00-\x7F]{4} = (x4) ASCII characters
			if re.match("[\x00-\x7F]{8}-[\x00-\x7F]{4}-[\x00-\x7F]{4}-[\x00-\x7F]{4}-[\x00-\x7F]{12}", qt_text_str):
				return 0
			else:
				print("Provided GATT Read UUID did not match format: xxxxxxxx-xxxx-xxxxx-xxxx-xxxxxxxxxxxx")
				return -1

		elif len(qt_text_str) == 0:
			print("GATT Read UUID is required to send a message to BLE GATT Server")
			return -1

		else:
			print("BLE GATT Read UUID with length " + str(len(qt_text_str)) + " exceeds char limit.")
			return -1

	# Check the message to be sent over BLE GATT is valid
	elif usr_field_name == ble_msg_str:
		if len(qt_text_str) <= max_msg_len:
			return 0
		else:
			print("Message string with length " + str(len(qt_text_str)) + " exceeds char limit.")
			return -1


# The OK button on the main GUI screen takes the text inputs from and prepares to send/receive GATT msg and reply
def main_screen_ok_button_clicked(input_obj: Result_String):
	print("Main GUI Page OK Button Clicked")
	print("The fields have been updated with the following values: ")
	device_known = 0  # To send a msg, either the MAC address or the Device Name must be provided

	for key, value in ble_msg_fields_dict.items():
		if check_if_valid_field_value(key, value) == 0:
			print(key, ": ", value)
			if key == ble_device_name and len(value) > 0:
				device_known = 1
			if key == ble_device_addr and len(value) > 0:
				device_known = 1

	result_str = ""

	if device_known == 1:
		print("Valid message ready to send")
		result_str = asyncio.run(main(ble_msg_fields_dict[ble_device_name], ble_msg_fields_dict[ble_device_addr],
						 ble_msg_fields_dict[ble_msg_str], ble_msg_fields_dict[ble_gatt_read_uuid],
						 ble_msg_fields_dict[ble_gatt_write_uuid]))
	else:
		print("Either the BLE Server MAC address or Device Name must be provided")

	input_obj.set_result_str(result_str)


# This function updates a ble_msg_fields_dict entry based on the value of a single QtWidgets.QTextEdit obj
def update_qt_text_str(usr_field_name: str, qt_text_str: str):
	print("The QTextEdit Object String is: " + qt_text_str)
	for field in field_names:
		if usr_field_name == field:

			# Certain fields need to be in lowercase to be used with the request handler
			if field == ble_device_addr or field == ble_gatt_write_uuid or field == ble_gatt_read_uuid:
				qt_text_str = qt_text_str.lower()

			ble_msg_fields_dict[field] = qt_text_str
			print("Field with name " + field + " has been updated\n")
