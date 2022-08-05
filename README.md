# picobird
:bird: Picobird is a flappy bird clone for Raspberry Pi Pico written in [MicroPython](https://micropython.org/).

![3Across](https://user-images.githubusercontent.com/2415156/183221824-29199a7d-3a28-4896-a8cb-d716be9346ac.png)

## Features
- 🖤 2 colors! Black and White!
- 👾 Sprites drawn directly to the 1.14 inch display via [framebuf](https://docs.micropython.org/en/latest/library/framebuf.html)
- 🪫 Working battery indicator
- 💯 Persistent high score tracking
- 😓 Progressively harder difficulty

## Required Hardware 
![hardware](https://user-images.githubusercontent.com/2415156/183222730-2b366be4-843f-4d9b-9a0f-c80137af3bb2.jpg)
**This project was built using:**
1. [Raspberry Pi Pico.](https://www.raspberrypi.com/products/raspberry-pi-pico/) Any version as of 2022 should work.
2. [Waveshare 1.14inch LCD](https://www.waveshare.com/wiki/Pico-LCD-1.14)
3. (Optional) [Waveshare UPS-B.](https://www.waveshare.com/wiki/Pico-UPS-B) This allows the game to be played via battery.

## Getting Started

1. Assemble the hardware listed above.
2. Install [Thonny.](https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico/2)
3. Flash your Pico with [MicroPython.](https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico/3)
4. Copy all files in the `src` directory to the root level of your Pico's filesystem.
5. Press the Run button or F5 in Thonny.
