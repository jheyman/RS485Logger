
//const byte ENABLE_PIN = 2;
const byte LED_PIN = 13;
unsigned long latestCharReceivedTime=0;
int nbReceived = 0;

void setup()
{
  Serial.begin(1000000);
  pinMode (LED_PIN, OUTPUT);  // built-in LED
  //pinMode (ENABLE_PIN, OUTPUT);  // driver output enable
  //digitalWrite (ENABLE_PIN, LOW);  // disable sending
}

void loop()
{
   char received;
  
   if (Serial.available() > 0) {
      latestCharReceivedTime = micros();
      received = Serial.read();
      nbReceived++;   
   }
    
   //if (nbReceived >=60)
   if (nbReceived !=0 && (micros() - latestCharReceivedTime > 2000))
   {
      digitalWrite (LED_PIN, HIGH);  // flash LED 
      delay(10);
      digitalWrite (LED_PIN, LOW);  // turn LED back off 
      nbReceived = 0;
   }
} 
