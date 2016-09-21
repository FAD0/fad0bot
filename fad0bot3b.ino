#include <Servo.h>

Servo servoLeft;
Servo servoRight;
Servo servoCam;

String instring;
String previous_instring = "nothing";
String sstrength;
int lturn_strength = 100;
int rturn_strength = 100;
int lstrength = 60;
int rstrength = 60;
int camTilt = 90;

void setup()
{
  Serial.begin(9600);
  // Attached drive pins
  servoLeft.attach(11);
  servoRight.attach(12);
  servoCam.attach(9);
  servoLeft.writeMicroseconds(1500);
  servoRight.writeMicroseconds(1500);
  servoCam.write(camTilt);
}

void loop()  {
  if (Serial.available()) {
    instring = Serial.readStringUntil('\n');
    Serial.println(instring);

    if (instring == "protocol_change") {
      Serial.println("Using LR protocol\n");
      while (!Serial.available()) {}
      sstrength = Serial.readStringUntil('\n');
      Serial.print("Left :");
      Serial.println(sstrength);
      lstrength = sstrength.toInt(); 
      while (!Serial.available()) {}
      sstrength = Serial.readStringUntil('\n'); 
      Serial.print("Right :");
      Serial.println(sstrength);
      rstrength = sstrength.toInt(); 
      servoLeft.writeMicroseconds(1500 - lstrength);
      servoRight.writeMicroseconds(1500 + rstrength);
      previous_instring = instring;
    }
    else if (instring == "protocol_change_turn") {
      Serial.println("Using LR turn protocol\n");
      while (!Serial.available()) {}
      sstrength = Serial.readStringUntil('\n');
      Serial.print("Left :");
      Serial.println(sstrength);
      lturn_strength = sstrength.toInt(); 
      while (!Serial.available()) {}
      sstrength = Serial.readStringUntil('\n'); 
      Serial.print("Right :");
      Serial.println(sstrength);
      rturn_strength = sstrength.toInt(); 
//      servoLeft.writeMicroseconds(1500 + lturn_strength);
//      servoRight.writeMicroseconds(1500 + rturn_strength);
      previous_instring = instring;
    }
    else if (instring == "forward") {
      Serial.println("Forward was received\n");
      servoLeft.writeMicroseconds(1500 - lstrength);
      servoRight.writeMicroseconds(1500 + rstrength);
      previous_instring = instring;
    }
    else if (instring == "backward") {
      Serial.println("Backward was received\n");
      servoLeft.writeMicroseconds(1500 + lstrength);
      servoRight.writeMicroseconds(1500 - rstrength);
      previous_instring = instring;
    }
    else if (instring == "right") {
      Serial.println("Right was received\n");
      servoLeft.writeMicroseconds(1500 - lturn_strength);
      servoRight.writeMicroseconds(1500 - rturn_strength);
      previous_instring = instring;
    }
    else if (instring == "left") {
      Serial.println("Left was received\n");
      servoLeft.writeMicroseconds(1500 + lturn_strength);
      servoRight.writeMicroseconds(1500 + rturn_strength);
      previous_instring = instring;
    }
    else if (instring == "stop") {
      Serial.println("Stop was received\n");
      servoLeft.writeMicroseconds(1500);
      servoRight.writeMicroseconds(1500);
      previous_instring = instring;
    }
    else if (instring == "increment_strength") {
      lstrength += 10;
      rstrength += 10;
      if (previous_instring == "forward") {
      servoLeft.writeMicroseconds(1500 - lstrength);
      servoRight.writeMicroseconds(1500 + rstrength);
      }   
      else if (previous_instring == "backward") {
      servoLeft.writeMicroseconds(1500 + lstrength);
      servoRight.writeMicroseconds(1500 - rstrength);
      }   
    }
    else if (instring == "decrement_strength") {
      lstrength += -10;
      rstrength += -10;
      if (previous_instring == "forward") {
      servoLeft.writeMicroseconds(1500 - lstrength);
      servoRight.writeMicroseconds(1500 + rstrength);
      }   
      else if (previous_instring == "backward") {
      servoLeft.writeMicroseconds(1500 + lstrength);
      servoRight.writeMicroseconds(1500 - rstrength);
      }   
    } 
    else if (instring == "increment_turn_strength") {
      lturn_strength += 10;
      rturn_strength += 10;
      if (previous_instring == "left") {
      servoLeft.writeMicroseconds(1500 + lturn_strength);
      servoRight.writeMicroseconds(1500 + rturn_strength);
      } 
      else if (previous_instring == "right") {
      servoLeft.writeMicroseconds(1500 - lturn_strength);
      servoRight.writeMicroseconds(1500 - rturn_strength);
      } 
    } 
    else if (instring == "decrement_turn_strength") {
      lturn_strength += -10;
      rturn_strength += -10;
      if (previous_instring == "left") {
      servoLeft.writeMicroseconds(1500 + lturn_strength);
      servoRight.writeMicroseconds(1500 + rturn_strength);
      } 
      else if (previous_instring == "right") {
      servoLeft.writeMicroseconds(1500 - lturn_strength);
      servoRight.writeMicroseconds(1500 - rturn_strength);
      } 
    } 
    else if (instring == "tilt_cam_up") {
      camTilt += 2;
      servoCam.write(camTilt);
    } 
    else if (instring == "tilt_cam_down") {
      camTilt += -2;
      servoCam.write(camTilt);
    } 
    delay(100);
  }
}
