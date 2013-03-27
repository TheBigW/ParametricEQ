ParametricEQ
============

A parametric equalizer plug-in for rhythmbox with up to 64 free configurable bands. I wrote it for the egoistical reason that I needed an EQ that helped me to get the low frequency response correct. There are several good tools that do that automatically (e.g. drc) but those require a microphone to measure the room response. There are also stand alone devices like antimode available, but why buy a separate device when you have a computer? :).

ere is a short description (more like poor mans guide :)) how to use this parametric EQ to improve your room response (especially for small rooms) and frequencies below 100 Hz.

Before you start to equalize or use any tools see if you can optimize your speaker placement (sub-woofer placement). There are several good sources ( just google 'optimal speaker placement' and same for sub woofer as this is a slightly different topic for lower frequencies). Remember: even the best tools will not be able to do anything against the laws of physics (bad speaker placement).

Another point to consider too are the acoustic properties of your room. For example in a concrete build cellar room with almost no furniture and worst case tiled floor it will be almost impossible to get any good sound. How to optimize that is best with acoustic treatment (absorbers, carpet etc.. google hint 'room acoustics')  

If all is set-up considering all above described parameters a parametric EQ can help you a lot to improve remaining non linearities. A linear response shall be the goal.
I use a downloaded frequency sweep (just google: 'mp3 sweep') as mp3 which goes step by step through all frequencies (be careful to lower the overall output volume before you start!!!).
You will recognize that some parts are played louder than others. To base it on more exact values you could measure with a SPL meter. You shall approximately write down where you discover peaks of loudness or absolute valleys of low volume. Its allays better to lower volume and remove peaks than to amplify if possible. So if you know the peaks you will also recognize the width in Hz of the peak. You can now define your EQ bands accordingly and lower the volume.
This will take some time and some recursions, but at the end you shall be able to have an quite linear response : now start and explore your music new :)!

Thanks to the guys of the rhythmbox IRC for their great help and the authors of the 10 band eq, which I used as a reference a lot! 

for installation just copy all files to HOME/.local/share/rhythmbox/plugins/ParametricEQ
