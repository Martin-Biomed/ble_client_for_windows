# Project Limitations

A disclaimer for this project is that it was not approached with a proper engineering mindset/rigour.
This may become apparent on some of the coding quality throughout the project.

## Testing Requirements

There are a series of automated unit tests that have been developed as part of this project.

To run these tests in the way they were intended, use the following command on the terminal:
   1. Navigate to the root directory of this project (ble_client)
   2. On the terminal type: `nosetests --with-spec --spec-color`

**Note:** This assumes that all project dependencies stated in (project_structure_README.md) have been installed.

### test_ble_send

Due to the lack of Python BLE server libraries and documentation available for Windows at this time, it became
 infeasible to simulate an actual BLE server using Python.

Because of the way the code was structured, we couldn't Mock a response from a BLE server, as only a single
function is called to both send and receive data from the BLE Server (the "send_ble_data" function).

We could not apply Mocking to the server response unless we refactored the code to be able to send and receive 
the data separately (which I just didn't have the time for).

In order for these tests to work, you need an ESP32 that has been loaded with the (wifi-data-acquisition-server)
project. The link to this project can be found here: https://github.com/Martin-Biomed/wifi-data-acquisition-server

## General Applicability

This project has only been tested with communicating with an ESP32 running (wifi-data-acquisition-server).

### BLE Characteristics

This specific project only uses two GATT Characteristics, but realistically, other devices may have more
characteristics or be further divided into groups and Services, which I don't think should affect the reliability
of this project, but since its untested, I am not sure.

