/***
 * SerialTalking Lib Work In progess: CRINSA 2024
 * 
 * Negrache	Gibril et Hilkens Boris
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

	EEPROM.begin(EEPROM_SIZE);

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
#ifdef BOARD_UUID //<- changé en tant que option pre-compil (voir platformio.ini)
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
	bind(SERIALTALKING_GETBUFFERSIZE_OPCODE, SerialTalking::GETBUFFERSIZE);
	bind(SERIALTALKING_CLEAR_EEPROM, SerialTalking::CLEAREEPROM);
}

void SerialTalking::bind(byte opcode, functionPtr instruction){
	//if(opcode>SERIALTALKING_MAX_OPCODE){return;}
	//if(instruction==nullptr){return;}//No null function
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

void SerialTalking::setUUID(const char* uuid){
	int i = 0;
	do
		EEPROM.write(SERIALTALKING_UUID_ADDRESS + i, uuid[i]);
	while(uuid[i++] != '\0');
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
	//digitalWrite(LED_BUILTIN, HIGH);
	char msg[5] = "pong";
	talking.writeTable(msg);
	talking.endTranfert();
	talking.m_connected=true;
}

void SerialTalking::GETUUID(){
	char uuid[SERIALTALKING_UUID_LENGTH];
	talking.getUUID(uuid);
	talking.writeTable(uuid);
	talking.endTranfert();
}

void SerialTalking::SETUUID() {

}
void SerialTalking::GETEEPROM() {}
void SerialTalking::SETEEPROM() {}
void SerialTalking::GETBUFFERSIZE() {}

void SerialTalking::CLEAREEPROM() {
	for(int i=0; i<EEPROM_SIZE;i++){
		EEPROM.write(i, 0xFF);
	}
	EEPROM.commit();
}