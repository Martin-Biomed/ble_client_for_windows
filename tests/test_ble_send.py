import time
from unittest import TestCase
from src.ble_request_handler import send_ble_data, find_ble_device
import asyncio
from bleak import BleakScanner

# Note: Due to the lack of BLE server libraries and documentation available for Windows at this time, it became
# infeasible to simulate an actual BLE server using Python.

# Note: Due to the way the asyncio framework works and that Python itself operates entirely on one real thread,
# we did not try to simulate keyboard interrupts or exiting the program prematurely.

# In order for these tests to work, we require an ESP32 loaded with a stable version
# of the (wifi-data-acquisition-server) software also hosted in the same GitHub repo.

# To run these tests in the way they were intended, use the following command on the terminal:
#   1. Navigate to the root directory of this project (ble_client)
#   2. On the terminal type: nosetests --with-spec --spec-color


# This function assumes there are additional bluetooth capable devices in the surrounding area
async def find_random_bluetooth_device(real_ble_device_name: str):
    devices = await BleakScanner.discover()
    default_addr = ""
    for d in devices:
        print("Device detected: ")
        if d.name != real_ble_device_name:
            return d.address

    return default_addr


# Note: To test the wifi_scan, we require the use of an ESP32 configured with the .... software
class TestSendingDataOverGatt(TestCase):

    ble_device_name = "ESP32-BLE-Server"
    known_ble_device_addr = ""
    ble_device_addr = asyncio.run(find_ble_device(ble_device_name, known_ble_device_addr))
    wrong_device_addr = asyncio.run(find_random_bluetooth_device(ble_device_name))

    def setUp(self):
        """ Setup before each Test """
        # This wait time is necessary so that the ESP32 has time to return to GATT advertisement consistently
        time.sleep(2)

    def test_successful_wifi_scan(self):
        """ Test 1: Normal Wi-Fi Scan over the BLE GATT Client """
        user_cmd = '{"cmd": "wifi_scan"}'
        gatt_write_uuid = "0000dead-0000-1000-8000-00805f9b34fb"
        gatt_read_uuid = "0000fef4-0000-1000-8000-00805f9b34fb"

        result_str = asyncio.run(send_ble_data(self.ble_device_addr, user_cmd, gatt_read_uuid, gatt_write_uuid))
        print("The number of results in the list: " + str(len(result_str)))
        self.assertTrue(len(result_str) > 1)

        self.assertNotEquals(result_str, "Asyncio Read GATT Operation: Cancelled")
        self.assertNotEquals(result_str, "Asyncio Write GATT Operation: Cancelled")
        self.assertNotEquals(result_str, "Device with address " + self.ble_device_addr + " was not found.")

    def test_wifi_scan_no_ble_address(self):
        """ Test 2: Call to a BLE Server when no server was found by (find_ble_device) """
        user_cmd = '{"cmd": "wifi_scan"}'
        empty_ble_device_addr = ""
        gatt_write_uuid = "0000dead-0000-1000-8000-00805f9b34fb"
        gatt_read_uuid = "0000fef4-0000-1000-8000-00805f9b34fb"
        result_str = asyncio.run(send_ble_data(empty_ble_device_addr, user_cmd, gatt_read_uuid, gatt_write_uuid))
        self.assertTrue(len(result_str) > 1)
        self.assertEqual(result_str, "Device with address " + empty_ble_device_addr + " was not found.")

    def test_wifi_scan_random_ble_address(self):
        """ Test 3: Call to a BLE Server when a random device MAC (not belonging to any device) is provided """
        user_cmd = '{"cmd": "wifi_scan"}'
        wrong_ble_device_addr = "AA:BB:CC:DD:EE:FF"
        gatt_write_uuid = "0000dead-0000-1000-8000-00805f9b34fb"
        gatt_read_uuid = "0000fef4-0000-1000-8000-00805f9b34fb"
        result_str = asyncio.run(send_ble_data(wrong_ble_device_addr, user_cmd, gatt_read_uuid, gatt_write_uuid))
        self.assertTrue(len(result_str) > 1)
        self.assertEqual(result_str, "Device with address " + wrong_ble_device_addr + " was not found.")

    def test_wifi_scan_wrong_gatt_write_uuid(self):
        """ Test 4: Call to a BLE Server when the wrong GATT UUID (Write) is provided """
        user_cmd = '{"cmd": "wifi_scan"}'
        gatt_write_uuid = "0000xxxx-0000-1000-8000-00805f9b34fb"
        gatt_read_uuid = "0000fef4-0000-1000-8000-00805f9b34fb"
        result_str = asyncio.run(send_ble_data(self.ble_device_addr, user_cmd, gatt_read_uuid, gatt_write_uuid))
        self.assertTrue(len(result_str) > 1)
        self.assertIn("Characteristic", result_str)
        self.assertIn("was not found!", result_str)

    def test_wifi_scan_wrong_gatt_read_uuid(self):
        """ Test 5: Call to a BLE Server when the wrong GATT UUID (Read) is provided """
        user_cmd = '{"cmd": "wifi_scan"}'
        gatt_write_uuid = "0000dead-0000-1000-8000-00805f9b34fb"
        gatt_read_uuid = "0000xxxx-0000-1000-8000-00805f9b34fb"
        result_str = asyncio.run(send_ble_data(self.ble_device_addr, user_cmd, gatt_read_uuid, gatt_write_uuid))
        self.assertTrue(len(result_str) > 1)
        self.assertIn("Characteristic", result_str)
        self.assertIn("was not found!", result_str)

    def test_wifi_scan_missing_gatt_write_uuid(self):
        """ Test 6: Call to a BLE Server when a blank GATT UUID (Write) is provided """
        user_cmd = '{"cmd": "wifi_scan"}'
        gatt_write_uuid = ""
        gatt_read_uuid = "0000fef4-0000-1000-8000-00805f9b34fb"
        result_str = asyncio.run(send_ble_data(self.ble_device_addr, user_cmd, gatt_read_uuid, gatt_write_uuid))
        self.assertTrue(len(result_str) > 1)
        self.assertIn("Characteristic", result_str)
        self.assertIn("was not found!", result_str)

    def test_wifi_scan_missing_gatt_read_uuid(self):
        """ Test 7: Call to a BLE Server when a blank GATT UUID (Read) is provided """
        user_cmd = '{"cmd": "wifi_scan"}'
        gatt_write_uuid = "0000dead-0000-1000-8000-00805f9b34fb"
        gatt_read_uuid = ""
        result_str = asyncio.run(send_ble_data(self.ble_device_addr, user_cmd, gatt_read_uuid, gatt_write_uuid))
        self.assertTrue(len(result_str) > 1)
        self.assertIn("Characteristic", result_str)
        self.assertIn("was not found!", result_str)