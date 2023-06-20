#include <WiFi.h>

const char* ssid = "BuenosDias";
const char* password = "NaoSeiAPass";
const char* receiverIP = "192.168.72.176"; // IP address of the receiver
const int receiverPort = 8081; // Port number of the receiver

WiFiClient client;

int value = 0;

void setup() {
  Serial.begin(115200);
  
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("Connected to WiFi");
  Serial.print("Local ESP32 IP: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  if (!client.connected()) {
     Serial.printf("Connecting to %s", receiverIP);
    if (client.connect(receiverIP, receiverPort)) {
      Serial.println("\nConnected to receiver");

      // Send data to the receiver
      // String data = "Hello, receiver!";
      // client.println(data);
      client.println(value);
      value++;

      // Read response from the receiver
      while (client.connected() && !client.available()) {
        delay(1);
      }

      if (client.available()) {
        String response = client.readStringUntil('\n');
        Serial.println("Receiver response: " + response);
      }

      client.stop();
    }
    else {
      Serial.println("Connection to receiver failed");
    }
  }

  delay(1000);
}
