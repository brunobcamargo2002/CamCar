#ifndef MOVE_CONTROLLER_H
#define MOVE_CONTROLLER_H

#include "WheelController.h"
#include <Arduino.h>

#define INA 12
#define INB 13

#define IN1 2
#define IN2 4
#define IN3 5
#define IN4 18

class MoveController{
  private:
    WheelController left, right;
    float angularVelocity = 10;

  public:
    MoveController();

    void moveLine(MotorState motorState);
    void setWheelsMove(MotorState leftState, float leftRPM, MotorState rightState, float rightRPM);
    void rotate(float angle, float velocity);

    ~MoveController();

};

#endif