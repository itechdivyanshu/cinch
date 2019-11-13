#include <ESP8266WiFi.h>

const char* SSID = "Itech Divyanshu(Jiofi_3)";
int pin = 2;
int pin1 = 13;
char input;
int off = 1;
long t = 0;

int32_t getRSSI(const char* target_ssid) {
  byte available_networks = WiFi.scanNetworks();

  for (int network = 0; network < available_networks; network++) {
    if (WiFi.SSID(network).compareTo(target_ssid) == 0) {     //stringOne.compareTo(stringTwo) < 0
      return WiFi.RSSI(network);
    }
  }
  return 0;
}

void setup() {
  // initialize GPIO 2 as an output.
  Serial.begin(9600);
  pinMode(pin, OUTPUT);
  pinMode(pin1, OUTPUT);
}

// the loop function runs over and over again forever
void loop() {
  int32_t rssi = getRSSI(SSID);
  if (rssi==0){
  t=t+1;
  }
 else{t=1;}
 if (off == 1){
 if(t>10){
  
    digitalWrite(pin, LOW);
}
else{
  if (rssi < (-70) && rssi != 0){
    digitalWrite(pin,LOW);
  }
  else{
    digitalWrite(pin,HIGH);
  }}}
  if (Serial.available()> 0){
    input = Serial.read();
    if(input == '1'){
      digitalWrite(pin,HIGH);
      Serial.println("Light1 is on");
      off = 0;
    }
    else if(input == '2'){
      digitalWrite(pin,LOW);
      Serial.println("Light1 is off");
      off =1;
    }
    if(input == '3'){
      digitalWrite(pin1,HIGH);
      Serial.println("Light2 is on");
    }
    else if(input == '4'){
      digitalWrite(pin1,LOW);
      Serial.println("Light2 is off");
    }
  }             
}
