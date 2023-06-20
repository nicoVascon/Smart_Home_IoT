#include <ESP32_Servo.h>

#include "Arduino.h"

#define VREF_PLUS 3.3
#define VREF_MINUS 0.0
#define ADC_RESOLUTION 4096.0

#define PIN_TempSensor 34

int analog_value = 0;
float analog_voltage = 0;

//------------------------------- TCP -------------------------------
#include <WiFi.h>
const char* ssid = "BuenosDias";
const char* password = "NaoSeiAPass";
const char* receiverIP = "192.168.72.176"; // IP address of the receiver
const int receiverPort = 8081; // Port number of the receiver
WiFiClient client;

//-------------------------------MOTOR-------------------------------
Servo myservo;  // create servo object to control a servo
// 16 servo objects can be created on the ESP32
int pos = 0;  // variable to store the servo position
int position_int = 0;
int pos_atual = 0;
// Recommended PWM GPIO pins on the ESP32 include 2,4,12-19,21-23,25-27,32-33
int servoPin = 14;
//-------------------------------------------------------------------
//--------------------------- Temp Sensor ----------------------------
float tempValue;

String motor_type;
String motor_val = "0";
String position = "0";

// --------------------------- Functions Delcaration ---------------------------
void TCP(void);


void setup() {

  Serial.begin(9600);
  while (!Serial) {}

  analogReadResolution(ADC_RESOLUTION);

  // myservo.setPeriodHertz(50);           // standard 50 hz servo
  myservo.attach(servoPin, 500, 2400);  // attaches the servo on pin 18 to the servo object
  motor_val = "0";

  //------------------------------- TCP -------------------------------
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
  TCP();
  //--------------------MOTOR----------------------------
  //motor_type="DIGITAL_INPUT";
  motor_type = "DI";
  // if (Serial.available()) {                   // if there is data comming
  //   position = Serial.readStringUntil('\n');  // read serial port value
  // }
  Serial.print("(MOTOR) Li no serial (string): ");
  Serial.print(position);
  Serial.println();
  position_int = position.toInt();
  // if (motor_val == "1") {
  //   position = "180";
  // } else {
  //   position = "0";
  // }
  position_int = position.toInt();
  if (pos_atual != position_int) {
    if (pos_atual < position_int) {
      for (pos = pos_atual; pos <= position_int; pos += 1) {  // goes from 0 degrees to 180 degrees
        // in steps of 1 degree
        //Serial.print("moving servo to ");
        //Serial.print(pos);
        myservo.write(pos);  // tell servo to go to position in variable 'pos'
        delay(15);           // waits 15ms for the servo to reach the position
      }
    } else {
      for (pos = pos_atual; pos >= position_int; pos -= 1) {  // goes from 180 degrees to 0 degrees
        myservo.write(pos);                                   // tell servo to go to position in variable 'pos'
        delay(15);                                            // waits 15ms for the servo to reach the position
      }
    }
    pos_atual = position_int;
  }
  //------------------------------------------------------

  analog_value = analogRead(PIN_TempSensor);
  analog_voltage = analog_value * (VREF_PLUS - VREF_MINUS)
                     / (ADC_RESOLUTION)
                   + VREF_MINUS;

  tempValue = analog_voltage * 100;
  Serial.printf("(Temperature) Temperatura Atual: %f", tempValue);
  
  
  delay(1000);
}

void TCP(void){
  if (!client.connected()) {
     Serial.printf("\nConnecting to %s", receiverIP);
    if (client.connect(receiverIP, receiverPort)) {
      Serial.println("\nConnected to receiver");

      // Send data to the receiver
      // String data = "Hello, receiver!";
      // client.println(data);
      client.println(tempValue);

      // Read response from the receiver
      while (client.connected() && !client.available()) {
        delay(1);
      }

      if (client.available()) {
        position = client.readStringUntil('\n');
        Serial.println("\nReceiver response: " + position);
      }

      client.stop();
    }
    else {
      Serial.println("\nConnection to receiver failed");
    }
  }

  // delay(1000);
}
