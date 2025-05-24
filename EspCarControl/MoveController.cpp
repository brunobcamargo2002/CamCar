#include "MoveController.h"

MoveController::MoveController(): 
left(IN1, IN2, INA), right(IN3, IN4, INB){
}

void MoveController::moveLine(MotorState motorState){
  left.setMove(motorState, 1);
  right.setMove(motorState, 1);
}

MoveController::~MoveController(){
  
}