
import asyncio
import logging

import src.ble_request_handler
from src.result_str_class import Result_String
from src.field_format_funcs import (ble_msg_fields_dict, field_names, check_if_valid_field_value, ble_device_name,
									ble_device_addr, ble_msg_str, ble_gatt_read_uuid, ble_gatt_write_uuid,
									ble_msg_result_str_dict, ble_msg_result_str)


# The OK button on the main GUI screen takes the text inputs from and prepares to send/receive GATT msg and reply
def main_screen_ok_button_clicked(input_obj: Result_String):
	logging.info("BLE Client Message Config Dialog OK Button Clicked")
	logging.info("The fields have been updated with the following values: ")
	device_known = 0  # To send a msg, either the MAC address or the Device Name must be provided

	for key, value in ble_msg_fields_dict.items():
		if check_if_valid_field_value(key, value) == 0:
			logging.info(key, ": ", value)
			if key == ble_device_name and len(value) > 0:
				device_known = 1
			if key == ble_device_addr and len(value) > 0:
				device_known = 1

	result_str = ""

	if device_known == 1:
		logging.info("Valid message ready to send")
		result_str = asyncio.run(src.ble_request_handler.main(ble_msg_fields_dict[ble_device_name],
														  ble_msg_fields_dict[ble_device_addr],
														  ble_msg_fields_dict[ble_msg_str],
														  ble_msg_fields_dict[ble_gatt_read_uuid],
														  ble_msg_fields_dict[ble_gatt_write_uuid]))
	else:
		logging.error("Either the BLE Server MAC address or Device Name must be provided")

	input_obj.set_result_str(result_str)


# This function updates a ble_msg_fields_dict entry based on the value of a single QtWidgets.QTextEdit object
def update_qt_text_str(usr_field_name: str, qt_text_str: str):
	logging.info("The QTextEdit Object String is: " + qt_text_str)
	# We iterate over all fields in the field_names array (basis for the fields in the dictionary)
	for field in field_names:

		if usr_field_name == field:

			# Certain fields need to be in lowercase to be used with the request handler
			if field == ble_device_addr or field == ble_gatt_write_uuid or field == ble_gatt_read_uuid:
				qt_text_str = qt_text_str.lower()

			ble_msg_fields_dict[field] = qt_text_str
			logging.info("Field with name " + field + " has been updated\n")

	# The result string is kept in its own separate dictionary
	if usr_field_name == ble_msg_result_str:
		logging.info("Field with name " + usr_field_name + " has been updated\n")
		ble_msg_result_str_dict[usr_field_name] = qt_text_str
