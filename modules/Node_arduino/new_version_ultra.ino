#include <SPI.h>
#include <Ethernet.h>
#include <PubSubClient.h>
#include <String.h>

// Function prototypes
void subscribeReceive(char* topic, byte* payload, unsigned int length);

// Set your MAC address and IP address here
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
IPAddress ip(192, 168, 1, 100);
 
// Make sure to leave out the http and slashes!
const char* server = "192.168.1.6";
 
// Ethernet and MQTT related objects
EthernetClient ethClient;
PubSubClient mqttClient(ethClient);

int in1,in2,in3=0;
int out1,out2,out3=0;

//declare parameter
int dect_dist=50;
int in_time=10;
int out_time=5;

void setup()
{
  // Useful for debugging purposes
  Serial.begin(9600);
  
  // declare pin
  pinMode(3,OUTPUT);
  pinMode(7,OUTPUT);
  pinMode(9,OUTPUT);
  pinMode(2,INPUT);
  pinMode(6,INPUT);
  pinMode(8,INPUT);

  // Start the ethernet connection
  Ethernet.begin(mac, ip);              
  
  // Ethernet takes some time to boot!
  delay(3000);                          
 
  // Set the MQTT server to the server stated above ^
  mqttClient.setServer(server, 1883);   
 
  // Attempt to connect to the server with the ID "myClientID"
  if (mqttClient.connect("myClientID")) 
  {
    Serial.println("Connection has been established, well done"); 
    // Establish the subscribe event
    mqttClient.setCallback(subscribeReceive);
  } 
  else 
  {
    Serial.println("Looks like the server connection failed...");
  }
}

void loop()
{
  // This is needed at the top of the loop!
  mqttClient.loop();

  String data1;
  String data2;
  String data3;
  digitalWrite(3,HIGH);
  delayMicroseconds(10);
  digitalWrite(3,LOW);
  
  int distance1 = pulseIn(2,HIGH)*340/2/10000;
  if (distance1<dect_dist){in1=in1+1;}  
  else {out1=out1+1;}
  
  digitalWrite(7,HIGH);
  delayMicroseconds(10);
  digitalWrite(7,LOW);
  
  int distance2 = pulseIn(6,HIGH)*340/2/10000;
  if (distance2<dect_dist){in2=in2+1;}
  else {out2=out2+1;}
  
  digitalWrite(9,HIGH);
  delayMicroseconds(10);
  digitalWrite(9,LOW);  
 
  int distance3 = pulseIn(8,HIGH)*340/2/10000;
  if (distance3<dect_dist){in3=in3+1;}
  else {out3=out3+1;}
  
  if (in1>in_time){
    Serial.println("location1-1:in");
    data1="1";
    mqttClient.publish("floor1/1", (char*)data1.c_str());  
    in1=0;
    out1=0;
    
    delay(100);
   }

  if (in2>in_time){
    Serial.println("location1-2:in");
    data2="1";
    mqttClient.publish("floor1/2", (char*)data2.c_str());
    in2=0;
    out2=0;
    
    delay(100);
   }

  if (in3>in_time){
    Serial.println("location1-3:in");
    data3="1";
    mqttClient.publish("floor1/3", (char*)data3.c_str());
    in3=0;
    out3=0;
    
    delay(100);
   }

  if (out1>out_time){
    Serial.println("location1-1:out");
    data1="0";
    mqttClient.publish("floor1/1", (char*)data1.c_str());
    out1=0;
    in1=0;
    
    delay(100);
    }
    
  if (out2>out_time){
    Serial.println("location1-2:out");
    data2="0";
    mqttClient.publish("floor1/2", (char*)data2.c_str());
    out2=0;
    in2=0;
    
    delay(100);
    }
 
  if (out3>out_time){
    Serial.println("location1-3:out");
    data3="0";
    mqttClient.publish("floor1/3", (char*)data3.c_str());
    out3=0;
    in3=0;
    
    delay(100);
    }

    
    delay(500);
}


void subscribeReceive(char* topic, byte* payload, unsigned int length)
{
  // Print the topic
  Serial.print("Topic: ");
  Serial.println(topic);
 
  // Print the message
  Serial.print("Message: ");
  for(int i = 0; i < length; i ++)
  {
    Serial.print(char(payload[i]));
  }
 
  // Print a newline
  Serial.println("");
}
