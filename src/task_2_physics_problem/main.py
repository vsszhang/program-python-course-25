import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


def apply_dirichlet(u: np.ndarray) -> None:
    """Dirichlet BC: u=0 on the boundary (in-place)

    Args:
        u (np.ndarray): numpy array
    """
    u[0, :] = 0
    u[-1, :] = 0
    u[:, 0] = 0
    u[:, -1] = 0


def make_grid(Lx: float, Ly: float, nx: int, ny: int):
    """Make grid

    Args:
        Lx (float): number of grid point
        Ly (float):
        nx (int): number of grid point
        ny (int): number of grid point

    Returns:
        tuple: grid info
    """
    dx = Lx / (nx - 1)
    dy = Ly / (ny - 1)
    x = np.linspace(0, Lx, nx)
    y = np.linspace(0, Ly, ny)
    X, Y = np.meshgrid(x, y, indexing="ij")
    return x, y, X, Y, dx, dy


def make_initial_condition(X: np.ndarray, Y: np.ndarray, dx: float, dy: float):
    """Narrow Gaussian centered at (0.5, 0.5), normalized so sum*dx*dy ~= 1
       Constructing the initial temperature field

    Args:
        X (np.ndarray): X
        Y (np.ndarray): Y
        dx (float): dx
        dy (float): dy
    """
    # initial condition: narrow Gaussian at center (normalized)
    x0, y0 = 0.5, 0.5
    sigma = 0.03
    u0 = np.exp(-((X - x0) ** 2 + (Y - y0) ** 2) / (2 * sigma**2))

    # normalize
    u0 = u0 / (u0.sum() * dx * dy)
    apply_dirichlet(u0)
    return u0


def choose_dt_ftcs(k: float, dx: float, dy: float, safety: float = 0.8) -> float:
    """Stable dt for 2D FTCS heat equation with a safety factor
       Calculate the stable time step `dt`

    Args:
        k (float): _description_
        dx (float): _description_
        dy (float): _description_
        safety (float, optional): _description_. Defaults to 0.8.

    Returns:
        float: _description_
    """
    dt_max = 1.0 / (2.0 * k * (1.0 / dx**2 + 1.0 / dy**2))
    return safety * dt_max


def step_ftcs(u: np.ndarray, k: float, dt: float, dx: float, dy: float) -> np.ndarray:
    """One FTCS step. Returns a new array; does not modify input.

    Args:
        u (np.ndarray): _description_
        k (float): _description_
        dt (float): _description_
        dx (float): _description_
        dy (float): _description_

    Returns:
        np.ndarray: _description_
    """
    u_new = u.copy()

    # FTCS update: only interior points (Dirichlet boundary kept as 0)
    u_new[1:-1, 1:-1] = u[1:-1, 1:-1] + k * dt * (
        (u[2:, 1:-1] - 2 * u[1:-1, 1:-1] + u[:-2, 1:-1]) / dx**2
        + (u[1:-1, 2:] - 2 * u[1:-1, 1:-1] + u[1:-1, :-2]) / dy**2
    )
    apply_dirichlet(u_new)
    return u_new


def preview_initial(u0: np.array):
    plt.figure()
    plt.imshow(u0.T, origin="lower", extent=[0, 1, 0, 1])
    plt.colorbar(label="temperature")
    plt.title("Initial temperature (t=0)")
    plt.xlabel("x")
    plt.ylabel("y")


def run_preview_frames(
    u0: np.ndarray,
    k: float,
    dt: float,
    dx: float,
    dy: float,
    t_end: float,
    vis_every: int,
):
    n_steps = int(t_end / dt)
    u = u0.copy()

    plt.figure()
    for n in range(n_steps + 1):
        # visualize
        if n % vis_every == 0:
            plt.clf()
            im = plt.imshow(u.T, origin="lower", extent=[0, 1, 0, 1])
            plt.colorbar(im, label="temperature")
            plt.title(f"Temperature field, step={n}, t={n * dt:.6f}")
            plt.xlabel("x")
            plt.ylabel("y")
            plt.pause(0.001)
        u = step_ftcs(u, k, dt, dx, dy)


def run_animation(
    u0: np.ndarray,
    k: float,
    dt: float,
    dx: float,
    dy: float,
    t_end: float,
    vis_every: int,
):
    n_steps = int(t_end / dt)
    frames = max(1, n_steps // vis_every)

    u = u0.copy()

    # Fix color scale to avoid re-scaling each frame
    vmin, vmax = 0.0, float(u0.max()) * 0.1

    fig, ax = plt.subplots()
    im = ax.imshow(
        u.T,
        origin="lower",
        extent=[0, 1, 0, 1],
        vmin=vmin,
        vmax=vmax,
        aspect="auto",
    )
    fig.colorbar(im, ax=ax, label="temperature")

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    title = ax.set_title("")

    def update(frame_idx: int):
        nonlocal u
        for _ in range(vis_every):
            u = step_ftcs(u, k, dt, dx, dy)

        # Update the image once per frame (after advancing vis_every steps)
        im.set_data(u.T)
        title.set_text(f"Temperature field, t={(frame_idx * vis_every * dt):.6f}")
        return (im, title)

    ani = FuncAnimation(fig, update, frames=frames, interval=30, blit=False)
    return fig, ani


def main():
    # ---- parameters ----
    Lx = Ly = 1.0
    nx = ny = 101

    k = 1.0

    # ---- grid + init ----
    _, _, X, Y, dx, dy = make_grid(Lx, Ly, nx, ny)
    u0 = make_initial_condition(X, Y, dx, dy)

    #  ---- dt (stable) ----
    dt = choose_dt_ftcs(k, dx, dy, safety=0.8)
    print("dx = ", dx)
    print("dt = ", dt)

    # ---- step-5 preview ----
    t_end = 0.05
    vis_every = 10
    fig, ani = run_animation(u0, k, dt, dx, dy, t_end, vis_every)

    plt.show()


if __name__ == "__main__":
    main()
