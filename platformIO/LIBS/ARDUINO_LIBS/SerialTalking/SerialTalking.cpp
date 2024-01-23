/**
 * @file SerialTalking.cpp
 * @author Boris HILKENS, NEGRACHE Gibril
 * @brief SerialTalking CPP side, WIP
 * @version 1.0
 * @date 2024-01-21
 * 
 * @copyright Copyright (c) 2024
 * 
 */

#include "SerialTalking.h"
#include <EEPROM.h>

SerialTalking talking;

// SerialTalking

void SerialTalking::begin(Stream& stream)
{
	//Attributs en privé
	m_stream = &stream;
	m_connected = false;
	m_bytesTX = 0;
	m_bytesRX = 0;

	for(uint16_t i=0; i<SERIALTALKING_MAX_OPCODE; i++){
		m_talkingTo[i] = nullptr;
	}

    //Config du transfert
    m_transfert_config.debug = SERIALTALKING_DEBUG;
    m_transfert_config.debugPort = &Serial;
    m_transfert_config.callbacks = m_talkingTo;
    m_transfert_config.callbacksLen = sizeof(m_talkingTo) / sizeof(functionPtr);
    m_transfert_config.timeout = __UINT32_MAX__;

    m_transfert.begin(*m_stream, m_transfert_config);

	//Déf de l'UUID
#ifdef BOARD_UUID //<- changé en pre-compil (voir platformio.ini)
	#define SERIALTALKING_UUID_LENGTH sizeof(BOARD_UUID)/sizeof(BOARD_UUID[0])
	setUUID(BOARD_UUID);
#else
	#define SERIALTALKING_UUID_LENGTH 32
	char uuid[SERIALTALKING_UUID_LENGTH];
	if (!getUUID(uuid) || uuid[0] == '\0')
	{
		generateRandomUUID(uuid, SERIALTALKING_UUID_LENGTH);
		setUUID(uuid);
	}
#endif // BOARD_UUID

	// Add UUID accessors
	bind(SERIALTALKING_PING_OPCODE,     SerialTalking::PING);
	bind(SERIALTALKING_GETUUID_OPCODE,  SerialTalking::GETUUID);
	bind(SERIALTALKING_SETUUID_OPCODE,  SerialTalking::SETUUID);
	bind(SERIALTALKING_GETEEPROM_OPCODE,SerialTalking::GETEEPROM);
	bind(SERIALTALKING_SETEEPROM_OPCODE,SerialTalking::SETEEPROM);
	//bind(SERIALTALKING_FREE_BUFFER_OPCODE, SerialTalking::FREEBUFFER);
}

void SerialTalking::bind(byte opcode, functionPtr instruction){
	if(opcode>SERIALTALKING_MAX_OPCODE){return;}
	if(instruction==nullptr){return;}//No null function
  	//if((m_talkingTo[opcode]!=nullptr)){return;}//No overdrive

  	m_talkingTo[opcode] = instruction;//On affecte la fonction au callbacks

  	return;
}

void SerialTalking::execute(){
	m_transfert.tick();
}

void SerialTalking::endTranfert(){
	if(m_bytesTX!=0){
		m_transfert.sendData(m_bytesTX);
	}
	m_bytesTX = 0; //On reset le counter TX
	m_bytesRX = 0; //RX Aussi
	talking.m_transfert.reset();
}

bool SerialTalking::getUUID(char* uuid){
	for (int i = 0; i < int(EEPROM.length()); i++){
		uuid[i] = EEPROM.read(SERIALTALKING_UUID_ADDRESS + i);

		switch(byte(uuid[i])){
		case '\0': return true;
		case 0xFF: return false;
		default  : continue;
		}
	}
	return false;
}

bool SerialTalking::setUUID(const char* uuid){
	for (int i = 0; i < int(EEPROM.length()); i++){
		EEPROM.update(SERIALTALKING_UUID_ADDRESS + i, uuid[i]);

		switch(byte(uuid[i])){
		case '\0': return true;
		default  : continue;
		}
	}
	return false;
	/* int i = 0;
	do
		EEPROM.update(SERIALTALKING_UUID_ADDRESS + i, uuid[i]);
	while(uuid[i++] != '\0'); */
}

void SerialTalking::generateRandomUUID(char* uuid, int length){
	// Initialize the random number generator
	randomSeed(analogRead(0));

	// Generate the UUID from a list of random hexadecimal numbers
	for (int i = 0; i < length; i++)
	{
		if (i % 5 == 4)
			uuid[i] = '-';
		else
		{
			long digit = random(16);
			if (digit < 10)
				uuid[i] = char('0' + digit);
			else
				uuid[i] = char('a' + digit - 10);
		}
	}
	uuid[length] = '\0';
}

/*
	Fonctions par défault de SerialTalking
*/

void SerialTalking::PING(){
	char pong[5] = "pong";
	talking.writeTable(pong);
	talking.endTranfert();
}

void SerialTalking::GETUUID(){
	char uuid[SERIALTALKING_UUID_LENGTH];
	talking.getUUID(uuid);
	talking.writeTable(uuid);
	talking.endTranfert();
}

void SerialTalking::SETUUID(){
	char uuid[20];
	talking.readTable(uuid, 20);
	talking.setUUID(uuid);
	talking.endTranfert();
}
void SerialTalking::GETEEPROM(){
	uint16_t address = talking.read<uint16_t>();
	uint8_t value = EEPROM.read(address);
	talking.write(value);
	talking.endTranfert();
}

void SerialTalking::SETEEPROM(){
	uint16_t address = talking.read<uint16_t>();
	uint8_t value = talking.read<uint8_t>();
	EEPROM.update(address, value);
	talking.endTranfert();
}

void SerialTalking::FREEBUFFER(){
	talking.endTranfert();
	m_transfert.reset();
}