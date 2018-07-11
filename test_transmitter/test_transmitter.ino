const byte ENABLE_PIN = 2;
const byte LED_PIN = 13;

void setup()
{
  Serial.begin(1000000);
  pinMode (ENABLE_PIN, OUTPUT);  // driver output enable
  pinMode (LED_PIN, OUTPUT);  // built-in LED
} 
  
void loop()
{
  digitalWrite (ENABLE_PIN, HIGH);  // enable sending
  digitalWrite (LED_PIN, HIGH);  // flash LED 

  Serial.write("ABCDEFGHIJKLMNOPQRSTUVWXYZ....XXXXXXXX..........ZZZZZZZZZZZZ");
  delayMicroseconds(100);
  Serial.write("WWWWWWWWWWWW..........ABCDEFGHIJKLMNOPQRSTUVWXYZ....XXXXXXXX");
  
  //Serial.write("PING");
  delay(1);
  //delay(1);

  

  digitalWrite (ENABLE_PIN, LOW);  // disable sending

  delay(100);

  digitalWrite (LED_PIN, LOW);  // turn LED back off 

  delay(1000);
}

