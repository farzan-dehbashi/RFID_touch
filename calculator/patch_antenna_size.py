import math

er= 2
freq = 919.0*1000*1000#hz
c= 299792458.0 #m/s
h= 0.005 #m
Lambda = c/freq
print('lambda = '+str(Lambda) + " (m)")

############
w=(c/(2*freq)) *(math.sqrt(2/(1+er)))
print("w = "+str(w)+" (m)")

############# effective dielectric constant
effectiveE = ((er+1)/2) + ((er-1)/2)*(1/(math.sqrt(1+12*(h/w))))
print('effective E = '+str(effectiveE))

############effective l
effectiveL = Lambda * (0.5) * (1/(math.sqrt(effectiveE)))
print('effective L = '+str(effectiveL)+' (m)')

############
deltaL = 0.412*h*(((effectiveE+0.3)*((w/h +0.264)))/((effectiveE-0.258)*(w/h+0.8)))
print('delta L = '+str(deltaL)+' (m)')
###########
L = effectiveL - 2* deltaL
print('L = '+str(L))