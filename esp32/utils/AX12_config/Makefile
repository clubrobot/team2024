BOARD = esp32
CHIP = esp32

#Arduino file
SKETCH = main.ino

BOARD_UUID = AX12_CONFIG
COMMON = ../../common
BUILD_DIR =../../build
#Setup all libs used !
LIBS = 	$(ESP_LIBS)/EEPROM \
		$(COMMON)/SerialTalks \
		$(COMMON)/CRC16 \
		$(COMMON)/AX12 \
		instructions.cpp \
		topics.cpp \
		$(COMMON)/serialutils.cpp

LIBS_with_i=$(addprefix  -I, $(LIBS))

CPPFLAGS = -fexceptions
CPPFLAGS += -DCONFIG_CXX_EXCEPTIONS=1
# Congratulations! You made a pretty Makefile :)
# Now let the grown-ups do the hard work :D
CPP_EXTRA += -DSERIALTALKS_MAX_OPCODE=0x30 $(LIBS_with_i)

CPP_EXTRA += -DBOARD_UUID=\"AX12_CONFIG\"
CPP_EXTRA += -DLOG_LEVEL=0

# Congratulations! You made a pretty Makefile :)
# Now let the grown-ups do the hard work :D
MODULEMK_DIR = ../../makefilesEsp
include $(MODULEMK_DIR)/Module.mk

