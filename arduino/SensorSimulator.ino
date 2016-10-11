long randNumber;
long iteration = 0;
int maxValue = 300;

void setup()
{
  Serial.begin(9600);

  // if analog input pin 0 is unconnected, random analog
  // noise will cause the call to randomSeed() to generate
  // different seed numbers each time the sketch runs.
  // randomSeed() will then shuffle the random function.
  randomSeed(analogRead(0));
}

void loop()
{
  randNumber = random(maxValue);
  Serial.print("1:");
  Serial.println(randNumber);
  if(iteration % 2 == 0)
  {
    randNumber = random(maxValue);
    Serial.print("2:");
    Serial.println(randNumber);
  }
  if(iteration % 3 == 0)
  {
    randNumber = random(maxValue);
    Serial.print("3:");
    Serial.println(randNumber);
  }
  iteration++;

  delay(50);
}

