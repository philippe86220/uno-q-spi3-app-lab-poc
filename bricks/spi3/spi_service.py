import json
import struct
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

import spidev

HOST = "0.0.0.0"
PORT = 9000

# 2 octets d'entête + 16 floats
NUM_BYTES = 66

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000
spi.mode = 0


def read_floats():
    # Demande au MCU de préparer une nouvelle trame
    spi.xfer2([0x0B] + [0x00] * 15)

    # Plusieurs tentatives pour récupérer une trame valide
    for _ in range(10):

        time.sleep(0.05)

        rx = spi.xfer2([0x00] * NUM_BYTES)

        # Vérification de l'entête
        if rx[0] != 0xA5:
            continue

        count = rx[1]

        if count > 16:
            return {
                "ok": False,
                "error": "Invalid count"
            }

        values = []

        offset = 2

        for i in range(count):

            start = offset + (i * 4)

            value = struct.unpack(
                "<f",
                bytes(rx[start:start + 4])
            )[0]

            values.append(value)

        return {
            "ok": True,
            "values": values
        }

    return {
        "ok": False,
        "error": "Invalid frame"
    }


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/values":

            payload = read_floats()

        else:

            payload = {
                "ok": False,
                "error": "Unknown endpoint"
            }

        body = json.dumps(payload).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()

        self.wfile.write(body)

    def log_message(self, format, *args):
        pass


print("SPI3 HTTP service started on port 9000", flush=True)

server = HTTPServer((HOST, PORT), Handler)

try:
    server.serve_forever()

finally:
    spi.close()
