# ENG17: Circuits I — Learning Objectives
## Topic: Response of the Series RLC Circuit

**Source:** `ENG17-series-RLC-derivation/main.tex`  
**Lecture:** 1 — *Response of the Series RLC Circuit*  
**Course:** ENG17: Circuits I, Spring 2025  
**Instructor:** Anthony Thomas  

---

## 1. Initial Conditions and Families of Solutions

- Recognize that a linear ODE has a *family* of solutions parameterized by free constants, not a single unique solution. For the first-order case:
$$f(t) = Ae^{-at} + \frac{b}{a}, \quad A \in \mathbb{C}$$
- Explain why selecting the physically correct solution requires matching known **initial conditions** (e.g., $v_C(0^+)$).
- Apply this principle to the RC step-response to recover:
$$v_C(t) = v_C(\infty) + \bigl(v_C(0^+) - v_C(\infty)\bigr)e^{-t/RC}$$

---

## 2. Deriving the Series RLC Governing ODE

Given a series RLC circuit with voltage source $V_s$, resistor $R$, inductor $L$, and capacitor $C$:

- Apply **KVL**: $-V_s + v_R + v_C + v_L = 0$
- Express element voltages in terms of $v_C(t)$ using series current continuity:
$$v_R(t) = RC\,v_C'(t), \qquad v_L(t) = LC\,v_C''(t)$$
- Derive the governing second-order ODE:
$$LC\,v_C''(t) + RC\,v_C'(t) + v_C(t) = V_s$$
- Divide through by $LC$ to obtain standard form:
$$v_C''(t) + \frac{R}{L}\,v_C'(t) + \frac{1}{LC}\,v_C(t) = \frac{V_s}{LC}$$
- Define the two fundamental circuit parameters:
$$\alpha = \frac{R}{2L} \quad \text{(damping coefficient)}, \qquad \omega_0 = \frac{1}{\sqrt{LC}} \quad \text{(natural frequency)}$$
- Write the characteristic roots compactly as:
$$s_{1,2} = -\alpha \pm \sqrt{\alpha^2 - \omega_0^2}$$

---

## 3. Transient and Steady-State Decomposition

- Decompose the complete response:
$$v_C(t) = v_{ss}(t) + v_{tr}(t)$$
- Determine the **steady-state response** by setting all derivatives to zero:
$$v_{ss}(t) = \frac{c}{b} = V_s = v_C(\infty)$$
- Show that the **transient response** $v_{tr}(t) = v_C(t) - v_{ss}(t)$ satisfies the *homogeneous* ODE:
$$v_{tr}''(t) + a\,v_{tr}'(t) + b\,v_{tr}(t) = 0$$
- State the required asymptotic condition:
$$\lim_{t \to \infty} v_{tr}(t) = 0$$

---

## 4. The Characteristic Polynomial

- Assume trial solution $v_{tr}(t) = e^{st}$; substituting gives $v_{tr}' = se^{st}$, $v_{tr}'' = s^2 e^{st}$, leading to:
$$e^{st}(s^2 + as + b) = 0 \implies s^2 + as + b = 0$$
- Recognize this as the **characteristic polynomial** whose roots $s_1, s_2$ determine the form of $v_{tr}$.
- Apply the **superposition principle**: if $f_1$ and $f_2$ are solutions to the homogeneous ODE, then so is any linear combination $\alpha f_1 + \beta f_2$.

---

## 5. Three Damping Regimes

The nature of the roots — and therefore the form of $v_C(t)$ — depends on the sign of $\alpha^2 - \omega_0^2$:

| Regime | Condition | Root character | Circuit condition |
|---|---|---|---|
| **Overdamped** | $\alpha > \omega_0$ | Two distinct real negative roots | $R > 2\sqrt{L/C}$ |
| **Critically damped** | $\alpha = \omega_0$ | One repeated real root | $R = 2\sqrt{L/C}$ |
| **Underdamped** | $\alpha < \omega_0$ | Complex-conjugate pair | $R < 2\sqrt{L/C}$ |

---

## 6. Overdamped Response ($\alpha > \omega_0$)

Roots $s_1, s_2$ are **real, distinct, and negative**:
$$s_1 = -\alpha + \sqrt{\alpha^2 - \omega_0^2}, \qquad s_2 = -\alpha - \sqrt{\alpha^2 - \omega_0^2}$$

**General solution:**
$$\boxed{v_C(t) = A_1 e^{s_1 t} + A_2 e^{s_2 t} + v_C(\infty)}$$

**Initial conditions** yield the $2 \times 2$ linear system:
$$A_1 + A_2 = v_C(0) - v_C(\infty)$$
$$s_1 A_1 + s_2 A_2 = \frac{i_C(0)}{C}$$

Solving:
$$A_1 = \frac{\dfrac{i_C(0)}{C} - s_2\bigl(v_C(0) - v_C(\infty)\bigr)}{s_1 - s_2}, \qquad A_2 = \frac{\dfrac{i_C(0)}{C} - s_1\bigl(v_C(0) - v_C(\infty)\bigr)}{s_2 - s_1}$$

**Key initial condition facts:**
- $v_C(0^+) = v_C(0^-)$ — capacitor voltage cannot change instantaneously
- $i_C(0^+) = i_L(0^+) = i_L(0^-)$ — inductor current cannot change instantaneously (series circuit)

**Worked Example:** $V_s = 16\text{ V}$, $R = 64\,\Omega$, $L = 0.8\text{ H}$, $C = 2\text{ mF}$, $v_C(0^-) = 0$

$$s^2 + 80s + \tfrac{10^4}{16} = 0 \implies s_1 = -8.8,\; s_2 = -71.2$$
$$v_C(t) = -18.25\,e^{-8.8t} + 2.25\,e^{-71.2t} + 16 \quad (t \geq 0)$$
$$i_C(t) = 0.32\bigl(e^{-8.8t} - e^{-71.2t}\bigr)\text{ A}$$

---

## 7. Underdamped Response ($\alpha < \omega_0$)

Roots are a **complex-conjugate pair**:
$$s_{1,2} = -\alpha \pm j\omega_d, \qquad \omega_d = \sqrt{\omega_0^2 - \alpha^2} \quad \text{(damped natural frequency)}$$

Applying **Euler's identity** $e^{j\theta} = \cos\theta + j\sin\theta$ converts complex exponentials to real sinusoids:

**General solution:**
$$\boxed{v_C(t) = e^{-\alpha t}\bigl(D_1\cos(\omega_d t) + D_2\sin(\omega_d t)\bigr) + v_C(\infty)}$$

**Invoking initial conditions:**
$$D_1 = v_C(0) - v_C(\infty)$$
$$D_2 = \frac{1}{\omega_d}\left(\frac{i_C(0)}{C} + \alpha\bigl(v_C(0) - v_C(\infty)\bigr)\right)$$

> **Alert — current initial condition:** Use continuity of *inductor* current to find $i_C(0^+) = i_L(0^-)$.  
> Do **not** use $i_C(0^-)$ directly — capacitor current *can* change instantaneously.

**Amplitude-phase form:** The sinusoidal factor can equivalently be written as:
$$D_1\cos(\omega_d t) + D_2\sin(\omega_d t) = D_3\cos(\omega_d t + \phi)$$
where:
$$D_3 = \sqrt{D_1^2 + D_2^2}, \qquad \phi = -\arctan\!\left(\frac{D_2}{D_1}\right)$$

**Physical interpretation:** The transient response is a sinusoid at frequency $\omega_d$ whose amplitude is exponentially damped, confined within the envelope:
$$-D_3 e^{-\alpha t} \leq v_{tr}(t) \leq D_3 e^{-\alpha t}$$

**Worked Example:** $V_s = 24\text{ V}$, $R = 12\,\Omega$, $L = 0.3\text{ H}$, $C = 0.72\text{ mF}$, $v_C(0^-) = 0$

$$s^2 + 40s + 4629.6 = 0 \implies s_{1,2} = -20 \pm 65j \implies \alpha = 20,\; \omega_d = 65$$
$$D_1 = -24, \qquad D_2 = -7.38$$
$$v_C(t) = e^{-20t}\bigl(-24\cos(65t) - 7.38\sin(65t)\bigr) + 24 \quad (t > 0)$$

---

## 8. Critically Damped Response ($\alpha = \omega_0$)

Single repeated root: $s_1 = s_2 = -\alpha$

**Why two plain exponentials fail:** $A_1 e^{st} + A_2 e^{st} = A_3 e^{st}$ collapses to one free constant, making it impossible to independently satisfy both $v_C(0)$ and $i_C(0)$.

**Correct transient form** (polynomial-times-exponential for repeated roots):
$$v_{tr}(t) = (B_1 + B_2 t)\,e^{-\alpha t}$$

Verification: substituting into the homogeneous ODE and collecting terms shows this satisfies $v_{tr}'' + av_{tr}' + bv_{tr} = 0$ if and only if $s = -\alpha$ (consistent with the repeated root).

**General solution:**
$$\boxed{v_C(t) = (B_1 + B_2 t)\,e^{-\alpha t} + v_C(\infty)}$$

**Invoking initial conditions:**
$$B_1 = v_C(0) - v_C(\infty)$$
$$B_2 = \frac{i_C(0)}{C} + \alpha\bigl(v_C(0) - v_C(\infty)\bigr)$$

---

## 9. Comparison of Damping Regimes

| Regime | Transient behavior | Decay rate |
|---|---|---|
| **Overdamped** | Monotonic decay to zero | Slower than critically damped; dominant term decays as $e^{s_1 t}$ with $s_1 > -\alpha$ |
| **Critically damped** | Monotonic decay to zero | **Fastest** monotonic decay |
| **Underdamped** | Oscillatory (sinusoidal) decay | Oscillates within exponential envelope before settling |

The critically damped case is fastest because the coefficient on $t$ in the exponent is exactly $-\alpha$, whereas in the overdamped case $s_1 = -\alpha + \sqrt{\alpha^2 - \omega_0^2} > -\alpha$, making the dominant term decay more slowly.

---

## Summary of Key Formulas

| Quantity | Formula |
|---|---|
| Damping coefficient | $\alpha = \dfrac{R}{2L}$ |
| Natural frequency | $\omega_0 = \dfrac{1}{\sqrt{LC}}$ |
| Damped frequency | $\omega_d = \sqrt{\omega_0^2 - \alpha^2}$ |
| Characteristic roots | $s_{1,2} = -\alpha \pm \sqrt{\alpha^2 - \omega_0^2}$ |
| Overdamped $v_C(t)$ | $A_1 e^{s_1 t} + A_2 e^{s_2 t} + v_C(\infty)$ |
| Underdamped $v_C(t)$ | $e^{-\alpha t}\!\left(D_1\cos\omega_d t + D_2\sin\omega_d t\right) + v_C(\infty)$ |
| Critically damped $v_C(t)$ | $(B_1 + B_2 t)\,e^{-\alpha t} + v_C(\infty)$ |
| Capacitor current | $i_C(t) = C\,v_C'(t)$ |

---

## Implicit Prerequisites

Students are expected to be fluent in:

- KVL and KCL, Ohm's law
- Continuity of $v_C$ and $i_L$ across switching events
- Solving $2 \times 2$ linear systems
- Derivatives of $e^{at}$, $\sin(at)$, $\cos(at)$; product rule
- Complex numbers: rectangular form, conjugates, Euler's identity
- Trigonometric identity: $\cos(x+\phi) = \cos x\cos\phi - \sin x\sin\phi$
