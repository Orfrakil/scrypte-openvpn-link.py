#! -*- coding: utf-8 -*-
import os
import os.path
import shutil
import paramiko
from paramiko import SSHClient
from scp import SCPClient

# informations client à indiquer
Nclient = raw_input('Nom du client : ')
IPclient = raw_input("IP du client : ")
Uclient = raw_input("Utilisateur du client : ")
MDPclient = raw_input("Mot de passe du client : ")

route = os.path.join('/etc/openvpn/client/', Nclient )

# vérifier si le dossier n'existe pas et le créer si c'est vrai
if not os.path.exists( route ):
    	os.makedirs( route )
    	print ("Dossier client créé")

# si non afficher que le dossier existe déja
else:
 	print ("Le dossier client existe déjà")

# générer le sertificat client
cmd = "/etc/openvpn/easy-rsa/easyrsa " + "gen-req " + Nclient + " nopass"
print (cmd)
os.system(cmd)

# signer le sertificat client
cmd2 = "/etc/openvpn/easy-rsa/easyrsa " + "sign-req " + "client " + Nclient
print (cmd2)
os.system(cmd2)

# copier les ressources dans le dossier client
privateroute = os.path.join('/etc/openvpn/easy-rsa/pki/private', Nclient )
privateroute += '.key'
shutil.copy(privateroute, route)

issuedroute = os.path.join('/etc/openvpn/easy-rsa/pki/issued', Nclient )
issuedroute += '.crt'
shutil.copy(issuedroute, route)

caroute = '/etc/openvpn/easy-rsa/pki/ca.crt'
shutil.copy(caroute, route)

fileconfovpnroute = '/etc/openvpn/client/clientconfovpn'
clientovpnroute = "/etc/openvpn/client/" + Nclient + "/" + Nclient + ".ovpn"
print (fileconfovpnroute)
print (clientovpnroute)

shutil.copy(fileconfovpnroute, clientovpnroute)

# éditer les fichier client.ovpn
cmd4 = "echo cert " + Nclient + ".crt >> /etc/openvpn/client/" + Nclient + "/" + Nclient + ".ovpn"
print (cmd4)
os.system(cmd4)

cmd5 = "echo key " + Nclient + ".key >> /etc/openvpn/client/" + Nclient + "/" + Nclient + ".ovpn"
print (cmd5)
os.system(cmd5)

# créer le répertoir client sur le poste client
cmd6 = "mkdir /home/" + Uclient + "/" + Nclient
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(IPclient, 22, Uclient, MDPclient)
stdin, stdout, stderr = ssh.exec_command(cmd6)

# envoyer les fichiers clients au client
ssh = SSHClient()
ssh.load_system_host_keys()
ssh.connect(IPclient, username=Uclient, password=MDPclient)
scp = SCPClient(ssh.get_transport())
cmd7 = "/etc/openvpn/client/" + Nclient + "/"
cmd8 = cmd7 + "ca.crt"
cmd9 = cmd7 + Nclient + ".crt"
cmd10 = cmd7 + Nclient + ".key"
cmd11 = cmd7 + Nclient + ".ovpn"
scp.put(cmd8)
scp.put(cmd9)
scp.put(cmd10)
scp.put(cmd11)

# copier les fichiers dans le répertoir
cmd12 = "/home/" + Uclient + "/"
cmd13 = cmd12 + "ca.crt " + cmd12 + Nclient + ".crt " + cmd12 + Nclient + ".key " + cmd12 + Nclient + ".ovpn "
cmd14 =  "cp " + cmd13 + cmd12 + Nclient + "/"
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(IPclient, 22, Uclient, MDPclient)
stdin, stdout, stderr = ssh.exec_command(cmd14)
cmd15 = "rm " + cmd13
print (cmd15)
ssh.connect(IPclient, 22, Uclient, MDPclient)

# établir la connection
cmd16 = "cd /home/" + Uclient + "/" + Nclient
cmd17 = "openvpn --config " + Nclient + ".ovpn"
ssh = paramiko.SSHClient()
ssh.set_mission_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(IPclient, 22, Uclient, MDPclient)
stdin, stdout, stderr = ssh.exec_command(cmd16)
dtdin, stdout, stderr = ssh.exec_command(cmd17)
