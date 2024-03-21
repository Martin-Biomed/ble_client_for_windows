import asyncio
import json

from bleak import BleakClient
from bleak import BleakScanner

ble_device_name = "ESP32-BLE-Server"
base_uuid = "-0000-1000-8000-00805f9b34fb"

read_uuid = "0000fef4"
write_uuid = "0000dead"

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
async def send_ble_data(ble_device_address: str, command: str) -> list:

    list_of_access_points = []

    # Connect to the ESP32 device
    async with BleakClient(ble_device_address, use_cached=False) as client:

        # Send parameter to ESP32
        print("Sending Message to: " + ble_device_name)

        complete_write_uuid = write_uuid + base_uuid

        print("Writing to Service with UUID: " + complete_write_uuid)
        await client.write_gatt_char(complete_write_uuid, command.encode('utf-8'), response=False)

        # Receive data from ESP32 via BLE (response from BLE server)
        try:
            print("Awaiting Response from Service with UUID: " + read_uuid + base_uuid)
            new_data = await client.read_gatt_char(read_uuid + base_uuid)

            # Executes when the user receives a msg from the selected GATT characteristic
            if new_data:
                print("Data from BLE Server: " + str(new_data))
                print("Length of ByteArray is: " + str(len(new_data)))
                encoding = json.detect_encoding(new_data)
                print("Data Has been Encoded using: " + encoding)

                if encoding == "utf-8":
                    print("Data from BLE Server: {0}".format("".join(map(chr, new_data))))
                    list_of_access_points.append(new_data.decode())

        except asyncio.CancelledError:
            print("The operation has been cancelled prematurely.")

        except asyncio.TimeoutError:
            print("The operation has timed out")

        return list_of_access_points
                            

async def main(user_command: str):
    print("Looking for Device with Name: " + ble_device_name)
    ble_device_addr = await find_ble_device(ble_device_name)

    print("Preparing to send BLE data")
    result_list = await send_ble_data(ble_device_addr, user_command)
    print("The result from the (send_ble_data) function is: \n")
    for result in result_list:
        print(result)


if __name__ == "__main__":
    # args = ["wifi_scan"]
    # asyncio.run(main(*args))

    user_cmd = "wifi_scan"
    asyncio.run(main(user_cmd))


#asyncio.run(send_ble_data())