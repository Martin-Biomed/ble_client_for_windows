# About this Project

This project was developed as a tool to be able to communicate with a BLE-enabled device which 
uses a single BLE GATT Characteristic for receiving instructions and another Characteristic for sending replies.

This tool ignores some of the higher-level structural elements that can be used to organise 
GATT Characteristic Groups (like BLE GATT Profiles and Services).

This project was only ever intended to be run in the Windows OS (version 10 or above).

## BLE GATT Usage

This app was developed as a standalone tool for communicating with simple BLE-capable devices (servers).

Bluetooth Low Energy (BLE) communication is significantly different than Classic Bluetooth communications. BLE was 
developed for using significantly less power, simplifying device pairing, and maintaining lower connection 
(but still reliable) connection speeds.

### BLE GATT Background Info

To use BLE for messaging requires a firm understanding of the GATT publish/subscribe method.

It is recommended that potential users become acquainted with basic BLE concepts, fortunately there are good resources online, like: 
https://learn.adafruit.com/introduction-to-bluetooth-low-energy/introduction

### Generic Access Profile (GAP) Device-to-Device Connections

The GAP device-to-device connection is the first step in establishing communications (using the BLE GATT methodology). 


### Generic ATTribute Profile (GATT) Services

Assuming we have a BLE-capable device that functions as a GATT Server, where a client (like this app) can then 
subscribe/publish to available services offered by the server.

GATT services are organised in a hierarchal order:

- **Profile (Highest Level):** Defines a collection of Services. This project ignores this level of the hierarchy and just
directly publishes/subscribes to specific GATT Characteristics.


- **Services:** Contains a group of characteristics, and are more commonly used if different types of functions are available from the 
same BLE server. This project ignores this level of the hierarchy and just directly publishes/subscribes to specific GATT Characteristics. 


- **Characteristics:** The lowest level concept in GATT transactions. Each characteristic is defined by a UUID. The UUID is commonly provided 
as a 16-bit reference or a 128-bit reference.


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