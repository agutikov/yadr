
/*
	A6 - pwm tim3
	A7 - pwm tim3

	A9 - usart1 tx
	A10 - usart1 rx

	B0 - pwm tim3

	C8 - blue led
	C9 - green led

	C0, C1 - adc for pressure sensor

 */

#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <limits.h>
#include <stdio.h>

#include "stm32f10x_rcc.h"
#include "stm32f10x_tim.h"
#include "stm32f10x_adc.h"

#include "usart.h"

#define DBG_TERM 0
/*
 * Convert a string to a long integer.
 *
 * Ignores `locale' stuff. Assumes that the upper and lower case
 * alphabets and digits are each contiguous.
 */
long strtol (const char *nptr, char **endptr, int base)
{
	const char *s = nptr;
	unsigned long acc;
	unsigned char c;
	unsigned long cutoff;
	int neg = 0, any, cutlim;

	/*
	* Skip white space and pick up leading +/- sign if any.
	* If base is 0, allow 0x for hex and 0 for octal, else
	* assume decimal; if base is already 16, allow 0x.
	*/

	do {
		c = *s++;
	} while (isspace(c));

	if (c == '-') {
		neg = 1;
		c = *s++;
	} else if (c == '+')
		c = *s++;


	if ((base == 0 || base == 16) &&
			c == '0' && (*s == 'x' || *s == 'X')) {
		c = s[1];
		s += 2;
		base = 16;
	}

	if (base == 0)
		base = c == '0' ? 8 : 10;

	/*
	* Compute the cutoff value between legal numbers and illegal
	* numbers. That is the largest legal value, divided by the
	* base. An input number that is greater than this value, if
	* followed by a legal input character, is too big. One that
	* is equal to this value may be valid or not; the limit
	* between valid and invalid numbers is then based on the last
	* digit. For instance, if the range for longs is
	* [-2147483648..2147483647] and the input base is 10,
	* cutoff will be set to 214748364 and cutlim to either
	* 7 (neg==0) or 8 (neg==1), meaning that if we have accumulated
	* a value > 214748364, or equal but the next digit is > 7 (or 8),
	* the number is too big, and we will return a range error.
	*
	* Set any if any `digits' consumed; make it negative to indicate
	* overflow.
	*/

	cutoff = neg ? -(unsigned long)LONG_MIN : LONG_MAX;
	cutlim = cutoff % (unsigned long)base;
	cutoff /= (unsigned long)base;

	for (acc = 0, any = 0;; c = *s++) {

		if (!isascii(c))
			break;
		if (isdigit(c))
			c -= '0';
		else if (isalpha(c))
			c -= isupper(c) ? 'A' - 10 : 'a' - 10;
		else
			break;

		if (c >= base)
			break;

		if (any < 0 || acc > cutoff || (acc == cutoff && c > cutlim))
			any = -1;
		else {
			any = 1;
			acc *= base;
			acc += c;
		}
	}

	if (any < 0) {
		acc = neg ? LONG_MIN : LONG_MAX;
	} else if (neg)
		acc = -acc;

	if (endptr != 0)
		*((const char **)endptr) = any ? s - 1 : nptr;

	return (acc);
}

int i2str (char* b, int i, int base, int field)
{
	char const digit[] = "0123456789ABCDEF";
	int len = 0;

	if (base == 0)
		base = 10;

	if (i < 0) {
		*b++ = '-';
		len++;
		i = -i;
	}

	int shifter = i;

	do { // Move to where representation ends
		++b;
		len++;
		shifter = shifter/base;
	} while (shifter);

	int f = field - len;

	if (f > 0) {
		b += f;
		len += f;
	}

	*b = '\0';

	do { // Move back, inserting digits as u go
		*--b = digit[i%base];
		i = i/base;
	} while (i);

	if (f > 0) {
		while (--f)
			*--b = '0';
	}
	*--b = '0';

	return len;
}

char tmp_num_str_buffer[32];
const char* numstr (int a) {
	i2str(tmp_num_str_buffer, a, 10, 0);
	return tmp_num_str_buffer;
}
const char* hexstr (int a) {
	i2str(tmp_num_str_buffer, a, 16, 2);
	return tmp_num_str_buffer;
}

#define USART_NUMBER 3
#define USART_BUFF_SIZE	512

uint8_t usart_buffers[2][USART_BUFF_SIZE];
usart_t usart_device;
usart_config_t usart_config =
	{
//		.AHB_clocks = RCC_AHBPeriph_DMA1,
		.APB1_clocks = 0,
		.APB2_clocks = RCC_APB2Periph_GPIOA | RCC_APB2Periph_USART1,

		.usart_gpio_port = GPIOA,
		.usart_gpio_tx_line = GPIO_Pin_9,
		.usart_gpio_rx_line = GPIO_Pin_10,

		.usart_regs = USART1,
		.usart_irqn = USART1_IRQn,

//		.dma_channel_regs = DMA1_Channel1,
//		.dma_irqn = DMA1_Channel1_IRQn,
//		.dma_channel_idx = 1
	};

usart_t* usart_1 = &usart_device;

void printstr (const char* str)
{
	term_putstr(usart_1, str);
}
void printnum (int i, int base)
{
	char buffer[32];
	i2str(buffer, i, base, 0);
	printstr(buffer);
}

void usart1_isr (void)
{
	usart_isr(&usart_device);
}
void usart1_tx_dma_isr(void)
{
	usart_handle_tx_dma_irq(&usart_device);
}


#define LED_NUMBER  2

uint32_t leds[LED_NUMBER][2] = {
		{(uint32_t)GPIOC, GPIO_Pin_9},
		{(uint32_t)GPIOC, GPIO_Pin_8},
};
void leds_init (void)
{
	GPIO_InitTypeDef GPIO_InitStructure;

	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOC, ENABLE);

	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_9 | GPIO_Pin_8;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;
	GPIO_Init(GPIOC, &GPIO_InitStructure);
}
void led_on (int led)
{
	if (led < LED_NUMBER)
		GPIO_WriteBit((GPIO_TypeDef *)leds[led][0], leds[led][1], 1);
}
void led_off (int led)
{
	if (led < LED_NUMBER)
		GPIO_WriteBit((GPIO_TypeDef *)leds[led][0], leds[led][1], 0);
}
void led_num (int n)
{
	for (int i = 0; i < LED_NUMBER; i++) {
		if (n & (1 << i))
			GPIO_WriteBit((GPIO_TypeDef *)leds[i][0], leds[i][1], 1);
		else
			GPIO_WriteBit((GPIO_TypeDef *)leds[i][0], leds[i][1], 0);
	}
}

void wait (uint32_t xz)
{
	for(uint32_t i = 0; i < xz*1000; i++)
		__ASM volatile ("nop");
}

void panic (int delay)
{
	while(1) {
		led_num(1);
		wait(delay);
		led_num(2);
		wait(delay);
	}
}

typedef struct delta_model {
	uint8_t pwm_enabled[3];
	uint16_t pwm_duty[3];
} delta_model_t;

delta_model_t delta = {
		.pwm_enabled = {1, 1, 1},
		.pwm_duty = {1400, 1400, 1400}
};

void servo_pwm_timer_init (void)
{
	RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM3, ENABLE);

	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA | RCC_APB2Periph_GPIOB |
						 RCC_APB2Periph_GPIOC | RCC_APB2Periph_AFIO, ENABLE);


	GPIO_InitTypeDef GPIO_InitStructure;

	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_6 | GPIO_Pin_7;
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;

	GPIO_Init(GPIOA, &GPIO_InitStructure);

	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_0;
	GPIO_Init(GPIOB, &GPIO_InitStructure);


	/*
		For servo we need 50 Hz output freq. and about 2% - 20% duty cycle.
		20 ms - period, high value 0.9 - 2.5 ms

		TIM3 Configuration: generate 3 PWM signals with 3 different duty cycles:
		The TIM3CLK frequency is set to SystemCoreClock (Hz), to get TIM3 counter
		clock at 1 MHz the Prescaler is computed as following:
		 - Prescaler = (TIM3CLK / TIM3 counter clock) - 1
		SystemCoreClock is set to 72 MHz for Low-density, Medium-density, High-density
		and Connectivity line devices and to 24 MHz for Low-Density Value line and
		Medium-Density Value line devices

		The TIM3 is running at 50 Hz: TIM3 Frequency = TIM3 counter clock/(ARR + 1)
													  = 1 MHz / 20000 = 50 Hz
		TIM3 Channel1 duty cycle = (TIM3_CCR1/ TIM3_ARR) * 20 ms
	*/

	TIM_TimeBaseInitTypeDef  TIM_TimeBaseStructure;
	TIM_OCInitTypeDef  TIM_OCInitStructure;
	uint16_t PrescalerValue = (SystemCoreClock / 1000000) - 1;
	/* Time base configuration */
	TIM_TimeBaseStructure.TIM_Period = 20000;
	TIM_TimeBaseStructure.TIM_Prescaler = PrescalerValue;
	TIM_TimeBaseStructure.TIM_ClockDivision = 0;
	TIM_TimeBaseStructure.TIM_CounterMode = TIM_CounterMode_Up;
	TIM_TimeBaseInit(TIM3, &TIM_TimeBaseStructure);

	/* All channels disabled at start - each will be enabled from commands. */

	/* Channel1 */
	TIM_OCInitStructure.TIM_OCMode = TIM_OCMode_PWM1;
	TIM_OCInitStructure.TIM_OutputState = TIM_OutputState_Disable;
	TIM_OCInitStructure.TIM_Pulse = delta.pwm_duty[0];
	TIM_OCInitStructure.TIM_OCPolarity = TIM_OCPolarity_High;
	TIM_OC1Init(TIM3, &TIM_OCInitStructure);
	TIM_OC1PreloadConfig(TIM3, TIM_OCPreload_Enable);

	/* Channel2 */
	TIM_OCInitStructure.TIM_OCMode = TIM_OCMode_PWM1;
	TIM_OCInitStructure.TIM_OutputState = TIM_OutputState_Disable;
	TIM_OCInitStructure.TIM_Pulse = delta.pwm_duty[1];
	TIM_OCInitStructure.TIM_OCPolarity = TIM_OCPolarity_High;
	TIM_OC2Init(TIM3, &TIM_OCInitStructure);
	TIM_OC2PreloadConfig(TIM3, TIM_OCPreload_Enable);

	/* Channel3 */
	TIM_OCInitStructure.TIM_OCMode = TIM_OCMode_PWM1;
	TIM_OCInitStructure.TIM_OutputState = TIM_OutputState_Disable;
	TIM_OCInitStructure.TIM_Pulse = delta.pwm_duty[2];
	TIM_OCInitStructure.TIM_OCPolarity = TIM_OCPolarity_High;
	TIM_OC3Init(TIM3, &TIM_OCInitStructure);
	TIM_OC3PreloadConfig(TIM3, TIM_OCPreload_Enable);


	TIM_ARRPreloadConfig(TIM3, ENABLE);
	/* TIM3 enable counter */
	TIM_Cmd(TIM3, ENABLE);
}

void servo_switch_pwm (int servo_id, int enable_state)
{
	if (enable_state)
		TIM3->CCER |= TIM_CCER_CC1E << (servo_id * 4);
	else
		TIM3->CCER &= ~(TIM_CCER_CC1E << (servo_id * 4));
}

void servo_switch_all_pwm (int enable_1, int enable_2, int enable_3)
{
	uint32_t mask = TIM3->CCER;
	mask &= ~(TIM_CCER_CC1E | TIM_CCER_CC2E | TIM_CCER_CC3E);
	mask |= enable_1 ? TIM_CCER_CC1E : 0;
	mask |= enable_2 ? TIM_CCER_CC2E : 0;
	mask |= enable_3 ? TIM_CCER_CC3E : 0;
	TIM3->CCER = mask;
}

void servo_set_pwm_duty (int servo_id, uint16_t duty_us)
{
	switch (servo_id) {
	case 0:
		TIM_SetCompare1(TIM3, duty_us);
		break;
	case 1:
		TIM_SetCompare2(TIM3, duty_us);
		break;
	case 2:
		TIM_SetCompare3(TIM3, duty_us);
		break;
	}
}

void servo_set_all_pwm_duty (uint16_t duty1_us, uint16_t duty2_us, uint16_t duty3_us)
{
	TIM_SetCompare1(TIM3, duty1_us);
	TIM_SetCompare2(TIM3, duty2_us);
	TIM_SetCompare3(TIM3, duty3_us);
}

void servo_sync_pwm (void)
{
	// first - disable
	for (int i = 0; i < 3; i++) {
		if (!delta.pwm_enabled[i])
			servo_switch_pwm(i, 0);
	}

	// next - set new duty
	servo_set_all_pwm_duty(delta.pwm_duty[0], delta.pwm_duty[1], delta.pwm_duty[2]);

	// last - enable
	for (int i = 0; i < 3; i++) {
		if (delta.pwm_enabled[i])
			servo_switch_pwm(i, 1);
	}
}



void adc_init (void)
{
	GPIO_InitTypeDef GPIO_InitStructure;

	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_1;
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AIN;
	GPIO_Init(GPIOC, &GPIO_InitStructure);
	// power for light sensor
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_0;
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;
	GPIO_Init(GPIOC, &GPIO_InitStructure);
	GPIO_WriteBit(GPIOC, GPIO_Pin_0, 1);

	RCC_ADCCLKConfig(RCC_PCLK2_Div8);
	/* Enable ADC1 clock so that we can talk to it */
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_ADC1, ENABLE);

	/* Put everything back to power-on defaults */
	ADC_DeInit(ADC1);

	ADC_InitTypeDef  ADC_InitStructure;
    ADC_StructInit(&ADC_InitStructure);
	/* ADC1 and ADC2 operate independently */
	ADC_InitStructure.ADC_Mode = ADC_Mode_Independent;
	/* Disable the scan conversion so we do one at a time */
	ADC_InitStructure.ADC_ScanConvMode = DISABLE;
	/* Don't do continuous conversions - do them on demand */
	ADC_InitStructure.ADC_ContinuousConvMode = DISABLE;
	/* Start conversin by software, not an external trigger */
	ADC_InitStructure.ADC_ExternalTrigConv = ADC_ExternalTrigConv_None;
	/* Conversions are 12 bit - put them in the lower 12 bits of the result */
	ADC_InitStructure.ADC_DataAlign = ADC_DataAlign_Right;
	/* Say how many channels would be used by the sequencer */
	ADC_InitStructure.ADC_NbrOfChannel = 2;
	/* Now do the setup */
	ADC_Init(ADC1, &ADC_InitStructure);

	/* Enable ADC1 */
	ADC_Cmd(ADC1, ENABLE);

	/* Enable ADC1 reset calibration register */
	ADC_ResetCalibration(ADC1);
	/* Check the end of ADC1 reset calibration register */
	while (ADC_GetResetCalibrationStatus(ADC1))
	{}
	/* Start ADC1 calibaration */
	ADC_StartCalibration(ADC1);
	/* Check the end of ADC1 calibration */
	while (ADC_GetCalibrationStatus(ADC1))
	{}
}

uint16_t adc_get_value (uint8_t channel)
{
	ADC_RegularChannelConfig(ADC1, channel, 1, ADC_SampleTime_1Cycles5);

	ADC_SoftwareStartConvCmd(ADC1, ENABLE);

	while (ADC_GetFlagStatus(ADC1, ADC_FLAG_EOC) == RESET)
	{};

	uint16_t value = ADC_GetConversionValue(ADC1);

	return value;
}

void adc_print (void)
{
	//TODO: where to find mapping ADC channels onto GPIO ?
	uint16_t adc0 = adc_get_value(10);
	printstr("\nADC 0: ");
	printnum(adc0, 0);

	uint16_t adc1 = adc_get_value(11);
	printstr("\nADC 1: ");
	printnum(adc1, 0);

	printstr("\n");
}


/*
 * TODO:
 * - manually implement int2str, byte2hex ...
 * - usart2 for device-device communication
 */

/*
 * User console:
 * 		- echo
 * 		- end of line
 * 		- command output
 *
 * Device-device interface:
 * 		- no echo, no end of line
 * 		- command recv accept
 * 		- command parse accept
 * 		- command execution result
 *
 *
 *
 *
 */


int argc = 0;
const char* argv[32] = {0};

void parse_args (char* cmd, uint32_t cmd_length)
{
	argc = 0;
	memset(argv, 0, sizeof(argv));

	int state = 0;

	for (int i = 0; i < cmd_length; i++, cmd++) {
		if (*cmd == ' ' || *cmd == '\t' || *cmd == '\n') {
			if (state) {
				argc++;
				*cmd = 0;
				state = 0;
			}
		} else {
			if (!state) {
				argv[argc] = cmd;
				state = 1;
			}
		}
	}
}

const char* help = "help, h, ? - print this message\n";

#define START_DUTY 2000

void test_pwm (int id)
{
	for (int duty = START_DUTY; duty < START_DUTY + 500; duty++) {
		servo_set_pwm_duty(id, duty);
		servo_switch_pwm(id, 1);
		wait(5);
	}
	for (int duty = START_DUTY + 500; duty > START_DUTY - 500; duty--) {
		servo_set_pwm_duty(id, duty);
		servo_switch_pwm(id, 1);
		wait(5);
	}
	for (int duty = START_DUTY - 500; duty < START_DUTY; duty++) {
		servo_set_pwm_duty(id, duty);
		servo_switch_pwm(id, 1);
		wait(5);
	}
}
void test_all_pwm ()
{
	for (int duty = START_DUTY; duty < START_DUTY + 500; duty++) {
		servo_set_all_pwm_duty(duty, duty, duty);
		servo_switch_all_pwm(1, 1, 1);
		wait(5);
	}
	for (int duty = START_DUTY + 500; duty > START_DUTY - 500; duty--) {
		servo_set_all_pwm_duty(duty, duty, duty);
		servo_switch_all_pwm(1, 1, 1);
		wait(5);
	}
	for (int duty = START_DUTY - 500; duty < START_DUTY; duty++) {
		servo_set_all_pwm_duty(duty, duty, duty);
		servo_switch_all_pwm(1, 1, 1);
		wait(5);
	}
}

char dbg_buffer [512] = {0};
int dbg_len = 0;

int pwm_duty_count = 0;

int cmd_exec (int argc, const char* argv[], usart_t* term)
{
	if (!strcmp(argv[0], "help") || argv[0][0] == '?' || argv[0][0] == 'h') {
		term_putstr(term, help);
		return 0;
	}
	if (!strcmp(argv[0], "reset")) {
		reset_isr();
	}

	if (!strcmp(argv[0], "start")) {

		int duty = START_DUTY;

		servo_set_all_pwm_duty(duty, duty, duty);
		servo_switch_all_pwm(1, 1, 1);

		term_putstr(term, "All pwm 2000\n");
		return 0;
	}

	if (!strcmp(argv[0], "test1")) {
		test_pwm(0);
		return 0;
	}
	if (!strcmp(argv[0], "test2")) {
		test_pwm(1);
		return 0;
	}
	if (!strcmp(argv[0], "test3")) {
		test_pwm(2);
		return 0;
	}
	if (!strcmp(argv[0], "test_all")) {
		test_all_pwm();
		return 0;
	}
	if (!strcmp(argv[0], "led") && argc == 2) {
		int num = strtol(argv[1], 0, 0);
		led_num(num);
		return 0;
	}
	if (!strcmp(argv[0], "adc")) {
		if (argc == 1) {
			adc_print();
			return 0;
		}
		if (!strcmp(argv[1], "cont") && argc == 4) {
			int counter = strtol(argv[2], 0, 0);
			int period = strtol(argv[3], 0, 0);
			while (counter--) {
				adc_print();
				wait(period);
			}
			return 0;
		}
		return 1;
	}
#if DBG_TERM
	if (!strcmp(argv[0], "dbg")) {
		for (int i = 0; i < dbg_len; i++) {
			term_putstr(term, hexstr(dbg_buffer[i]));
			term_putstr(term, " ");
			if (((i+1) % 16) == 0) {
				term_putstr(term, "\n");
			}
		}
		term_putstr(term, "\n");
		return 0;
	}
#endif
	if (!strcmp(argv[0], "pwm") && argc > 1) {

		if (!strcmp(argv[1], "state")) {
			for (int i = 0; i < 3; i++) {
				term_putstr(term, "servo pwm #");
				term_putstr(term, numstr(i));
				term_putstr(term, delta.pwm_enabled[i] ? " enabled" : " disabled");
				term_putstr(term, ", duty=");
				term_putstr(term, numstr(delta.pwm_duty[i]));
				term_putstr(term, "\n");
			}
			return 0;
		}
		if (!strcmp(argv[1], "en") && argc == 5) {

			for (int i = 0; i < 3; i++) {
				int enable = strtol(argv[2+i], 0, 0);
				delta.pwm_enabled[i] = enable;
			}
			servo_sync_pwm();
			return 0;
		}
		if (!strcmp(argv[1], "duty") && argc == 5) {

			for (int i = 0; i < 3; i++) {
				uint16_t duty = strtol(argv[2+i], 0, 0);
				delta.pwm_duty[i] = duty;
			}
			led_num(pwm_duty_count++);

			servo_sync_pwm();
			return 0;
		}


		return 1;
	}

	return 1;
}


char cmd_buffer[USART_BUFF_SIZE];

void main( void )
{
	leds_init();

	usart_init(usart_1, &usart_config,
			usart_buffers[0], USART_BUFF_SIZE,
			usart_buffers[1], USART_BUFF_SIZE);

	usart_enable(usart_1);

	term_putstr(usart_1, "Yet Another Delta Robot\n");

	servo_pwm_timer_init();

	term_putstr(usart_1, "Servo PWM configured.\n");

	adc_init();

	term_putstr(usart_1, "ADC C0,C1 configured.\n");

	int recv;

	term_putstr(usart_1, "~ # ");
	while (1) {

		recv = term_getline(usart_1, cmd_buffer, sizeof(cmd_buffer));
#if DBG_TERM
		if (dbg_len + recv < sizeof(dbg_buffer)) {
			memcpy(&dbg_buffer[dbg_len], cmd_buffer, recv);
			dbg_len += recv;
			dbg_buffer[dbg_len] = 0;
		}
#endif
		if (recv > 0) {

			if (cmd_buffer[0] != LF) {

				parse_args(cmd_buffer, recv);
#if 0
				for (int i = 0; i < argc; i++) {
					term_putstr(usart_1, argv[i]);
					term_putstr(usart_1, "\n");
				}
				term_putstr(usart_1, "\n");
#endif
				int result = cmd_exec(argc, argv, usart_1);

				if (result < 0) {
	//				term_printf(usart_1, "ERROR: error code %d (0x%X)\n", result, result);
				} else if (result == 1) {
					term_putstr(usart_1, "ERROR: command not implemented\n");
				}

			}

			term_putstr(usart_1, "~ # ");

//			term_putstr(usart_1, cmd_buffer);
//			term_send(usart_1, cmd_buffer, recv);
//			term_printf(usart_1, "recvd %d bytes\n", recv);

		} else {
		}


	}

}
