## Introduction
Gm/Id design methodology is a good analog design tool.  Long time ago, I planned to work on it using the open-source PDK and the open-source design tools, but I could not plot the Gm/Id related plots in a user-friendly way.
Until recently With the help of generative AI, I successfully come up a python program to visualize different Gm/Id related plots based on the ngspice simulation results.
In this work, I use the [IIC-OSIC-TOOLS Docker Image](https://github.com/iic-jku/IIC-OSIC-TOOLS), in where I use the [IHP 130nm BiCMOS Open Source PDK](https://ihp-open-pdk-docs.readthedocs.io/en/latest/), [XSCHEM](https://github.com/StefanSchippers/xschem), and [NGSPICE](https://ngspice.sourceforge.io/), to simulate the data I need.  Then, the AI generated python program is used to visualize the following plots:
- Gm/Id vs Vgt (Vgt = Vgs - Vth)
- Gm/Gds vs Gm/Id
- fT vs Gm/Id
- Id/W vs Gm/Id
