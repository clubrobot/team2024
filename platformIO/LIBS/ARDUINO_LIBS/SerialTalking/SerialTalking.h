#ifndef __SERIALTALKING_H__
#define __SERIALTALKING_H__

/***
 * SerialTalking Lib Work In progess: CRINSA 2024
 * 
 * Negrache	Gibril et Hilkens Boris
 * 
*/

#include <Arduino.h>
#include "SerialTransfer.h"

#define SERIALTALKING_BAUDRATE 115200 /*!< Baudrate utiliser */
#define SERIALTALKING_DEBUG true
#define SERIALTALKING_DEBUG_PORT Serial

#define SERIALTALKING_INPUT_BUFFER_SIZE 64
#define SERIALTALKING_OUTPUT_BUFFER_SIZE 64

#define SERIALTALKING_UUID_ADDRESS 0x0000000000
#define SERIALTALKING_UUID_LENGTH 32

#define SERIALTALKING_MAX_OPCODE 0x20
#define SERIALTALKING_MAX_BUFFER_RECV 0x10
//On fait un ACK? même si c'est un ordre sans réponse ?

#define SERIALTALKING_PING_OPCODE           0x00
#define SERIALTALKING_GETUUID_OPCODE        0x01
#define SERIALTALKING_SETUUID_OPCODE        0x02
#define SERIALTALKING_DISCONNECT_OPCODE     0x03
#define SERIALTALKING_GETEEPROM_OPCODE      0x04
#define SERIALTALKING_SETEEPROM_OPCODE      0x05
#define SERIALTALKING_GETBUFFERSIZE_OPCODE  0x06
#define SERIALTALKING_RESEND_OPCODE         0x07
#define SERIALTALKING_FREE_BUFFER_OPCODE    0x08
#define SERIALTALKING_STDOUT_RETCODE 0xFFFFFFFF
#define SERIALTALKING_STDERR_RETCODE 0xFFFFFFFE

/** class SerialTalking
 *  \brief Object de communication serial avec un ordinateur.
 *	\author Negrache Gibril
	\author Hilkens Boris
 *  est un outil permettant à l'arduino de pouvoir répondre aux requêtes recu depuis le serial.
 *  Il utilise donc le port serial (unsb) pour envoyer ou recevoir des données avec l'ordinateur ou la raspberry
 *  La classe est capable de lancer des methodes sur demande de l'ordinateur ou de la raspberry.
 *  Très inspiré de serialTalks mais mieux 👈(ﾟヮﾟ👈)
 */
class SerialTalking{

public:
   
    //! Initialise le SerialTalking avec un Stream d'<arduino.h>.
    /*!
		\param stream Flux à associer pour la communication de SerialTalking.
	*/
    void begin(Stream &stream);

    //! Associe une Instruction à un OPCODE.
    /*!
		\param opcode Code à associer à la fonction.
		\param instruction Fonction à répertorier dans SerialTalking.
	*/
    void bind(byte opcode, functionPtr instruction);

    //! Indique si SerialTalking est bien connecté au rasp. (avec handshake)
    /*!
		\return Vrai si le stream est connecté.
	*/
    bool isConnected() const { return m_connected; }

    /*tick le transfert
    */
    void execute();

    /*! Ajoute un objet au buffer serial transfert
    \param val valeur à ajouter
    */
    template <typename T>
    void addTxDatum(const T& val){
        m_bytesNumber = m_transfert.txObj((uint16_t) sizeof(val), m_bytesNumber); //On envoie la taille de la donnée!
  	    m_bytesNumber = m_transfert.txObj(val, m_bytesNumber, sizeof(val));
    }


    /*! Ajoute un buffer au buffer serial transfert
        \param val valeur à ajouter
    */
    template <typename T>
    void addTxData(const T& val){
        m_bytesNumber = m_transfert.txObj((uint16_t) sizeof(val)/sizeof(val[0]), m_bytesNumber); //On envoie la taille de la donnée!
  	    m_bytesNumber = m_transfert.txObj(val, m_bytesNumber, sizeof(val)/sizeof(val[0]));
    }

    /*! Ajoute un buffer au buffer serial transfert
    \param val valeur à ajouter
    */
    template <typename T>
    void receiveTransfert(const T& data, const uint16_t& len = sizeof(T)){
        m_bytesCounter=0;

        uint16_t data_size=0; 
        m_bytesCounter = m_transfert.rxObj(data_size, m_bytesCounter); //On envoie la taille de la donnée!

        if(len<data_size){
            digitalWrite(LED_BUILTIN, HIGH);
            return;
        }

        for(uint16_t i=0; i<data_size; i++){
            m_bytesCounter = m_transfert.rxObj(data[i], m_bytesCounter);
        }
    }

    /*! Envoie toutes les données du buffer transfert
    */
    void sendTranfert();

    //! Méthode bloquante jusqu'à handshake avec le raspberry ou jusqu'au timeout.
    /*!
		\param timeout Timeout pour la méthode 
		\return Vrai si le Stream est connecté.
	*/
    bool waitUntilConnected(float timeout = -1);

    //! Ecrit sur le pointeur l'UUID enregistré dans l'EEPROM de l'Arduino.
    /*!
		\param uuid Pointeur à utiliser.
		\return Vrai si il existe bien un UUID.
	*/
    bool getUUID(char *uuid);

    //! Enregistre l'UUID dans l'EEPROM de l'Arduino.
    /*!
		\param uuid Pointeur de l'UUID à enregistrer.
	*/

    void setUUID(const char *uuid);
    //! Génère un UUID
    /*!
		\param uuid Pointeur pour renvoyer l'UUID.
		\param length Longueur en octet de l'UUID à générer.
	*/
    static void generateRandomUUID(char *uuid, int length);


protected: // Protected methods
    /**
	 * @brief Méthode interne pour traiter les retours de requêtes.
	 *  ??? qu'est ce que c'est que ça ???
	 */
    bool receive(byte *inputBuffer);

    // Attributes

    Stream *m_stream; /*!< Stream de communication utilisé par SerialTalking.*/
    SerialTransfer m_transfert; /* Transfert utilisé par SerialTalking*/
    bool m_connected; /*!< Représente l'état de connection.*/

    configST m_transfert_config;// Configuration du transfert

    functionPtr m_talkingTo[SERIALTALKING_MAX_OPCODE] = {nullptr}; //Liste des callbakcs
 
    enum // m_order
    {
        SERIALTALKING_ORDER,  ///< Requête reçu de la raspberry.
        SERIALTALKING_RETURN, ///< Retour de requête.
    } m_order;              /// Type de requête reçu.

    byte m_bytesNumber;  /*!< Variable pour la réception de données qui correspond à la longueur de la requête en bytes (valeur donnée dans le deuxième byte d'une requête).*/
    byte m_bytesCounter; /*!< Variable d'incrementation pour la réception de données.*/
    long m_lastTime;     /*!< Timeout pour la réception d'octets d'une même requête.*/
    unsigned long m_lastRetcode;

private:

    /**
	 * @brief Méthode interne pour demander le réenvoie de la requête.
	 * 
	 */
    void launchResend(void);

    //! Méthode pour la requête de ping.
    static void PING();
    //! Méthode pour la requête d'UUID.
    static void GETUUID();
    //! Méthode pour la requête de changement d'UUID.
    static void SETUUID();
    //! Méthode pour lire dans l'EEPROM.
    static void GETEEPROM();
    //! Méthode pour écire dans l'EEPROM.
    static void SETEEPROM();
    //! Méthode pour récuperer la taille du Buffer.
    static void GETBUFFERSIZE();
};

extern SerialTalking talking;

#endif // __SERIALTALKING_H__