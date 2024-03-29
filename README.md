## Auto_storm overview:
A python program to automatically search and gather key information for storm surge modeling and validation projects


## Background and Motivation:
With the rapid advancement of computational science, we are able to construct all kinds of natural systems using mathematical models and numerical methods. Coastal hazards, which lies under the domain, is considered to be a major concern because nearly 40% of the world population reside close to the coastline. Among all coastal hazards, the most common, wide-spread hazard is the storm surge, which is the abnormal and significant rise of sea water level caused by storm systems like hurricanes and typhoons. Storm surges can be disastrous to coastal communities.

The **Clawpack** (Conservation Law Package) software suite is designed to solve nonlinear conservation law problems, balance laws, and many more other hyperbolic partial differential equations which are not necessarily in conservation form. **GeoClaw**, a variant of the Clawpack software, is developed to specifically solve the two-dimensional shallow water equations over topography for modeling various geophysical flows like hurricane, tsunami, or dam break. 

We will focus on modeling and validating water surge generated by storm systems using GeoClaw. The documentation for the original workflow can be found [here](https://github.com/mandli/surge-examples/tree/master/storm_setup). However, given the complexity of the procedure which includes data collection, run-time parameters selection, water level gauges selection, and etc., as well as the long program execution time, a python program was consequently developed to assist users on visualizing and auto-selecting most of the data before running the program. 

<font size="2">*Reference: Jinpai Zhao. Storm Surge Modeling and Validation. [Poster](https://github.com/MaxPaiPai/Research-Symposium-22/blob/main/Poster_Jinpai%20(Max)%20Zhao.pdf) Presentation at Columbia University Engineering Symposium, 2022*</font>


