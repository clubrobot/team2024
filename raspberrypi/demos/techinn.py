
#import imp
from common.components import Manager
from daughter_cards.wheeledbase import WheeledBase
from daughter_cards.actionneur import Actionneur, AX12
import time
# simple inquiry example
""" import bluetooth

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

bluetooth.advertise_service(server_sock, "SampleServer", service_id=uuid,
                            service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                            profiles=[bluetooth.SERIAL_PORT_PROFILE],
                            # protocols=[bluetooth.OBEX_UUID]
                            )

print("Waiting for connection on RFCOMM channel", port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from", client_info)

try:
    while True:
        data = client_sock.recv(1024)
        if not data:
            break
        print("Received", data)
except OSError:
    pass

print("Disconnected.")

client_sock.close()
server_sock.close()
print("All done.") """

wb = WheeledBase('wheeledbase')
actionneur = Actionneur('actionneurs')

cane = AX12(1, actionneur)
elevateur = AX12(2, actionneur)
pince_droite = AX12(3, actionneur)
pince_gauche = AX12(4, actionneur)

pince_gauche.setEndlessMode(False)
pince_gauche.setMaxTorque(1023)

### pince gauche 200 ouvert; 230 fermé
time.sleep(2)
pince_gauche.move(200)
wb.set_openloop_velocities(1000,-1000)
time.sleep(1)
wb.set_openloop_velocities(0,0)
time.sleep(1)
pince_gauche.move(230)
time.sleep(1)
wb.set_openloop_velocities(200,200)
time.sleep(1.56)
wb.set_openloop_velocities(1000,-1000)
time.sleep(1)
wb.set_openloop_velocities(0,0)
pince_gauche.move(200)
time.sleep(1.6)
wb.set_openloop_velocities(200,200)
time.sleep(1.6)
wb.set_openloop_velocities(0,0)