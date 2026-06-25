# Module 1 Topics — Series RLC Circuit Response

## Chapter 1 — Initial Conditions and ODE Derivation (chapter_id = 1)

| Row | Topic | Subtopic | Learning Objective | Bloom Level | Difficulty |
|-----|-------|----------|--------------------|-------------|------------|
| 1 | Differential Equations | Families of solutions | Recognize that a linear ODE has a family of solutions parameterized by free constants, and explain why initial conditions are needed to select the physically correct one | Understand | 2 |
| 2 | Differential Equations | Initial condition application | Apply an initial condition to fix the free constant in the first-order RC step-response solution | Apply | 2 |
| 3 | Series RLC ODE | KVL and element relations | Apply KVL to a series RLC circuit and express the resistor and inductor voltages in terms of \(v_C(t)\) using series current continuity | Apply | 3 |
| 4 | Series RLC ODE | Governing ODE derivation | Derive the second-order constant-coefficient ODE \(v_C'' + \frac{R}{L}v_C' + \frac{1}{LC}v_C = \frac{V_s}{LC}\) for a series RLC circuit | Apply | 3 |
| 5 | Circuit Parameters | Alpha and omega-zero | Define the damping coefficient \(\alpha = R/(2L)\) and natural frequency \(\omega_0 = 1/\sqrt{LC}\), and express the characteristic roots as \(s_{1,2} = -\alpha \pm \sqrt{\alpha^2 - \omega_0^2}\) | Remember | 2 |

## Chapter 2 — Transient and Steady-State Decomposition (chapter_id = 2)

| Row | Topic | Subtopic | Learning Objective | Bloom Level | Difficulty |
|-----|-------|----------|--------------------|-------------|------------|
| 6 | Response Decomposition | Transient and steady-state | Decompose the complete response as \(v_C(t) = v_{ss}(t) + v_{tr}(t)\) and identify what each term represents physically | Understand | 2 |
| 7 | Response Decomposition | Steady-state response | Determine the steady-state response \(v_{ss} = V_s = v_C(\infty)\) by setting all derivatives to zero | Apply | 2 |
| 8 | Response Decomposition | Transient homogeneous ODE | Show that the transient response satisfies the homogeneous ODE and state the required asymptotic condition \(\lim_{t\to\infty}v_{tr}(t) = 0\) | Understand | 3 |
| 9 | Characteristic Polynomial | Trial solution and roots | Substitute the trial solution \(e^{st}\) into the homogeneous ODE to derive the characteristic polynomial \(s^2 + as + b = 0\), and state the superposition principle for homogeneous solutions | Apply | 3 |

## Chapter 3 — Overdamped Response (chapter_id = 3)

| Row | Topic | Subtopic | Learning Objective | Bloom Level | Difficulty |
|-----|-------|----------|--------------------|-------------|------------|
| 10 | Damping Classification | Identifying the regime | Classify a series RLC circuit as overdamped, critically damped, or underdamped given \(R\), \(L\), \(C\) values by comparing \(\alpha\) and \(\omega_0\) | Apply | 2 |
| 11 | Overdamped Response | General solution form | State the general overdamped solution \(v_C(t) = A_1 e^{s_1 t} + A_2 e^{s_2 t} + v_C(\infty)\) and identify the roles of \(s_1\), \(s_2\), and the constants \(A_1\), \(A_2\) | Remember | 2 |
| 12 | Overdamped Response | Initial conditions system | Set up and solve the 2×2 linear system from \(v_C(0^+)\) and \(i_C(0^+)\) to find \(A_1\) and \(A_2\) in the overdamped solution | Apply | 3 |
| 13 | Overdamped Response | Continuity constraints | Apply the continuity of capacitor voltage (\(v_C\) cannot change instantaneously) and inductor current (\(i_L\) cannot change instantaneously) to determine \(v_C(0^+)\) and \(i_C(0^+)\) | Apply | 3 |
| 14 | Overdamped Response | Worked example | Given \(V_s\), \(R\), \(L\), \(C\) for an overdamped circuit, solve for \(v_C(t)\) and compute \(i_C(t) = C\,v_C'(t)\) | Apply | 4 |

## Chapter 4 — Underdamped Response (chapter_id = 4)

| Row | Topic | Subtopic | Learning Objective | Bloom Level | Difficulty |
|-----|-------|----------|--------------------|-------------|------------|
| 15 | Underdamped Response | Complex roots and damped frequency | Identify complex-conjugate roots \(s_{1,2} = -\alpha \pm j\omega_d\) and define the damped natural frequency \(\omega_d = \sqrt{\omega_0^2 - \alpha^2}\) | Understand | 2 |
| 16 | Underdamped Response | Euler's identity and general form | Apply Euler's identity \(e^{j\theta} = \cos\theta + j\sin\theta\) to convert complex exponential solutions to real form and write \(v_C(t) = e^{-\alpha t}(D_1\cos\omega_d t + D_2\sin\omega_d t) + v_C(\infty)\) | Apply | 3 |
| 17 | Underdamped Response | Initial conditions | Invoke initial conditions to find \(D_1 = v_C(0) - v_C(\infty)\) and \(D_2\), using inductor current continuity (not capacitor current) for \(i_C(0^+)\) | Apply | 3 |
| 18 | Underdamped Response | Amplitude-phase form | Convert \(D_1\cos(\omega_d t) + D_2\sin(\omega_d t)\) to amplitude-phase form \(D_3\cos(\omega_d t + \phi)\) where \(D_3 = \sqrt{D_1^2 + D_2^2}\) and \(\phi = -\arctan(D_2/D_1)\) | Apply | 3 |
| 19 | Underdamped Response | Physical interpretation — envelope | Describe the oscillatory envelope behavior: the transient is bounded by \(\pm D_3 e^{-\alpha t}\) and decays to zero, explaining why the solution eventually reaches steady state | Understand | 3 |
| 20 | Underdamped Response | Worked example | Given \(V_s\), \(R\), \(L\), \(C\) for an underdamped circuit, determine \(\alpha\), \(\omega_d\), \(D_1\), \(D_2\), and write \(v_C(t)\) | Apply | 4 |

## Chapter 5 — Critically Damped Response and Comparison (chapter_id = 5)

| Row | Topic | Subtopic | Learning Objective | Bloom Level | Difficulty |
|-----|-------|----------|--------------------|-------------|------------|
| 21 | Critically Damped Response | Repeated root problem | Explain why \(A_1 e^{st} + A_2 e^{st}\) collapses to one free constant and cannot independently satisfy both \(v_C(0)\) and \(i_C(0)\) when \(s_1 = s_2\) | Understand | 3 |
| 22 | Critically Damped Response | General solution form | State and verify that \(v_C(t) = (B_1 + B_2 t)e^{-\alpha t} + v_C(\infty)\) satisfies the homogeneous ODE in the critically damped case | Apply | 3 |
| 23 | Critically Damped Response | Initial conditions | Solve for \(B_1 = v_C(0) - v_C(\infty)\) and \(B_2 = i_C(0)/C + \alpha(v_C(0) - v_C(\infty))\) from initial conditions | Apply | 3 |
| 24 | Damping Regime Comparison | Decay rate comparison | Compare the transient decay rates of overdamped, critically damped, and underdamped responses and explain why the critically damped regime decays most rapidly without oscillation | Analyze | 4 |
