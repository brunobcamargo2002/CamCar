#include "MoveController.h"

MoveController* moveController;

void setup() {
  moveController = new MoveController();
}

void loop() {
  moveController->moveLine(FORWARD);
}
