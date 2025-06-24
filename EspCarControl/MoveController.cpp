#include "MoveController.h"

#define VELOCITY 0.8

MoveController::MoveController(): 
left(IN1, IN2, INA), right(IN3, IN4, INB){
}

void MoveController::moveLine(MotorState motorState){
  left.setMove(motorState, VELOCITY);
  right.setMove(motorState, VELOCITY);
}

void MoveController::setWheelsMove(MotorState leftState, float leftRPM, MotorState rightState, float rightRPM){
  left.setMove(leftState, VELOCITY);
  right.setMove(rightState, VELOCITY);
}

void MoveController::rotate(float angle, float velocity) {
  float duration = abs(angle) / velocity;

  unsigned long durationMs = (unsigned long)(duration * 1000);

  if (angle > 0) {
    left.setMove(STOPPED, 0);
    right.setMove(FORWARD, VELOCITY);
  } 
  else if (angle < 0) {
    left.setMove(FORWARD, VELOCITY);
    right.setMove(STOPPED, 0.0);
  } 
  else {
    return;
  }

  delay(durationMs);

  left.setMove(STOPPED, 0.0);
  right.setMove(STOPPED, 0.0);
}

MoveController::~MoveController(){
  
}