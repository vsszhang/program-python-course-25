# Task 2 Physics problem

## 1. Main Call Flow (Execution Order)

1. **`main()`**  
   → program entry point, coordinates the whole simulation

2. **`make_grid(Lx, Ly, nx, ny)`**  
   → create spatial grid and grid spacing

3. **`make_initial_condition(X, Y, dx, dy)`**  
   → build the initial temperature field  
   → internally calls **`apply_dirichlet(u)`**

4. **`choose_dt_ftcs(k, dx, dy, safety)`**  
   → compute a stable time step for the FTCS scheme

5. **`run_animation(u0, k, dt, dx, dy, t_end, vis_every)`**  
   → set up the animation window and color scale  
   → internally registers **`update(frame_idx)`**

6. **`update(frame_idx)`** *(called repeatedly by Matplotlib)*  
   → advance the solution in time  
   → internally calls **`step_ftcs(u, k, dt, dx, dy)`** multiple times

7. **`step_ftcs(u, k, dt, dx, dy)`**  
   → perform one FTCS update step  
   → internally calls **`apply_dirichlet(u_new)`**

8. **`plt.show()`**  
   → start the GUI event loop and play the animation

---

## 2. Functions and Their Meanings

- **`main()`**  
  Controls the entire simulation workflow.

- **`make_grid()`**  
  Creates a uniform 2D spatial grid and grid spacing.

- **`make_initial_condition()`**  
  Generates the initial temperature field using a centered Gaussian heat source.

- **`apply_dirichlet()`**  
  Enforces zero temperature on the domain boundary.

- **`choose_dt_ftcs()`**  
  Computes a stable time step according to the FTCS stability condition.

- **`step_ftcs()`**  
  Advances the temperature field by one explicit FTCS time step.

- **`run_animation()`**  
  Builds and runs a smooth Matplotlib animation of the temperature field.

- **`update()`**  
  Updates the solution and visualization for each animation frame.

---

## 3. Summary

The program follows the pattern:  
**initialize → discretize → time-step → visualize**,  
which is typical for numerical solutions of partial differential equations.