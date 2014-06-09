
#include "usart.h"

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
//		.dma_tc_flag = DMA1_FLAG_TC1
	};

void usart1_isr (void)
{
	usart_isr(&usart_device);
}
void usart1_tx_dma_isr(void)
{
//	usart_handle_tx_dma_irq(&usart_devices[0]);
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

/*
 * TODO:
 * - strlen
 * - __FILE__, __LINE__, __FUNCTION__
 * - snprntf, printy >> usart1
 */

const char hello[] = "Yet Another Delta Robot\r\n";

uint8_t buffer[128];

extern int usart_dbg_get_byte (uint8_t* b);

void main( void )
{
	leds_init();

	usart_t* usart_1 = &usart_device;

	usart_init(usart_1, &usart_config,
			usart_buffers[0], USART_BUFF_SIZE,
			usart_buffers[1], USART_BUFF_SIZE);

	usart_enable(usart_1);


#if 0
	uint8_t byte;
	int rcvd = 0;

	while (1) {

		if (!rcvd && USART_GetFlagStatus(usart_1->usart_regs, USART_FLAG_RXNE) != RESET) {
			byte = USART_ReceiveData(usart_1->usart_regs);
			rcvd = 1;
		}


		if (rcvd && USART_GetFlagStatus(usart_1->usart_regs, USART_FLAG_TXE) != RESET) {
			USART_SendData(usart_1->usart_regs, byte);
			rcvd = 0;
		}
	}
#endif



	usart_send(usart_1, hello, sizeof(hello)-1);

	int recv;

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


	while (1) {

		recv = usart_recv(usart_1, buffer, sizeof(buffer));

		if (recv > 0) {
			usart_send(usart_1, buffer, recv);
		} else {
		}


	}

}
