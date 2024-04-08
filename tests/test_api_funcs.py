from unittest import TestCase
from access_api_functions import api, server_ip, server_port
from field_format_funcs import max_msg_len, max_mac_addr_len, max_device_name_len, max_uuid_str_len
import random
import string


# In order for these tests to work, we require an ESP32 loaded with a stable version
# of the (wifi-data-acquisition-server) software also hosted in the same GitHub repo.

# To run these tests in the way they were intended, use the following command on the terminal:
#   1. Navigate to the root directory of this project (ble_client)
#   2. On the terminal type: nosetests --with-spec --spec-color

def random_mac():
	separator_char = ':'
	separator_spacing = 2
	unseparated_mac = ''.join([hex(random.randint(0, 255))[2:].zfill(2) for _ in range(6)])
	return f'{separator_char}'.join(
		unseparated_mac[i:i + separator_spacing] for i in range(0, len(unseparated_mac), separator_spacing))


def generate_random_string(length: int):
	characters = string.ascii_letters + string.digits + "-" + "_" + "+" + "*"
	# Randomly choose characters from letters for the given length of the string
	# Certain punctuation characters can cause unwanted URL interpretation implications
	random_string = ''.join(random.choice(characters) for i in range(length))
	return random_string


class TestBleClientApi(TestCase):
	# Flask servers have a built-in test client option to output status messages in the terminal (being used to run tests)
	api.testing = True
	api.config['SERVER_NAME'] = server_ip + ":" + str(server_port)
	test_api_instance = api.test_client()

	def setUp(self):
		""" Setup before each Test """
		# Write API Functions to clear the value of each of the terms
		endpoint = "/clear_fields"
		response = self.test_api_instance.post(endpoint)
		self.assertEquals(response.status_code, 200)

	def test_update_valid_device_name(self):
		""" Test 1: Updating a valid BLE Device Name value using the API endpoint  """
		endpoint = "/device/name"
		arg = "ESP32-BLE-Server"
		print("Sending PUT request to: " + endpoint + "/" + arg)
		response = self.test_api_instance.put(endpoint + "/" + arg)
		self.assertTrue(len(response.data.decode('utf-8')) > 1)
		self.assertEquals(response.data.decode('utf-8'), "Value Updated")
		self.assertEquals(response.status_code, 200)

	def test_update_blank_device_name(self):
		""" Test 2: Updating a blank BLE Device Name value using the API endpoint  """
		endpoint = "/device/name"
		arg = ""
		print("Sending PUT request to: " + endpoint + "/" + arg)
		response = self.test_api_instance.put(endpoint + "/" + arg)
		self.assertTrue(len(response.data.decode('utf-8')) > 1)
		self.assertEquals(response.status_code, 404)

	def test_update_excess_length_device_name(self):
		""" Test 3: Updating a BLE Device Name (consisting of excess chars) using the API endpoint  """
		endpoint = "/device/name"
		arg = generate_random_string(max_device_name_len * 2)
		print("Sending PUT request to: " + endpoint + "/" + arg)
		response = self.test_api_instance.put(endpoint + "/" + arg)
		self.assertTrue(len(response.data.decode('utf-8')) > 1)
		self.assertEquals(response.data.decode('utf-8'), "Received string exceeds char limit")
		self.assertEquals(response.status_code, 400)

	def test_update_valid_device_addr(self):
		""" Test 4: Updating a valid BLE Device Address value using the API endpoint  """
		endpoint = "/device/address"
		# We create a random MAC Address (with valid format)
		arg = random_mac()
		print("Sending PUT request to: " + endpoint + "/" + arg)
		response = self.test_api_instance.put(endpoint + "/" + arg)
		self.assertTrue(len(response.data.decode('utf-8')) > 1)
		self.assertEquals(response.data.decode('utf-8'), "Value Updated")
		self.assertEquals(response.status_code, 200)

	def test_update_blank_device_addr(self):
		""" Test 5: Updating a blank BLE Device Address value using the API endpoint  """
		endpoint = "/device/address"
		arg = ""
		print("Sending PUT request to: " + endpoint + "/" + arg)
		response = self.test_api_instance.put(endpoint + "/" + arg)
		self.assertTrue(len(response.data.decode('utf-8')) > 1)
		self.assertEquals(response.status_code, 404)

	def test_update_wrong_delimiter_device_addr(self):
		""" Test 6: Updating a BLE Device Address value (using the wrong delimiter) using the API endpoint  """
		endpoint = "/device/address"
		arg = "AA+AA+BB+CC+DD"
		print("Sending PUT request to: " + endpoint + "/" + arg)
		response = self.test_api_instance.put(endpoint + "/" + arg)
		self.assertTrue(len(response.data.decode('utf-8')) > 1)
		self.assertEquals(response.data.decode('utf-8'),
						"MAC address did not match format: xx:xx:xx:xx:xx:xx (Note: F is highest Hex value allowed)")
		self.assertEquals(response.status_code, 400)

	def test_update_wrong_str_format_device_addr(self):
		""" Test 7: Updating a BLE Device Address value (random string of expected length) using the API endpoint  """
		endpoint = "/device/address"
		arg = generate_random_string(max_mac_addr_len)
		print("Sending PUT request to: " + endpoint + "/" + arg)
		response = self.test_api_instance.put(endpoint + "/" + arg)
		self.assertTrue(len(response.data.decode('utf-8')) > 1)
		self.assertEquals(response.data.decode('utf-8'),
						"MAC address did not match format: xx:xx:xx:xx:xx:xx (Note: F is highest Hex value allowed)")
		self.assertEquals(response.status_code, 400)

	def test_update_wrong_str_length_device_addr(self):
		""" Test 8: Updating a BLE Device Address value (MAC Address with extra octet) using the API endpoint  """
		endpoint = "/device/address"
		arg = ':'.join('%02x' % random.randint(0, 255) for x in range(7))
		print("Sending PUT request to: " + endpoint + "/" + arg)
		response = self.test_api_instance.put(endpoint + "/" + arg)
		self.assertTrue(len(response.data.decode('utf-8')) > 1)
		self.assertEquals(response.data.decode('utf-8'),
						"MAC address did not match format: xx:xx:xx:xx:xx:xx (Note: F is highest Hex value allowed)")
		self.assertEquals(response.status_code, 400)

	def test_update_write_uuid(self):
		""" Test 9: Updating a valid BLE Write GATT UUID value using the API endpoint  """
		endpoint = "/gatt/write"
		arg = "0000dead-0000-1000-8000-00805f9b34fb"
		print("Sending PUT request to: " + endpoint + "/" + arg)
		response = self.test_api_instance.put(endpoint + "/" + arg)
		self.assertTrue(len(response.data.decode('utf-8')) > 1)
		self.assertEquals(response.data.decode('utf-8'), "Value Updated")
		self.assertEquals(response.status_code, 200)

	def test_update_empty_write_uuid(self):
		""" Test 10: Updating a blank BLE Write GATT UUID value using the API endpoint  """
		endpoint = "/gatt/write"
		arg = ""
		print("Sending PUT request to: " + endpoint + "/" + arg)
		response = self.test_api_instance.put(endpoint + "/" + arg)
		self.assertTrue(len(response.data.decode('utf-8')) > 1)
		self.assertEquals(response.status_code, 404)

	def test_update_wrong_delimiter_write_uuid(self):
		""" Test 11: Updating a BLE Write GATT UUID value (using the wrong delimiter) using the API endpoint  """
		endpoint = "/gatt/write"
		arg = "0000dead:0000:1000:8000:00805f9b34fb"
		print("Sending PUT request to: " + endpoint + "/" + arg)
		response = self.test_api_instance.put(endpoint + "/" + arg)
		self.assertTrue(len(response.data.decode('utf-8')) > 1)
		self.assertEquals(response.data.decode('utf-8'),
						"Received string is not in correct format (xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)")
		self.assertEquals(response.status_code, 400)

	def test_update_wrong_str_format_write_uuid(self):
		""" Test 12: Updating a BLE GATT Write UUID value (random string of expected length) using the API endpoint  """
		endpoint = "/gatt/write"
		arg = generate_random_string(max_uuid_str_len)
		print("Sending PUT request to: " + endpoint + "/" + arg)
		response = self.test_api_instance.put(endpoint + "/" + arg)
		self.assertTrue(len(response.data.decode('utf-8')) > 1)
		self.assertEquals(response.data.decode('utf-8'),
						"Received string is not in correct format (xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)")
		self.assertEquals(response.status_code, 400)

	def test_update_read_uuid(self):
		""" Test 13: Updating a valid BLE Read GATT UUID value using the API endpoint  """
		endpoint = "/gatt/read"
		# We create a random MAC Address (with valid format)
		arg = "0000fef4-0000-1000-8000-00805f9b34fb"
		print("Sending PUT request to: " + endpoint + "/" + arg)
		response = self.test_api_instance.put(endpoint + "/" + arg)
		self.assertTrue(len(response.data.decode('utf-8')) > 1)
		self.assertEquals(response.data.decode('utf-8'), "Value Updated")
		self.assertEquals(response.status_code, 200)

	def test_update_empty_read_uuid(self):
		""" Test 14: Updating a blank BLE Read GATT UUID value using the API endpoint  """
		endpoint = "/gatt/read"
		# We create a random MAC Address (with valid format)
		arg = ""
		print("Sending PUT request to: " + endpoint + "/" + arg)
		response = self.test_api_instance.put(endpoint + "/" + arg)
		self.assertTrue(len(response.data.decode('utf-8')) > 1)
		self.assertEquals(response.status_code, 404)

	def test_update_wrong_delimiter_read_uuid(self):
		""" Test 15: Updating a BLE GATT Read UUID value (using the wrong delimiter) using the API endpoint  """
		endpoint = "/gatt/read"
		arg = "0000fef4:0000:1000:8000:00805f9b34fb"
		print("Sending PUT request to: " + endpoint + "/" + arg)
		response = self.test_api_instance.put(endpoint + "/" + arg)
		self.assertTrue(len(response.data.decode('utf-8')) > 1)
		self.assertEquals(response.data.decode('utf-8'),
						"Received string is not in correct format (xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)")
		self.assertEquals(response.status_code, 400)

	def test_update_wrong_str_format_read_uuid(self):
		""" Test 16: Updating a BLE GATT Read UUID value (random string of expected length) using the API endpoint  """
		endpoint = "/gatt/read"
		arg = generate_random_string(max_uuid_str_len)
		print("Sending PUT request to: " + endpoint + "/" + arg)
		response = self.test_api_instance.put(endpoint + "/" + arg)
		self.assertTrue(len(response.data.decode('utf-8')) > 1)
		self.assertEquals(response.data.decode('utf-8'),
						"Received string is not in correct format (xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)")
		self.assertEquals(response.status_code, 400)

	def test_update_valid_msg(self):
		""" Test 17: Updating a valid message string using the API endpoint  """
		endpoint = "/msg"
		arg = "wifi_scan"
		print("Sending PUT request to: " + endpoint + "/" + arg)
		response = self.test_api_instance.put(endpoint + "/" + arg)
		self.assertTrue(len(response.data.decode('utf-8')) > 1)
		self.assertEquals(response.data.decode('utf-8'), "Value Updated")
		self.assertEquals(response.status_code, 200)

	def test_update_max_length_valid_msg(self):
		""" Test 18: Updating a random valid message string (max allowable char limit) using the API endpoint  """
		endpoint = "/msg"
		arg = generate_random_string(max_msg_len)
		print("Sending PUT request to: " + endpoint + "/" + arg)
		response = self.test_api_instance.put(endpoint + "/" + arg)
		self.assertTrue(len(response.data.decode('utf-8')) > 1)
		self.assertEquals(response.data.decode('utf-8'), "Value Updated")
		self.assertEquals(response.status_code, 200)

	def test_update_blank_msg(self):
		""" Test 19: Updating a blank message string using the API endpoint  """
		endpoint = "/msg"
		arg = ""
		print("Sending PUT request to: " + endpoint + "/" + arg)
		response = self.test_api_instance.put(endpoint + "/" + arg)
		self.assertTrue(len(response.data.decode('utf-8')) > 1)
		self.assertEquals(response.status_code, 404)

	def test_update_excess_length_msg(self):
		""" Test 20: Updating a message string (consisting of excess chars) using the API endpoint  """
		endpoint = "/msg"
		arg = generate_random_string(max_msg_len * 2)
		print("Sending PUT request to: " + endpoint + "/" + arg)
		response = self.test_api_instance.put(endpoint + "/" + arg)
		self.assertTrue(len(response.data.decode('utf-8')) > 1)
		self.assertEquals(response.data.decode('utf-8'), "Received string exceeds char limit")
		self.assertEquals(response.status_code, 400)

	# These tests are effective when the ESP32 running the (wifi-data-acquisition-server) is available
	def test_valid_device_name_send_msg(self):
		""" Test 21: Sending the Message String to the BLE GATT device (Using Device Name) using the API endpoint  """
		# Ensure that the device name is appropriate
		endpoint = "/device/name"
		arg = "ESP32-BLE-Server"
		print("Sending PUT request to: " + endpoint + "/" + arg)
		response = self.test_api_instance.put(endpoint + "/" + arg)
		self.assertTrue(len(response.data.decode('utf-8')) > 1)
		self.assertEquals(response.data.decode('utf-8'), "Value Updated")
		self.assertEquals(response.status_code, 200)

		# Ensure that the BLE GATT Write UUID is appropriate
		endpoint = "/gatt/write"
		arg = "0000dead-0000-1000-8000-00805f9b34fb"
		print("Sending PUT request to: " + endpoint + "/" + arg)
		response = self.test_api_instance.put(endpoint + "/" + arg)
		self.assertTrue(len(response.data.decode('utf-8')) > 1)
		self.assertEquals(response.data.decode('utf-8'), "Value Updated")
		self.assertEquals(response.status_code, 200)

		# Ensure that the BLE GATT Read UUID is appropriate
		endpoint = "/gatt/read"
		arg = "0000fef4-0000-1000-8000-00805f9b34fb"
		print("Sending PUT request to: " + endpoint + "/" + arg)
		response = self.test_api_instance.put(endpoint + "/" + arg)
		self.assertTrue(len(response.data.decode('utf-8')) > 1)
		self.assertEquals(response.data.decode('utf-8'), "Value Updated")
		self.assertEquals(response.status_code, 200)

		# Ensure the msg is configured to do a wifi-scan on an ESP32 device loaded with the appropriate sw (see top of file)
		endpoint = "/msg"
		arg = "wifi_scan"
		print("Sending PUT request to: " + endpoint + "/" + arg)
		response = self.test_api_instance.put(endpoint + "/" + arg)
		self.assertTrue(len(response.data.decode('utf-8')) > 1)
		self.assertEquals(response.data.decode('utf-8'), "Value Updated")
		self.assertEquals(response.status_code, 200)

		# Send the message
		endpoint = "/send_msg"
		print("Sending POST request to: " + endpoint)
		response = self.test_api_instance.post(endpoint)
		self.assertTrue(len(response.data.decode('utf-8')) > 1)
		self.assertEquals(response.status_code, 200)

	def test_valid_device_addr_send_msg(self):
		""" Test 22: Sending the Message String to the BLE GATT device (Using Device Address) using the API endpoint  """
		# Ensure that the device name is appropriate
		endpoint = "/device/address"
		arg = "aa:bb:cc:dd:ee:ff"
		print("Sending PUT request to: " + endpoint + "/" + arg)
		response = self.test_api_instance.put(endpoint + "/" + arg)
		self.assertTrue(len(response.data.decode('utf-8')) > 1)
		self.assertEquals(response.data.decode('utf-8'), "Value Updated")
		self.assertEquals(response.status_code, 200)

		# Ensure that the BLE GATT Write UUID is appropriate
		endpoint = "/gatt/write"
		arg = "0000dead-0000-1000-8000-00805f9b34fb"
		print("Sending PUT request to: " + endpoint + "/" + arg)
		response = self.test_api_instance.put(endpoint + "/" + arg)
		self.assertTrue(len(response.data.decode('utf-8')) > 1)
		self.assertEquals(response.data.decode('utf-8'), "Value Updated")
		self.assertEquals(response.status_code, 200)

		# Ensure that the BLE GATT Read UUID is appropriate
		endpoint = "/gatt/read"
		arg = "0000fef4-0000-1000-8000-00805f9b34fb"
		print("Sending PUT request to: " + endpoint + "/" + arg)
		response = self.test_api_instance.put(endpoint + "/" + arg)
		self.assertTrue(len(response.data.decode('utf-8')) > 1)
		self.assertEquals(response.data.decode('utf-8'), "Value Updated")
		self.assertEquals(response.status_code, 200)

		# Ensure the msg is configured to do a wifi-scan on an ESP32 device loaded with the appropriate sw (see top of file)
		endpoint = "/msg"
		arg = "wifi_scan"
		print("Sending PUT request to: " + endpoint + "/" + arg)
		response = self.test_api_instance.put(endpoint + "/" + arg)
		self.assertTrue(len(response.data.decode('utf-8')) > 1)
		self.assertEquals(response.data.decode('utf-8'), "Value Updated")
		self.assertEquals(response.status_code, 200)

		# Send the message
		endpoint = "/send_msg"
		print("Sending POST request to: " + endpoint)
		response = self.test_api_instance.post(endpoint)
		self.assertTrue(len(response.data.decode('utf-8')) > 1)
		self.assertEquals(response.status_code, 200)

	def test_missing_device_name_send_msg(self):
		""" Test 23: Sending the Message String to the BLE GATT device (Missing Device Name) using the API endpoint  """
		# The set up function ensures that the Device Name field is blank by default

		# Ensure that the BLE GATT Write UUID is appropriate
		endpoint = "/gatt/write"
		arg = "0000dead-0000-1000-8000-00805f9b34fb"
		print("Sending PUT request to: " + endpoint + "/" + arg)
		response = self.test_api_instance.put(endpoint + "/" + arg)
		self.assertTrue(len(response.data.decode('utf-8')) > 1)
		self.assertEquals(response.data.decode('utf-8'), "Value Updated")
		self.assertEquals(response.status_code, 200)

		# Ensure that the BLE GATT Read UUID is appropriate
		endpoint = "/gatt/read"
		arg = "0000fef4-0000-1000-8000-00805f9b34fb"
		print("Sending PUT request to: " + endpoint + "/" + arg)
		response = self.test_api_instance.put(endpoint + "/" + arg)
		self.assertTrue(len(response.data.decode('utf-8')) > 1)
		self.assertEquals(response.data.decode('utf-8'), "Value Updated")
		self.assertEquals(response.status_code, 200)

		# Ensure the msg is configured to do a wifi-scan on an ESP32 device loaded with the appropriate sw (see top of file)
		endpoint = "/msg"
		arg = "wifi_scan"
		print("Sending PUT request to: " + endpoint + "/" + arg)
		response = self.test_api_instance.put(endpoint + "/" + arg)
		self.assertTrue(len(response.data.decode('utf-8')) > 1)
		self.assertEquals(response.data.decode('utf-8'), "Value Updated")
		self.assertEquals(response.status_code, 200)

		# Send the message
		endpoint = "/send_msg"
		print("Sending POST request to: " + endpoint)
		response = self.test_api_instance.post(endpoint)
		self.assertTrue(len(response.data.decode('utf-8')) > 1)
		self.assertEquals(response.data.decode('utf-8'), "One (or more) data fields are missing or wrongly formatted")
		self.assertEquals(response.status_code, 400)

	def test_blank_fields_send_msg(self):
		""" Test 24: Sending the Message String to the BLE GATT device (All Field Names Blank) using the API endpoint  """
		# Send the message
		endpoint = "/send_msg"
		print("Sending POST request to: " + endpoint)
		response = self.test_api_instance.post(endpoint)
		self.assertTrue(len(response.data.decode('utf-8')) > 1)
		self.assertEquals(response.data.decode('utf-8'), "One (or more) data fields are missing or wrongly formatted")
		self.assertEquals(response.status_code, 400)

	def test_valid_device_name_result_str(self):
		""" Test 25: Retrieving the valid Result String using the API function """
		# Ensure that the device name is appropriate
		endpoint = "/device/name"
		arg = "ESP32-BLE-Server"
		print("Sending PUT request to: " + endpoint + "/" + arg)
		response = self.test_api_instance.put(endpoint + "/" + arg)
		self.assertTrue(len(response.data.decode('utf-8')) > 1)
		self.assertEquals(response.data.decode('utf-8'), "Value Updated")
		self.assertEquals(response.status_code, 200)

		# Ensure that the BLE GATT Write UUID is appropriate
		endpoint = "/gatt/write"
		arg = "0000dead-0000-1000-8000-00805f9b34fb"
		print("Sending PUT request to: " + endpoint + "/" + arg)
		response = self.test_api_instance.put(endpoint + "/" + arg)
		self.assertTrue(len(response.data.decode('utf-8')) > 1)
		self.assertEquals(response.data.decode('utf-8'), "Value Updated")
		self.assertEquals(response.status_code, 200)

		# Ensure that the BLE GATT Read UUID is appropriate
		endpoint = "/gatt/read"
		arg = "0000fef4-0000-1000-8000-00805f9b34fb"
		print("Sending PUT request to: " + endpoint + "/" + arg)
		response = self.test_api_instance.put(endpoint + "/" + arg)
		self.assertTrue(len(response.data.decode('utf-8')) > 1)
		self.assertEquals(response.data.decode('utf-8'), "Value Updated")
		self.assertEquals(response.status_code, 200)

		# Ensure the msg is configured to do a wifi-scan on an ESP32 device loaded with the appropriate sw (see top of file)
		endpoint = "/msg"
		arg = "wifi_scan"
		print("Sending PUT request to: " + endpoint + "/" + arg)
		response = self.test_api_instance.put(endpoint + "/" + arg)
		self.assertTrue(len(response.data.decode('utf-8')) > 1)
		self.assertEquals(response.data.decode('utf-8'), "Value Updated")
		self.assertEquals(response.status_code, 200)

		# Send the message
		endpoint = "/send_msg"
		print("Sending POST request to: " + endpoint)
		response = self.test_api_instance.post(endpoint)
		self.assertTrue(len(response.data.decode('utf-8')) > 1)
		self.assertEquals(response.status_code, 200)

		# Retrieve message result
		endpoint = "/result_str"
		print("Sending GET request to: " + endpoint)
		response = self.test_api_instance.get(endpoint)
		self.assertTrue(len(response.data.decode('utf-8')) > 1)
		self.assertEquals(response.status_code, 200)
