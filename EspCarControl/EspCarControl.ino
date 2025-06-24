#include "MoveController.h"
#include "ServerCommunication.h"

MoveController* moveController = new MoveController();
ServerCommunication* serverCommunication;
float velocidade = 1.0;
void setup() {
  //moveController = new MoveController();
  //moveController->rotate(90);
  //ServerCommunication::moveController = moveController;
  //serverCommunication = new ServerCommunication();
}

void loop() {
  //moveController->rotate(90, velocidade);
  moveController->moveLine(FORWARD);
  delay(3000);
  //moveController->moveLine(STOPPED);
  //delay(1000);
  velocidade += 1;
}
