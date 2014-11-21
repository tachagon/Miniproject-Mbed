void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
}

void loop() {
  // read the input on analog pin 0:
  int Vldr = analogRead(A0);
  int Vtem = analogRead(A1);
  // print out the value you read:
  /*
  Serial.print("LDR = ");
  Serial.print(Vldr);
  Serial.print(" , temperature = ");
  Serial.println(Vtem);
  */
  String str = String(Vldr)+","+String(Vtem)+",\n";
  Serial.print(str);
  delay(1000);        // delay in between reads for stability
}
