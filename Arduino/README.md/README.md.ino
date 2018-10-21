#include <Servo.h>
Servo rotationServo; 
Servo shootServo;
String inByte;
int rotation;
int shoot;

void setup() {
  rotationServo.attach(9);
  shootServo.attach(10);
  Serial.begin(9600);
  rotationServo.write(0);
  shootServo.write(180);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop()
{    
  if(Serial.available())  
    { 
    inByte = Serial.readStringUntil('\n'); 
    rotation = inByte.toInt();    
    if (rotation == 242) {
      shootServo.write(80);
      delay(100);
      shootServo.write(180);           
     } else {    
      Serial.write(rotation);     
      rotationServo.write(rotation);  
    }
  }   
}
