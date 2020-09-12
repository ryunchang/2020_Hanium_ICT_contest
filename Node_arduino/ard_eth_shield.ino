#include <SPI.h>
#include <Ethernet.h>
#include <PubSubClient.h>
#include <string>

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


void setup()
{
  // Useful for debugging purposes
  Serial.begin(9600);
  pinMode(2,OUTPUT);
  pinMode(3,INPUT);

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
 


  digitalWrite(2,HIGH);
  delayMicroseconds(10);
  digitalWrite(2,LOW);

  
  int distance = pulseIn(3,HIGH)*340/2/10000;
  string data = ;
  Serial.print(distance);
  Serial.println("cm");
  data = (char)distance;

  // Ensure that we are subscribed to the topic "MakerIOTopic"
  //mqttClient.subscribe("floor1");
 
  // Attempt to publish a value to the topic "MakerIOTopic"
  if(mqttClient.publish("floor1", "data"))
  {
    Serial.println("Publish message success");
  }
  else
  {
    Serial.println("Could not send message :(");
  }
 
  // Dont overload the server!
  delay(4000);
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
