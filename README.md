# About this Project

This project was developed as a tool to be able to communicate with a BLE-enabled device which 
uses BLE GATT Characteristics for receiving instructions and sending replies.

This tool ignores some of the higher-level structural elements that can be used to organise 
GATT Characteristic Groups (like BLE GATT Profiles and Services).

This project was only ever intended to be run in the Windows OS (version 10 or above).

## BLE GATT Usage

The ESP32 uses a BLE GATT Event Bus to receive requests to execute functions. Most of the configuration for the BLE communications is done within the "ble_setup" module.

### BLE GATT Background Info

One of the mechanisms for using BLE for messaging is to use a GATT publish/subscribe method.

It is recommended that potential users become acquainted with basic BLE concepts, fortunately there are good resources online, like: 
https://learn.adafruit.com/introduction-to-bluetooth-low-energy/introduction

### Generic Access Profile (GAP) Device-to-Device Connections

The GAP device-to-device connection is the first step in establishing communications (using this BLE methodology). 

The ESP32 advertises its device BLE characteristics (like its Device Name and MAC Address). This allows BLE-enabled devices to detect and establish a connection to the ESP32.

### Generic ATTribute Profile (GATT) Services

The ESP32 functions as a GATT Server, where a client can then subscribe/publish to available Services offered by the ESP32.

GATT Services are organised in a hierarchal order:

- **Profile (Highest Level):** Defines a collection of Services. In this project, there is only a single (implicitly-defined) Profile.


- **Services:** Contains a group of characteristics, and are more commonly used if different types of functions are available from the same BLE server. This project only uses a single service.


- **Characteristics:** The lowest level concept in GATT transactions. Each characteristic is defined by a UUID. The UUID is commonly provided as a 16-bit reference of 128-bit reference.

    -  This project uses two separate BLE GATT characteristics:

        - **READ Characteristic (0xFEF4):** This characteristic is where the ESP32 reads any input from BLE clients. A BLE client can publish 
       commands to this GATT characteristic to control the execution of the ESP32 functions (Refer to the project "documentation" directory for more info).

        - **WRITE Characteristic (0xDEAD):** This characteristic is where the ESP32 publishes any data that is meant to be accessible to an external BLE client.

**Note:** The (128-bit) representation of the BLE Characteristic UUID is the (16-bit) Byte UUID superimposed over the standard Bluetooth Base UUID 
(Refer to the project "documentation" directory for more info on how we use UUIDs).

## Modes of Operation

This Application can run in two separate modes of operation:

- **Manual Mode:** The user can fill in the required fields in the GUI to prepare a message to send via BLE GATT. This specific app 
was designed to be used with a BLE Server device that receives commands on one BLE GATT Characteristic and sends responses on
another BLE Characteristic (Each has a separate UUID).


- **API Mode:** The user can provide the same required fields that are available in the manual mode by sending specially-formatted 
HTTP requests (Refer to "documentation" folder for more details).

**Note:** Both modes only support using the 128-bit versions of the GATT Characteristic UUIDs. This is because
these forms can be sent as plain strings, as opposed to raw bytes that then have to be decoded.