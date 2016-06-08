# -*- coding: utf-8 -*-
"""
Script for calculation of PDN parameters
"""

# Things to import
from math import log10
from scipy.constants import epsilon_0
# Definition of physical properties
epsilon_r_F4    = 4.8 #Relative dielectric constant of Prepeg F-4
epsilon_r_Isola = 4 #Relative dielectric constant of Prepeg F-4
epsilon_r       = epsilon_r_Isola
epsilon         = epsilon_r*epsilon_0  #Dielectric constant of Prepeg F-4

"""
Functions definitions
"""
def func_L_trace(h_top,len_trace,w_trace,len_cap,w_cap):
    """ Capacitor trace inductance 
    Model dimensions are given in mil.
    Output inductance in pH.
    """
    ratio_trace = len_trace/w_trace
    ratio_cap = len_cap/w_cap
    return 32*h_top*(2*ratio_trace + ratio_cap)

def func_L_vias(h_top,s,D):
    """ Via pair loop inductance
    Model dimensions are given in mil.
    Output inductance in pH (1*10^-12H).
    """
    return  10*h_top*log10(2*s/D)
    
def func_L_spread(h_plane,B,D):
    """ Via pair loop inductance
    Model dimensions are given in mil.
    Output inductance in pH (1*10^-12H).
    """
    return 10*h_plane*log10(B/D)

m2mil = lambda x:x*39370.1
mil2m = lambda x:x*2.54E-5
"""
Dimensions definitions
"""

len_p_0603 = m2mil(1.6E-3)  # in m
w_p_0603   = m2mil(0.8E-3)  
len_p_0805 = m2mil(2E-3)  # in m
w_p_0805   = m2mil(1.25E-3)  


B         = m2mil(10E-3) #: Distance from cap to power pins
p_spacing = m2mil(1.2E-3)  #: Power pin spacing
D         = m2mil(0.2E-3)#: Pillar thickness
metal_1   = m2mil(35E-6) #: Thickness of metal in layer 1.
metal_2   = m2mil(18E-6) #: Thickness of metal in layer 2.
metal_3   = m2mil(18E-6) #: Thickness of metal in layer 3
metal_6   = m2mil(18E-6) #: Thickness of metal in layer 6.
metal_7   = m2mil(18E-6) #: Thickness of metal in layer 7.

h_prepeg_1    = m2mil(126E-6)#: Prepeg thickness btw 1 and 2.
h_laminate_1  = m2mil(107E-6)#: Prepeg thickness btw 1 and 2.

h_top_1       = h_prepeg_1 + metal_1
h_planes_1    = metal_2 + h_laminate_1 + metal_3#: Laminate btw 2 and 3.

len_trace = m2mil(0.9E-3) 
w_trace   = m2mil(0.8E-3) 
s_p_0603  = m2mil(3E-3) #2*len_trace + len_p_0603

L_trace  = func_L_trace(h_top_1, len_trace, w_trace, len_p_0603, w_p_0603)
L_vias   = func_L_vias(h_top_1, s_p_0603, D)
L_spread = func_L_spread(h_planes_1, B, D)

L_1 = L_trace+L_vias+L_spread

print(L_trace,L_vias,L_spread)
print(L_1)

h_prepeg_2    = m2mil(200E-6)#: Prepeg thickness btw 6 and 7.
h_laminate_2  = m2mil(200E-6)#: Prepeg thickness btw 6 and 7.

h_top_2    =  h_prepeg_2 + metal_1 # h_top for our PDN design stackup 
h_planes_2 =  metal_2 + h_laminate_2 + metal_3#: Laminate btw 2 and 3 for our PDN design stackup .

L_trace_2  = func_L_trace(h_top_2, len_trace, w_trace, len_p_0603, w_p_0603)
L_vias_2   = func_L_vias(h_top_2, s_p_0603, D)
L_spread_2 = func_L_spread(h_planes_2, B, D)

print(L_trace_2,L_vias_2,L_spread_2)
L_2 = L_trace_2+L_vias_2+L_spread_2
print(L_2)

ratio_stackups = L_2/L_1
print("ratio_stackups",ratio_stackups)

""" 
    Near to far effect in stackup 1 according 
    to model 
"""
h_top_far_1       = 3*h_prepeg_1 + 4*metal_2 + metal_1
h_planes_far_1    = metal_6 + h_laminate_1 + metal_7#: Laminate btw 2 and 3.
    
L_trace_far_1  = func_L_trace(h_top_far_1, len_trace, w_trace, len_p_0603, w_p_0603)
L_vias_far_1   = func_L_vias(h_top_far_1, s_p_0603, D)
L_spread_far_1 = func_L_spread(h_planes_far_1, B, D)

L_far_1 = L_trace_far_1 + L_vias_far_1 + L_spread_far_1

ratio_power_planes_1 = L_far_1/L_1
print("ratio power planes ",ratio_power_planes_1)

""" 
    Near to far effect in stackup 2 according 
    to model 
"""
h_top_far_2       = 3*h_prepeg_2 + 4*metal_2 + metal_1
h_planes_far_2    = metal_6 + h_laminate_2 + metal_7#: Laminate btw 2 and 3.
    
L_trace_far_2  = func_L_trace(h_top_far_2, len_trace, w_trace, len_p_0603, w_p_0603)
L_vias_far_2   = func_L_vias(h_top_far_2, s_p_0603, D)
L_spread_far_2 = func_L_spread(h_planes_far_2, B, D)

L_far_2 = L_trace_far_2 + L_vias_far_2 + L_spread_far_2

ratio_power_planes_2 = L_far_2/L_2
print("ratio power planes stackup 2",ratio_power_planes_2)


""" 
    Near to far effect according 
    to experiments by Kristian
"""
L_near_exp_1 = 657.1E-12 # H from layer 1-2 on experimental stackup
L_far_exp_1  = 980.3E-12 # H from layer 1-6 on experimental stackup

ratio_power_planes_exp = L_far_exp_1/L_near_exp_1
print("ratio power planes exp",ratio_power_planes_exp)

"""
    Capacitance due to power planes    
"""

C_planes_1_2 = epsilon * 60E-3 * 50E-3 /mil2m(h_laminate_2)

print("Powe planes 1-2 capacitance", C_planes_1_2)