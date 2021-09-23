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
df = pd.read_excel("IAEA-prover_Marielle_20210831.xlsx",sheet_name="data", names=rubriker, usecols="A:V", skiprows=2) # Skipping the first 5 rows

burk_A180 = df[df["Sample"].str.contains("A180")]  
burk_A10 = df[df["Sample"].str.contains("A10")]  
burk_60P = df[df["Sample"].str.contains("60P")]  

def fit(element, burk="all"):
    """Function that take two arguments: an element and what type of cointainer. 
    The element is either: Cs or K.
    The cointainer by default is all, but can be: A180, 60P or A10.
    
    The function then make a second degree polynomial fit between the mass and cps for the given element and cointainer."""


    if (burk == "all"):
        x = df["Mass"]
        y = df["cps-" + element]
    else:
        data = df[df["Sample"].str.contains(burk)]
        x = data["Mass"]
        y = data["cps-" + element]

    
    X = np.column_stack((x,x**2))
    X = sm.add_constant(X)

    # # Fit regression model
    model = sm.OLS(y, X)
    result = model.fit()

    return result


#################################
ele = "K"
#################################

different_coontainer = ["A180", "A10", "60P"]

m = []
parameters = []
# Obtaining the parameters for the fits for the different cointainers
# Aswell as creating the an array for the x-values
for b in different_coontainer:
    con = df[df["Sample"].str.contains(b)]
    m.append( np.arange(0,max(con["Mass"])+1, 1) )

    results = fit(ele , b)
    parameters.append( results.params )

Y = []
# Getting the Y-vaules using the fit-parameters and the x-values for the for-loop above
for i in range(len(different_coontainer)):
    mass = m[i]
    Y.append( parameters[i][2]*mass**2 + parameters[i][1]*mass + parameters[i][0] )

# Make a fit for all the data-points:
all = fit(ele)
all_m = np.arange(0,max(df["Mass"])+1, 1)
all_Y = all.params[2]*all_m**2 + all.params[1]*all_m + all.params[0]

# print( all.summary() )

# Confidence interval:
st, data, ss2 = summary_table(all, alpha=0.05)
ci_095_low = data[:,4]
ci_095_high = data[:,5]


###################################################################################
# # # Plot:
# plt.scatter(MASS_1, CPS_1)
# plt.scatter(MASS_2, CPS_2)

# Data for the different containers
plt.scatter(burk_A180["Mass"], burk_A180["cps-"+ele], label="A180", marker=".")
plt.scatter(burk_A10["Mass"], burk_A10["cps-"+ele], label="A10", marker=".")
plt.scatter(burk_60P["Mass"], burk_60P["cps-"+ele], label="60P", marker=".")

# The fit for the three different containers
plt.plot(m[0], Y[0], label="fit for "+different_coontainer[0], linestyle="dashed")
plt.plot(m[1], Y[1], label="fit for "+different_coontainer[1], linestyle="dashed")
plt.plot(m[2], Y[2], label="fit for "+different_coontainer[2], linestyle="dashed")

# Fit using all the data-points
plt.plot(all_m, all_Y, label="fit for all", color="red")
plt.fill_between(np.sort(df["Mass"]), np.sort(ci_095_low), np.sort(ci_095_high), color='red', alpha=.2)

plt.legend()
plt.ylim(0)
plt.xlim(0)
plt.title("Result of the measurements of K-40 for grass")
plt.xlabel("Mass [g]")
plt.ylabel("cps")
plt.grid()
plt.savefig("grass_all+trends_"+ele+".png")
plt.show()
