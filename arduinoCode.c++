int AnalogPin = A5;
int time = 1000;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(AnalogPin, INPUT);
  
  

}

void loop() {
  // put your main code here, to run repeatedly:
  int potiValue = analogRead(AnalogPin);  
    Serial.println(potiValue);        
    delay(time);  

}