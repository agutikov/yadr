
CROSS_PREFIX=arm-none-eabi-

CC=$(CROSS_PREFIX)gcc
OBJCOPY=$(CROSS_PREFIX)objcopy
OBJDUMP=$(CROSS_PREFIX)objdump
LD=$(CROSS_PREFIX)ld

CFLAGS=-std=gnu99 -ffreestanding -nostdlib -nostdinc
CFLAGS+=-ggdb -O0
# CFLAGS+=-O2
CFLAGS+= -mcpu=cortex-m3 -mlittle-endian -mthumb
CFLAGS+= -Wall
# STM32F10X_MD_VL enables the maximum system clock (24MHz) in system_stm32f10x.c
CFLAGS+= -DSTM32F10X_MD_VL

SPL_LIB_PATH=../../../../stm32/spl/STM32F10x_StdPeriph_Lib_V3.5.0
NEWLIB_DIR=../../../../stm32/stm32_sandbox/lib/newlib/libc
LOCAL_LIB_DIR=../../../../stm32/stm32_sandbox/lib

# STDLIB_DIR=/opt/arm-none-eabi/arm-none-eabi/lib/armv7e-m/
# GCCLIB_DIR=/opt/arm-none-eabi/lib/gcc/arm-none-eabi/4.8.3/armv7e-m/softfp/

SPL_SYSTEM_DIR=$(SPL_LIB_PATH)/Libraries/CMSIS/CM3/DeviceSupport/ST/STM32F10x
SPL_CORE_DIR=$(SPL_LIB_PATH)/Libraries/CMSIS/CM3/CoreSupport
SPL_DRIVER_DIR=$(SPL_LIB_PATH)/Libraries/STM32F10x_StdPeriph_Driver

NEWLIB_SRC_DIR=$(NEWLIB_DIR)/string
NEWLIB_INC_DIR=$(NEWLIB_DIR)/include

CFLAGS+= -I.
CFLAGS+= -I$(SPL_SYSTEM_DIR)
CFLAGS+= -I$(SPL_CORE_DIR)
CFLAGS+= -I$(SPL_DRIVER_DIR)/inc
CFLAGS+= -I$(NEWLIB_INC_DIR)
CFLAGS+= -I$(LOCAL_LIB_DIR)/include

LDSCRIPT=stm32f100rb.ld

LDFLAGS= -nostdlib -M -Map firmware.map

SRCS=main.c startup.c usart.c
LOCAL_OBJS=$(SRCS:.c=.o)
NEWLIB_OBJS=memcpy.o
SPL_SYSTEM_OBJS=system_stm32f10x.o
SPL_DRIVER_OBJS=stm32f10x_gpio.o stm32f10x_rcc.o stm32f10x_usart.o \
	stm32f10x_adc.o stm32f10x_tim.o stm32f10x_flash.o stm32f10x_can.o \
	stm32f10x_dma.o stm32f10x_exti.o stm32f10x_rtc.o misc.o
ALL_OBJS=$(LOCAL_OBJS) $(SPL_SYSTEM_OBJS) $(SPL_DRIVER_OBJS) $(NEWLIB_OBJS)

.PHONY: all
all: firmware.bin firmware.lst firmware.elf firmware.hex

%.hex: %.elf
	$(OBJCOPY) $^ -O ihex $@

%.bin: %.elf
	$(OBJCOPY) -O binary $^ $@

# ld script should be first prerequisite because of -T $^
%.elf: $(LDSCRIPT) $(ALL_OBJS)
	$(LD) $(LDFLAGS) -T $^ -o $@

$(SPL_SYSTEM_OBJS): %.o: $(SPL_SYSTEM_DIR)/%.c
	$(CC) $(CFLAGS) -c -o $@ $^

$(SPL_DRIVER_OBJS): %.o: $(SPL_DRIVER_DIR)/src/%.c
	$(CC) $(CFLAGS) -c -o $@ $^

$(LOCAL_OBJS): %.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $^

$(NEWLIB_OBJS): %.o: $(NEWLIB_SRC_DIR)/%.c
	$(CC) $(CFLAGS) -c -o $@ $^

%.lst:	%.elf
	$(OBJDUMP) -htS $< > $@

.PHONY: clean
clean:
	rm -rf *.o *.elf *.bin *.lst *.map *.hex


######### Flash and Debug

OPENOCD_CFG=board/stm32vldiscovery.cfg

FLASH_ADDR=0x8000000

.PHONY: flash
flash: firmware.hex
#	st-flash write v1 $^ $(FLASH_ADDR)
	openocd -f $(OPENOCD_CFG) -c "program firmware.hex verify reset"

.PHONY: gdb-server
gdb-server:
#	st-util -1
	openocd -f $(OPENOCD_CFG)

.PHONY: gdb
gdb: firmware.elf
	$(CROSS_PREFIX)gdb --eval-command="target remote localhost:3333" firmware.elf


