#ifndef SERVER_COMMUNICATION_H
#define SERVER_COMMUNICATION_H

#include "MoveController.h"

#include <WiFi.h>
#include <WebServer.h>
#include <ArduinoJson.h>

class ServerCommunication{
  private:
    const char* ssid = "Motog84";
    const char* password = "asuaal33";

    static WebServer* server;
    
  public:
    ServerCommunication();
    static MoveController* moveController;
    
  private:
    void setup();
    static void handleMove();
    
  public:
    void handleClient();
    ~ServerCommunication();
};

#endif