## Introduction
Gm/Id design methodology is a good analog design tool.  Long time ago, I planned to work on it using the open-source PDK and the open-source design tools, but I could not plot the Gm/Id related plots in a user-friendly way.  Until recently With the help of generative AI, I successfully come up a python program to visualize different Gm/Id related plots based on the ngspice simulation results.  In this work, I use the [IIC-OSIC-TOOLS Docker Image](https://github.com/iic-jku/IIC-OSIC-TOOLS), in where I use the [IHP 130nm BiCMOS Open Source PDK](https://ihp-open-pdk-docs.readthedocs.io/en/latest/), [XSCHEM](https://github.com/StefanSchippers/xschem), and [NGSPICE](https://ngspice.sourceforge.io/), to simulate the data I need.  Then, the AI generated python program is used to visualize the following plots:
- Gm/Id vs Vgt (Vgt = Vgs - Vth)
- Gm/Gds vs Gm/Id
- fT vs Gm/Id
- Id/W vs Gm/Id

## XSCHEM Schematic Explain
In this schematic, NMOS is used as an example.  The simulation sweeps the VGS voltage and keep the VDS at a constant value.  Be reminded to set the VDS value closed to the actual bias point in your circuit.  The VGS sweep is repeated for each channel length specified by the user:
```
foreach Lnow 0.5 1.0 1.5 2.0 5.0 10
```
Once the simulation is completed.  Four data files are generated in the 'simulations' directory.  They are:
- gmid_vgt.dat
- gain_gmid.dat
- ft_gmid.dat
- idw_gmid.dat
Then, we can execute the python code and select the data file to show the plot (Right now the python code can only show the data from one file.  However, we can execute the python code 4 times :p) 
```
python gmid_plot.py &
```



