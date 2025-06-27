#ifndef SERVER_COMMUNICATION_H
#define SERVER_COMMUNICATION_H

#include "MoveController.h"

#include <WiFi.h>
#include <WebServer.h>
#include <ArduinoJson.h>

class ServerCommunication{
  private:
    const char* ssid = "PC_MIYAIJI 8457";
    const char* password = "019283Th";

    static WebServer* server;
    
  public:
    ServerCommunication();
    static MoveController* moveController;
    
  private:
    void setup();
    static void handleLine();
    static void handleStop();
    static void handleRotation();
    
  public:
    void handleClient();
    ~ServerCommunication();
};

#endif