import math
import matplotlib.pyplot as plt
import numpy as np

# Define constants and initial setup
nbodies = 10  # Number of bodies (Sun + 9 planets including "My Planet")
AU = 1.495978707e11  # Astronomical Unit in meters
G = 6.6743e-11  # Gravitational constant (m^3 kg^-1 s^-2)

# Masses of celestial bodies (kg); most planets set to 0 except Sun and Earth
msun = 1.989e30
mearth = 5.972e24
mr = 0
mmer = 0
mven = 0
mmar = 0
mjup = 0
msat = 0
mura = 0
mnep = 0

# Calculate semi-major axis for "My Planet" based on student number
r = 0.4 + (8991 / 25000) * AU

# Initial velocity magnitude for circular orbit around the Sun
vmag = np.sqrt((G * msun) / AU)

# Arrays for masses and names of bodies
mass = [msun, mearth, mr, mmer, mven, mmar, mjup, msat, mura, mnep]
name_list = ['Sun', 'Earth', 'My Planet', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']

# Lists to store x and y positions for each body over time
xlist = []
ylist = []
for n in range(nbodies):
    xlist.append([])  # Initialize empty list for x positions of each body
    ylist.append([])  # Initialize empty list for y positions of each body

# Arrays for Runge-Kutta coefficients (position and velocity in x and y directions)
xa = np.zeros(nbodies)
vxa = np.zeros(nbodies)
xb = np.zeros(nbodies)
vxb = np.zeros(nbodies)
xc = np.zeros(nbodies)
vxc = np.zeros(nbodies)
xd = np.zeros(nbodies)
vxd = np.zeros(nbodies)

ya = np.zeros(nbodies)
vya = np.zeros(nbodies)
yb = np.zeros(nbodies)
vyb = np.zeros(nbodies)
yc = np.zeros(nbodies)
vyc = np.zeros(nbodies)
yd = np.zeros(nbodies)
vyd = np.zeros(nbodies)

# Lists to store position, velocity, and time values (though not used in plotting)
xvals = []
vxvals = []
yvals = []
vyvals = []
tvals = []

# Array to store orbital periods
t_orbit = np.zeros(nbodies)

# Initial positions (x-axis in meters), y positions set to 0
x = [0, AU, r, 0.4 * AU, 0.7 * AU, AU * 1.5, AU * 5.2, AU * 9.5, AU * 19.8, AU * 30]
y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Initial velocities
vx = np.zeros(nbodies)  # Initial x-velocity is 0
vy = np.zeros(nbodies)  # y-velocity will be set for circular orbits

# Arrays for storing previous y positions to detect orbit completion
yold = np.zeros(nbodies)

# Time step and maximum simulation time
dt = 86400  # Time step of 1 day (in seconds)
tmax = 86400 * 366 * 165  # Simulate for 165 Earth years to capture outer planets' orbits

# Initialize variable for Sun's acceleration (though Sun is stationary)
xa0 = 0

# Function to calculate x-component of acceleration due to gravity
def accx(x1, y1, x2, y2, mass):
    xdiff = x2 - x1  # Difference in x positions
    ydiff = y2 - y1  # Difference in y positions
    dist = np.sqrt(xdiff**2 + ydiff**2)  # Distance between bodies
    accx = (G * mass * xdiff) / dist**3  # Gravitational acceleration in x direction
    return accx

# Function to calculate y-component of acceleration due to gravity
def accy(x1, y1, x2, y2, mass):
    xdiff = x2 - x1  # Difference in x positions
    ydiff = y2 - y1  # Difference in y positions
    dist = np.sqrt(xdiff**2 + ydiff**2)  # Distance between bodies
    accy = (G * mass * ydiff) / dist**3  # Gravitational acceleration in y direction
    return accy

# Small offset for Earth's x position (possibly for numerical stability)
XE = x[1] + 1e-3

# Initialize time and flag for simulation loop
t = 0
flag = 0

# Set initial y-velocities for circular orbits around the Sun
for i in range(1, len(mass), 1):
    vy[i] = np.sqrt((G * msun) / x[i])  # Velocity for circular orbit: sqrt(G * M / r)

# Main simulation loop using 4th-order Runge-Kutta method
for t in np.arange(dt, tmax, dt):
    # Store previous y positions to detect orbit completion
    for n1 in range(1, len(mass), 1):
        yold[n1] = y[n1]  # Save current y position as "old" for next iteration

    # Calculate k1 coefficients for Runge-Kutta
    for n1 in range(1, len(mass), 1):
        xa[n1] = vx[n1]  # Velocity in x direction
        vxa[n1] = 0  # Initialize acceleration in x direction
        ya[n1] = vy[n1]  # Velocity in y direction
        vya[n1] = 0  # Initialize acceleration in y direction
        for n2 in range(0, len(mass), 1):
            if (n2 == n1):  # Skip self-interaction
                continue
            vxa[n1] += accx(x[n1], y[n1], x[n2], y[n2], mass[n2])  # Accumulate x acceleration
            vya[n1] += accy(x[n1], y[n1], x[n2], y[n2], mass[n2])  # Accumulate y acceleration

    # Calculate k2 coefficients for Runge-Kutta
    for n1 in range(0, len(mass), 1):
        xb[n1] = vx[n1] + dt * vxa[n1] / 2  # Intermediate velocity in x direction
        vxb[n1] = 0  # Initialize acceleration in x direction
        yb[n1] = vy[n1] + dt * vya[n1] / 2  # Intermediate velocity in y direction
        vyb[n1] = 0  # Initialize acceleration in y direction
        for n2 in range(0, 2, 1):  # Note: This range limits interactions to Sun and Earth
            if (n2 == n1):  # Skip self-interaction
                continue
            vxb[n1] += accx(x[n1] + (dt / 2) * xa[n1], y[n1] + (dt / 2) * ya[n1], x[n2] + (dt / 2) * xa[n2], y[n2] + (dt / 2) * ya[n2], mass[n2])  # Accumulate x acceleration
            vyb[n1] += accy(x[n1] + (dt / 2) * xa[n1], y[n1] + (dt / 2) * ya[n1], x[n2] + (dt / 2) * xa[n2], y[n2] + (dt / 2) * ya[n2], mass[n2])  # Accumulate y acceleration

    # Calculate k3 coefficients for Runge-Kutta
    for n1 in range(1, len(mass), 1):
        xc[n1] = vx[n1] + dt * vxb[n1] / 2  # Intermediate velocity in x direction
        vxc[n1] = 0  # Initialize acceleration in x direction
        yc[n1] = vy[n1] + dt * vyb[n1] / 2  # Intermediate velocity in y direction
        vyc[n1] = 0  # Initialize acceleration in y direction
        for n2 in range(0, 2, 1):  # Note: This range limits interactions to Sun and Earth
            if (n2 == n1):  # Skip self-interaction
                continue
            vxc[n1] += accx(x[n1] + (dt / 2) * xb[n1], y[n1] + (dt / 2) * yb[n1], x[n2] + (dt / 2) * xb[n2], y[n2] + (dt / 2) * yb[n2], mass[n2])  # Accumulate x acceleration
            vyc[n1] += accy(x[n1] + (dt / 2) * xb[n1], y[n1] + (dt / 2) * yb[n1], x[n2] + (dt / 2) * xb[n2], y[n2] + (dt / 2) * yb[n2], mass[n2])  # Accumulate y acceleration

    # Calculate k4 coefficients for Runge-Kutta
    for n1 in range(1, len(mass), 1):
        xd[n1] = vx[n1] + dt * vxc[n1]  # Intermediate velocity in x direction
        vxd[n1] = 0  # Initialize acceleration in x direction
        yd[n1] = vy[n1] + dt * vyc[n1]  # Intermediate velocity in y direction
        vyd[n1] = 0  # Initialize acceleration in y direction
        for n2 in range(0, 2, 1):  # Note: This range limits interactions to Sun and Earth
            if (n2 == n1):  # Skip self-interaction
                continue
            vxd[n1] += accx(x[n1] + dt * xc[n1], y[n1] + dt * yc[n1], x[n2] + dt * xc[n2], y[n2] + dt * yc[n2], mass[n2])  # Accumulate x acceleration
            vyd[n1] += accy(x[n1] + dt * xc[n1], y[n1] + dt * yc[n1], x[n2] + dt * xc[n2], y[n2] + dt * yc[n2], mass[n2])  # Accumulate y acceleration

    # Update positions and velocities using Runge-Kutta formula
    for n1 in range(1, len(mass), 1):
        x[n1] = x[n1] + (1 / 6) * (xa[n1] + 2 * (xb[n1] + xc[n1]) + xd[n1]) * dt  # Update x position
        vx[n1] = vx[n1] + (1 / 6) * (vxa[n1] + 2 * (vxb[n1] + vxc[n1]) + vxd[n1]) * dt  # Update x velocity
        y[n1] = y[n1] + (1 / 6) * (ya[n1] + 2 * (yb[n1] + yc[n1]) + yd[n1]) * dt  # Update y position
        vy[n1] = vy[n1] + (1 / 6) * (vya[n1] + 2 * (vyb[n1] + vyc[n1]) + vyd[n1]) * dt  # Update y velocity
        xlist[n1].append(x[n1])  # Store x position
        ylist[n1].append(y[n1])  # Store y position

    # Detect orbit completion by checking when body crosses the x-axis
    for n1 in range(1, len(mass), 1):
        if x[n1] > 0 and y[n1] * yold[n1] < 0:  # Check if body crosses x-axis
            t_orbit[n1] = t - dt * y[n1] / (y[n1] - yold[n1])  # Calculate orbital period

# Plot the orbits of the rocky planets (Earth, My Planet, Mercury, Venus, Mars)
plt.figure()
for n1 in range(1, 6):
    plt.plot(xlist[n1], ylist[n1], label=name_list[n1])  # Plot orbit for each rocky planet
plt.xlabel("X-Axis (m)")
plt.ylabel("Y-Axis (m)")
plt.title("Rocky Planets orbit")
plt.legend()
plt.savefig('test fig1')  # Save plot as 'test fig1'

# Plot the orbits of the gas giants (Jupiter, Saturn, Uranus, Neptune)
plt.figure()
for n1 in range(6, 10):
    plt.plot(xlist[n1], ylist[n1], label=name_list[n1])  # Plot orbit for each gas giant
plt.xlabel("X-Axis (m)")
plt.ylabel("Y-Axis (m)")
plt.title("Gassy Planets orbit")
plt.legend()
plt.savefig('test fig2')  # Save plot as 'test fig2'