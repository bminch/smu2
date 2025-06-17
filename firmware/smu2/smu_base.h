#ifndef _SMUBASE_H_
#define _SMUBASE_H_

#include "pic24fj.h"
#include "common.h"
#include <stdint.h>

#define NO_FLOW_CONTROL

// LED pin definitions
#define LED1                LATDbits.LATD7
#define LED2                LATFbits.LATF0
#define LED3                LATFbits.LATF1

#define LED1_DIR            TRISDbits.TRISD7
#define LED2_DIR            TRISFbits.TRISF0
#define LED3_DIR            TRISFbits.TRISF1

// Tactile switch pin definitions
#define SW1                 PORTCbits.RC15
#define SW1_DIR             TRISCbits.TRISC15

// Power supply pin definitions
#define ENA12V              LATCbits.LATC12
#define ENA12V_DIR          TRISCbits.TRISC12

// Digital header pin definitions
#define D0                  PORTGbits.RG7
#define D1                  PORTBbits.RB4
#define D2                  PORTBbits.RB6
#define D3                  PORTBbits.RB7

#define D0_DIR              TRISGbits.TRISG7
#define D1_DIR              TRISBbits.TRISB4
#define D2_DIR              TRISBbits.TRISB6
#define D3_DIR              TRISBbits.TRISB7

#define D0_LAT              LATGbits.LATG7
#define D1_LAT              LATBbits.LATB4
#define D2_LAT              LATBbits.LATB6
#define D3_LAT              LATBbits.LATB7

#define D0_RP               26
#define D1_RP               28
#define D2_RP               6
#define D3_RP               7

#define D0_OD               ODCGbits.ODG7
#define D1_OD               ODCBbits.ODB4
#define D2_OD               ODCBbits.ODB6
#define D3_OD               ODCBbits.ODB7

#define D0_PU               CNPU1bits.CN9PUE
#define D1_PU               CNPU1bits.CN6PUE
#define D2_PU               CNPU2bits.CN24PUE
#define D3_PU               CNPU2bits.CN25PUE

#define D0_PD               CNPD1bits.CN9PDE
#define D1_PD               CNPD1bits.CN6PDE
#define D2_PD               CNPD2bits.CN24PDE
#define D3_PD               CNPD2bits.CN25PDE

// Channel mode and range selection signal pin definitions
#define RD0_                LATDbits.LATD0
#define RD1_                LATDbits.LATD1
#define RD2_                LATDbits.LATD2
#define RD3_                LATDbits.LATD3
#define RD4_                LATDbits.LATD4
#define RD5_                LATDbits.LATD5
#define RD6_                LATDbits.LATD6
#define RE0_                LATEbits.LATE0
#define RE1_                LATEbits.LATE1
#define RE2_                LATEbits.LATE2
#define RE3_                LATEbits.LATE3
#define RE4_                LATEbits.LATE4
#define RE5_                LATEbits.LATE5
#define RE6_                LATEbits.LATE6

#define RD0_DIR             TRISDbits.TRISD0
#define RD1_DIR             TRISDbits.TRISD1
#define RD2_DIR             TRISDbits.TRISD2
#define RD3_DIR             TRISDbits.TRISD3
#define RD4_DIR             TRISDbits.TRISD4
#define RD5_DIR             TRISDbits.TRISD5
#define RD6_DIR             TRISDbits.TRISD6
#define RE0_DIR             TRISEbits.TRISE0
#define RE1_DIR             TRISEbits.TRISE1
#define RE2_DIR             TRISEbits.TRISE2
#define RE3_DIR             TRISEbits.TRISE3
#define RE4_DIR             TRISEbits.TRISE4
#define RE5_DIR             TRISEbits.TRISE5
#define RE6_DIR             TRISEbits.TRISE6

// DAC16 (DAC8565) pin definitions
#define DAC_CSN             LATDbits.LATD8
#define DAC_SCK             LATDbits.LATD11
#define DAC_MOSI            LATDbits.LATD10
#define DAC_MISO            PORTDbits.RD9

#define DAC_CSN_DIR         TRISDbits.TRISD8
#define DAC_SCK_DIR         TRISDbits.TRISD11
#define DAC_MOSI_DIR        TRISDbits.TRISD10
#define DAC_MISO_DIR        TRISDbits.TRISD9

#define DAC_CSN_RP          2
#define DAC_SCK_RP          12
#define DAC_MOSI_RP         3
#define DAC_MISO_RP         4

// ADC18 (ADS8887) pin definitions
#define ADC_CONVST          LATGbits.LATG8
#define ADC_CSN1            LATFbits.LATF5
#define ADC_CSN2            LATFbits.LATF3
#define ADC_SCK             PORTBbits.RB15
#define ADC_MISO            PORTFbits.RF4
#define ADC_MOSI            PORTBbits.RB14

#define ADC_CONVST_DIR      TRISGbits.TRISG8
#define ADC_CSN1_DIR        TRISFbits.TRISF5
#define ADC_CSN2_DIR        TRISFbits.TRISF3
#define ADC_SCK_DIR         TRISBbits.TRISB15
#define ADC_MISO_DIR        TRISFbits.TRISF4
#define ADC_MOSI_DIR        TRISBbits.TRISB14

#define ADC_CONVST_RP       19
#define ADC_CSN1_RP         17
#define ADC_CSN2_RP         16
#define ADC_SCK_RP          29
#define ADC_MISO_RP         10
#define ADC_MOSI_RP         14

// BLE module (RN4871) pin definitions
#define BLE_RX_IND          LATBbits.LATB12
#define BLE_RST_N           LATEbits.LATE7
#define BLE_RX              PORTBbits.RB1
#define BLE_TX              PORTBbits.RB2
#define BLE_RTS             PORTBbits.RB5
#define BLE_CTS             PORTGbits.RG6

#define BLE_RX_IND_DIR      TRISBbits.TRISB12
#define BLE_RST_N_DIR       TRISEbits.TRISE7
#define BLE_RX_DIR          TRISBbits.TRISB1
#define BLE_TX_DIR          TRISBbits.TRISB2
#define BLE_RTS_DIR         TRISBbits.TRISB5
#define BLE_CTS_DIR         TRISGbits.TRISG6

#define BLE_RX_RP           1
#define BLE_TX_RP           13
#define BLE_RTS_RP          18
#define BLE_CTS_RP          21

// Peripheral remappable pin definitions
#define INT1_RP             1
#define INT2_RP             2
#define INT3_RP             3
#define INT4_RP             4

#define MOSI1_RP            7
#define SCK1OUT_RP          8
#define MOSI2_RP            10
#define SCK2OUT_RP          11

#define MISO1_RP            40
#define SCK1IN_RP           41
#define MISO2_RP            44
#define SCK2IN_RP           45

#define OC1_RP              18
#define OC2_RP              19
#define OC3_RP              20
#define OC4_RP              21
#define OC5_RP              22
#define OC6_RP              23
#define OC7_RP              24
#define OC8_RP              25
#define OC9_RP              35

#define U1TX_RP             3
#define U1RTS_RP            4
#define U2TX_RP             5
#define U2RTS_RP            6
#define U3TX_RP             28
#define U3RTS_RP            29
#define U4TX_RP             30
#define U4RTS_RP            31

#define U1RX_RP             36
#define U1CTS_RP            37
#define U2RX_RP             38
#define U2CTS_RP            39
#define U3RX_RP             35
#define U3CTS_RP            43
#define U4RX_RP             54
#define U4CTS_RP            55

// Convenience boolean values definitions
#define FALSE               0
#define TRUE                1

#define OFF                 0
#define ON                  1

#define OUT                 0
#define IN                  1

#define U1TX_BUFFER_LENGTH  1024
#define U1RX_BUFFER_LENGTH  1024

typedef struct {
    uint8_t *data;
    uint16_t length;
    uint16_t head;
    uint16_t tail;
    uint16_t count;
} RINGBUFFER;

extern RINGBUFFER U1TXbuffer, U1RXbuffer;
extern uint8_t U1TX_buffer[];
extern uint8_t U1RX_buffer[];
extern uint16_t U1TXthreshold;

void init_smu_base(void);

void init_dac16(void);
uint16_t dac16_get_dac0(void);
void dac16_set_dac0(uint16_t val);
uint16_t dac16_get_dac1(void);
void dac16_set_dac1(uint16_t val);
uint16_t dac16_get_dac2(void);
void dac16_set_dac2(uint16_t val);
uint16_t dac16_get_dac3(void);
void dac16_set_dac3(uint16_t val);
void dac16_set_ch1(uint16_t pos, uint16_t neg);
void dac16_set_ch2(uint16_t pos, uint16_t neg);

void init_adc18(void);
int32_t adc18_meas_ch1(void);
int32_t adc18_meas_ch2(void);
void adc18_meas_both(int32_t *ch1val, int32_t *ch2val);
int32_t adc18_meas_ch1_avg(void);
int32_t adc18_meas_ch2_avg(void);
void adc18_meas_both_avg(int32_t *ch1val, int32_t *ch2val);

void init_ble(void);
uint16_t ble_in_waiting(void);
void ble_putc(uint8_t ch);
uint8_t ble_getc(void);
void ble_puts(uint8_t *str);

uint16_t dummy_in_waiting(void);
void dummy_putc(uint8_t ch);
uint8_t dummy_getc(void);
void dummy_puts(uint8_t *str);

uint16_t U1inWaiting(void);
void U1flushTxBuffer(void);
void U1putc(uint8_t ch);
uint8_t U1getc(void);
void U1puts(uint8_t *str);
void U1gets(uint8_t *str, uint16_t len);
void U1gets_term(uint8_t *str, uint16_t len);

#endif

