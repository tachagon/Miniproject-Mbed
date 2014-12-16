
#define FOSC (16000000UL)
#include <avr/io.h>
//*********************************** usart set and method ***********************************

void USART_init( uint16_t baudrate ) {
  uint16_t ubrr;
  // UCSR0A register settings
  // U2X0=0 => normal speed
  // MPCM0=0 => don't use multi‐processor communication mode
  UCSR0A = 0;
  
#ifdef DOUBLE_SPEED
  UCSR0A |= (1<<U2X0); // use double speed
  ubrr = ((FOSC/8)/baudrate)-1;
#else
  ubrr = ((FOSC/16)/baudrate)-1 ;
#endif
  // set baudrate
  UBRR0H = (uint8_t)(ubrr>>8); // high byte
  UBRR0L = (uint8_t)(ubrr); // low byte
  
  // UCSR0B register settings
  // RXEN0=1, TXEN0=1 => Enable both RX and TX
  // UCSZ02=0 => don't use ninth‐bit data
  // RXCIE0=0, TXCIE0=0, UDRIE0=0 => no TX/RX interrupt
  UCSR0B = (1<<RXEN0)|(1<<TXEN0);
  // UCSR0C register settings
  // UMSEL01=0, UMSEL00=0 => Asynchronous USART
  // UPM01=0, UPM00=0 => no parity bit
  // USBS0=0 => 1‐stop bit
  // UCSZ01=1, UCSZ00=1 => 8‐bit data
  UCSR0C = (1<<UCSZ01)|(1<<UCSZ00);
}

void USART_send( uint8_t data ) {
  // Wait for empty transmit buffer (the UDRE0 bit is set.)
  while ( !(UCSR0A & (1<<UDRE0)) ) ;
  // Put data into buffer, sends the data
  UDR0 = data;
}
void send_m( String &s ) {
  for(uint16_t i = 0 ; i < s.length(); i++){
    USART_send(s[i]);
  }
}

uint8_t USART_receive( void ) {
  // Wait for data to be received (the RXC0 bit is set.)
  while ( !(UCSR0A & (1<<RXC0)) ) ;
  // Get and return received data from buffer
  return UDR0;
}
//*********************************** end usart set and method | ADC set and method ***********************************

void ADC_init() {
  DIDR0 = (1<<ADC5D)|(1<<ADC4D)|(1<<ADC3D)|(1<<ADC2D)|(1<<ADC1D)|(1<<ADC0D);
  // REFS1=0, REFS0=0: use AVCC, ADLAR=0: right]alignment,
  // MUX3..0=0000 => ADC0
  ADMUX = (1<<REFS0);
  ADCSRB = 0; // ADTS2=0,ADTS1=0,ADTS0=0 (with ADATE=1): free]running mode
  // 10]bit resolution requires a clock between 50khz and 200kHz.
  ADCSRA = (1<<ADPS2)|(1<<ADPS1)|(1<<ADPS0); // set ADC clock prescaler: 128
  // enable/start ADC, auto]trigger (ADATE=1)
  ADCSRA |= (1<<ADEN)|(1<<ADSC)|(1<<ADATE);
  // The first conversion starts 25 FADC cycles after ADEN set
  // 16MHz/128 = 125kHz => 8usec x 25 = 200 usec at least
  delayMicroseconds(205);
}

uint16_t readADC( uint8_t channel ){
  static uint8_t current_channel = 0;
  uint16_t x;
  if( current_channel != channel) {
    current_channel = channel;
    while ( !(ADCSRA & (1<<ADIF)) );
    ADCSRA |= (1<<ADIF);
    ADMUX &= 0xF0;
    ADMUX |= (channel & 0x0F);
    delayMicroseconds(205);
  }
  x = (uint16_t)ADCL;
  x |= ((uint16_t)ADCH << 8);
  return (x & 0x3FF);
}

//*********************************** end ADC set and method | time/ counter 1 set and method ***********************************

void T1_init() {
  TCNT1 = 0;
  OCR1A = 0;
  OCR1B = 0;
  ICR1 = 0;
  TCCR1A = 0;
  TCCR1B = 0;
  TIMSK1 = 0; // disable all interrupts
  TIFR1 = (1<<ICF1) | (1<<OCF1B) | (1<<OCF1A) | (1<<TOV1); // clear all flags
  TCNT1 = 0;
  // Use Timer/Count1 in normal mode (no output compare, no PWM)
  TCCR1B |= (1<<CS12) | (1<<CS10); // prescaler=1024
  TIMSK1 = (1<<TOIE1); // Timer1 Overflow Interrupt Enable
}
volatile uint16_t count = 0;

ISR(TIMER1_OVF_vect) { // ISR for Timer/Counter1 Overflow Interrupt
  count++; // increment counter
}

void delay_test(uint16_t msec){
  TCCR1B |= (1<<CS12) | (1<<CS10); // prescaler=1024
  count = 0;
  TCNT1 = 0;
  uint16_t real_count = msec/0.064;
  uint16_t b = real_count/65535;
  uint16_t pece = real_count%65535;
  while(TCNT1 < pece or count < b);
}

//*********************************** end time/ counter 1 set and method ***********************************
int LED_PIN = 3;

void setup() {
  DDRD |= 1 << DDD3;// set pin3 = out
  USART_init(9600);//set rate
  ADC_init();
  T1_init();
  DDRD |= (1<<DDD1); // PD1/TXD as output
  //Serial.begin(9600); 
}

void loop() {
  // read the input on analog pin 0:
  int Vldr = readADC(0);
  int Vtem = readADC(1);
  // print out the value you read:
  /*
  Serial.print("LDR = ");
  Serial.print(Vldr);
  Serial.print(" , temperature = ");
  Serial.println(Vtem);
  */
  String str = String(Vldr)+","+String(Vtem)+"\n";
  //Serial.print(str);
  //int b = 20;
  //char test[] = "abc" + char(b);
  //char da[10] = String(Vldr) + "," + String(Vtem);
  uint8_t data = 100;
  send_m(str);
  PORTD |= 1 << 3;
  delay_test(1000);
  PORTD &= ~( 1 << 3 );
  delay_test(1000);        // delay in between reads for stability
}

//******************************** method ***********************************



