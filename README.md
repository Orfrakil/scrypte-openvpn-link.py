# scrypte-openvpn-link.py
This crypt is made to initiate vpn link between a openvpn main server with one client.

Conditions :
Openvpn must be installed on the master and the client.
SSH must be installed on the master and the client. 
The client must have a user which accept SSH connection. 
The vpn master configuration have to be done and ready (certificat and key). 
The scipt has to be locat in the file /etc/openvpn/easy-rsa/ or the ca.crt will not find the easy-rsa file.
The paramiko modul for python must be allmost on v2.0 for efficient SSH key.
