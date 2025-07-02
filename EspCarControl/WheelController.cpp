  #include "WheelController.h"

WheelController::WheelController(unsigned int pinControl1, unsigned int pinControl2, unsigned int pinPWM, unsigned int pinEncoder)
  : pinControl1(pinControl1), pinControl2(pinControl2), pinPWM(pinPWM), pinEncoder(pinEncoder), countTicks(0), rpm_buffer_idx(0)
  /*,motorPID(&RPM, &currentPWM, &TargetRPM, KP, KI, KD, DIRECT)*/ {
  initPins();
  stop();
  //motorPID.SetOutputLimits(MIN_DUTY_CYCLE, MAX_DUTY_CYCLE);
  //motorPID.SetMode(AUTOMATIC);

  // Inicializa buffer da média móvel com zeros
  for (int i = 0; i < RPM_AVG_SIZE; i++) {
    rpm_buffer[i] = 0;
  }
}

WheelController::WheelController(unsigned int pinControl1, unsigned int pinControl2, unsigned int pinPWM, int dutyCycle)
: pinControl1(pinControl1), pinControl2(pinControl2), pinPWM(pinPWM), dutyCycle(dutyCycle){
  initPins();
  stop();
}



void WheelController::initPins(){
  pinMode(pinControl1, OUTPUT);
  pinMode(pinControl2, OUTPUT);
  pinMode(pinEncoder, INPUT);
  ledcAttach(pinPWM, PWM_FREQ, PWM_RESOLUTION_BITS); // Mantido seu código original
  ledcWrite(pinPWM, dutyCycle);
}

void WheelController::setSpeed(int dutyCycle){
  this->dutyCycle = dutyCycle;
  ledcWrite(pinPWM, dutyCycle);
}

void WheelController::setMove(bool forward, float targetRPM){
  this->motorState = (forward) ? MOTOR_FORWARD : MOTOR_BACKWARD;
  this->TargetRPM = targetRPM;
  refreshState();
}

void WheelController::setMove(bool forward, int dutyCycle){
  this->motorState = (forward) ? MOTOR_FORWARD : MOTOR_BACKWARD;
  dutyCycle = (dutyCycle == -1) ? this->dutyCycle : dutyCycle;
  ledcWrite(pinPWM, dutyCycle);
  refreshState();
  gradualVelocity();
}

void WheelController::gradualVelocity() {
  const int step = 5;                // incremento por passo
  const int delayMs = 3;            // atraso entre passos

  for (int duty = 100; duty <= dutyCycle; duty += step) {
    ledcWrite(pinPWM, duty);
    delay(delayMs);
  }
  ledcWrite(pinPWM, dutyCycle);
}

void WheelController::gradualRedution(){
  const int step = 10;                // incremento por passo
  const int delayMs = 3;            // atraso entre passos

  for (int duty = dutyCycle; duty >= 80; duty -= step) {
    ledcWrite(pinPWM, duty);
    delay(delayMs);
  }
  ledcWrite(pinPWM, 0);

}


void WheelController::stop(){
  gradualRedution();
  this->motorState = MOTOR_STOPPED;
  refreshState();
}

void WheelController::refreshState(){
  switch(motorState){
    case MOTOR_STOPPED:
      digitalWrite(pinControl1, LOW);
      digitalWrite(pinControl2, LOW);
      break;
    case MOTOR_FORWARD:
      digitalWrite(pinControl1, HIGH);
      digitalWrite(pinControl2, LOW);
      break;
    case MOTOR_BACKWARD:
      digitalWrite(pinControl1, LOW);
      digitalWrite(pinControl2, HIGH);
      break;
  }
}

void WheelController::refreshRPM(unsigned long deltaTime){
  double currentRPM = countTicks * (60000.0 / DISK_TICKS) / deltaTime;
  countTicks = 0;

  rpm_buffer[rpm_buffer_idx] = currentRPM;
  rpm_buffer_idx = (rpm_buffer_idx + 1) % RPM_AVG_SIZE;

  double soma = 0;
  for (int i = 0; i < RPM_AVG_SIZE; i++) {
    soma += rpm_buffer[i];
  }
  RPM = soma / RPM_AVG_SIZE;
}

void WheelController::computePWM(){
  //motorPID.Compute();
  ledcWrite(pinPWM, currentPWM); // Mantido seu código original
}

void WheelController::incrementTick(){
  countTicks++;
}

WheelController::~WheelController(){

}
