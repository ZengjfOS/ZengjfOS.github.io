echo "sudo src/dnsmasq --keep-in-foreground --no-poll --dhcp-authoritative  --pid-file -C dnsmasq.conf.example -r /run/dnsmasq/resolv.conf -q"
sudo src/dnsmasq --keep-in-foreground --no-poll --dhcp-authoritative  --pid-file -C dnsmasq.conf.example -r /run/dnsmasq/resolv.conf -q

# sudo gdb src/dnsmasq 
