import numpy as np

# The relationship between cps and the mass for moss-soil and the grass
# See moss-soil.py and grass.py for how the parameters were obtained
def C_soil(mass):
    return -0.000056*mass**2 + 0.009808*mass + 0.003617

def C_grass(mass):
    return -0.001059*mass**2 + 0.201450*mass + 0.065212


# The corrected values for the massic activity.
# See corr_massic_activity.py for the calculations
A_grass = 8012
A_soil = 322 


def calc_other(mass, type, cps):
    """Function that can be used for calculating the activity of a sample given a mass and if the sample is
    similar to either 'grass' or 'moss-soil'.
    The fuction takes the arguments: 
        - The mass of the sample (in gram)
        - What type of sample it is, either 'grass' or 'moss-soil'
        - The measured cps 
    
    The funtion then return both the calculated C_i and A_sample"""

    if (type == "grass"):
        C_i = C_grass(mass)
        A_sample = ( cps / C_i ) * A_grass

    elif (type == "moss-soil"):
        C_i = C_soil(mass)
        A_sample = ( cps / C_i ) * A_soil

    return C_i, A_sample


mass_mushrooms = [43.2, 19.75, 24.09, 28.7, 16.67]
cps_mushrooms = [12.04, 5.963, 7.683, 1.560, 1.073]

# Printing the values for C_i and A_sample for the mushrooms samples
for i in range(len(mass_mushrooms)):
    print(" MUSHROOMS ")
    print("C_i and A_sample for sample ", i+1," is:")
    print( calc_other(mass_mushrooms[i], "grass", cps_mushrooms[i]), "\n")


mass_sediment = [9.29, 9.67]
cps_sediment = [0.031, 0.096]

# Printing the values for C_i and A_sample for the sediment samples
for i in range(len(mass_sediment)):
    print(" SEDIMENT ")
    print("C_i and A_sample for sample ", i+1," is:")
    print( calc_other(mass_sediment[i], "moss-soil", cps_sediment[i]), "\n")


# The uncertainties
err_mass= 0.01
err_cps_mushrooms = [0.08, 0.1, 0.115, 0.03, 0.042]
err_cps_sediment =[0.002, 0.004]

err_Ci = 0.05


def calc_err_A_sample(mass, err_cps, cps):
    """Function to calculate the error in A_sample"""
    return ( (err_mass/mass)**2 + (err_cps/cps)**2 + err_Ci**2 )**0.5


# Printing the values for error in A_sample for the mushroom samples
for i in range(len(err_cps_mushrooms)):
    _ , A_s = calc_other(mass_mushrooms[i], "grass", cps_mushrooms[i])

    print(" MUSHROOMS ")
    print("Error for A_sample nr", i+1," is:")
    print( calc_err_A_sample(mass_mushrooms[i], err_cps_mushrooms[i], cps_mushrooms[i] ) * A_s, "\n")


# Printing the values for error in A_sample for the sediment samples
for i in range(len(err_cps_sediment)):
    _ , A_s = calc_other(mass_sediment[i], "grass", cps_sediment[i])

    print(" SEDIMENT ")
    print("Error for A_sample nr", i+1," is:")
    print( calc_err_A_sample(mass_sediment[i], err_cps_sediment[i], cps_sediment[i] ) * A_s, "\n")
