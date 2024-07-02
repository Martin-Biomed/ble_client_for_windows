
import re
import logging

# Each field has a max number of chars allowed
max_uuid_str_len = 36
max_mac_addr_len = 18
max_device_name_len = 100
max_msg_len = 100

############################ Dictionary ##############################

# We need to access the values in the dictionary from multiple files
global ble_msg_fields_dict
ble_msg_fields_dict = {}

# BLE Field names required to send a message to the BLE GATT Client
ble_device_name = "ble_device_name"
ble_device_addr = "ble_device_addr"
ble_gatt_write_uuid = "ble_gatt_write_uuid"
ble_gatt_read_uuid = "ble_gatt_read_uuid"
ble_msg_str = "ble_msg_str"

field_names = [ble_device_name, ble_device_addr, ble_gatt_write_uuid, ble_gatt_read_uuid, ble_msg_str]

# We create a dictionary with a single term in it so that the result_str is available in multiple files
global ble_msg_result_str_dict
ble_msg_result_str_dict = {}
ble_msg_result_str = "ble_msg_result_str"

################################ Functions ########################################

# There is a specific set of criteria for each field value to determine if the value is valid
def check_if_valid_field_value(usr_field_name: str, qt_text_str: str) -> int:
	# Valid Value -> Return 0

	# Check the BLE Device Name is valid
	if usr_field_name == ble_device_name:
		if len(qt_text_str) <= max_device_name_len:
			return 0
		else:
			logging.error("Device Name with length " + str(len(qt_text_str)) + " exceeds char limit.")
			return -1

	# Check the BLE Device Address is valid
	elif usr_field_name == ble_device_addr:
		if 0 < len(qt_text_str) <= max_mac_addr_len:
			# Check if the entered MAC address matches the format for a MAC address
			if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", qt_text_str):
				return 0
			else:
				logging.error("Provided MAC address did not match format: xx:xx:xx:xx:xx:xx (Note: F is highest Hex value allowed)")
				return -1

		elif len(qt_text_str) == 0:
			return 0

		else:
			logging.error("Device MAC Address with length " + str(len(qt_text_str)) + " exceeds char limit.")
			return -1

	# Check the BLE GATT Write Characteristic UUID is valid
	elif usr_field_name == ble_gatt_write_uuid:
		if max_uuid_str_len >= len(qt_text_str) > 0:
			# [\x00-\x7F]{4} = (x4) ASCII characters. Only ASCII characters are acceptable for UUID.
			if re.match("[\x00-\x7F]{8}-[\x00-\x7F]{4}-[\x00-\x7F]{4}-[\x00-\x7F]{4}-[\x00-\x7F]{12}", qt_text_str):
				return 0
			else:
				logging.error("Provided GATT Write UUID did not match format: xxxxxxxx-xxxx-xxxxx-xxxx-xxxxxxxxxxxx")
				return -1

		elif len(qt_text_str) == 0:
			logging.error("GATT Write UUID is required to receive replies from BLE GATT Server")
			return -1

		else:
			logging.error("BLE GATT Write UUID with length " + str(len(qt_text_str)) + " exceeds char limit.")
			return -1

	# Check the BLE GATT Read Characteristic UUID is valid
	elif usr_field_name == ble_gatt_read_uuid:
		if max_uuid_str_len >= len(qt_text_str) > 0:
			# [\x00-\x7F]{4} = (x4) ASCII characters. Only ASCII characters are acceptable for UUID.
			if re.match("[\x00-\x7F]{8}-[\x00-\x7F]{4}-[\x00-\x7F]{4}-[\x00-\x7F]{4}-[\x00-\x7F]{12}", qt_text_str):
				return 0
			else:
				logging.error("Provided GATT Read UUID did not match format: xxxxxxxx-xxxx-xxxxx-xxxx-xxxxxxxxxxxx")
				return -1

		elif len(qt_text_str) == 0:
			logging.error("GATT Read UUID is required to send a message to BLE GATT Server")
			return -1

		else:
			logging.error("BLE GATT Read UUID with length " + str(len(qt_text_str)) + " exceeds char limit.")
			return -1

	# Check the message to be sent over BLE GATT is valid
	elif usr_field_name == ble_msg_str:
		if len(qt_text_str) <= max_msg_len:
			return 0
		else:
			logging.error("Message string with length " + str(len(qt_text_str)) + " exceeds char limit.")
			return -1

