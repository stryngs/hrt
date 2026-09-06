HackRF Toolkit
==============================================================
<hr>

Overview:
---

* An attempt to modularize some of the features from GNU-Radio Companion for the HackRF

Goals:
---
* Give the user an easy way to switch between receiving and transmission without closing out the session
* Make the HackRF a life-saving 2-way communications tool in the event of disaster

To Do List:
---

* Add software amplification boost options for tx/rx modes
* Add the WAV and Siren flows to hrt
* Allow the user to change pitch and tone for the Siren flow
* Design a low-cost easy-to-build amplifier solution to increase the reception and transmission range
* Design a low-cost easy-to-build antenna solution for usage with different frequencies

How to use:
---
* `gcc usbreset.c -o usbreset`
* `sudo apt install libasound2-plugins pipewire-alsa`
* `git clone https://github.com/stryngs/hrt.git && cd hrt && python3 ./hrt`

Flowgraph development:
---
* Generate `fmRX.py` and `fmTX.py` from GNU Radio Companion into `flowgraphs/`.
* `lib/fmRX.py` and `lib/fmTX.py` are stable hrt wrappers around those generated files.

