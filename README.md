# Arduino UNO Q - SPI3 App Lab Brick (Proof Of Concept)

## Introduction

This project is a Proof of Concept (POC) demonstrating the use of the SPI3 link between the STM32U585 MCU and the Qualcomm QRB2210 MPU on the Arduino UNO Q through a custom Arduino App Lab brick.

The goal is to demonstrate that it is possible to:

- Access `/dev/spidev0.0` from an App Lab brick.
- Exchange data between the MCU and the MPU using SPI3.
- Transfer arrays of floating-point values.
- Expose the received data to an App Lab application through a simple Python API.

This project is experimental and intended to explore the internal architecture of the UNO Q.

---

## Architecture

```text
STM32U585 (MCU)
       |
       | SPI3
       |
QRB2210 Linux (MPU)
       |
   /dev/spidev0.0
       |
   spi_service.py
       |
      HTTP
       |
    SPI3 Brick
       |
     App Lab
```

---

## Operation

### MCU Side

The Arduino sketch:

- Generates an array of floating-point values.
- Builds an SPI frame.
- Adds a synchronization header.
- Sends the data to the MPU.

Frame structure:

```text
Byte 0  : 0xA5 (signature)
Byte 1  : number of floats
Byte 2+ : float data
```

---

### MPU Side


The App Lab brick:

- Accesses `/dev/spidev0.0` through `python3-spidev`.
- Receives SPI frames.
- Verifies the `0xA5` header.
- Converts received bytes back into floating-point values.
- Exposes the data through a simple Python API.

Example:

```python
from spi3 import SPI3

spi = SPI3()

if spi.begin():
    value = spi.read_float()
    print(value)

    values = spi.read_floats(16)
    print(values)
```
---

## Demonstration Data Source

For demonstration purposes, the MCU generates an array of random floating-point values.  
The generated values are packed into an SPI frame and transmitted to the MPU through SPI3.

In a real-world application, these values could easily be replaced by:

* Analog readings (A0, A1, etc.)
* Sensor measurements
* GPS data
* IMU data
* LiDAR samples
* Any other application-specific payload

The purpose of this project is not the data source itself, but the demonstration of SPI3 communication between the MCU and MPU on the Arduino UNO Q.

---

## Validated Features

- SPI3 access from an App Lab brick.
- Access to `/dev/spidev0.0`.
- MCU → MPU communication.
- Transfer of float arrays.
- Decoding on the Linux side.
- Data exposure inside App Lab.
- Use of a dedicated Docker container.

---

## Known Limitations

This project is an experimental prototype.

Current limitations:

- Synchronization between MCU and MPU can be improved.
- The brick keeps the last valid frame.
- Minimal protocol implementation.
- No CRC or integrity checking.

These areas can be improved in future versions.

---

## Educational Purpose

This repository is not intended to become an official library.

Its primary purpose is to demonstrate:

- How to create a custom App Lab brick.
- How to use a dedicated Docker container.
- How to access Linux devices from that container.
- How to use SPI3 between the MCU and MPU on the UNO Q.

---

## Why does this custom Brick use a Docker service and an HTTP API?

A common question is:

> Why not access `/dev/spidev0.0` directly from `main.py`?

The answer is that Arduino App Lab applications run in a managed environment that does not necessarily have direct access to all Linux devices, system packages, or kernel interfaces.

In this proof of concept:

```text
MCU
  ↓
SPI3
  ↓
/dev/spidev0.0
  ↓
Docker service
  ↓
HTTP API
  ↓
App Lab Python code
```

The custom Brick creates a dedicated Linux service running inside a container.

This service:

* has access to `/dev/spidev0.0`
* installs and uses `python3-spidev`
* communicates directly with the SPI3 interface
* exposes a simple HTTP API

The App Lab Python code does not need to know how SPI transactions are performed. It simply calls:

```python
spi = SPI3()

value = spi.read_float()
values = spi.read_floats()
```

The Brick acts as an abstraction layer between the App Lab application and the Linux SPI device.

This approach provides several advantages:

* keeps the App code simple
* isolates Linux-specific dependencies
* makes the functionality reusable across multiple projects
* follows the philosophy of App Lab Bricks as reusable building blocks

The same architecture could be used for many other Linux resources, such as:

* ALSA audio devices
* GPS receivers
* serial ports
* I2C devices
* network services
* custom hardware interfaces

The SPI3 proof of concept demonstrates one practical example of this pattern.

---

## Why use an HTTP server?

Some readers may wonder why this project uses an HTTP server.

The answer is simple:

The HTTP server is not used to create a website.

It is only used as a communication channel between two Python programs running on the Linux MPU.

Think of it this way:

```text
App Lab Python
        |
        | "Please give me the SPI3 values"
        v
SPI3 Service
        |
        | Reads /dev/spidev0.0
        v
SPI3 Hardware
```

The HTTP request is simply a message sent from one program to another.

For example:

```python
spi.read_floats()
```

internally becomes:

```text
GET /values
```

The SPI3 service receives this request, reads the SPI3 interface, and sends the result back.

The App Lab application then receives the values and continues normally.

Why use HTTP?

Because it is:

* simple
* reliable
* easy to debug
* supported by standard Python libraries

The HTTP server is only running locally inside the UNO Q Linux environment.

No Internet connection is required.

You can think of it as a "messenger" between the App Lab application and the Linux service that has access to the SPI3 device.

---

## Acknowledgements

This project was created as part of a personal exploration of the Arduino UNO Q platform.

A significant part of the investigation, debugging, experimentation, and design process was carried out with the assistance of ChatGPT.


## Status

Experimental Project (POC)

Successfully tested on Arduino UNO Q.

---

## Credits

This proof-of-concept is based on the SPI3 peripheral support work by @facchinm:

- ArduinoCore-zephyr PR #383
- Original SPI3 discussion on the Arduino Forum

The App Lab brick and MPU-side proof-of-concept were developed from these foundations.

---
