import numpy as np   
from matplotlib import pyplot as plt   
from matplotlib import animation
from pyaudio import PyAudio, paInt16
import Queue
queue =Queue.Queue()
# first set up the figure, the axis, and the plot element we want to animate   
fig = plt.figure()   
ax = plt.axes(xlim=(0, 1), ylim=(-10000, 10000))   
line, = ax.plot([], [], lw=2)   
  
# initialization function: plot the background of each frame   
def init():   
    line.set_data([], [])   
    return line   
  
# animation function.  this is called sequentially   
def animate(i):   
    x = np.linspace(0, 2, 1000)   
    y = 30*np.sin(2 * np.pi * (x - 0.01 * i))
    line.set_data(x, y)
    return line

CHUNK         = 4096
FORMAT        = paInt16
CHANNELS      = 2
SAMPLING_RATE = 44100

#open audio stream
pa = PyAudio()
stream = pa.open(
				format   = FORMAT, 
				channels = CHANNELS, 
				rate     = SAMPLING_RATE, 
				input    = True,
				frames_per_buffer  = CHUNK
				)
NUM = 100
while NUM:
	wdata = np.fromstring(stream.read(CHUNK), dtype=np.short)
	wdata.shape = -1,2
	wdata = wdata.T
	queue.put(wdata[0])
	NUM -= 1

def update(i):
	x = np.linspace(0, 2, 4096)   
	data = queue.get()
	line.set_data(x, data)
	return line

# call the animator.  blit=true means only re-draw the parts that have changed.   
anim = animation.FuncAnimation(fig, update, init_func=init, frames=20, interval=1, blit=True)   
plt.show()