BOARD = esp32
CHIP = esp32

#Arduino file
SKETCH = main.ino

BOARD_UUID = actionneurs
COMMON = ../common
BUILD_DIR =../build
#Setup all libs used !
LIBS = 	$(ESP_LIBS)/EEPROM \
		$(COMMON)/SerialTalks \
		$(COMMON)/CRC16 \
		$(COMMON)/AX12 \
		$(COMMON)/ESP32Servo \
		instructions.cpp \
		topics.cpp \
		$(COMMON)/serialutils.cpp

LIBS_with_i=$(addprefix  -I, $(LIBS))

CPPFLAGS = -fexceptions
CPPFLAGS += -DCONFIG_CXX_EXCEPTIONS=1
# Congratulations! You made a pretty Makefile :)
# Now let the grown-ups do the hard work :D 
CPP_EXTRA += -DSERIALTALKS_MAX_OPCODE=0x30 $(LIBS_with_i) -DLOG_LEVEL=0  -DBOARD_UUID=\"actionneurs\"


# Congratulations! You made a pretty Makefile :)
# Now let the grown-ups do the hard work :D
MODULEMK_DIR = ../makefilesEsp
include $(MODULEMK_DIR)/Module.mk

