## Introduction
Gm/Id design methodology is a good analog design tool.  Long time ago, I planned to work on it using the open-source PDK and the open-source design tools, but I could not plot the Gm/Id related plots in a user-friendly way.  Until recently With the help of generative AI, I successfully come up a python program to visualize different Gm/Id related plots based on the ngspice simulation results.  In this work, I use the [IIC-OSIC-TOOLS Docker Image](https://github.com/iic-jku/IIC-OSIC-TOOLS), in where I use the [IHP 130nm BiCMOS Open Source PDK](https://ihp-open-pdk-docs.readthedocs.io/en/latest/), [XSCHEM](https://github.com/StefanSchippers/xschem), and [NGSPICE](https://ngspice.sourceforge.io/), to simulate the data I need.  Then, the AI generated python program is used to visualize the following plots:
- Gm/Id vs Vgt (Vgt = Vgs - Vth)
- Gm/Gds vs Gm/Id
- fT vs Gm/Id
- Id/W vs Gm/Id

## XSCHEM Schematic Explain
In this schematic (Fig. 1), NMOS is used as an example.  The simulation sweeps the VGS voltage and keep the VDS at a constant value.  Be reminded to set the VDS value closed to the actual bias point in your circuit.  The VGS sweep is repeated for each channel length specified by the user:
```
foreach Lnow 0.5 1.0 1.5 2.0 5.0 10
```

Fig. 1:  Screen capture of the schematic

Once the simulation is completed.  Four data files are generated in the 'simulations' directory.  They are:
- gmid_vgt.dat
- gain_gmid.dat
- ft_gmid.dat
- idw_gmid.dat

Then, we can execute the python code and select the data file to show the plot (Right now the python code can only show the data from one file.  However, we can execute the python code 4 times :p) 
```
python gmid_plot.py &
```
After the above command is executed, we have to select the data file (Fig. 2)

<img src="/images/select_gmid_file.png" width="320px" ><br>
Fig. 2:  Data file selection

Following are screen captures of all four Gm/Id related plots.  The python program has a vertical cursor for you to check all the y-axis values at the same time.  Take the Gain vs Gm/Id plot as an example, we can check how the gain and also the gds is affected by the channel length under the same Gm/Id value.

<img src="/images/gmid_vgt.png" width="640px" ><br>
Fig. 3:  Gm/Id vs Vgt.  From this plot we can choose the Gm/Id value based on the required Gm (e.g., controlled by bandwidth) and the sepcified IQ specification.  Be reminded we have to check the Vgt to make sure it is not either too small (e.g., negaitve) and too large.  A too small Vgt can introduce mismatch and noise issues that may not be included in the model.  Once Vgt is too large, the minimum VDD headroom can be impacted.

<img src="/images/gain_gmid.png" width="640px" ><br>
Fig. 4:  Gain vs Gm/Id.  Assume the Gm/Id value is chosen.  From this plot we can choose the required channle length based on the required intrinsic gain (e.g., gm/gds) or the required output resistance (e.g., 1/gds).

<img src="/images/ft_gmid.png" width="640px" ><br>
Fig. 5:  fT vs Gm/Id.  Assume the Gm/Id and the channel length values are chosen.  From this plot we can check whether the fT is high enough for our design target.  Of course, if the fT is smaller than what we need.  We have to trade off between the gain and the fT.

<img src="/images/idw_gmid.png" width="640px" ><br>
Fig. 6:  Id/W vs Gm/Id.  Assume the Gm/Id and the channel length values are chosen, and the bias current (Id) is known.  Then, we can use this plot to retrieve the total width of the transistor.  At this point, we know the W and L of your transistor design :).
