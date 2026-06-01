from spi3 import SPI3
import time

spi = SPI3()

print("=== Test brick SPI3 UNO Q ===")
print(spi.status())

if not spi.begin():
    print("SPI3 service non disponible")
    while True:
        time.sleep(1)

print("SPI3 service pret")
print("Lecture des donnees envoyees par le MCU via SPI3")
print()

while True:
    values = spi.read_floats(16)

    print("Nouvelle trame recue du MCU :")
    print("--------------------------------")

    for index, value in enumerate(values):
        print(f"Valeur {index:02d} : {value:.1f}")

    print("--------------------------------")
    print()

    time.sleep(1)
