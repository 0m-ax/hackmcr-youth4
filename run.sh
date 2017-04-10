#!/bin/bash
cd /home/pi/woo
screen -d -m node index
screen -d -m python pi.py
