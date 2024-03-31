import asyncio
import json
import sys
import os

import bleak
from bleak import BleakClient
from bleak import BleakScanner

ble_device_name = "ESP32-BLE-Server"
base_uuid = "-0000-1000-8000-00805f9b34fb"

read_uuid = "0000fef4"
write_uuid = "0000dead"


def generic_exception_handler(e: BaseException) -> str:
    print(f'Exception caught: {e}')
    err_str = str(e)
    return err_str


# This function allows this device to connect to a remote BLE GAP server
async def find_ble_device(device_name: str) -> str:
    devices = await BleakScanner.discover()
    for d in devices:
        print("Device detected: ")
        print(d.address)
        print(d.name)

        if d.name == device_name:
            return d.address

    return "BLE Device Not Found"


# This function requires the following known GATT characteristic UUIDs:
# - GATT Write Characteristic of Remote GATT server
# - GATT Read Characteristic of Remote GATT server

# The function sends a message (cmd) to the remote server through the remote device's GATT Write UUID
# and receives the corresponding callback msg from the remote device's GATT Read UUID.
async def send_ble_data(ble_device_address: str, command: str) -> str:

    try:
        # Connect to the ESP32 device
        async with BleakClient(ble_device_address, use_cached=False) as client:

            # Send parameter to ESP32
            print("Sending Message to: " + ble_device_name)
            complete_write_uuid = write_uuid + base_uuid

            print("Writing to Service with UUID: " + complete_write_uuid)
            try:
                # We send the data over GATT and await the asynchronous response
                await client.write_gatt_char(complete_write_uuid, command.encode('utf-8'), response=False)

            except asyncio.CancelledError:
                access_points_str = "Asyncio Write GATT Operation: Cancelled"
                try:
                    disconnect_result = await client.disconnect()
                    print("Disconnect Successful: " + str(disconnect_result))
                except Exception as e:
                    access_points_str += "\n "
                    access_points_str += generic_exception_handler(e)
                return access_points_str

            # Receive data from ESP32 via BLE (response from BLE server)
            try:
                print("Awaiting Response from Service with UUID: " + read_uuid + base_uuid)
                new_data = await client.read_gatt_char(read_uuid + base_uuid)

            except asyncio.CancelledError:
                access_points_str = "Asyncio Read GATT Operation: Cancelled"
                try:
                    disconnect_result = await client.disconnect()
                    print("Disconnect Successful: " + str(disconnect_result))
                except Exception as e:
                    access_points_str += "\n "
                    access_points_str += generic_exception_handler(e)
                return access_points_str

            # Executes when the user receives a msg from the selected GATT characteristic
            print("Data from BLE Server: " + str(new_data))
            print("Length of ByteArray is: " + str(len(new_data)))
            encoding = json.detect_encoding(new_data)
            print("Data Has been Encoded using: " + encoding)

            if encoding == "utf-8":
                print("Data from BLE Server: {0}".format("".join(map(chr, new_data))))
                access_points_str = new_data.decode()
                return access_points_str

    except Exception as e:
        error_str = generic_exception_handler(e)
        print("Error String: " + error_str)
        return error_str


async def main(user_command: str):
    print("Looking for Device with Name: " + ble_device_name)
    ble_device_addr = await find_ble_device(ble_device_name)

    print("Preparing to send BLE data")
    result_str = await send_ble_data(ble_device_addr, user_command)
    print("The result from the (send_ble_data) function is: \n")
    print(result_str)


if __name__ == "__main__":
    # args = ["wifi_scan"]
    # asyncio.run(main(*args))

    user_cmd = "wifi_scan"
    asyncio.run(main(user_cmd))

# asyncio.run(send_ble_data())
