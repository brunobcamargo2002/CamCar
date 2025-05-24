#include "WheelController.h"

WheelController::WheelController(unsigned int pinControl1, unsigned int pinControl2, unsigned int pinPWM)
  : pinControl1(pinControl1), pinControl2(pinControl2), pinPWM(pinPWM){
  initPins();
  setMotorState(STOPPED);
  setDutyCyclePercentage(1.0);
}

void WheelController::initPins(){
  pinMode(pinControl1, OUTPUT);
  pinMode(pinControl2, OUTPUT);      
  ledcAttach(pinPWM, PWM_FREQ, PWM_RESOLUTION_BITS);
}

void WheelController::setMove(MotorState motorState, float dutyCyclePercentage){
  setMotorState(motorState);
  setDutyCyclePercentage(dutyCyclePercentage);
}

void WheelController::setMotorState(MotorState motorState){
  this->motorState = motorState;
  refreshMovimentation();
}

void WheelController::setDutyCyclePercentage(float dutyCyclePercentage){
  if(dutyCyclePercentage < 0 || dutyCyclePercentage > 1){ //gerenciar a exceção
    Serial.println("Erro: dutyCyclePercentage fora de [0, 1]");
    return;
  }
  this->dutyCyclePercentage = dutyCyclePercentage;
  refreshVelocity();
}

void WheelController::refreshMovimentation(){
  switch(motorState){
    case STOPPED:
      digitalWrite(pinControl1, LOW);
      digitalWrite(pinControl2, LOW);
      break;
    case FORWARD:
      digitalWrite(pinControl1, HIGH);
      digitalWrite(pinControl2, LOW);
      break;
    case BACKWARD:
      digitalWrite(pinControl1, LOW);
      digitalWrite(pinControl2, HIGH);
      break;
  }
}

void WheelController::refreshVelocity(){
  unsigned int dutyCycle = (int)(this->dutyCyclePercentage * MAX_DUTY_CYCLE);
  ledcWrite(pinPWM, dutyCycle);
}


WheelController::~WheelController(){

}