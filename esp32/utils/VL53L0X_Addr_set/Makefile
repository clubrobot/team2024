# Board properties
BOARD = esp32doit-devkit-v1
CHIP = esp32

#Arduino file
SKETCH = main.ino

BOARD_UUID = sensors
COMMON = ../../common
BUILD_DIR =../build
#EXPAND_LIBS=1
#Setup all libs used !
LIBS =  $(ESP_LIBS)/EEPROM \
		$(ESP_LIBS)/Wire \
		$(COMMON)/CRC16 \
		$(COMMON)/VL53L0X \
		$(COMMON)/ShiftRegister

LIBS_with_i=$(addprefix  -I, $(LIBS))

# Define
CPP_EXTRA += -DSERIALTALKS_MAX_OPCODE=0x30 $(LIBS_with_i)

CPP_EXTRA += -DBOARD_UUID=\"sensors\"
CPP_EXTRA += -DLOG_LEVEL=0

# Congratulations! You made a pretty Makefile :)
# Now let the grown-ups do the hard work :D
MODULEMK_DIR = ../../makefilesEsp
include $(MODULEMK_DIR)/Module.mk