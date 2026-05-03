#include <AFMotor_R4.h>
#include <SoftwareSerial.h>


AF_DCMotor motor1(1); 
AF_DCMotor motor2(2); 
AF_DCMotor motor3(3); 
AF_DCMotor motor4(4);

// RX on 2, RX on A1
SoftwareSerial BT(2, A1); 
//RX = Purple Wire, TX = Orange Wire
double distance = 100;
long duration = 0;


void setup() {
  Serial.begin(9600); 
  BT.begin(9600);
  
  pinMode(A3, OUTPUT); //TrigPin
  pinMode(A5, INPUT); //echoPin
  Serial.println("System Online. Waiting for Bluetooth...");

  motor1.setSpeed(200);
  motor2.setSpeed(200);
  motor3.setSpeed(200);
  motor4.setSpeed(200);
}

void loop() {

  if (BT.available() > 0) {
    String msg = BT.readStringUntil('\n');
    msg.trim();
    Serial.println("Bluetooth Received: ");
    Serial.println(msg);
    
    if (msg == "LEFT") {
      motor1.setSpeed(100);
      motor2.setSpeed(100);
      motor3.setSpeed(100);
      motor4.setSpeed(100);
      motor2.run(FORWARD);
      motor3.run(FORWARD);
      motor1.run(RELEASE);
      motor4.run(RELEASE);
    } 
    else if(msg == "RIGHT"){
      motor1.setSpeed(100);
      motor2.setSpeed(100);
      motor3.setSpeed(100);
      motor4.setSpeed(100);
      motor1.run(FORWARD);
      motor4.run(FORWARD);
      motor2.run(RELEASE);
      motor3.run(RELEASE);
    }
    else if (msg == "FWD"){
      digitalWrite(A3, LOW);
      delayMicroseconds(2);
      digitalWrite(A3, HIGH);
      delayMicroseconds(10);
      digitalWrite(A3, LOW);

      duration = pulseIn(A5, HIGH, 30000);
      distance = duration * 0.0343 / 2;
      
      Serial.print("Distance: ");
      Serial.println(distance);
      motor1.setSpeed(200);
      motor2.setSpeed(200);
      motor3.setSpeed(200);
      motor4.setSpeed(200);
      if (distance > 20) {
        motor1.run(FORWARD);
        motor2.run(FORWARD);
        motor3.run(FORWARD);
        motor4.run(FORWARD);
      } else {
        motor1.run(RELEASE);
        motor2.run(RELEASE);
        motor3.run(RELEASE);
        motor4.run(RELEASE);
      }
    }
    else if (msg == "REV"){
      motor1.setSpeed(200);
      motor2.setSpeed(200);
      motor3.setSpeed(200);
      motor4.setSpeed(200);
      motor1.run(BACKWARD);
      motor2.run(BACKWARD);
      motor3.run(BACKWARD);
      motor4.run(BACKWARD);
    }
    else if (msg == "BACKLEFT"){
      motor1.setSpeed(100);
      motor2.setSpeed(100);
      motor3.setSpeed(100);
      motor4.setSpeed(100);
      motor1.run(RELEASE);
      motor2.run(BACKWARD);
      motor3.run(BACKWARD);
      motor4.run(RELEASE);
    }
    else if (msg == "BACKRIGHT"){
      motor1.setSpeed(100);
      motor2.setSpeed(100);
      motor3.setSpeed(100);
      motor4.setSpeed(100);
      motor1.run(BACKWARD);
      motor2.run(RELEASE);
      motor3.run(RELEASE);
      motor4.run(BACKWARD);
    }
    else if (msg == "MYSTERY1"){
      motor1.setSpeed(200);
      motor2.setSpeed(200);
      motor3.setSpeed(200);
      motor4.setSpeed(200);
      motor1.run(BACKWARD);
      motor2.run(FORWARD);
      motor3.run(FORWARD);
      motor4.run(BACKWARD);
    }
    else if (msg == "MYSTERY2"){
      motor1.setSpeed(200);
      motor2.setSpeed(200);
      motor3.setSpeed(200);
      motor4.setSpeed(200);
      motor1.run(FORWARD);
      motor2.run(BACKWARD);
      motor3.run(BACKWARD);
      motor4.run(FORWARD);
    }
    else{
      motor1.run(RELEASE);
      motor2.run(RELEASE);
      motor3.run(RELEASE);
      motor4.run(RELEASE);
    }
  }
}
