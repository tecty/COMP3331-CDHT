#!/bin/bash

# tmux new-session -d -s "CDHT" "python3 cdht.py 1 3 4 300 0.3"
# tmux split-window -v "python3 cdht.py  3 4 5 300 0.3"
# tmux split-window -h -t 0 "python3 cdht.py  10 12 15 300 0.3"
# tmux split-window -h -t 1 "python3 cdht.py  12 15 1 300 0.3"
# tmux split-window -h -t 0 "python3 cdht.py  15 1 3 300 0.3"
# tmux split-window -h -t 4 "python3 cdht.py  4 5 8 300 0.3"
# tmux split-window -h -t 5 "python3 cdht.py  5 8 10 300 0.3"
# tmux split-window -h -t 4 "python3 cdht.py  8 10 12 300 0.3"
# tmux a 

gnome-terminal  -t "Peer 1" -- bash -c 'python3  cdht.py 1 3 4 300 0.3; exec /bin/bash -i'  &
gnome-terminal  -t "Peer 3" -- bash -c 'python3  cdht.py  3 4 5 300 0.3; exec /bin/bash -i'  &
gnome-terminal  -t "Peer 4" -- bash -c 'python3  cdht.py  4 5 8 300 0.3; exec /bin/bash -i'  &
gnome-terminal  -t "Peer 5" -- bash -c 'python3  cdht.py  5 8 10 300 0.3; exec /bin/bash -i'  &
gnome-terminal  -t "Peer 8" -- bash -c 'python3  cdht.py  8 10 12 300 0.3; exec /bin/bash -i'  &
gnome-terminal  -t "Peer 10" -- bash -c 'python3 cdht.py  10 12 15 300 0.3; exec /bin/bash -i'  &
gnome-terminal  -t "Peer 12" -- bash -c 'python3 cdht.py  12 15 1 300 0.3; exec /bin/bash -i'  &
gnome-terminal  -t "Peer 15" -- bash -c 'python3 cdht.py  15 1 3 300 0.3; exec /bin/bash -i'  &