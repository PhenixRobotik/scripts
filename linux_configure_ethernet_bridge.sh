#!/usr/bin/env bash
exit 1

##### méthode plus générique

# sur le pc a configurer une fois
yay -S --needed hostapd
sudo dnsmasq hostapd
sudo systemctl stop dnsmasq
sudo systemctl stop dhcpcd ou hostapd


nano /etc/dhcpcd.conf

interface enp3s25 #nom de l'interface ethernet
static ip_address=192.168.5.1/24


nano /etc/dnsmasq.conf

interface=enp3s25
dhcp-range=192.168.5.20,192.168.5.40,255.255.255.0,24h
dhcp-host=mac,ip


# pour démarrer le pont
sudo systemctl start dnsmasq
sudo systemctl start dhcpcd

echo 1 > /proc/sys/net/ipv4/ip_forward
iptables -t nat -A POSTROUTING -o wlo1 -j MASQUERADE
iptables -A FORWARD -i enp3s0 -o wlo1 -j ACCEPT
iptables -A FORWARD -i wlo1 -o enp3s0 -m state --state RELATED,ESTABLISHED -j ACCEPT
#pour un accès depuis l'extérieur ramplacer la dernière ligne par:
iptables -A FORWARD -i wlo1 -o enp3s0 -j ACCEPT

# depuis un pc sur un réseau extérieur:
route add -net 192.168.4.0 netmask 255.255.255.0 gw 192.168.0.94
réseau et ip du pc qui fait le pont

###############################################################################

##### méthode rudimentaire

cat /etc/network/interfaces

# interfaces(5) file used by ifup(8) and ifdown(8)
# Include files from /etc/network/interfaces.d:
source-directory /etc/network/interfaces.d

auto eth0
iface eth0 inet static
  address 192.168.1.1
  netmask 255.255.255.0
  gateway 192.168.1.2
  dns-nameservers 1.1.1.1 9.9.9.9


# regler l'ip du pc sur 192.168.1.2
# et executer a chaque démarrage pour accéder à internet depuis la carte
#(changer le nom des interfaces si nécessaire)

sudo echo 1 > /proc/sys/net/ipv4/ip_forward
sudo iptables -t nat -A POSTROUTING -o wlo1 -j MASQUERADE
sudo iptables -A FORWARD -i enp3s0 -o wlo1 -j ACCEPT
sudo iptables -A FORWARD -i wlo1 -o enp3s0 -m state --state RELATED,ESTABLISHED -j ACCEPT
