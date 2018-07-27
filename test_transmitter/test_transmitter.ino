const byte ENABLE_PIN = 2;
const byte LED_PIN = 13;

#define ERROR_WRONG_DATA_EVERY 100
#define ERROR_SHORT_DATA_EVERY 250
char sendBuf[120];
char sendWrongBuf[120];
char sendTooShortBuf[60];
unsigned long loop_index=0;

void setup()
{
  Serial.begin(1000000);
  pinMode (ENABLE_PIN, OUTPUT);  // driver output enable
  pinMode (LED_PIN, OUTPUT);  // built-in LED

  for (int i=0; i<120;i++)
  {
    sendBuf[i] = i;
    sendWrongBuf[i] = i;
    if (i < 60)
      sendTooShortBuf[i]=i;
  }

  sendWrongBuf[30] = 255;
} 
  
void loop()
{
  digitalWrite (ENABLE_PIN, HIGH);  // enable sending
  digitalWrite (LED_PIN, HIGH);  // flash LED 

  if (loop_index % ERROR_WRONG_DATA_EVERY ==0) {
    Serial.write(&sendWrongBuf[0], 60);
    delayMicroseconds(100);
    Serial.write(&sendWrongBuf[60], 60);    
  } else if (loop_index % ERROR_SHORT_DATA_EVERY ==0) {
    Serial.write(&sendTooShortBuf[0], 60);
  }
  else {
    Serial.write(&sendBuf[0], 60);
    delayMicroseconds(100);
    Serial.write(&sendBuf[60], 60);
  }

  // wait 1ms before release the enable: the last chars might still be in the RX buffer and not yet sent.
  delay(1);

  digitalWrite (ENABLE_PIN, LOW);  // disable sending

  // delay small enough to fit tested message rate, but long enough that the LED flash is visible
  delay(10);

  digitalWrite (LED_PIN, LOW);  // turn LED back off 

  // the rest of the delay is such that the sum of the three delays = the desired message period.
  delay(9);

  loop_index++;
}

