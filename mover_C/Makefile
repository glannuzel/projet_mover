all: a.bin
	avrdude -p m328p -P /dev/ttyACM0 -c arduino -U flash:w:a.bin

#en binaire
a.bin: a.elf
	avr-objcopy -O binary a.elf a.bin

#compiler
a.elf: main.c
	avr-gcc -Os -DF_CPU=16000000UL -mmcu=atmega328p main.c -o a.elf