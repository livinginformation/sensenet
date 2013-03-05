/*
  Web Server
 
 A simple web server that shows the value of the analog input pins.
 using an Arduino Wiznet Ethernet shield. 
 
 Circuit:
 * Ethernet shield attached to pins 10, 11, 12, 13
 * Analog inputs attached to pins A0 through A5 (optional)
 
 created 18 Dec 2009
 by David A. Mellis
 modified 9 Apr 2012
 by Tom Igoe
 
 */

#include <SPI.h>
#include <Ethernet.h>

// Enter a MAC address and IP address for your controller below.
// The IP address will be dependent on your local network:
byte mac[] = { 
  0x91, 0xA2, 0xDB, 0x0D, 0x9B, 0x1A };
byte senseServ[] = {
  192, 168, 0, 4}; // SenseNet LAN Address
byte serverIp[] = {
  192,168,0,19};
const int buttonPin = 7;
const int ledPin = 2;
int buttonState;


String readString = String(100);
String name = "";
String setTo = "";

String sensor1Name = "LightSwitchOne";
int sensor1Pin = 7;
int sensor1State = 0;

String sensor2Name = "LED1";
int sensor2Pin = 2;
int sensor2State = 0;

// Initialize the Ethernet server library
// with the IP address and port you want to use 
// (port 80 is default for HTTP):
Server server(80);
Client senseNet(senseServ,8000);

void setup() {
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  pinMode(buttonPin, INPUT); 
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, sensor2Pin);
  buttonState = digitalRead(buttonPin);


  // start the Ethernet connection and the server:
  Ethernet.begin(mac, serverIp);
  server.begin();
}


void loop() {
  // listen for incoming clients
  Client client = server.available();
  if (client) {
    // an http request ends with a blank line
    boolean currentLineIsBlank = true;
    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        readString += c;
        if (c == '\n' && currentLineIsBlank) {
          // Format of GET request: *Name^SetValue@
          name = getName(readString);
          setTo = getSet(readString);
          if(sensorWrite(name,stringToNumber(setTo))){;
            Serial.println("Set sensor.");
          }else{
            Serial.print("Didn't set sensor: ");
            Serial.println(name);
          }
          break;
        }
        if (c == '\n') {
          currentLineIsBlank = true;
        } 
        else if (c != '\r') {
          currentLineIsBlank = false;
        }
      }
    }
    client.println("HTTP/1.1 200 OK");
    client.println("Content-Type: text/html");
    client.println();
    delay(1);
    client.stop();
    readString = "";
    Serial.println("client disonnected");
  }

  checkSensorStates();

}

String getName(String readString){
  return readString.substring(readString.indexOf('*')+1,readString.indexOf(':'));
}

String getSet(String readString){
  return readString.substring(readString.indexOf(':')+1,readString.indexOf('@'));
}

void checkSensorStates(){
  if (sensorRead(sensor1Name) != sensor1State){
    sensor1State = sensorRead(sensor1Name); 
    pushJSON(sensor1Name,sensorRead(sensor1Name));
  }/*
  if (sensorRead(sensor2Name) != sensor2State){
    sensor2State = sensorRead(sensor2Name); 
    pushJSON(sensor2Name,sensorRead(sensor2Name));
  }*/
}


int sensorRead(String name){
  if(returnPin(name) == 0){
    Serial.println("Nonexistent Sensor!");
    return -1;  
  }
  else{
    return digitalRead(returnPin(name));
  }
  /*   if (digitalRead(returnPin(name)) != value){
   value = 
   pushJSON(name, digitalRead(returnPin(name)))
   }*/
}


int returnPin(String sensorName){
  if (sensorName == sensor1Name){
    return sensor1Pin;
  }
  else if(sensorName == sensor2Name){
    return sensor2Pin;
  }
  else{
    Serial.println(sensorName);
    Serial.println(sensor1Name);
    Serial.println(sensor2Name);
    return 0; 
  }
}

int sensorWrite(String name, int value){
  if(returnPin(name) == 0){
    Serial.println("Nonexistent Sensor!"); 
    return 0; 
  }
  else{
    digitalWrite(returnPin(name),value);
    return 1;
  }
}

void pushJSON(String name, int value){
  if(senseNet.connect()){
    Serial.println("Sending JSON Object");
    senseNet.print("GET /s/?name=");
    senseNet.print(name);
    senseNet.print("&val=");
    senseNet.print(value);
    senseNet.println(" HTTP/1.1");
    Serial.println("Object Sent.");
    Serial.println("Disconnecting . . .");
    senseNet.stop();
  }
  else{
    Serial.println("Connection to Server Failed.");
  }
  Serial.print("Sensor name: ");
  Serial.println(name);
  Serial.print("Changed value: ");
  Serial.println(value);
}

int stringToNumber(String thisString) {
  int i, value = 0, length;
  length = thisString.length();
  for(i=0; i<length; i++) {
    value = (10*value) + thisString.charAt(i)-(int) '0';
    ;
  }
  return value;
}
Window size: x 
Viewport size: x