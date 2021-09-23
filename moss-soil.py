import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.outliers_influence import summary_table
import pandas as pd
import matplotlib.pyplot as plt

rubriker = ["Date", "Sample", "Mass", "Height", "Live time", 
            "Energy-Cs", "FWHM-Cs", 	"Gross-Cs", "Net-Cs", "Error-Cs", 
            "Energy-K", "FWHM-K", "Gross-K", "Net-K", "Error-K", "Comment", "cps-Cs",	
            "cps/kg-Cs", "rel error-Cs", "cps-K", "cps/kg-K", "rel error-K"]

# Data-file:
df = pd.read_excel("IAEA-prover_Marielle_20210831.xlsx",sheet_name="moss-soil", names=rubriker, usecols="A:V", skiprows=2)


def fit(element):
    """Function that thake the argument of either Cs or K and calculate a second degree polynomial fit 
    between the mass and cps for the given element."""

    x = df["Mass"]
    y = df["cps-" + element]

    X = np.column_stack((x,x**2))
    X = sm.add_constant(X)

    # Fit regression model
    model = sm.OLS(y, X)
    # # Inspect the results
    result = model.fit()

    return result

###############################
ele = ["Cs", "K"]
###############################

results = []
ci_095_low = []
ci_095_high = []

# Getting a fit for both Cs and K as well as the Confidence interval:
for e in ele:
    results.append( fit(e) )

    st, data, ss2 = summary_table(fit(e), alpha=0.05)
    ci_095_low.append( data[:,4] )
    ci_095_high.append( data[:,5] )

m = np.arange(0,max(df["Mass"])+1, 1)
print("min m: ", np.min(m), " and the max m: ", np.max(m) )

# Printing the parameters for Cs-137 and K-40
for i in range(len(ele)):
    print("Parameters for "+ele[i] + " is:")
    print(results[i].params)

# 2nd degree:
Y_Cs = results[0].params[2]*m**2 + results[0].params[1]*m + results[0].params[0]
Y_K = results[1].params[2]*m**2 + results[1].params[1]*m + results[1].params[0]


# 425 Bq/kg for Cs-137 and 550 Bq/kg for K-40, 12 years ago. 
# See corr_massic_activity.py for the calculations
Bq_Cs = 0.322*m # Bq/g
Bq_K = 0.550*m  # Bq/g

###################################################################################
# # Plot:

# Data-points:
# plt.scatter(df["Mass"], df["cps-Cs"], label="Cs-137", s=15, color="blue",marker="*")
# plt.scatter(df["Mass"], df["cps-K"], label="K-40", s=15, color="green", marker="d")

# # Fit for Cs and the Confidence interval
# plt.plot(m, Y_Cs, label="fit Cs-137", color="blue")
# plt.fill_between(np.sort(df["Mass"]), np.sort(ci_095_low[0]), np.sort(ci_095_high[0]), color='blue', alpha=.2)

# # # Fit for K and the Confidence interval
# plt.plot(m, Y_K,  label="fit K-40", color="green")
# plt.fill_between(np.sort(df["Mass"]), np.sort(ci_095_low[1]),  np.sort(ci_095_high[1]), color='green', alpha=.2)

plt.plot(Y_Cs, Bq_Cs, label="Cs-137", color="blue")
plt.plot(Y_K, Bq_K, label="K-40", color="green")
plt.title("The relationship between the activity and the cps for moss-soil")
plt.xlabel("cps")
plt.ylabel("Activity [Bq]")
plt.legend(loc="upper right")


# plt.title("Result of the measurements for moss-soil")
# plt.legend(loc="upper left")
# plt.ylabel("cps")
# plt.xlabel("Mass [g]")

plt.ylim(0)
plt.xlim(0)
plt.grid()
plt.savefig("moss-soil_Bq_cps.png")
plt.show()
