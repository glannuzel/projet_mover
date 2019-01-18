#include <avr/io.h>
#include <util/delay.h>

#define BAUD 115200
#define MYUBRR F_CPU/8/BAUD-1
// change pin that buzzer is connected to here
#define BUZZER_PIN  5
// define led colors pins
#include <FastLED.h>
#define LED_PIN     3
#define NUM_LEDS    60

//Master : on envoie des données
//Slave : on va t'interroger sur tes données

//Init : dire au processeur que on active le SPI
//On est maitre (processeur), notre puce est esclave
//Mais il arrive que le processeur soit esclave
void SPI_MasterInit(void)
{
  /* Set MOSI and SCK output, all others input */
  //DDRX=(1<<MOSI)|(1<<SCK) on choisit quelle pin sera MOSI et laquelle sera SCK
  DDRB |= (1<<DDB3)|(1<<DDB5); //port x : DDBX
  /* Enable SPI, Master, set clock rate fck/16 */
  SPCR = (1<<SPE)|(1<<MSTR)|(1<<SPR0);
}

//Pour transmettre une valeur binaire
void SPI_MasterTransmit(char cData)
{
  /* Start transmission */
  SPDR = cData;
  /* Wait for transmission complete */
  while
  (!(SPSR & (1<<SPIF)))
  ;
}

void USART_Init( unsigned int ubrr)
{
  /*Set baud rate */
  UBRR0H = (unsigned char)(ubrr>>8);
  UBRR0L = (unsigned char)ubrr;
  /*Enable receiver and transmitter */
  UCSR0B = (1<<RXEN0)|(1<<TXEN0);
  /* Set frame format: 8data, 2stop bit */
  UCSR0C = (1<<USBS0)|(3<<UCSZ00);
}

void USART_Transmit( unsigned char data )
{
/* Wait for empty transmit buffer */
while ( !( UCSR0A & (1<<UDRE0)) );
/* Put data into buffer, sends the data */
UDR0 = data;
}

unsigned char USART_Receive( void )
{
/* Wait for data to be received */
while ( !(UCSR0A & (1<<RXC0)) );
/* Get and return received data from buffer */
return UDR0;
}

void setDac(uint16_t value)
{
  //mettre CS à 0
  PORTB &= ~(1<<PORTB2); //On met le bit DDB2 à 1
  //Le bus lit en 2 octets
  uint8_t octet1, octet2;
  //octet 1 je recupére les 4 bits de poids fort de value : v16 v15 v14 v13 v12 v11 v10 v9
  //v16 v15 v14 v13 v12 v11 v10 v9 v8 v7 v6 v5 v4 v3 v2 v1 => je garde v11 v10 v9 v8
  octet1=(value>>8) & 0xf;
  //(value>>8) : Je décale vers la droite de 8 bits afin de récupérer les bits à gauche
  // & 0xf = 0b1111 = 0 0 0 0 1 1 1 1 : donc je récupère v12 v11 v10 v9
  //octet 1 je recupére les 8 bits de poids faible de value : v8 v7 v6 v5 v4 v3 v2 v1
  octet1 |= (1<<4); //non shutdown : SHDN (shutdown) : on met à 1 car on veut pas que ça soit shutdown
  //0xf = 0b1111 = 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1
  octet2=value & 0xff;

  //Transmettre octet 1
  SPI_MasterTransmit(octet1);
  SPI_MasterTransmit(octet2);

  //Mettre CS à 1
  PORTB |= (1<<PORTB2);

  //LATCH :  Mettre LDac à 0 & Mettre LDac à 1 (on ferme : 0, on attend d'avoir toutes les données, et on met à 1 : on envoie toutes les données d'un coup)
  //Mettre LDac à 0
  PORTD &= ~(1<<PORTD6);

  //mettre LDAC à 1
  PORTD |= (1<<PORTD6);


}
int main(){

  //Mettre CS et lDAC en sortie car on veut les contrôler
  //cs : je mets à 1 la pin DDB2 (correspond à la CS°)
  DDRB |= (1<<DDB2);

  //LDAC : mettre à 1
  DDRD |= (1<<DDD6);
  PORTD |= (1<<PORTD6);
  //Initialiser le SPI
  SPI_MasterInit();

  //Valeur que l'on veut envoyer au DAC
  setDac(1);


    USART_Init(MYUBRR);
    // Active et allume la broche PB5 (led)
    /*DDRB |= _BV(PB5);
    int i;
    for (i=0;i<5;i++){
      //Met le PB5 à 1
      PORTB |=_BV(PB5);
      //Attendre 1 seconde. Attention indiquer la fréquence de notre microcontroleur
      _delay_ms(1000);
      //Met le PB5 à 0
      PORTB &=~_BV(PB5);
      //Attendre 1 seconde. Attention indiquer la fréquence de notre microcontroleur
      _delay_ms(1000);
    }*/

    while(1)
    {
      USART_Transmit(USART_Receive()+1);
    }
}