#include <LiquidCrystal.h>

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

unsigned long intervallMillis = 50;
unsigned long lastIteration = 0;
unsigned long timeDifference = 0;
int analogValues[] = {0,0,0,0,0};

// Error Codes
int errorIntervallTimeExceeded = 100;

void setup()
{
  // put your setup code here, to run once:
  Serial.begin(9600);

  lcd.begin(16, 2);
  lcd.print("Rotor Testing Bench");
  lastIteration = millis();
}

void loop()
{
  timeDifference = millis() - lastIteration;
  if(timeDifference < intervallMillis)
    delay(intervallMillis-timeDifference);
    
  // Send error if intervall couldnt be reached
  if(timeDifference > intervallMillis)
    sendError(errorIntervallTimeExceeded);
    
  // Read all values here
  readAnalogValues();

  // Send all values here
  sendAnalogValues();

  //Write to display
  lcd.setCursor(0, 1);
  lcd.print(timeDifference);
  lcd.print(" of ");
  lcd.print(intervallMillis);
    
  // Reset current time
  lastIteration = millis();  
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
  Serial.print("{\"pin\": ");
  Serial.print(pin);
  Serial.print(", \"value\": ");
  Serial.print(value);
  Serial.print(", \"time\": ");
  Serial.print(timestamp);
  Serial.println("}");
}

