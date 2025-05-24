#include "WheelController.h"

#define INA 12
#define INB 13

#define IN1 2
#define IN2 4
#define IN3 5
#define IN4 18

class MoveController{
  private:
    WheelController left, right;

  public:
    MoveController();

    void moveLine(MotorState motorState);

    ~MoveController();

};