import matplotlib.pyplot as plt
import numpy as np

# ---- parameters ----
Lx = Ly = 1.0
nx = ny = 101  # number of grid point
k = 1.0  # thermal diffusivity

dx = Lx / (nx - 1)
dy = Ly / (ny - 1)

# ---- grid ----
x = np.linspace(0, Lx, nx)
y = np.linspace(0, Ly, ny)
X, Y = np.meshgrid(x, y, indexing="ij")

# ---- initial condition: narrow Gaussian at center (normalized) ----
x0, y0 = 0.5, 0.5
sigma = 0.03
u = np.exp(-((X - x0) ** 2 + (Y - y0) ** 2) / (2 * sigma**2))

# normalize
u = u / (u.sum() * dx * dy)

u[0, :] = 0
u[-1, :] = 0
u[:, 0] = 0
u[:, -1] = 0

# quick look
plt.imshow(u.T, origin="lower", extent=[0, 1, 0, 1])
plt.colorbar(label="temperature")
plt.title("Initial temperature (t=0)")
plt.xlabel("x")
plt.ylabel("y")
# plt.show()

dt = 0.8 * (dx**2 / (4 * k))
u_new = u.copy()

# FTCS update: only interior points (Dirichlet boundary kept as 0)
u_new[1:-1, 1:-1] = u[1:-1, 1:-1] + k * dt * (
    (u[2:, 1:-1] - 2 * u[1:-1, 1:-1] + u[:-2, 1:-1]) / dx**2
    + (u[1:-1, 2:] - 2 * u[1:-1, 1:-1] + u[1:-1, :-2]) / dy**2
)

# enforce Dirichlet boundary explicitly
u_new[0, :] = 0
u_new[-1, :] = 0
u_new[:, 0] = 0
u_new[:, -1] = 0

print("max before: ", u.max())
print("max after: ", u_new.max())
