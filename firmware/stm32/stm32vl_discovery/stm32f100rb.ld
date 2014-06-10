
ENTRY(reset_isr)

MEMORY
{
    FLASH (rx)    : ORIGIN = 0x08000000, LENGTH = 128K
    SRAM (rxw)     : ORIGIN = 0x20000000, LENGTH = 8K
}

SECTIONS
{
	.text :
	{
		. = ALIGN(4);
		_text = .;
		KEEP(*(.isr_vector))
		*(.text)
		*(.text*)
		. = ALIGN(4);
		_etext = .;
		_rodata = .;
		*(.rodata)
		*(.rodata*)
		. = ALIGN(4);
		_erodata = .;
	} > FLASH

	.data : AT (ADDR(.text) + SIZEOF(.text))
	{
		. = ALIGN(4);
		_data = .;
		*(.data)
		*(.data*)
		. = ALIGN(4);
		_edata = .;
	} > SRAM

	_data_at_flash = ADDR(.text) + SIZEOF(.text);
	_edata_at_flash = _data_at_flash + SIZEOF(.data);

	.bss :
	{
		. = ALIGN(4);
		_bss = .;
		*(.bss)
		*(.bss*)
		*(COMMON)
		. = ALIGN(4);
		_ebss = .;
	} > SRAM

	.heap :
	{
		. = ALIGN(4);
		_heap = .;
		. = . + 0;
		. = ALIGN(4);
		_eheap = .;
	} > SRAM

	_stack_size = 1024;
	_estack = ORIGIN(SRAM) + LENGTH(SRAM);
	_stack = _estack - _stack_size;
	. = _stack;
	.stack :
	{
		. = . + _stack_size;
	} > SRAM
}
