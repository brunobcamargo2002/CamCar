#include "MoveController.h"

MoveController::MoveController(): 
left(IN1, IN2, INA), right(IN3, IN4, INB){
}

void MoveController::moveLine(MotorState motorState){
  left.setMove(motorState, 1);
  right.setMove(motorState, 1);
}

void MoveController::setWheelsMove(MotorState leftState, float leftRPM, MotorState rightState, float rightRPM){
  left.setMove(leftState, leftRPM);
  right.setMove(rightState, rightRPM);
}

MoveController::~MoveController(){
  
}