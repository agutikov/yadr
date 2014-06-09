
#include "usart.h"

#include <string.h>

#define USE_DMA 0


void usart_init (usart_t* usart, const usart_config_t* cfg,
		void* tx_buffer, uint32_t tx_buffer_size,
		void* rx_buffer, uint32_t rx_buffer_size)
{
	ring_buffer_init(&usart->tx, tx_buffer, tx_buffer_size);
	ring_buffer_init(&usart->rx, rx_buffer, rx_buffer_size);

	usart->last_tx_dma = 0;
	usart->dma_tc_flag = cfg->dma_tc_flag;

	usart->tx_started = 0;

	usart->usart_regs = cfg->usart_regs;
	usart->dma_channel_regs = cfg->dma_channel_regs;

	if (cfg->AHB_clocks)
		RCC_AHBPeriphClockCmd(cfg->AHB_clocks, ENABLE);
	if (cfg->APB1_clocks)
		RCC_APB1PeriphClockCmd(cfg->APB1_clocks, ENABLE);
	if (cfg->APB2_clocks)
		RCC_APB2PeriphClockCmd(cfg->APB2_clocks, ENABLE);

	GPIO_InitTypeDef GPIO_InitStructure;

// No remap if standard gpio lines used (PA9 and PA10 for USART1)
//	GPIO_PinRemapConfig(GPIO_Remap_USART1, ENABLE);

	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;
	GPIO_InitStructure.GPIO_Pin = cfg->usart_gpio_tx_line;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_Init(cfg->usart_gpio_port, &GPIO_InitStructure);

	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IN_FLOATING;
	GPIO_InitStructure.GPIO_Pin = cfg->usart_gpio_rx_line;
	GPIO_Init(cfg->usart_gpio_port, &GPIO_InitStructure);

	NVIC_InitTypeDef NVIC_InitStructure;

//	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_0);

	NVIC_InitStructure.NVIC_IRQChannel = cfg->usart_irqn;
	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 0;
	NVIC_InitStructure.NVIC_IRQChannelSubPriority = 0;
	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;
	NVIC_Init(&NVIC_InitStructure);

#if USE_DMA
	NVIC_InitStructure.NVIC_IRQChannel = cfg->dma_irqn;
	NVIC_Init(&NVIC_InitStructure);

	DMA_DeInit(usart->dma_channel_regs);
	usart->DMA_InitStructure.DMA_PeripheralBaseAddr = (uint32_t)&usart->usart_regs->DR;
	usart->DMA_InitStructure.DMA_MemoryBaseAddr = (uint32_t)usart->tx.head;
	usart->DMA_InitStructure.DMA_DIR = DMA_DIR_PeripheralDST;
	usart->DMA_InitStructure.DMA_BufferSize = 0;
	usart->DMA_InitStructure.DMA_PeripheralInc = DMA_PeripheralInc_Disable;
	usart->DMA_InitStructure.DMA_MemoryInc = DMA_MemoryInc_Enable;
	usart->DMA_InitStructure.DMA_PeripheralDataSize = DMA_PeripheralDataSize_Byte;
	usart->DMA_InitStructure.DMA_MemoryDataSize = DMA_MemoryDataSize_Byte;
	usart->DMA_InitStructure.DMA_Mode = DMA_Mode_Normal;
	usart->DMA_InitStructure.DMA_Priority = DMA_Priority_VeryHigh;
	usart->DMA_InitStructure.DMA_M2M = DMA_M2M_Disable;
	// run it on first transmit
	// DMA_Init(usart->dma_channel_regs, &usart->DMA_InitStructure);
#endif

	USART_InitTypeDef USART_InitStructure;

	USART_InitStructure.USART_BaudRate = 115200;
	USART_InitStructure.USART_WordLength = USART_WordLength_8b;
	USART_InitStructure.USART_StopBits = USART_StopBits_1;
	USART_InitStructure.USART_Parity = USART_Parity_No;
	USART_InitStructure.USART_HardwareFlowControl = USART_HardwareFlowControl_None;
	USART_InitStructure.USART_Mode = USART_Mode_Rx | USART_Mode_Tx;
	USART_Init(usart->usart_regs, &USART_InitStructure);
}

void usart_enable (usart_t* usart)
{
	// enable usart
	usart->usart_regs->CR1 |= USART_CR1_UE;

	if (ring_buffer_av_space(&usart->rx)) {
		// enable rx interrupt
		usart->usart_regs->CR1 |= USART_CR1_RXNEIE;
	}
}
void usart_disable (usart_t* usart)
{

}

static void _tx_start (usart_t* usart)
{
#if USE_DMA
	if (!usart->last_tx_dma) {
//		DMA_DeInit(usart->dma_channel_regs);
		usart->DMA_InitStructure.DMA_MemoryBaseAddr = (uint32_t)usart->tx.head;
		usart->last_tx_dma = ring_buffer_av_data_cont(&usart->tx);
		usart->DMA_InitStructure.DMA_BufferSize = usart->last_tx_dma;
		DMA_Init(usart->dma_channel_regs, &usart->DMA_InitStructure);

		USART_DMACmd(usart->usart_regs, USART_DMAReq_Tx, ENABLE);
		DMA_Cmd(usart->dma_channel_regs, ENABLE);
	}
#endif
}

int usart_recv (usart_t* usart, void *ptr, uint32_t size)
{
	uint32_t rcvd = ring_buffer_pop(&usart->rx, ptr, size);

	if (ring_buffer_av_space(&usart->rx)
			&& !(usart->usart_regs->CR1 & USART_CR1_RXNEIE)) {
		usart->usart_regs->CR1 |= USART_CR1_RXNEIE;
	}

	return rcvd;
}

void usart_isr (usart_t* usart)
{
	uint32_t sr = usart->usart_regs->SR;

	if (sr & USART_SR_PE) {

	}
	if (sr & USART_SR_FE) {

	}
	if (sr & USART_SR_NE) {

	}
	if (sr & USART_SR_ORE) {

	}
	if (sr & USART_SR_IDLE) {

	}
	if (sr & USART_SR_RXNE) {
		uint32_t dr = usart->usart_regs->DR;
		uint8_t byte = dr;

		ring_buffer_push(&usart->rx, &byte, 1);

		//TODO: flow control
		if (!ring_buffer_av_space(&usart->rx)) {
			usart->usart_regs->CR1 &= ~USART_CR1_RXNEIE;
		}
	}
	if (sr & USART_SR_TC) {

	}
	if (sr & USART_SR_TXE) {

	}
	if (sr & USART_SR_LBD) {

	}
	if (sr & USART_SR_CTS) {

	}
}

int usart_send (usart_t* usart, const void *ptr, uint32_t size)
{
	//	int send = ring_buffer_push(&usart->tx, ptr, size);

	for (int tx_count = 0; tx_count < size; tx_count++) {
		while (!(usart->usart_regs->SR & USART_SR_TXE)) {}
		usart->usart_regs->DR = (uint16_t)(0x01FF) & ((uint8_t*)ptr)[tx_count];
	}

	return size;
}


void usart_handle_tx_dma_irq (usart_t* usart)
{
	//TODO: dma subsystem
	if (DMA_GetFlagStatus(usart->dma_tc_flag) == SET) {
		// transmit finished - clear related buffer
		ring_buffer_fflush_head(&usart->tx, usart->last_tx_dma);
		usart->last_tx_dma = 0;

		// clear interrupt flag
		DMA_ClearFlag(usart->dma_tc_flag);

		// if there are more data to send - start tx
		// else - disable DMA
		if (ring_buffer_av_data(&usart->tx)) {
			_tx_start(usart);
		} else {
			USART_DMACmd(usart->usart_regs, USART_DMAReq_Tx, DISABLE);
			DMA_Cmd(usart->dma_channel_regs, DISABLE);
		}
	}
}



