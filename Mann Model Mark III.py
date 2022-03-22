#!/usr/bin/env python
# coding: utf-8

# In[41]:


#Import necessary libraries
import numpy as np
import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar as cal
import datetime
from datetime import date
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

def model(d2d_q,network_q):
    from pandas.tseries.holiday import USFederalHolidayCalendar as cal
    #Today
    today = datetime.date.today()

    #Daily Close Rates
    p1 = 10 #Cameron   
    p2 = 10 #Jenna
    p3 = 2  #Amil
    p4 = 10 #Braxton
    p5 = 15  #Bob
    p6 = 0  #Amber
    p7 = 0  #Will
    ptotal = p1+p2+p3+p4+p5+p6+p7

    #Daily open rate
    network_open = 15
    d2d_open = 10

    #Capacity focus
    network_switch = .5
    d2d_switch = 1 - network_switch

    #Business Days and Holdiday Check
    dr = pd.bdate_range(start='today', end='2022-04-08')
    df = pd.DataFrame()
    df['Date'] = dr
    cal = cal()
    holidays = cal.holidays(start=dr.min(), end=dr.max())
    df['Holiday'] = df['Date'].isin(holidays)
    df["Check"] = df["Holiday"].astype(int)
    x=0

    #convert dataframe to arrays
    total_array = df.to_numpy()
    check_array = total_array[:,2]

    #Initiate lists and variables to append to for graphs
    network_list = []
    d2d_list = []
    i = 0
    l = 0

    #Queue Calc Loop
    for start in dr:
        if l < 1:
            l+=1
        elif check_array[i] == 0:
            daily_close = (ptotal)*.7
            network_q += network_open
            d2d_q += d2d_open
            if network_q >= int(daily_close*network_switch):
                network_q -= int(daily_close*network_switch)
                d2d_q -= int(daily_close*d2d_switch)
            elif network_q < int(daily_close*network_switch):
                if d2d_q >= int(daily_close*network_switch):
                    d2d_q -= int(daily_close - network_q)
                    network_q -= network_q
                elif d2d_q < int(daily_close*network_switch):
                    extra = int(daily_close - (d2d_q + network_q))
                    d2d_q -= d2d_q
                    network_q -= network_q
            else:
                break
        network_list.append(network_q) 
        d2d_list.append(d2d_q)
        i += 1
    return(network_list,d2d_list)

#Function to show graphs
def graph(some_list):
    plt.figure(figsize=(10,6))
    plt.bar(dr,some_list, color ='blue', width = 0.8)
    plt.xticks(dr)
    plt.xticks(rotation = 90)
    for i, v in enumerate(some_list):
        plt.text(dr[i], v+0.5, str(v))
    plt.xlabel('Date')
    plt.ylabel('Queue Running Total')
    if network_list == some_list:
        plt.title('Network Queue Consumption Profile')
    else:
        plt.title('Day to Day Consumption Profile')
    plt.show()


# In[42]:


model(168,23)


# In[43]:


graph(network_list)
graph(d2d_list)


# In[ ]:




