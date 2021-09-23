import numpy as np

# Time that have past since 15th Nov. 2009:
t = 12

# Half-life:
T_12_Cs = 30.08
T_12_K = 1.277*10**9 

# Decay-constant:
def decay_const(halflife):
    return np.log(2) / halflife

# Starting values:
N0_Cs = 425 /10**3 #Bq/g
N0_K = 550 /10**3 #Bq/g

N_Cs = N0_Cs * np.exp( - decay_const(T_12_Cs) * t )
print("Cs-137: ", N_Cs)


N_K = N0_K * np.exp( - decay_const(T_12_K) * t )
print("K-40: ", N_K)