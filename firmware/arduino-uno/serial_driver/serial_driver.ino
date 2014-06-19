#include <Servo.h>


// every iteration will blink by 13-pin led, then check data from the serial
// and adjust all 3 servos to input digit degrees/pulse (using 19200b serial)

int led = 13;

Servo servoA;
Servo servoB;
Servo servoC;

int minAngle = 0;
int maxAngle = 180;

int minPulse = 1000;
int maxPulse = 2000;

int midAngle = 90;
int midPulse = 1500;

int angleA = 0;
int angleB = 0;
int angleC = 0;

int pulseF = 0;
int pulseG = 0;
int pulseH = 0;

int stateSum = 0;

void setup() {
  servoA.attach(11);
  servoB.attach(10);
  servoC.attach(9);
  
    // initialize the digital pin as an output.
  pinMode(led, OUTPUT);

  Serial.begin(19200);
  Serial.println("Ready");
  
  blinkLed(2);
  angleA = midAngle;
  angleB = midAngle;
  angleC = midAngle;
  
  pulseF = midPulse;
  pulseG = midPulse;
  pulseH = midPulse;
  
  setAngle(angleA, angleB, angleC);
}

void loop() { // Loop through motion tests

  // blinkLed(1);

  if ( Serial.available()) {
    char ch = Serial.read();
	
	//echo
	Serial.write(ch);
	
    switch(ch) {
      case '0'...'9':
	      stateSum = stateSum * 10;
              stateSum = stateSum + (ch - '0');
            break;
		
	  case 'a':
	    angleA = stateSum;
		stateSum = 0;
		break;
		
	  case 'b':
	    angleB = stateSum;
		stateSum = 0;
		break;
		
	  case 'c':
	    angleC = stateSum;
		stateSum = 0;
						//c is also a terminator
		setAngle(angleA, angleB, angleC);
		break;
      	  
	  case 'f':
	    pulseF = stateSum;
		stateSum = 0;
		break;
		
	  case 'g':
	    pulseG = stateSum;
		stateSum = 0;
		break;
		
	  case 'h':
	    pulseH = stateSum;
		stateSum = 0;
						//h is also a terminator
		setSignal(pulseF, pulseG, pulseH);
		break;
      	  
	  case 'z':
		setZeroPoint();
		break;
		
	  case 'p':
	    printPosition();
		break;
    }
  }
}

void blinkLed(int amount){
  for (int t = 0; t < amount; ++t)
  {
    digitalWrite(led, HIGH); // turn the LED on (HIGH is the voltage level)
    delay(50); // wait for a 50 mseconds
    digitalWrite(led, LOW); // turn the LED off by making the voltage LOW
    delay(50);
  }
}

void setAngle(int a, int b, int c){
  Serial.println(a);
  Serial.println(b);
  Serial.println(c);
  if ( (a >= minAngle) && (a <= maxAngle) ) servoA.write(a);
  if ( (b >= minAngle) && (b <= maxAngle) ) servoB.write(b);
  if ( (c >= minAngle) && (c <= maxAngle) ) servoC.write(c);
}


void setSignal(int ua, int ub, int uc){
  Serial.println(ua);
  Serial.println(ub);
  Serial.println(uc);
  if ( (ua >= minPulse) && (ua <= maxPulse) )servoA.writeMicroseconds(ua);
  if ( (ub >= minPulse) && (ub <= maxPulse) )servoB.writeMicroseconds(ub);
  if ( (uc >= minPulse) && (uc <= maxPulse) )servoC.writeMicroseconds(uc);
}

void setZeroPoint(){
  angleA = 90;
  angleB = 90;
  angleC = 90;
		
  pulseF = 1500;
  pulseG = 1500;
  pulseH = 1500;
		
  stateSum = 0;
		
  setAngle(angleA, angleB, angleC);
	
  blinkLed(3);
}

void printPosition(){
  if ( Serial.available()) {
    Serial.println("");
	Serial.print("a = ");
	Serial.print(servoA.read());
	Serial.print("; b = ");
	Serial.print(servoB.read());
	Serial.print("; c = ");
	Serial.print(servoC.read());
	
	Serial.print("f = ");
	Serial.print(servoA.readMicroseconds());
	Serial.print("; g = ");
	Serial.print(servoB.readMicroseconds());
	Serial.print("; h = ");
	Serial.print(servoC.readMicroseconds());
	Serial.println(";");
  }
}
