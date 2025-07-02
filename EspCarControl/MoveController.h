#ifndef MOVE_CONTROLLER_H                                                                                          
#define MOVE_CONTROLLER_H

#include "WheelController.h"

#include <Arduino.h>

#define INA 25
#define INB 33

#define IN1 2
#define IN2 4
#define IN3 5
#define IN4 18

#define ENCODER_LEFT 35
#define ENCODER_RIGHT 34

class MoveController{
  private:
    WheelController left, right;
    float angularVelocity = 10;

    static WheelController* leftPtr;
    static WheelController* rightPtr;

  public:
    MoveController();

    void processMove();

    void moveLine(bool forward, float RPM);
    void moveLine(bool forward);
    void stop();
    void rotate(bool clockwise);

    void static incrementTickLeft();
    void static incrementTickRight();

    ~MoveController();

};

#endif