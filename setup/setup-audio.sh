#!/usr/bin/bash

sudo modprobe snd-bcm2835                      # load module for single boot
echo "snd-bcm2835" | sudo tee -a /etc/modules  # load module for persistance
pulseaudio -D
amixer cset numid=3 1

