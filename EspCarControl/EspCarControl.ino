#include "MoveController.h"
#include "ServerCommunication.h"

MoveController* moveController = new MoveController();
ServerCommunication* serverCommunication;
float velocidade = 1.0;
void setup() {
  //moveController = new MoveController();
  //moveController->rotate(90);
  ServerCommunication::moveController = moveController;
  serverCommunication = new ServerCommunication();
  Serial.begin(115200);
  moveController->moveLine(true, 180);
}

void loop() {
  serverCommunication->handleClient();
  // moveController->processMove();
  // moveController->moveLine(true);
  // delay(2500);
  // moveController->stop();
  // moveController->moveLine(false);
  // delay(8000);
  // moveController->stop();
  // delay(1000);
}
