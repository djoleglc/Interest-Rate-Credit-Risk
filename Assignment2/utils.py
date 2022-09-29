
import math 
import matplotlib.pyplot as plt
import numpy as np 


def cash_flow_b(maturity, N, cr):
    cf = {}
    for j in range(1, maturity+1):
        if j == maturity: 
            cf[j] = cr * N + N
        else:
            cf[j] = cr * N
    return cf
   
    
       
def price(cash_flow, term_structure):
    price_bond = 0 
    for j in range(1, len(cash_flow)+1):
        disc = math.exp(j * -term_structure[j]/100) 
        price_bond += disc * cash_flow[j]
    return price_bond
   
   
def duration(cash_flow, price, term_structure):
    duration = 0
    for j in range(1, len(cash_flow)+1):
        disc = math.exp(j* -term_structure[j]/100) 
        duration += disc * cash_flow[j] * j
    duration = duration/price
    return duration 


def convexity(cash_flow, price, term_structure):
    convexity = 0
    for j in range(1, len(cash_flow)+1):
        disc = math.exp(j * -term_structure[j]/100) 
        convexity += disc * cash_flow[j] * j**2
    convexity = convexity/price
    return convexity 
    


def shift(t,s):
    shifted = {}
    for j in t.keys():
        shifted[j] = s + t[j]
    return shifted

def value_hedged(cash_flow, cash_flow_b1, cash_flow_b2, term_structure, q):
    price_port = price(cash_flow, term_structure)
    price_b1 = price(cash_flow_b1, term_structure)
    price_b2 = price(cash_flow_b2, term_structure)
    return price_port + q[0]*price_b1 + q[1]*price_b2