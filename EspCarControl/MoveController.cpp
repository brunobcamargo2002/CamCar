#include "MoveController.h"

WheelController* MoveController::leftPtr = nullptr;
WheelController* MoveController::rightPtr = nullptr;

MoveController::MoveController(): 
left(IN1, IN2, INA, 210), right(IN4, IN3, INB, 210){
  leftPtr = &left;
  rightPtr = &right;

  attachInterrupt(digitalPinToInterrupt(ENCODER_LEFT), incrementTickLeft, FALLING);
  attachInterrupt(digitalPinToInterrupt(ENCODER_RIGHT), incrementTickRight, FALLING);
}

void MoveController::incrementTickLeft(){
  if(leftPtr != nullptr)
    leftPtr->incrementTick();
}

void MoveController::incrementTickRight(){
  if(rightPtr != nullptr)
    rightPtr->incrementTick();
}
unsigned long timeold = 0;
void MoveController::processMove(){
  if (millis() - timeold >= 300){
    // unsigned long deltaTime = millis() - timeold;
    detachInterrupt(ENCODER_LEFT);
    detachInterrupt(ENCODER_RIGHT);
    left.refreshRPM(millis() - timeold);
    right.refreshRPM(millis() - timeold);
    timeold = millis();

    // Debug
    // Serial.println("Left");
    // Serial.print("Vel: ");
    // Serial.print(left.currentPWM, 2);
    // Serial.print("    ");
    // Serial.print("RPM: ");
    // Serial.println(left.RPM, 0);
    
    // Serial.println("Right");
    // Serial.print("Vel: ");
    // Serial.print(right.currentPWM, 2);
    // Serial.print("    ");
    // Serial.print("RPM: ");
    // Serial.println(right.RPM, 0);
    
    attachInterrupt(ENCODER_LEFT, incrementTickLeft, FALLING);
    attachInterrupt(ENCODER_RIGHT, incrementTickRight, FALLING);
  }
  left.computePWM();
  right.computePWM();
}

void MoveController::moveLine(bool forward, float RPM){
  left.setMove(forward, RPM);
  right.setMove(forward, RPM);
}

void MoveController::moveLine(bool forward){
  left.setSpeed(210);
  right.setSpeed(210);
  left.setMove(forward);
  right.setMove(forward);
}

void MoveController::rotate(bool clockwise){
  right.setSpeed(190);

  right.setMove(clockwise);
}

void MoveController::stop(){
  left.stop();
  right.stop();
}

/*
void MoveController::rotate(float angle) {
  float duration = abs(angle) / 60.0;

  unsigned long durationMs = (unsigned long)(duration * 1000);

  if (angle > 0) {
    left.setMove(false, 255);
    right.stop();
  } 
  else if (angle < 0) {
    left.stop();
    right.setMove(false, 255);
  } 
  else {
    return;
  }

  delay(durationMs);

  left.stop();
  right.stop();
}
*/


MoveController::~MoveController(){
  
}