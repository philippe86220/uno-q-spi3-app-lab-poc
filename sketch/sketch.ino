#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include "SPIPeripheral.h"


#define num_vals 180

#define HEADER_BYTE 0xA5
#define NUM_FLOATS 16

SPIPeripheralClass<1024> spi;

void floats_to_bytes(const float* src, size_t float_count, uint8_t* dst) {
    if (!src || !dst || float_count == 0) return;
    memcpy(dst, src, float_count * sizeof(float));
}

float sensorValues[num_vals];
uint8_t buffer[12];
long randNumber ;

void get_sensor_data() {
    for(int i = 0; i < num_vals; i++) {
      randNumber = random(300);
      sensorValues[i] = float(randNumber) / 10.0;
    }
}
void setup() {
  Monitor.begin();
  delay(5000);
  Monitor.println("Begin SPI3 Test....");

  randomSeed(analogRead(A0));

  spi.begin();
}

void loop() {
  //uint8_t bytes[num_vals * sizeof(float)];
  uint8_t packet[2 + NUM_FLOATS * sizeof(float)];
  spi.depopulate(*buffer, 12);
    
  for(uint8_t i = 0; i < 12; i++) {
    Monitor.print(buffer[i], HEX); 
    Monitor.print(", ");
  } 
  Monitor.println();

  //if(buffer[0] == 0x0B) {
    // Convert float array → bytes
    if (buffer[0] == 0x0B) {
    get_sensor_data();

    packet[0] = HEADER_BYTE;
    packet[1] = NUM_FLOATS;

    memcpy(&packet[2], sensorValues,NUM_FLOATS * sizeof(float));

    spi.populate(packet, sizeof(packet));

    spi.ready();
 }

}



