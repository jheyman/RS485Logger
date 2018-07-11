
#include <SPI.h>
#include <Ethernet.h>
#include <EthernetUdp.h>
#include <MsTimer2.h>


byte mac[] = {
  0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED
};
IPAddress local_ip(192, 168, 0, 40);
IPAddress remote_ip(192, 168, 0, 11);

unsigned int localPort = 8888;

char  ReplyBuffer[256];     

EthernetUDP Udp;

int nbReceived = 0;
unsigned long start_time;
unsigned long stop_time;

unsigned long latestCharReceivedTime=0;
unsigned long now=0;
unsigned long gaptime=0;
const byte TEST_PIN = 2;
const byte LED_PIN = 13;

void setup()
{
  Ethernet.begin(mac, local_ip);
  Udp.begin(localPort);
  
  Serial.begin(1000000);
  
  pinMode (TEST_PIN, OUTPUT);  // driver output enable
  digitalWrite (TEST_PIN, LOW);  // disable sending
  pinMode(LED_PIN, OUTPUT);

  MsTimer2::set(75, onTimer);
  //MsTimer2::start();  
}

bool firstIdleAfterChar=false;

bool dumpData = false;
bool timerStarted = false;


void onTimer() {

  digitalWrite (TEST_PIN, HIGH);        
  delay(100);
  digitalWrite (TEST_PIN, LOW);
  dumpData = true;        
}



void loop()
{
   char received;

   if (Serial.available() > 0) {
      received = Serial.read();     
      ReplyBuffer[nbReceived++] = received;
      firstIdleAfterChar = false;
      //MsTimer2::stop();  
   }

        // first empty buffer after RX : initialize gaptime 
        if (nbReceived>0) {

          if (!timerStarted){
            MsTimer2::start();
            timerStarted = true;
          }
         /*
          if (firstIdleAfterChar==false) {
            
            firstIdleAfterChar = true;
            //latestCharReceivedTime = micros();
            //gaptime = 0;
            //digitalWrite (TEST_PIN, HIGH);      
            MsTimer2::start();  
          }
          else
          {
            //now = micros();
            //gaptime  += (now - latestCharReceivedTime);
            //latestCharReceivedTime = now;
          }  
          */
        } 

        



   if (dumpData) {
      dumpData = false;
      MsTimer2::stop();
      timerStarted = false;
   // if (nbReceived >=120) {
    //now = micros();
   //if (nbReceived !=0 && ((now - latestCharReceivedTime) > 10000)) {
    //if (gaptime > 10000) {
       //digitalWrite (TEST_PIN, LOW); 
            
        digitalWrite (LED_PIN, HIGH);  // flash LED 
        Udp.beginPacket(remote_ip, 8888);
        Udp.write(ReplyBuffer, nbReceived);
        Udp.endPacket();
       
       delay(100);
       digitalWrite (LED_PIN, LOW);  // turn LED back off

       //delay(900);
       firstIdleAfterChar = false;
       nbReceived = 0;
   } 
   
} 
