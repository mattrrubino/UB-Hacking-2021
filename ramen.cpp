#include <Ethernet.h>

// MAC address of ClearCore
byte mac[] = {0x24, 0x15, 0x10, 0xB0, 0x07, 0x37};

EthernetServer server(12345);

void setup() {
  Serial.begin(9600);
  
  Ethernet.begin(mac);
  while (Ethernet.linkStatus() == LinkOFF) {
    delay(1000);
  }

  Serial.println(Ethernet.localIP());

  server.begin();
}

void loop() {
    EthernetClient client = server.available();

    if (client.connected()) {
      while (client.available() > 0) {
        char c = client.read();
        Serial.println(c);
      }
    }
}
