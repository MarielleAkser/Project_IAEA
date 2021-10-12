import numpy as np

# Time that have past since [15th Nov. 2009, 1st June 2006]:
t = [12, 15]

# Half-life:
T_12_Cs = 30.08 # years
T_12_K = 1.277*10**9 # years

# Decay-constant:
def decay_const(halflife):
    return np.log(2) / halflife

# Starting values [moss-soil, grass]:
N0_Cs = [425, 11320] #Bq/kg
N0_K = [550, 1060] #Bq/kg

N_Cs = []
N_K = []

# Cs-137
for i in range(len(N0_Cs)):
    N_Cs.append( N0_Cs[i] * np.exp( - decay_const(T_12_Cs) * t[i] ) )


# K-40
for i in range(len(N0_K)):
    N_K.append( N0_K[i] * np.exp( - decay_const(T_12_K) * t[i] ) )

print("Moss-soil")
print("Cs-137: ", N_Cs[0])
print("K-40: ", N_K[0])

print("Grass")
print("Cs-137: ", N_Cs[1])
print("K-40: ", N_K[1])