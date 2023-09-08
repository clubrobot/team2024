# Board properties
BOARD = esp32doit-devkit-v1
CHIP = esp32

#Arduino file
SKETCH = SerialTopics.ino

BOARD_UUID = SerialTopics
COMMON = ../common

#Setup all libs used !
LIBS =  $(ESP_LIBS)/EEPROM \
		instructions.cpp \
		topics.cpp \
		$(COMMON)/SerialTalks \
		$(COMMON)/CRC16 \
		$(COMMON)/SerialTopics \
		$(COMMON)/serialutils.cpp

LIBS_with_i=$(addprefix  -I, $(LIBS))

# Define
CPP_EXTRA += -DSERIALTALKS_MAX_OPCODE=0x30 $(LIBS_with_i)

CPP_EXTRA += -DBOARD_UUID=\"$(BOARD_UUID)\"
CPP_EXTRA += -DLOG_LEVEL=0

# Congratulations! You made a pretty Makefile :)
# Now let the grown-ups do the hard work :D
MODULEMK_DIR = ../makefilesEsp
include $(MODULEMK_DIR)/Module.mk