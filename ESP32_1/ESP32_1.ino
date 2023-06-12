#include "Arduino.h"

#define PIN_GAS 34

#define VREF_PLUS 3.3
#define VREF_MINUS 0.0
#define ADC_RESOLUTION 4096.0

int analog_value = 0;
float analog_voltage = 0;

//-------------------------------BUZZER-------------------------------
int buzzer = 33;  //set digital IO pin of the buzzer
String buzz_type;
String buzz_val = "0";
String buzz_activ_temp = "0";
//-------------------------------GAS-------------------------------
String gas_type;
String gas_val = "0";
//-------------------------------FLAME SENSOR-------------------------
const int flamePin = 4;
bool StateFlame = LOW; // variable for reading status
String flame_type;
String flame_val="0";
//--------------------------------------------------------------------


void setup() {

  Serial.begin(9600);
  while(!Serial){}

  pinMode(buzzer, OUTPUT);  // set digital IO pin pattern, OUTPUT to be output
  buzz_val = "0";

  gas_val = "0";

  pinMode(flamePin, INPUT);
  flame_val="0";
}

void loop() {
  //-----------------------GAS SENSOR---------------------
  //gas_type="ANALOG_INPUT";
  gas_type = "AI";
  analog_value = analogRead(PIN_GAS);
  analog_voltage = analog_value * (VREF_PLUS - VREF_MINUS)
                     / (ADC_RESOLUTION)
                   + VREF_MINUS;
  Serial.print("(GAS SENSOR)Gas voltage (0-3.3V): ");
  Serial.println(analog_voltage);
  gas_val = String(round(analog_voltage * 30));



  for (int i = 0; i < 80; i++) {     // output a frequency sound
    digitalWrite(buzzer, HIGH);  // sound
    delay(1);                    //delay1ms
    digitalWrite(buzzer, LOW);   //not sound
    delay(1);                    //ms delay
  }
  for (int i = 0; i < 100; i++)  // output a frequency sound
  {
    digitalWrite(buzzer, HIGH);  // sound
    digitalWrite(buzzer, LOW);   //not sound
    delay(2);                    //2ms delay
  }

  //----------------FLAME SENSOR-------------------------------
  flame_type="DIGITAL_INPUT";
  flame_type = "DI";
  StateFlame = digitalRead(flamePin);
  Serial.print("(FLAME SENSOR)");
  if (StateFlame == LOW) {
    flame_val = "1";
    Serial.println("Chama detetada!!!!!");
  } else {
    // turn LED off:
    Serial.println("Chama nao detetada");
    flame_val = "0";
  }
  //--------------------------------------------------------------
}
