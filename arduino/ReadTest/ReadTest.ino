#include "SD.h"

#define LOG_INTERVAL  1000 // mills between entries
#define redLEDpin 3
#define greenLEDpin 4
#define leftXPin 0
#define leftYPin 1
#define leftZPin 2

// for the data logging shield, we use digital pin 10 for the SD cs line
const int chipSelect = 10;
const int powPin = 8; // no idea

// the logging file
File logfile;

void error(char *str) {

  digitalWrite(redLEDpin, HIGH);
  Serial.print("--> error: ");
  Serial.println(str);
  while(1);
  
}

void setup(void) {
  
  Serial.begin(9600);
  
  // initialize the SD card
  Serial.print("Initializing SD card...");
  pinMode(10, OUTPUT); // default chip select pin is set to output, needed
  pinMode(powPin, OUTPUT);  
  digitalWrite(powPin, HIGH);  
  
  // see if the card is present and can be initialized:
  if (!SD.begin(chipSelect)) {
    error("card failed, or not present");
  }
  Serial.println("--> initialized");
  
  // find the next unused filename
  char filename[] = "log_00.cv";  
  for (uint8_t i = 0; i < 100; i++) {
    filename[4] = i/10 + '0';
    filename[5] = i%10 + '0';
    if (!SD.exists(filename)) {
      break;
    }
  }  
  File logfile = SD.open(filename, FILE_WRITE);   
  if (!logfile) {
    error("couldnt create file");
  }
  Serial.print("Logging to: ");
  Serial.println(filename);
  
  Serial.println("t,left_x,left_y,left_z");
  logfile.println("t,left_x,left_y,left_z");
  logfile.flush();

  pinMode(redLEDpin, OUTPUT);
  pinMode(greenLEDpin, OUTPUT);
 
   // If you want to set the aref to something other than 5v
  //analogReference(EXTERNAL);
}


void loop(void) {
  
  // delay for the amount of time we want between readings
  delay((LOG_INTERVAL -1) - (millis() % LOG_INTERVAL));
  
  // digitalWrite(greenLEDpin, HIGH);

  // String output = "";

  // log milliseconds since starting
  uint32_t t = millis();
  // output += String(t);
  // output += ",";

  // int leftX = analogRead(leftXPin);
  // delay(5);
  // int leftY = analogRead(leftYPin);
  // delay(5);
  // int leftZ = analogRead(leftZPin);
  // delay(5);
  // output += String(leftX);
  // output += ",";
  // output += String(leftY);
  // output += ",";
  // output += String(leftZ);

  logfile.println(t);
  logfile.flush();
  Serial.println(t);
  


  // digitalWrite(greenLEDpin, LOW);

} 
