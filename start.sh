#!/bin/bash



gnome-terminal  -t "Peer 1" -- python3 cdht.py 1 3 4 300 0.3 &
gnome-terminal  -t "Peer 3" -- python3 cdht.py  3 4 5 300 0.3 &
gnome-terminal  -t "Peer 4" -- python3 cdht.py  4 5 8 300 0.3 &
gnome-terminal  -t "Peer 5" -- python3 cdht.py  5 8 10 300 0.3 &
gnome-terminal  -t "Peer 8" -- python3 cdht.py  8 10 12 300 0.3 &
gnome-terminal  -t "Peer 10" -- python3 cdht.py  10 12 15 300 0.3 &
gnome-terminal  -t "Peer 12" -- python3 cdht.py  12 15 1 300 0.3 &
gnome-terminal  -t "Peer 15" -- python3 cdht.py  15 1 3 300 0.3 &