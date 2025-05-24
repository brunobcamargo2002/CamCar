#include <Arduino.h>

#define PWM_FREQ 9000
#define PWM_RESOLUTION_BITS 8
#define MAX_DUTY_CYCLE ((1 << PWM_RESOLUTION_BITS) - 1)

enum MotorState {
  STOPPED,
  FORWARD,
  BACKWARD
};

class WheelController {
  private:
    MotorState motorState;
    float dutyCyclePercentage;

    const unsigned int pinPWM;
    const unsigned int pinControl1;
    const unsigned int pinControl2;

  public:
    WheelController(unsigned int pinControl1, unsigned int pinControl2, unsigned int pinPWM);

    void initPins();
    void setMove(MotorState motorState, float dutyCyclePercentage);
    void setMotorState(MotorState motorState);
    void setDutyCyclePercentage(float dutyCyclePercentage);

  private:
    void refreshMovimentation();
    void refreshVelocity();

  public:
    ~WheelController();
};
