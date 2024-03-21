import asyncio
from bleak import BleakClient
from bleak import BleakScanner

ble_device_name = "ESP32-BLE-Server"
base_uuid = "-0000-1000-8000-00805f9b34fb"

read_uuid = "0000fef4"
write_uuid = "0000dead"

# This script can be used to debug the connection to a BLE device with name "ESP32-BLE-Server"

# The example UUIDs are specific to the GATT characteristics corresponding to the code in:
# ESP-IDF project: example-packet-sniffer
async def receive_ble_data():

    devices = await BleakScanner.discover()
    for d in devices:
        print(d.address)
        print(d.name)

        if d.name == ble_device_name:
            async with BleakClient(d.address, use_cached=False) as client:

                print("Looking for Service with UUID: " + read_uuid + base_uuid)

                new_data = await client.read_gatt_char(read_uuid + base_uuid)
                print("Data from BLE Server: " + new_data.decode())
                #print("Data from BLE Server: {0}".format("".join(map(chr, new_data))))


async def send_ble_data():

    #esp32 = await BleakScanner.find_device_by_name(ble_device_name)

    devices = await BleakScanner.discover()
    for d in devices:
        print(d.address)
        print(d.name)

        if d.name == ble_device_name:

            # Connect to the ESP32 device
            async with BleakClient(d.address) as client:
                # Send parameter to ESP32

                print("Sending Message to: " + ble_device_name)

                complete_write_uuid = write_uuid + base_uuid
                command = "wifi_scan"

                print("Writing to ESP32 Service with UUID: " + complete_write_uuid)
                await client.write_gatt_char(complete_write_uuid, str.encode(command))

                # Receive data from ESP32 via BLE

                while True:
                    data = await client.read_gatt_char(read_uuid + base_uuid)
                    if data:
                        value = str.encode(command)  # Convert bytes to integer
                        print(f"Received data: {value}")



asyncio.run(send_ble_data())