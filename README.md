ParametricEQ
============

A parametric equalizer plugin for rhythmbox with up to 64 free configurable bands. I wrote it for the egoistic reason that I needed an EQ that helps me to get the low frequency response right. There are several good tools that do that even automatic (e.g. drc), but those require a microphone to measure the room response. There are also stand alone devices like antimode available, but why buy a separate device when you have a computer :).

Here is a short description (more like poor mans guide :)) how to use this parametric EQ to improve your room response (especially for small rooms) and requencies below 100 Hz. Before you start to equalize oir use any tools see if you can optimize your speaker placement (subwoofer placement). There are several good sources - just google. Remember: even the best tools will not be able to do anything against the laws of physics (bad spaeker placement).

I use a downloaded frequency (just google: 'mp3 sweep') sweep as mp3 which goes step by step through all frequencies (be carefull to lower the overall output volume before you start!!!).
You will recognize that some parts are played louder than others. To quantitize that you could measure with a SPL meter. You shall apx. write down where you discover peaks of loudness or absolute valeays of low volume. Its allways better to lower volume and remove peaks than to amplify if possible. So if you know the peaks you will also apx. the width in Hz of the peak. You can now define your EQ bands accordingly and lower the volume.
This will take some time and some recursions, but at the end you shall be able to have an quite linear response : now start and explore your music new :)!

Thanks to the guys of the rhythmbox IRC for their great help and the authors of the 10 band eq, which I used as a reference a lot! 

for installation just copy all files to HOME/.local/share/rhythmbox/plugins/ParametricEQ
