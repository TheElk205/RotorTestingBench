unsigned long intervallMillis = 500;
unsigned long lastIteration = 0;
unsigned long timeDifference = 0;
int sensorValues[] = {0,0,0,0,0};

void setup() {
  Serial.begin(9600);
}

void loop() {
  timeDifference = millis() - lastIteration;
  if(timeDifference < 500)
    delay(500-timeDifference);
  // Do stuff here.....
  sensorValues[0] = analogRead(0);
  sensorValues[1] = analogRead(1);
  sensorValues[2] = analogRead(2);
  sensorValues[3] = analogRead(3);
  sensorValues[4] = analogRead(4);
  Serial.println("Data");
  Serial.println(sensorValues[0]);
  Serial.println(sensorValues[1]);
  Serial.println(sensorValues[2]);
  Serial.println(sensorValues[3]);
  Serial.println(sensorValues[4]);
  Serial.println(timeDifference);
  lastIteration = millis();
}
