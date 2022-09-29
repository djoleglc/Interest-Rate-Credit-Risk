
import math 
import matplotlib.pyplot as plt
import numpy as np 
from utils import *

term_structure = {1:6, 
                  2:5.8, 
                  3:5.620, 
                  4: 5.460, 
                  5:5.330,  
                  6: 5.250, 
                  7:5.200, 
                  8:5.160, 
                  9:5.125,
                  10: 5.1 }

cash_flow = {1:6, 
             2:8,
             3:106, 
             4: 7 ,
             5 : 0 ,
             6:102,
             7:3,
             8: 3,
             9: 3,
             10: 110 }

N = 100
maturity_b1 = 7
cr_b1 = 0.04
maturity_b2 = 8
cr_b2  = 0.1

cash_flow_b1, cash_flow_b2 = cash_flow_b(maturity_b1, N, cr_b1), cash_flow_b(maturity_b2, N, cr_b2)
    

price_port = price(cash_flow, term_structure)
price_b1 = price(cash_flow_b1, term_structure)
price_b2 = price(cash_flow_b2, term_structure)
print(f"Prices\nPort: {price_port}, B1: {price_b1}, B2: {price_b2}")

duration_port = duration(cash_flow, price_port, term_structure)
duration_b1 = duration(cash_flow_b1, price_b1, term_structure)
duration_b2 = duration(cash_flow_b2, price_b2, term_structure)
print(f"Durations\nPort: {duration_port}, B1: {duration_b1}, B2: {duration_b2}")

convexity_port = convexity(cash_flow, price_port, term_structure)
convexity_b1 = convexity(cash_flow_b1, price_b1, term_structure)
convexity_b2 = convexity(cash_flow_b2, price_b2, term_structure)
print(f"Convexity:\nPort: {convexity_port}, B1: {convexity_b1}, B2: {convexity_b2}")
print("")


#######################################################################

# convexity hedging

m = np.array([[ -duration_b1*price_b1, -duration_b2*price_b2 ], 
              [convexity_b1 *price_b1,  convexity_b2*price_b2]])
y = np.array([[duration_port*price_port], [-convexity_port*price_port]])

q = np.linalg.inv(m) @ y
print(f"Shares B1: {q[0].item()}")
print(f"Shares B2: {q[1].item()}")

#######################################################################


#shift yield curve 
initial_value = value_hedged(cash_flow, cash_flow_b1, cash_flow_b2, term_structure, q)
s = np.linspace(-0.2,0.2, 40)
terms = [shift(term_structure, 100 * j) for j in s]
values = [value_hedged(cash_flow, cash_flow_b1, cash_flow_b2, t, q) for t in terms]

plt.plot(s, np.array(values) - initial_value)
plt.plot(s, [0 for j in s], color ="red",  linestyle = "dotted")
plt.xlabel("Shift")
plt.ylabel("Value Change")
plt.title("Hedged Portfolio Value Change")
plt.show()




