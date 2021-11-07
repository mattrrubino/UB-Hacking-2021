#include <Ethernet.h>
#include "ClearCore.h"

#define motor ConnectorM0
#define baudRate 9600

int sliceDistance = 10000;
int velocityLimit = 30000;
int accelerationLimit = 100000;

// MAC address of ClearCore
byte mac[] = {0x24, 0x15, 0x10, 0xB0, 0x07, 0x37};

EthernetServer server(12345);

void setupMotor(){
  MotorMgr.MotorInputClocking(MotorManager::CLOCK_RATE_NORMAL);
  MotorMgr.MotorModeSet(MotorManager::MOTOR_ALL, Connector::CPM_MODE_STEP_AND_DIR);
  
  motor.HlfbMode(MotorDriver::HLFB_MODE_HAS_BIPOLAR_PWM);
  motor.HlfbCarrier(MotorDriver::HLFB_CARRIER_482_HZ);
  motor.VelMax(velocityLimit);
  motor.AccelMax(accelerationLimit);

  motor.EnableRequest(true);
  while (motor.HlfbState() != MotorDriver::HLFB_ASSERTED) {
      continue;
  }
    
  Serial.println("Motor Enabled");
}

void setup() {
  Serial.begin(9600);
  setupMotor();
  
  Ethernet.begin(mac);
  while (Ethernet.linkStatus() == LinkOFF) {
    delay(1000);
  }

  Serial.println(Ethernet.localIP());
  
  server.begin();
}

bool moveAbsolutePosition(int position) {
    if (motor.StatusReg().bit.AlertsPresent) {
        Serial.println("Motor status: 'In Alert'. Move Canceled.");
        return false;
    }
    motor.Move(position, MotorDriver::MOVE_TARGET_ABSOLUTE);
    while (!motor.StepsComplete() || motor.HlfbState() != MotorDriver::HLFB_ASSERTED) {
        continue;
    }
    return true;
}

void slice() {
  moveAbsolutePosition(sliceDistance);
  delay(1000);
  moveAbsolutePosition(0);
}

void loop() {
    EthernetClient client = server.available();

    if (client.connected()) {
      while (client.available() > 0) {
        char c = client.read();
        slice();
        Serial.println(c);
      }
    }
}
