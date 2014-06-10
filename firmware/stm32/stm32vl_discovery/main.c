
/*
	A6 - pwm tim3
	A7 - pwm tim3

	A9 - usart1 tx
	A10 - usart1 rx

	B0 - pwm tim3

	C8 - blue led
	C9 - green led





 */

#include <string.h>
#include <stdlib.h>

#include "stm32f10x_tim.h"

#include "usart.h"


#define USART_NUMBER 3
#define USART_BUFF_SIZE	256

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
		.pwm_enabled = {0, 0, 0},
		.pwm_duty = {0, 0, 0}
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
	uint16_t PrescalerValue = 0;

	/* Compute the prescaler value */
	PrescalerValue = (uint16_t) (SystemCoreClock / 1000000) - 1;
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
	TIM_SetCompare1(TIM3, delta.pwm_duty[0]);
	TIM_SetCompare1(TIM3, delta.pwm_duty[1]);
	TIM_SetCompare1(TIM3, delta.pwm_duty[2]);

	// last - enable
	for (int i = 0; i < 3; i++) {
		if (delta.pwm_enabled[i])
			servo_switch_pwm(i, 1);
	}
}

/*
 * TODO:
 * - vsnprintf >> printy into usart1
 * - struct of cammands and function binding, separate parsing parameters
 * - autocomplete, history
 * - scripting language (for example lisp)
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

int cmd_exec (int argc, const char* argv[], usart_t* term)
{
	if (!strcmp(argv[0], "help") || argv[0][0] == '?' || argv[0][0] == 'h') {
		term_putstr(term, help);
		return 0;
	}

	if (!strcmp(argv[0], "pwm") && argc > 1) {

		if (!strcmp(argv[1], "state")) {
			for (int i = 0; i < 3; i++) {
				term_putstr(term, "servo pwm #x ");
				term_putstr(term, delta.pwm_enabled[i] ? "enabled" : "disabled");
				term_putstr(term, "\n");
			}
		}
		if (!strcmp(argv[1], "en") && argc == 5) {

			for (int i = 0; i < 3; i++) {
				int enable = strtol(argv[2+i], 0, 0);
				delta.pwm_enabled[i] = enable;
			}
			servo_sync_pwm();
		}
		if (!strcmp(argv[1], "duty") && argc == 5) {

			for (int i = 0; i < 3; i++) {
				uint16_t duty = strtol(argv[2+i], 0, 0);
				delta.pwm_duty[i] = duty;
			}
			servo_sync_pwm();
		}


		return 0;
	}

	return 1;
}


char cmd_buffer[USART_BUFF_SIZE];

void main( void )
{
	leds_init();

	usart_t* usart_1 = &usart_device;

	usart_init(usart_1, &usart_config,
			usart_buffers[0], USART_BUFF_SIZE,
			usart_buffers[1], USART_BUFF_SIZE);

	usart_enable(usart_1);

	term_putstr(usart_1, "Yet Another Delta Robot\n");

	servo_pwm_timer_init();

	term_putstr(usart_1, "Servo PWM configured.\n");
#if 0
	int a = strtol("123", 0, 0);

	if (a == 123) {
		led_num(1);
	} else {
		led_num(3);
	}
#endif

	int recv;

	term_putstr(usart_1, "~ # ");
	while (1) {

		recv = term_getline(usart_1, cmd_buffer, sizeof(cmd_buffer));

		if (recv > 0) {

			if (cmd_buffer[0] != LF) {

				parse_args(cmd_buffer, recv);
#if 1
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
