# Robot-Song

This is the code for the "Grippers on the Robot" song, an intereactive children song and dance that runs on Baxter. 

This code uses PyAudio to play the music files, which can be downloaded from their website: https://people.csail.mit.edu/hubert/pyaudio

Once you have PyAudio working, all you need to do is run singing.py, which can be done by going into the correct directory and running python singing.py.

If you wish to only do certian parts of the dance, you can go into the singing.py file, go to the ask method of EinClientBoth, and switch the order of the three dance functions, gripprs, servos, and IK.
