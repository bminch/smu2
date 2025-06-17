#include "smu_base.h"

uint16_t dac16_dac0, dac16_dac1, dac16_dac2, dac16_dac3;

uint16_t adc18_high, adc18_low;

RINGBUFFER U1TXbuffer, U1RXbuffer;
uint8_t U1TX_buffer[U1TX_BUFFER_LENGTH];
uint8_t U1RX_buffer[U1RX_BUFFER_LENGTH];
uint16_t U1TXthreshold;

void init_smu_base(void) {
    CLKDIV = 0x0100;        // RCDIV = 001 (4MHz, div2),
                            // CPDIV = 00 (FOSC = 32MHz, FCY = 16MHz)

//    OSCTUN = 0x9000;        // enable FRC self tuning with USB host clock
    OSCCONbits.SOSCEN = 1;  // enable secondary oscillator (SOSC)
    OSCTUNbits.STEN = 1;    // enable FRC oscillator self tuning from SOSC

    // Make all pins digital I/Os
    ANSB = 0;
    ANSC = 0;
    ANSD = 0;
    ANSF = 0;
    ANSG = 0;

    ANSBbits.ANSB0 = 1;     // configure RB0 (AN0) for analog function
    TRISBbits.TRISB0 = 1;   // tristate RB0's output driver

    ANSGbits.ANSG9 = 1;     // configure RG9 (DAC1) for analog function
    TRISGbits.TRISG9 = 1;   // tristate RG9's output driver
    DAC1CON = 0x8081;       // enable DAC1, no trigger, and reference is DREF+
    DAC1DAT = 0;

    ANSBbits.ANSB13 = 1;    // configure RB13 (DAC2) for analog function
    TRISBbits.TRISB13 = 1;  // tristate RB13's output driver
    DAC2CON = 0x8081;       // enable DAC2, no trigger, and reference is DREF+
    DAC2DAT = 0;

    // Configure LED pins as outputs, set to high (off)
    LED1 = 1; LED1_DIR = OUT;
    LED2 = 1; LED2_DIR = OUT;
    LED3 = 1; LED3_DIR = OUT;

    // Configure SW pin as inputs
    SW1_DIR = IN;

    // Configure ENA12V pin as an output, set to low (off)
    ENA12V = OFF; ENA12V_DIR = OUT;

    // Configure mode and range pins as outputs, set to low
    RD0_DIR = OUT; RD0_ = 0;
    RD1_DIR = OUT; RD1_ = 0;
    RD2_DIR = OUT; RD2_ = 0;
    RD3_DIR = OUT; RD3_ = 0;
    RD4_DIR = OUT; RD4_ = 0;
    RD5_DIR = OUT; RD5_ = 0;
    RD6_DIR = OUT; RD6_ = 0;

    RE0_DIR = OUT; RE0_ = 0;
    RE1_DIR = OUT; RE1_ = 0;
    RE2_DIR = OUT; RE2_ = 0;
    RE3_DIR = OUT; RE3_ = 0;
    RE4_DIR = OUT; RE4_ = 0;
    RE5_DIR = OUT; RE5_ = 0;
    RE6_DIR = OUT; RE6_ = 0;

    // Configure digital pins to be outputs
    D0_DIR = OUT; D0 = 0;
    D1_DIR = OUT; D1 = 0;
    D2_DIR = OUT; D2 = 0;
    D3_DIR = OUT; D3 = 0;

    // Configure initial PWM frequencies to 1 kHz and duty cycles to 50%
    OC1RS = 15999;
    OC1R = 7999;
    OC1TMR = 0;

    OC2RS = 15999;
    OC2R = 7999;
    OC2TMR = 0;

    OC3RS = 15999;
    OC3R = 7999;
    OC3TMR = 0;

    OC4RS = 15999;
    OC4R = 7999;
    OC4TMR = 0;

    // Configure Timer1 to have a period of 20 ms
    T1CON = 0x0010;
    PR1 = 0x9C3F;

    TMR1 = 0;
    T1CONbits.TON = 1;

    init_dac16();
    init_adc18();
    init_ble();
}

// Functions for interfacing with the quad 16-bit DAC (DAC8564)
void init_dac16(void) {
    uint8_t *RPOR, *RPINR;

    // Configure DAC16 pins and SPI peripheral (SPI1)
    DAC_CSN_DIR = OUT; DAC_CSN = 1;
    DAC_SCK_DIR = OUT; DAC_SCK = 1;
    DAC_MOSI_DIR = OUT; DAC_MOSI = 0;
    DAC_MISO_DIR = IN;

    RPOR = (uint8_t *)&RPOR0;
    RPINR = (uint8_t *)&RPINR0;

    __builtin_write_OSCCONL(OSCCON & 0xBF);
    RPINR[MISO1_RP] = DAC_MISO_RP;
    RPOR[DAC_MOSI_RP] = MOSI1_RP;
    RPOR[DAC_SCK_RP] = SCK1OUT_RP;
    __builtin_write_OSCCONL(OSCCON | 0x40);

    SPI1CON1 = 0x017B;      // SPI1 mode = 2, SCK freq = 2 MHz
    SPI1CON2 = 0;
    SPI1STAT = 0x8000;

    dac16_dac0 = 0;
    dac16_dac1 = 0;
    dac16_dac2 = 0;
    dac16_dac3 = 0;
}

uint16_t dac16_get_dac0(void) {
    return dac16_dac0;
}

void dac16_set_dac0(uint16_t val) {
    uint16_t temp;

    dac16_dac0 = val;

    DAC_CSN = 0;

    // Write to buffer with data and load DAC0
    SPI1BUF = 0b00010000;
    while (SPI1STATbits.SPIRBF == 0) {}
    temp = SPI1BUF;

    // Write high byte of DAC0 value
    SPI1BUF = dac16_dac0 >> 8;
    while (SPI1STATbits.SPIRBF == 0) {}
    temp = SPI1BUF;

    // Write low byte of DAC0 value
    SPI1BUF = dac16_dac0 & 0xFF;
    while (SPI1STATbits.SPIRBF == 0) {}
    temp = SPI1BUF;

    DAC_CSN = 1;
}

uint16_t dac16_get_dac1(void) {
    return dac16_dac1;
}

void dac16_set_dac1(uint16_t val) {
    uint16_t temp;

    dac16_dac1 = val;

    DAC_CSN = 0;

    // Write to buffer with data and load DAC1
    SPI1BUF = 0b00010010;
    while (SPI1STATbits.SPIRBF == 0) {}
    temp = SPI1BUF;

    // Write high byte of DAC1 value
    SPI1BUF = dac16_dac1 >> 8;
    while (SPI1STATbits.SPIRBF == 0) {}
    temp = SPI1BUF;

    // Write low byte of DAC1 value
    SPI1BUF = dac16_dac1 & 0xFF;
    while (SPI1STATbits.SPIRBF == 0) {}
    temp = SPI1BUF;

    DAC_CSN = 1;
}

uint16_t dac16_get_dac2(void) {
    return dac16_dac2;
}

void dac16_set_dac2(uint16_t val) {
    uint16_t temp;

    dac16_dac2 = val;

    DAC_CSN = 0;

    // Write to buffer with data and load DAC2
    SPI1BUF = 0b00010100;
    while (SPI1STATbits.SPIRBF == 0) {}
    temp = SPI1BUF;

    // Write high byte of DAC2 value
    SPI1BUF = dac16_dac2 >> 8;
    while (SPI1STATbits.SPIRBF == 0) {}
    temp = SPI1BUF;

    // Write low byte of DAC2 value
    SPI1BUF = dac16_dac2 & 0xFF;
    while (SPI1STATbits.SPIRBF == 0) {}
    temp = SPI1BUF;

    DAC_CSN = 1;
}

uint16_t dac16_get_dac3(void) {
    return dac16_dac3;
}

void dac16_set_dac3(uint16_t val) {
    uint16_t temp;

    dac16_dac3 = val;

    DAC_CSN = 0;

    // Write to buffer with data and load DAC3
    SPI1BUF = 0b00010110;
    while (SPI1STATbits.SPIRBF == 0) {}
    temp = SPI1BUF;

    // Write high byte of DAC3 value
    SPI1BUF = dac16_dac3 >> 8;
    while (SPI1STATbits.SPIRBF == 0) {}
    temp = SPI1BUF;

    // Write low byte of DAC3 value
    SPI1BUF = dac16_dac3 & 0xFF;
    while (SPI1STATbits.SPIRBF == 0) {}
    temp = SPI1BUF;

    DAC_CSN = 1;
}

void dac16_set_ch1(uint16_t pos, uint16_t neg) {
    uint16_t temp;

    dac16_dac2 = neg;

    DAC_CSN = 0;

    // Write to buffer 2 with data
    SPI1BUF = 0b00000100;
    while (SPI1STATbits.SPIRBF == 0) {}
    temp = SPI1BUF;

    // Write high byte of DAC2 value
    SPI1BUF = dac16_dac2 >> 8;
    while (SPI1STATbits.SPIRBF == 0) {}
    temp = SPI1BUF;

    // Write low byte of DAC2 value
    SPI1BUF = dac16_dac2 & 0xFF;
    while (SPI1STATbits.SPIRBF == 0) {}
    temp = SPI1BUF;

    DAC_CSN = 1;

    dac16_dac3 = pos;

    DAC_CSN = 0;

    // Write to buffer 3 with data and load all DACs simultaneously
    SPI1BUF = 0b00100110;
    while (SPI1STATbits.SPIRBF == 0) {}
    temp = SPI1BUF;

    // Write high byte of DAC3 value
    SPI1BUF = dac16_dac3 >> 8;
    while (SPI1STATbits.SPIRBF == 0) {}
    temp = SPI1BUF;

    // Write low byte of DAC3 value
    SPI1BUF = dac16_dac3 & 0xFF;
    while (SPI1STATbits.SPIRBF == 0) {}
    temp = SPI1BUF;

    DAC_CSN = 1;
}

void dac16_set_ch2(uint16_t pos, uint16_t neg) {
    uint16_t temp;

    dac16_dac0 = neg;

    DAC_CSN = 0;

    // Write to buffer 0 with data
    SPI1BUF = 0b00000000;
    while (SPI1STATbits.SPIRBF == 0) {}
    temp = SPI1BUF;

    // Write high byte of DAC0 value
    SPI1BUF = dac16_dac0 >> 8;
    while (SPI1STATbits.SPIRBF == 0) {}
    temp = SPI1BUF;

    // Write low byte of DAC0 value
    SPI1BUF = dac16_dac0 & 0xFF;
    while (SPI1STATbits.SPIRBF == 0) {}
    temp = SPI1BUF;

    DAC_CSN = 1;

    dac16_dac1 = pos;

    DAC_CSN = 0;

    // Write to buffer 1 with data and load all DACs simultaneously
    SPI1BUF = 0b00100010;
    while (SPI1STATbits.SPIRBF == 0) {}
    temp = SPI1BUF;

    // Write high byte of DAC1 value
    SPI1BUF = dac16_dac1 >> 8;
    while (SPI1STATbits.SPIRBF == 0) {}
    temp = SPI1BUF;

    // Write low byte of DAC1 value
    SPI1BUF = dac16_dac1 & 0xFF;
    while (SPI1STATbits.SPIRBF == 0) {}
    temp = SPI1BUF;

    DAC_CSN = 1;
}

// Functions for interfacing with the 18-bit SAR ADCs (ADS8887)
void init_adc18(void) {
    uint8_t *RPOR, *RPINR;

    // Configure ADC18 pins and Timer2
    ADC_CONVST_DIR = OUT; ADC_CONVST = 0;
    ADC_CSN1_DIR = OUT; ADC_CSN1 = 1;
    ADC_CSN2_DIR = OUT; ADC_CSN2 = 1;
    ADC_SCK_DIR = OUT; ADC_SCK = 0;
    ADC_MOSI_DIR = OUT; ADC_MOSI = 0;
    ADC_MISO_DIR = IN;

    // Configure Timer2 to have a period of 102.25us so 163 cycles is 16.667ms
    T2CON = 0x0000;
    PR2 = 0x0663;
}

int32_t adc18_meas_ch1(void) {
    WORD32 result;

    adc18_high = 0;
    adc18_low = 0;

    disable_interrupts();
    ADC_CONVST = 1;
    __asm__("repeat #139");
    __asm__("nop");
    ADC_CSN1 = 0;
    __asm__("clr W1");
    ADC_SCK = 1;                    // SCK1, D17
    __asm__("mov _PORTF, W0");      // RF4 is ADC_MISO
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK2, D16
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK3, D15
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK4, D14
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK5, D13
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK6, D12
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK7, D11
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK8, D10
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK9, D9
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK10, D8
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK11, D7
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK12, D6
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK13, D5
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK14, D4
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK15, D3
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK16, D2
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("clr W2");
    ADC_SCK = 1;                    // SCK17, D1
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W2");
    __asm__("sl W2, W2");
    ADC_SCK = 1;                    // SCK18, D0
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W2");
    __asm__("sl W2, #14, W2");
    ADC_CSN1 = 1;
    __asm__("mov W1, _adc18_high");
    __asm__("mov W2, _adc18_low");
    ADC_CONVST = 0;
    enable_interrupts();

    result.w[1] = adc18_high;
    result.w[0] = adc18_low;
    return result.l >> 14;
}

int32_t adc18_meas_ch2(void) {
    WORD32 result;

    adc18_high = 0;
    adc18_low = 0;

    disable_interrupts();
    ADC_CONVST = 1;
    __asm__("repeat #139");
    __asm__("nop");
    ADC_CSN2 = 0;
    __asm__("clr W1");
    ADC_SCK = 1;                    // SCK1, D17
    __asm__("mov _PORTF, W0");      // RF4 is ADC_MISO
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK2, D16
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK3, D15
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK4, D14
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK5, D13
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK6, D12
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK7, D11
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK8, D10
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK9, D9
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK10, D8
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK11, D7
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK12, D6
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK13, D5
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK14, D4
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK15, D3
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK16, D2
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("clr W2");
    ADC_SCK = 1;                    // SCK17, D1
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W2");
    __asm__("sl W2, W2");
    ADC_SCK = 1;                    // SCK18, D0
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W2");
    __asm__("sl W2, #14, W2");
    ADC_CSN2 = 1;
    __asm__("mov W1, _adc18_high");
    __asm__("mov W2, _adc18_low");
    ADC_CONVST = 0;
    enable_interrupts();

    result.w[1] = adc18_high;
    result.w[0] = adc18_low;
    return result.l >> 14;
}

void adc18_meas_both(int32_t *ch1val, int32_t *ch2val) {
    WORD32 result;

    adc18_high = 0;
    adc18_low = 0;

    disable_interrupts();
    ADC_CONVST = 1;
    __asm__("repeat #139");
    __asm__("nop");

    ADC_CSN1 = 0;
    __asm__("clr W1");
    ADC_SCK = 1;                    // SCK1, D17
    __asm__("mov _PORTF, W0");      // RF4 is ADC_MISO
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK2, D16
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK3, D15
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK4, D14
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK5, D13
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK6, D12
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK7, D11
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK8, D10
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK9, D9
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK10, D8
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK11, D7
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK12, D6
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK13, D5
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK14, D4
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK15, D3
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK16, D2
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("clr W2");
    ADC_SCK = 1;                    // SCK17, D1
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W2");
    __asm__("sl W2, W2");
    ADC_SCK = 1;                    // SCK18, D0
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W2");
    __asm__("sl W2, #14, W2");
    ADC_CSN1 = 1;

    __asm__("mov W1, _adc18_high");
    __asm__("mov W2, _adc18_low");
    result.w[1] = adc18_high;
    result.w[0] = adc18_low;
    *ch1val = result.l >> 14;
    adc18_high = 0;
    adc18_low = 0;

    ADC_CSN2 = 0;
    __asm__("clr W1");
    ADC_SCK = 1;                    // SCK1, D17
    __asm__("mov _PORTF, W0");      // RF4 is ADC_MISO
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK2, D16
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK3, D15
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK4, D14
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK5, D13
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK6, D12
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK7, D11
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK8, D10
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK9, D9
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK10, D8
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK11, D7
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK12, D6
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK13, D5
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK14, D4
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK15, D3
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("sl W1, W1");
    ADC_SCK = 1;                    // SCK16, D2
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W1");
    __asm__("clr W2");
    ADC_SCK = 1;                    // SCK17, D1
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W2");
    __asm__("sl W2, W2");
    ADC_SCK = 1;                    // SCK18, D0
    __asm__("mov _PORTF, W0");
    __asm__("btst.c W0, #4");
    ADC_SCK = 0;
    __asm__("addc #0, W2");
    __asm__("sl W2, #14, W2");
    ADC_CSN2 = 1;

    __asm__("mov W1, _adc18_high");
    __asm__("mov W2, _adc18_low");
    result.w[1] = adc18_high;
    result.w[0] = adc18_low;
    *ch2val = result.l >> 14;

    ADC_CONVST = 0;
    enable_interrupts();
}

int32_t adc18_meas_ch1_avg(void) {
    int32_t avg_result;
    uint16_t i;

    // Lower Timer2 interrupt flag and start Timer2
    IFS0bits.T2IF = 0;
    TMR2 = 0;
    T2CONbits.TON = 1;

    avg_result = 0;
    for (i = 163; i > 0; i--) {
        avg_result += adc18_meas_ch1();

        while (IFS0bits.T2IF == 0) {}
        IFS0bits.T2IF = 0;
    }

    // Stop Timer2
    T2CONbits.TON = 0;

    return avg_result / 163;
}

int32_t adc18_meas_ch2_avg(void) {
    int32_t avg_result;
    uint16_t i;

    // Lower Timer2 interrupt flag and start Timer2
    IFS0bits.T2IF = 0;
    TMR2 = 0;
    T2CONbits.TON = 1;

    avg_result = 0;
    for (i = 163; i > 0; i--) {
        avg_result += adc18_meas_ch2();

        while (IFS0bits.T2IF == 0) {}
        IFS0bits.T2IF = 0;
    }

    // Stop Timer2
    T2CONbits.TON = 0;

    return avg_result / 163;
}

void adc18_meas_both_avg(int32_t *ch1val, int32_t *ch2val) {
    int32_t val1, val2;
    uint16_t i;

    // Lower Timer2 interrupt flag and start Timer2
    IFS0bits.T2IF = 0;
    TMR2 = 0;
    T2CONbits.TON = 1;

    *ch1val = 0;
    *ch2val = 0;
    for (i = 163; i > 0; i--) {
        adc18_meas_both(&val1, &val2);
        *ch1val += val1;
        *ch2val += val2;

        while (IFS0bits.T2IF == 0) {}
        IFS0bits.T2IF = 0;
    }

    // Stop Timer2
    T2CONbits.TON = 0;

    *ch1val = (*ch1val) / 163;
    *ch2val = (*ch2val) / 163;
}

// Functions relating to the BLE module (RN4871)
void init_ble(void) {
    uint8_t *RPOR, *RPINR;
    uint16_t i;

    RPOR = (uint8_t *)&RPOR0;
    RPINR = (uint8_t *)&RPINR0;

    // Configure BLE module pins
    BLE_RST_N_DIR = OUT; BLE_RST_N = 1;
    BLE_RX_DIR = OUT; BLE_RX = 1;
    BLE_TX_DIR = IN;
    BLE_CTS_DIR = OUT; BLE_CTS = 1;
    BLE_RTS_DIR = IN;

    // Configure BLE pins to use UART1
    __builtin_write_OSCCONL(OSCCON & 0xBF);
    RPINR[U1RX_RP] = BLE_TX_RP;
    RPOR[BLE_RX_RP] = U1TX_RP;
    RPINR[U1CTS_RP] = BLE_RTS_RP;
    RPOR[BLE_CTS_RP] = U1RTS_RP;
    __builtin_write_OSCCONL(OSCCON | 0x40);

#ifdef NO_FLOW_CONTROL
    U1MODE = 0x0008;            // configure UART1 for transmission at
    U1BRG = 0x0022;             //   115,200 baud, no parity, 1 stop bit
#else
    U1MODE = 0x0208;            // configure UART1 for transmission at
    U1BRG = 0x0022;             //   115,200 baud, no parity, 1 stop bit
                                //   with hardware flow control
#endif

    U1TXbuffer.data = U1TX_buffer;
    U1TXbuffer.length = U1TX_BUFFER_LENGTH;
    U1TXbuffer.head = 0;
    U1TXbuffer.tail = 0;
    U1TXbuffer.count = 0;
    U1TXthreshold = 3 * U1TX_BUFFER_LENGTH / 4;

    U1RXbuffer.data = U1RX_buffer;
    U1RXbuffer.length = U1RX_BUFFER_LENGTH;
    U1RXbuffer.head = 0;
    U1RXbuffer.tail = 0;
    U1RXbuffer.count = 0;

    U1STAbits.UTXISEL1 = 0;     // set UART1 UTXISEL<1:0> = 01, TX interrupt
    U1STAbits.UTXISEL0 = 1;     //   when all transmit operations are done

    IFS0bits.U1TXIF = 0;        // lower UART1 TX interrupt flag
    IEC0bits.U1TXIE = 1;        // enable UART1 TX interrupt

    IFS0bits.U1RXIF = 0;        // lower UART1 RX interrupt flag
    IEC0bits.U1RXIE = 1;        // enable UART1 RX interrupt

    U1MODEbits.UARTEN = 1;      // enable UART1 module
    U1STAbits.UTXEN = 1;        // enable UART1 data transmission

    BLE_RST_N = 0;
    for (i = 1000; i; i--) {}
    BLE_RST_N = 1;
}

uint16_t ble_in_waiting(void) {
    return U1inWaiting();
}

void ble_putc(uint8_t ch) {
    U1putc(ch);
    U1flushTxBuffer();
}

uint8_t ble_getc(void) {
    return U1getc();
}

void ble_puts(uint8_t *str) {
    U1puts(str);
    U1flushTxBuffer();
}

uint16_t dummy_in_waiting(void) {
    return 0;
}

void dummy_putc(uint8_t ch) {
    // Do nothing...
}

uint8_t dummy_getc(void) {
    return 0;
}

void dummy_puts(uint8_t *str) {
    // Do nothing...
}

void __attribute__((interrupt, auto_psv)) _U1TXInterrupt(void) {
    uint8_t ch;

    IFS0bits.U1TXIF = 0;            // lower UART1 TX interrupt flag

    if (U1TXbuffer.count == 0)      // if nothing left in UART1 TX buffer, 
        U1STAbits.UTXEN = 0;        //   disable data transmission

    while ((U1STAbits.UTXBF == 0) && (U1TXbuffer.count != 0)) {
        disable_interrupts();
        ch = U1TXbuffer.data[U1TXbuffer.head];
        U1TXbuffer.head++;
        if (U1TXbuffer.head == U1TXbuffer.length)
            U1TXbuffer.head = 0;
        U1TXbuffer.count--;
        enable_interrupts();
        U1TXREG = (uint16_t)ch;
    }
}

void __attribute__((interrupt, auto_psv)) _U1RXInterrupt(void) {
    IFS0bits.U1RXIF = 0;            // lower UART1 RX interrupt flag

    while ((U1STAbits.URXDA == 1) && (U1RXbuffer.count != U1RXbuffer.length)) {
        disable_interrupts();
        U1RXbuffer.data[U1RXbuffer.tail] = (uint8_t)U1RXREG;
        U1RXbuffer.tail++;
        if (U1RXbuffer.tail == U1RXbuffer.length)
            U1RXbuffer.tail = 0;
        U1RXbuffer.count++;
        enable_interrupts();
    }
}

uint16_t U1inWaiting(void) {
    return U1RXbuffer.count;
}

void U1flushTxBuffer(void) {
    if (U1STAbits.UTXEN == 0)       // if UART1 transmission is disabled,
        U1STAbits.UTXEN = 1;        //   enable it
}

void U1putc(uint8_t ch) {
    while (U1TXbuffer.count == U1TXbuffer.length) {}    // wait until UART1 TX 
                                                        //   buffer is not full
    disable_interrupts();
    U1TXbuffer.data[U1TXbuffer.tail] = ch;
    U1TXbuffer.tail++;
    if (U1TXbuffer.tail == U1TXbuffer.length)
        U1TXbuffer.tail = 0;
    U1TXbuffer.count++;
    enable_interrupts();

    if (U1TXbuffer.count >= U1TXthreshold)          // if UART1 TX buffer is 
        U1STAbits.UTXEN = 1;                        //   full enough, enable 
                                                    //   data transmission
}

uint8_t U1getc(void) {
    uint8_t ch;

    while (U1RXbuffer.count == 0) {}    // wait until UART1 RX buffer is not empty

    disable_interrupts();
    ch = U1RXbuffer.data[U1RXbuffer.head];
    U1RXbuffer.head++;
    if (U1RXbuffer.head == U1RXbuffer.length)
        U1RXbuffer.head = 0;
    U1RXbuffer.count--;
    enable_interrupts();

    return ch;
}

void U1puts(uint8_t *str) {
    while (*str)
        U1putc(*str++);
    U1flushTxBuffer();
}

void U1gets(uint8_t *str, uint16_t len) {
    if (len == 0)
        return;

    if (len == 1) {
        *str = '\0';
        return;
    }

    while (1) {
        *str = U1getc();
        if ((*str == '\r') || (len == 1))
            break;
        str++;
        len--;
    }
    *str = '\0';
}

void U1gets_term(uint8_t *str, uint16_t len) {
    uint8_t *start;
    uint16_t left;

    if (len == 0)
        return;

    if (len == 1) {
        *str = '\0';
        return;
    }

    U1putc(0x1B);                           // save current cursor position
    U1putc('7');
    U1flushTxBuffer();
    start = str;
    left = len;
    while (1) {
        *str = U1getc();                    // get a character
        if (*str == '\r')                   // if character is return,
            break;                          //   end the loop
        if (*str == 0x1B) {                 // if character is escape,
            U1putc(0x1B);                   //   restore cursor position,
            U1putc('8');
            U1putc(0x1B);                   //   clear to end of line, and
            U1putc('[');
            U1putc('K');
            U1flushTxBuffer();
            str = start;                    //   start over at the beginning
            left = len;
            continue;
        }
        if ((*str == '\b') ||               // if character is backspace
            (*str == 0x7F)) {               //   or delete, 
            if (str > start) {              //   and we are not at the start, 
                U1putc('\b');               //   erase the last character and
                U1putc(' ');
                U1putc('\b');
                U1flushTxBuffer();
                str--;                      //   back up the pointer,
                left++;
            } else {                        //   otherwise
                U1putc('\a');               //   send alert/bell character
                U1flushTxBuffer();
            }
            continue;
        }
        if (left == 1) {                    // if string buffer is full,
            U1putc('\a');                   //   send alert/bell character
            U1flushTxBuffer();
            continue;
        }
        if ((*str >= 32) && (*str < 127)) { // if character is printable,
            U1putc(*str);                   //   echo the received character
            U1flushTxBuffer();
            str++;                          //   and advance the pointer
            left--;
        }
    }
    *str = '\0';                            // terminarte the string with null
    U1putc('\n');                           // send newline and
    U1putc('\r');                           //   carriage return
    U1flushTxBuffer();
}
