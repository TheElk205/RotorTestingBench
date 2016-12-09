#include <LiquidCrystal.h>
#include "fromArduino.h"

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

unsigned long intervallMicros = 50e3; // millisecondse3

unsigned long lastIteration = 0;
unsigned long iterationStarted = 0;
unsigned long iterationDuration = 0;
unsigned long timeDifference = 0;
int iterationsDone = 0;

int analogValues[] = {0,0,0,0,0};
int pwmMotor1 = 0;
int motorPin = 3;

// Error Codes
int errorIntervallTimeExceeded = 100;

boolean inCycle = true;

void setup()
{
  pinMode(motorPin, OUTPUT);
  
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("Started");

  lcd.begin(16, 2);
  lcd.clear();
  lcd.print("Rotor Testing");
  lastIteration = micros();
}

void loop()
{  
  if(inCycle)
  {
    iterationStarted = micros();

    // Read commands from python program
    readFromSerial();

    //Write Motor Vlaues
    writeAnalogValues();
    
    // Read all values here
    readAnalogValues();
    
    // Send all values here
    sendAnalogValues();

    //Wirte to display here
    printToDisplay();
    
    // Reset current time
    inCycle = false;
    lastIteration = micros();
    iterationDuration = lastIteration - iterationStarted;
  }
  else
  {
    timeDifference = micros() - lastIteration;
    if(timeDifference >= intervallMicros)
    {
      inCycle = true;
    }
  }

}

void printToDisplay()
{
  lcd.setCursor(0, 1);
  lcd.print("                ");
  lcd.setCursor(0, 1);
  lcd.print("");
  lcd.print(iterationDuration);
  lcd.print(" Pwm: ");
  lcd.print(pwmMotor1);
}

void readFromSerial()
{
  if (Serial.available() > 0){
    pwmMotor1 = Serial.read();
  }
}

void readAnalogValues()
{
  for(int i = 0; i < 5; i ++)
  {
    analogValues[i] = analogRead(i);
  }
}

void writeAnalogValues()
{
  analogWrite(motorPin, pwmMotor1);
  sendData(5, pwmMotor1, millis());
}

void sendAnalogValues()
{
  for(int i = 0; i < 5; i++)
  {
    sendData(i, analogValues[i], millis());
  }
}

void sendAnalogValuesProtobuf()
{
  /*
  RotorTestingBench__ToArduino toSend;
  toSend.pressure1 = analogValues[0];
  toSend.pressure2 = analogValues[1];
  toSend.pressure3 = analogValues[2];
  toSend.pressure4 = analogValues[3];

  //number of bytes to transmit
  size_t packageSize = rotor_testing_bench__to_arduino__get_packed_size(&toSend);
  uint8_t *buffer = (uint8_t) malloc(packageSize);
  rotor_testing_bench__to_arduino__pack(&toSend, buffer);
  Serial.write(buffer, packageSize);
  
  free(buffer);  
  */
}

void sendError(int errorCode)
{
  sendData(-1, errorCode, millis());
}

// Will be replaced by protobuf soon
void sendData(int pin, int value, unsigned long timestamp)
{
  /*
  Serial.print("{\"pin\": ");
  Serial.print(pin);
  Serial.print(", \"value\": ");
  Serial.print(value);
  Serial.print(", \"time\": ");
  Serial.print(timestamp);
  Serial.println("}");
  */
  //Start
  Serial.write(0);
  Serial.write(0);
  Serial.write(0);
  Serial.write(0);
  Serial.write(0);
  Serial.write(0);

  //Write pin
  Serial.write(getNthByte(pin, 0));

  //Write value
  Serial.write(getNthByte(value, 0));
  Serial.write(getNthByte(value, 1));

  //Write Timestamp
  Serial.write(getNthByte(timestamp, 0));
  Serial.write(getNthByte(timestamp, 1));
  Serial.write(getNthByte(timestamp, 2));
  Serial.write(getNthByte(timestamp, 3));
}

char getNthByte(int number, int n)
{
  return (number >> (8*n)) & 0xff;
}

char getNthByte(unsigned long number, int n)
{
  return (number >> (8*n)) & 0xff;
}

