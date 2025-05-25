#include "MoveController.h"
#include "ServerCommunication.h"

MoveController* moveController;
ServerCommunication* serverCommunication;

void setup() {
  moveController = new MoveController();
  moveController->moveLine(FORWARD);
  ServerCommunication::moveController = moveController;
  serverCommunication = new ServerCommunication();
}

void loop() {
  serverCommunication->handleClient();
}
