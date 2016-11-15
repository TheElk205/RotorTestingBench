#include <LiquidCrystal.h>

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

unsigned long intervallMicros = 50e3;
unsigned long lastIteration = 0;
unsigned long iterationStarted = 0;
unsigned long iterationDuration = 0;
unsigned long timeDifference = 0;
int iterationsDone = 0;

int analogValues[] = {0,0,0,0,0};

// Error Codes
int errorIntervallTimeExceeded = 100;

boolean inCycle = true;

void setup()
{
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
    // Read all values here
    readAnalogValues();
  
    // Send all values here
    sendAnalogValues();
    
    // Reset current time
    inCycle = false;
    lastIteration = micros();
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

void readAnalogValues()
{
  for(int i = 0; i < 5; i ++)
  {
    analogValues[i] = analogRead(i);
  }
}

void sendAnalogValues()
{
  for(int i = 0; i < 5; i++)
  {
    sendData(i, analogValues[i], millis());
  }
}

void sendError(int errorCode)
{
  sendData(-1, errorCode, millis());
}

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

