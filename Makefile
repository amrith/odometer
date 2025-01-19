all: 200.gif 500k.gif 1bb.gif p-200.gif p-500k.gif p-1bb.gif pa-1bb.gif pa-500k.gif pa-200.gif

200.gif: odometer.py
	python odometer.py --finish 200 --time 5 --mode DIGITAL --file 200.gif

500k.gif: odometer.py
	python odometer.py --finish 500000 --time 15 --mode DIGITAL --file 500k.gif

1bb.gif: odometer.py
	python odometer.py --finish 1000000000 --time 30 --mode DIGITAL --file 1bb.gif

p-200.gif: odometer.py
	python odometer.py --finish 200 --time 5 --mode ANALOG --file p-200.gif

p-500k.gif: odometer.py
	python odometer.py --finish 500000 --time 15 --mode ANALOG --file p-500k.gif

p-1bb.gif: odometer.py
	python odometer.py --finish 1000000000 --time 30 --mode ANALOG --file p-1bb.gif

pa-200.gif: odometer.py
	python odometer.py --finish 200 --time 5 --mode ANALOG_ALL --file pa-200.gif

pa-500k.gif: odometer.py
	python odometer.py --finish 500000 --time 15 --mode ANALOG_ALL --file pa-500k.gif

pa-1bb.gif: odometer.py
	python odometer.py --finish 1000000000 --time 30 --mode ANALOG_ALL --file pa-1bb.gif
