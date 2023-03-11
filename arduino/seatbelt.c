#define SENSOR_PIN 2;


void setup() 
{
    Serial.begin(9600);
    pinMode(SENSOR_PIN, INPUT);
}
 
void loop() 
{
    if (digitalRead(SENSOR_PIN) == HIGH)
    {
        Serial.print("true");
    }
    else
    {
        Seria.println("false");
    } 
    delay(200);
}