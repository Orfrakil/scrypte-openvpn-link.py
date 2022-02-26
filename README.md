# scrypte-openvpn-link.py
Small scrypt to initiate vpn link between a openvpn main server with clients.

Conditions :
Openvpn must be installed on the master and the client.
The vpn master configuration have to be done and ready (certificat and key). 
The scipt has to be locat in the file /etc/openvpn/easy-rsa/ or the ca.crt will not find the easy-rsa file.
The paramiko modul for python must be allmost on v2.0 for efficient SSH key.
