#ifndef WHEEL_CONTROLLER_H
#define WHEEL_CONTROLLER_H

#include <Arduino.h>
#include <PID_v1.h>

#define PWM_FREQ 5000
#define PWM_RESOLUTION_BITS 8
#define MIN_DUTY_CYCLE 0
#define MAX_DUTY_CYCLE ((1 << PWM_RESOLUTION_BITS) - 1)
// #define KP 0.5   // Proporcional: resposta forte, mas não muito agressiva
// #define KI 0.05  // Integral: corrige erro acumulado devagar
// #define KD 0.02
#define KP 0.2
#define KI 0.2
#define KD 0.005
#define DISK_TICKS 20
#define RPM_AVG_SIZE 5

enum MotorState{
  MOTOR_STOPPED,
  MOTOR_FORWARD,
  MOTOR_BACKWARD 
};

class WheelController {
  public: 
    volatile MotorState motorState;
    double RPM, TargetRPM;
    double currentPWM;
    //PID motorPID;
    volatile unsigned long countTicks;
    int dutyCycle;
    
    const unsigned int pinPWM;
    const unsigned int pinControl1;
    const unsigned int pinControl2;
    unsigned int pinEncoder; //é const

    double rpm_buffer[RPM_AVG_SIZE];
    int rpm_buffer_idx;

  public:
    WheelController(unsigned int pinControl1, unsigned int pinControl2, unsigned int pinPWM, unsigned int pinEncoder);

    WheelController(unsigned int pinControl1, unsigned int pinControl2, unsigned int pinPWM, int dutyCycle);

    void setMove(bool forward, float targetRPM);
    void setMove(bool forward);
    void gradualVelocity();
    void gradualRedution();
    void stop();
    void refreshRPM(unsigned long deltaTime);
    void computePWM();
    void incrementTick();

  private:
    void initPins();
    void refreshState();

  public:
    ~WheelController();
};

#endif
