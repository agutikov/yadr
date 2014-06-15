#include <Servo.h>


// every 2 seconds will blink by 13-pin led, then check data from the serial
// and adjust all 3 servos to 10*input digit degrees up from the middle point

int led = 13;

Servo servoA;
Servo servoB;
Servo servoC;

void setup() { 
  servoA.attach(11);
  servoB.attach(10);
  servoC.attach(9);
  
    // initialize the digital pin as an output.
  pinMode(led, OUTPUT);

  Serial.begin(19200);
  Serial.println("Ready");
  
  setServo(90,90,90);
} 

void loop() {            // Loop through motion tests

blinkLed();

int v = 90;

if ( Serial.available()) {
    char ch = Serial.read();

    switch(ch) {
      case '0'...'9':
        v = 90 + 10 * (ch - '0');
        break;
    }
}

setServo(v,v,v);

delay(2000);

//setServo(80,80,80);

//delay(2000);

}

void blinkLed(){
  digitalWrite(led, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(50);                 // wait for a 50 mseconds
  digitalWrite(led, LOW);    // turn the LED off by making the voltage LOW
  delay(50);
}

void setServo(int a, int b, int c){
//set servo A
servoA.write(a);
//set servo B
servoB.write(b);
//set servo C
servoC.write(c);
}
