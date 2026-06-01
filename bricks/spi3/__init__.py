import json
import time
from urllib.request import urlopen
from urllib.error import URLError


class SPI3:

    def __init__(self):
        self.base_url = "http://spi3:9000"
        self.last_values = []

    def begin(self, timeout=20):

        start = time.time()

        while time.time() - start < timeout:

            try:

                with urlopen(
                    self.base_url + "/values",
                    timeout=2
                ) as response:

                    response.read()

                return True

            except URLError:

                time.sleep(0.5)

        return False

    def read_floats(self, count=16):

        with urlopen(
            self.base_url + "/values",
            timeout=2
        ) as response:

            data = json.loads(
                response.read().decode("utf-8")
            )

        # Conserver la dernière trame valide
        if data.get("ok", False):

            self.last_values = data.get(
                "values",
                []
            )

        return self.last_values[:count]

    def read_float(self):

        values = self.read_floats(1)

        if values:
            return values[0]

        return None

    def status(self):

        return {
            "ok": True,
            "message": "SPI3 brick loaded"
        }
