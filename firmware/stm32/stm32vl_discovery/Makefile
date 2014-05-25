
CROSS_PREFIX=arm-none-eabi-

CC=$(CROSS_PREFIX)gcc
OBJCOPY=$(CROSS_PREFIX)objcopy
OBJDUMP=$(CROSS_PREFIX)objdump
LD=$(CROSS_PREFIX)ld

CFLAGS=-std=gnu99 -ffreestanding -nostdlib
# -nostdinc
CLFAGS+=-ggdb -O0
# CFLAGS+=-O2
CFLAGS+= -mcpu=cortex-m3 -mlittle-endian -mthumb
# STM32F10X_MD_VL enables the maximum system clock (24MHz) in system_stm32f10x.c
CFLAGS+= -DSTM32F10X_MD_VL
CFLAGS+= -Wall

LIB_PATH=../lib
SPL_LIB_PATH=../../../../stm32/spl/STM32F10x_StdPeriph_Lib_V3.5.0

CFLAGS+= -I.
CFLAGS+= -I$(SPL_LIB_PATH)/Libraries/CMSIS/CM3/DeviceSupport/ST/STM32F10x
CFLAGS+= -I$(SPL_LIB_PATH)/Libraries/CMSIS/CM3/CoreSupport

LDSCRIPT=stm32vl_discovery.ld

LDFLAGS= -nostdlib -M -Map firmware.map

SRCS=main.c startup.c
OBJS=$(SRCS:.c=.o)
SPL_OBJS=system_stm32f10x.o

.PHONY: all
all: firmware.bin firmware.lst

%bin: %elf
	$(OBJCOPY) -O binary $^ $@

# ld script should be first prerequisite because of -T $^
%.elf: $(LDSCRIPT) $(OBJS) $(SPL_OBJS)
	$(LD) $(LDFLAGS) -T $^ -o $@

system_stm32f10x.o: $(SPL_LIB_PATH)/Libraries/CMSIS/CM3/DeviceSupport/ST/STM32F10x/system_stm32f10x.c
	$(CC) $(CFLAGS) -c -o $@ $^

$(OBJS): %.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $^

%.lst:	%.elf
	$(OBJDUMP) -htS $< > $@

.PHONY: clean
clean:
	rm -rf *.o *.elf *.bin *.lst *.map


######### Flash and Debug

OPENOCD_CFG=board/stm32vldiscovery.cfg

FLASH_ADDR=0x8000000

.PHONY: flash
flash: $(APPLICATION).bin
	openocd -f $(OPENOCD_CFG) -c "program firmware.bin verify reset"

.PHONY: gdb-server
gdb-server:
	openocd -f $(OPENOCD_CFG)


