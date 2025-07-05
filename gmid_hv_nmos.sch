v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -110 70 -110 90 {
lab=GND}
N -110 -0 -110 10 {
lab=#net1}
N 20 30 20 90 {
lab=GND}
N 150 30 150 90 {
lab=GND}
N 20 -70 20 -30 {
lab=#net2}
N 150 -70 150 -30 {
lab=#net3}
N 20 0 70 0 {
lab=GND}
N 70 0 70 90 {
lab=GND}
N 20 -70 50 -70 {
lab=#net2}
N 110 -70 150 -70 {
lab=#net3}
N -110 0 -20 0 {
lab=#net1}
C {devices/code_shown.sym} -200 160 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib cornerMOShv.lib mos_tt
"}
C {devices/code_shown.sym} 240 -310 0 0 {name=NGSPICE only_toplevel=true 
value="
.param temp=27
.control

set filetype=ascii
save @N.XM1.Nsg13_hv_nmos[ide] @N.XM1.Nsg13_hv_nmos[vgt] 
save @N.XM1.Nsg13_hv_nmos[gm]  @N.XM1.Nsg13_hv_nmos[gds] 
save @N.XM1.Nsg13_hv_nmos[cgg] @N.XM1.Nsg13_hv_nmos[w]

set wr_vecnames
foreach Lnow 0.5 1.0 1.5 2.0 5.0 10 
alter @N.XM1.Nsg13_hv_nmos[l]=$Lnow*1e-6
dc Vgs 0.0 3.0 0.01
let n=$Lnow
let vgt\{$&n\}=@N.XM1.Nsg13_hv_nmos[vgt]
let gmid\{$&n\}=@N.XM1.Nsg13_hv_nmos[gm]/@N.XM1.Nsg13_hv_nmos[ide]
let gain\{$&n\}=@N.XM1.Nsg13_hv_nmos[gm]/@N.XM1.Nsg13_hv_nmos[gds]
let idw\{$&n\}=@N.XM1.Nsg13_hv_nmos[ide]/@N.XM1.Nsg13_hv_nmos[w]
let ft\{$&n\}=@N.XM1.Nsg13_hv_nmos[gm]/(2*pi*@N.XM1.Nsg13_hv_nmos[cgg])
wrdata gmid_vgt.dat gmid\{$&n\} vs vgt\{$&n\}
wrdata gain_gmid.dat gain\{$&n\} vs gmid\{$&n\}
wrdata ft_gmid.dat ft\{$&n\} vs gmid\{$&n\}
wrdata idw_gmid.dat idw\{$&n\} vs gmid\{$&n\}
set appendwrite

end

.endc
"}
C {devices/gnd.sym} 20 90 0 0 {name=l1 lab=GND}
C {devices/gnd.sym} -110 90 0 0 {name=l2 lab=GND}
C {devices/vsource.sym} -110 40 0 0 {name=Vgs value=0.75}
C {devices/vsource.sym} 150 0 0 0 {name=Vds value=1.0
}
C {devices/gnd.sym} 150 90 0 0 {name=l3 lab=GND}
C {devices/gnd.sym} 70 90 0 0 {name=l4 lab=GND}
C {devices/title.sym} -130 260 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {devices/ammeter.sym} 80 -70 1 0 {name=Vd}
C {sg13g2_pr/sg13_hv_nmos.sym} 0 0 0 0 {name=M1
l=0.45u
w=10u
ng=1
m=1
model=sg13_hv_nmos
spiceprefix=X
}
