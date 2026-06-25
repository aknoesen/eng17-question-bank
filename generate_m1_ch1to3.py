#!/usr/bin/env python3
"""
ENG17 Question Bank — Module 1, Chapters 1-3 (topics 1-14)
Initializes DB schema, inserts metadata, generates and inserts questions one topic at a time.
"""
import sqlite3, json, datetime, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
DB   = os.path.join(BASE, "veriqa.db")
SCHEMA = os.path.join(BASE, "schema.sql")

# ── schema + metadata ──────────────────────────────────────────────────────

MODULES = [
    (1, 1, "Response of the Series RLC Circuit", "ENG17"),
    (2, 2, "Thevenin & Norton Equivalence + Maximum Power Transfer", "ENG17"),
]
CHAPTERS = [
    (1, 1, "1", "Initial Conditions and ODE Derivation"),
    (2, 1, "2", "Transient and Steady-State Decomposition"),
    (3, 1, "3", "Overdamped Response"),
    (4, 1, "4", "Underdamped Response"),
    (5, 1, "5", "Critically Damped Response and Comparison"),
    (6, 2, "1", "Thevenin's Theorem"),
    (7, 2, "2", "Norton Equivalence and Source Transformation"),
    (8, 2, "3", "Maximum Power Transfer"),
]
TOPICS = [
    (1,1,1,"Differential Equations","Families of solutions","Recognize that a linear ODE has a family of solutions parameterized by free constants, and explain why initial conditions are needed to select the physically correct one","Understand",2),
    (2,1,2,"Differential Equations","Initial condition application","Apply an initial condition to fix the free constant in the first-order RC step-response solution","Apply",2),
    (3,1,3,"Series RLC ODE","KVL and element relations","Apply KVL to a series RLC circuit and express the resistor and inductor voltages in terms of v_C(t) using series current continuity","Apply",3),
    (4,1,4,"Series RLC ODE","Governing ODE derivation","Derive the second-order constant-coefficient ODE for the series RLC circuit","Apply",3),
    (5,1,5,"Circuit Parameters","Alpha and omega-zero","Define the damping coefficient alpha=R/(2L) and natural frequency omega_0=1/sqrt(LC), and express the characteristic roots","Remember",2),
    (6,2,6,"Response Decomposition","Transient and steady-state","Decompose v_C(t)=v_ss(t)+v_tr(t) and identify what each term represents physically","Understand",2),
    (7,2,7,"Response Decomposition","Steady-state response","Determine the steady-state response v_ss=V_s=v_C(infinity) by setting all derivatives to zero","Apply",2),
    (8,2,8,"Response Decomposition","Transient homogeneous ODE","Show that the transient response satisfies the homogeneous ODE and state the required asymptotic condition","Understand",3),
    (9,2,9,"Characteristic Polynomial","Trial solution and roots","Substitute the trial solution e^{st} into the homogeneous ODE to derive the characteristic polynomial","Apply",3),
    (10,3,10,"Damping Classification","Identifying the regime","Classify a series RLC circuit as overdamped, critically damped, or underdamped given R, L, C values by comparing alpha and omega_0","Apply",2),
    (11,3,11,"Overdamped Response","General solution form","State the general overdamped solution and identify the roles of s1, s2, A1, A2","Remember",2),
    (12,3,12,"Overdamped Response","Initial conditions system","Set up and solve the 2x2 linear system from initial conditions to find A1 and A2 in the overdamped solution","Apply",3),
    (13,3,13,"Overdamped Response","Continuity constraints","Apply the continuity of capacitor voltage and inductor current to determine v_C(0+) and i_C(0+)","Apply",3),
    (14,3,14,"Overdamped Response","Worked example","Given V_s, R, L, C for an overdamped circuit, solve for v_C(t) and compute i_C(t)=C*v_C'(t)","Apply",4),
]

# chapter_id -> module_id lookup
CH_MOD = {c[0]: c[1] for c in CHAPTERS}

# ── question data: topic_id -> list of 3 dicts ─────────────────────────────
# KaTeX: use \\( ... \\) for inline, \\[ ... \\] for display.
# Python string \\( becomes \( in the string value, which json.dumps encodes as \\(

Q = {}

Q[1] = [
  dict(
    title="ODE family: role of free constant",
    question_text="A first-order linear ODE has the general solution \\( f(t) = Ae^{-at} + b/a \\) for any constant \\( A \\). What role does \\( A \\) play?",
    choices=[
        "It changes the form of the differential equation.",
        "It shifts the steady-state value \\( b/a \\) up or down.",
        "It parameterizes the entire family of solutions; a specific initial condition selects the unique physical value of \\( A \\).",
        "It determines whether the solution is stable or unstable."
    ],
    correct_answer_index=2,
    feedback_correct="Correct. Any value of \\( A \\) satisfies the ODE algebraically. The initial condition \\( f(0) = f_0 \\) fixes \\( A = f_0 - b/a \\), selecting the unique physically meaningful solution.",
    feedback_incorrect="The ODE is satisfied for every \\( A \\); the equation itself does not pin down \\( A \\). Only an initial condition (a measurement of the circuit state at \\( t=0 \\)) narrows the family to a single physical trajectory.",
    bloom_level="Understand", difficulty=2, katex_present=1,
  ),
  dict(
    title="ODE family: rejecting a non-physical solution",
    question_text="The general solution to an RC circuit ODE is \\( v_C(t) = Ae^{-at} + V_s \\). A student proposes \\( v_C(t) = \\pi e^{-at} + V_s \\). Why is this rejected as the physical solution for an uncharged capacitor?",
    choices=[
        "The function \\( \\pi e^{-at} \\) does not satisfy the differential equation.",
        "It satisfies the ODE but does not satisfy the initial condition \\( v_C(0^+) = 0 \\).",
        "The coefficient \\( \\pi \\) causes the solution to grow without bound.",
        "It gives the wrong steady-state value as \\( t \\to \\infty \\)."
    ],
    correct_answer_index=1,
    feedback_correct="Correct. Substituting \\( t=0 \\) gives \\( v_C(0) = \\pi + V_s \\neq 0 \\) for an uncharged capacitor. The ODE is satisfied, but the physical initial condition is violated.",
    feedback_incorrect="The function \\( \\pi e^{-at}+V_s \\) does satisfy the ODE and decays correctly. The problem is purely the initial condition: \\( v_C(0) = \\pi + V_s \\neq 0 \\), so it does not describe an uncharged capacitor.",
    bloom_level="Understand", difficulty=2, katex_present=1,
  ),
  dict(
    title="ODE family: why two solutions coexist",
    question_text="Both \\( v_C(t) = 3e^{-at} + V_s \\) and \\( v_C(t) = -7e^{-at} + V_s \\) satisfy the same first-order RC ODE. Which statement best explains this?",
    choices=[
        "Each solution corresponds to a different differential equation.",
        "The homogeneous equation \\( v_C' + av_C = 0 \\) has infinitely many solutions of the form \\( Ae^{-at} \\), so adding any constant \\( A \\) to the particular solution gives a valid member of the family.",
        "The two solutions have different steady-state values, making both valid only in different circuits.",
        "Linear superposition does not apply to first-order ODEs."
    ],
    correct_answer_index=1,
    feedback_correct="Correct. The inhomogeneous ODE \\( v_C' + av_C = b \\) has a particular solution \\( V_s \\) plus the homogeneous family \\( Ae^{-at} \\). Any choice of \\( A \\) satisfies the equation; initial conditions select the unique physical \\( A \\).",
    feedback_incorrect="Both solutions satisfy the same ODE and share the same steady-state \\( V_s \\). The difference is only in the free constant \\( A \\) of the homogeneous solution. The initial condition uniquely determines which family member is physical.",
    bloom_level="Understand", difficulty=2, katex_present=1,
  ),
]

Q[2] = [
  dict(
    title="Applying IC to RC step response",
    question_text="The general RC step-response solution is \\( v_C(t) = Ae^{-t/RC} + V_s \\). If the capacitor is uncharged at \\( t=0^+ \\), i.e., \\( v_C(0^+) = 0 \\), what is \\( A \\)?",
    choices=[
        "\\( A = V_s \\)",
        "\\( A = -V_s \\)",
        "\\( A = 0 \\)",
        "\\( A = 1/V_s \\)"
    ],
    correct_answer_index=1,
    feedback_correct="Correct. Substituting \\( t=0 \\): \\( 0 = A + V_s \\Rightarrow A = -V_s \\). This gives the familiar result \\( v_C(t) = V_s(1-e^{-t/RC}) \\).",
    feedback_incorrect="Set \\( t=0 \\) in the general solution: \\( v_C(0) = A + V_s = 0 \\), so \\( A = -V_s \\). The complete solution then becomes \\( v_C(t) = V_s - V_s e^{-t/RC} = V_s(1-e^{-t/RC}) \\).",
    bloom_level="Apply", difficulty=2, katex_present=1,
  ),
  dict(
    title="IC with pre-charged capacitor",
    question_text="A capacitor is initially charged to \\( V_0 \\) before the step is applied. The general solution is \\( v_C(t) = Ae^{-t/RC} + V_s \\). What value of \\( A \\) matches this initial condition?",
    choices=[
        "\\( A = V_0 + V_s \\)",
        "\\( A = V_0 - V_s \\)",
        "\\( A = V_s - V_0 \\)",
        "\\( A = V_0 \\)"
    ],
    correct_answer_index=1,
    feedback_correct="Correct. \\( v_C(0) = A + V_s = V_0 \\Rightarrow A = V_0 - V_s \\). The solution \\( v_C(t) = V_s + (V_0 - V_s)e^{-t/RC} \\) correctly starts at \\( V_0 \\) and approaches \\( V_s \\).",
    feedback_incorrect="At \\( t=0 \\): \\( v_C(0) = A + V_s = V_0 \\). Solving for \\( A \\) gives \\( A = V_0 - V_s \\).",
    bloom_level="Apply", difficulty=2, katex_present=1,
  ),
  dict(
    title="IC procedure for first-order ODE",
    question_text="Which procedure correctly selects the unique physical solution from the family \\( f(t) = Ae^{-at} + b/a \\)?",
    choices=[
        "Differentiate \\( f \\) and set \\( f'(0)=0 \\) to find \\( A \\).",
        "Evaluate \\( f \\) at \\( t \\to \\infty \\) to eliminate the transient.",
        "Substitute the known circuit state \\( f(0^+) = f_0 \\) into the general solution and solve for \\( A \\).",
        "Choose \\( A \\) so that the ODE coefficient \\( a \\) equals zero."
    ],
    correct_answer_index=2,
    feedback_correct="Correct. Setting \\( t=0 \\): \\( f_0 = A + b/a \\Rightarrow A = f_0 - b/a \\). This is the standard procedure for first-order constant-coefficient ODEs.",
    feedback_incorrect="The initial condition \\( f(0^+) = f_0 \\) is the physical measurement that pins down \\( A \\). Setting \\( t=0 \\) in \\( f(t) = Ae^{-at}+b/a \\) gives \\( A = f_0 - b/a \\).",
    bloom_level="Apply", difficulty=2, katex_present=1,
  ),
]

Q[3] = [
  dict(
    title="Resistor voltage in series RLC via KVL",
    question_text="In a series RLC circuit, all elements share the same current. Using \\( i_C(t) = Cv_C'(t) \\), which expression gives the resistor voltage \\( v_R(t) \\)?",
    choices=[
        "\\( v_R(t) = LCv_C'(t) \\)",
        "\\( v_R(t) = RCv_C'(t) \\)",
        "\\( v_R(t) = \\frac{R}{L}v_C(t) \\)",
        "\\( v_R(t) = Rv_C(t) \\)"
    ],
    correct_answer_index=1,
    feedback_correct="Correct. In series, \\( i_R = i_C = Cv_C'(t) \\). By Ohm's law, \\( v_R = Ri_R = RCv_C'(t) \\).",
    feedback_incorrect="All elements in series share the same current: \\( i_R = i_C = Cv_C'(t) \\). Ohm's law then gives \\( v_R = Ri_R = RCv_C'(t) \\).",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
  dict(
    title="Inductor voltage in series RLC",
    question_text="In a series RLC circuit with \\( i_C(t) = Cv_C'(t) \\), which expression gives the inductor voltage \\( v_L(t) \\)?",
    choices=[
        "\\( v_L(t) = LCv_C'(t) \\)",
        "\\( v_L(t) = \\frac{L}{C}v_C(t) \\)",
        "\\( v_L(t) = LCv_C''(t) \\)",
        "\\( v_L(t) = \\frac{R}{L}v_C'(t) \\)"
    ],
    correct_answer_index=2,
    feedback_correct="Correct. \\( v_L = Li_L'(t) = Li_C'(t) = L(Cv_C'(t))' = LCv_C''(t) \\).",
    feedback_incorrect="Since \\( i_L = i_C = Cv_C'(t) \\), we have \\( v_L = Li_L' = L(Cv_C'(t))' = LCv_C''(t) \\).",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
  dict(
    title="KVL equation for series RLC",
    question_text="After substituting \\( v_R = RCv_C'(t) \\) and \\( v_L = LCv_C''(t) \\) into the KVL equation \\( -V_s + v_R + v_C + v_L = 0 \\), which equation results?",
    choices=[
        "\\( LCv_C''(t) + v_C'(t) + RCv_C(t) = V_s \\)",
        "\\( LCv_C''(t) + RCv_C'(t) + v_C(t) = V_s \\)",
        "\\( RCv_C''(t) + LCv_C'(t) + v_C(t) = V_s \\)",
        "\\( v_C''(t) + RCv_C'(t) + LCv_C(t) = V_s/LC \\)"
    ],
    correct_answer_index=1,
    feedback_correct="Correct. Substituting and rearranging: \\( LCv_C'' + RCv_C' + v_C = V_s \\). Note the coefficients: \\( LC \\) on the second derivative, \\( RC \\) on the first.",
    feedback_incorrect="The KVL equation gives \\( v_R + v_C + v_L = V_s \\). Substituting: \\( RCv_C' + v_C + LCv_C'' = V_s \\), which reorders to \\( LCv_C'' + RCv_C' + v_C = V_s \\).",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
]

Q[4] = [
  dict(
    title="Normalized series RLC ODE",
    question_text="Starting from \\( LCv_C'' + RCv_C' + v_C = V_s \\), dividing through by \\( LC \\) yields which normalized ODE?",
    choices=[
        "\\( v_C'' + RCv_C' + \\frac{1}{LC}v_C = \\frac{V_s}{LC} \\)",
        "\\( v_C'' + \\frac{R}{L}v_C' + \\frac{1}{LC}v_C = \\frac{V_s}{LC} \\)",
        "\\( v_C'' + \\frac{R}{L}v_C' + v_C = \\frac{V_s}{LC} \\)",
        "\\( v_C'' + \\frac{R}{LC}v_C' + \\frac{1}{LC}v_C = \\frac{V_s}{LC} \\)"
    ],
    correct_answer_index=1,
    feedback_correct="Correct. Dividing each term by \\( LC \\): \\( \\frac{RC}{LC} = \\frac{R}{L} \\), \\( \\frac{1}{LC} \\), and \\( \\frac{V_s}{LC} \\). This is the standard form with \\( a=R/L \\), \\( b=1/LC \\), \\( c=V_s/LC \\).",
    feedback_incorrect="Divide every term of \\( LCv_C''+RCv_C'+v_C=V_s \\) by \\( LC \\): the \\( v_C' \\) coefficient becomes \\( RC/LC = R/L \\), the \\( v_C \\) coefficient becomes \\( 1/LC \\), and the RHS becomes \\( V_s/LC \\).",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
  dict(
    title="Units of the ODE coefficient R/L",
    question_text="In the normalized ODE \\( v_C'' + (R/L)v_C' + (1/LC)v_C = V_s/(LC) \\), what are the SI units of the coefficient \\( R/L \\)?",
    choices=[
        "Henries (H)",
        "Inverse seconds \\( (\\text{s}^{-1}) \\)",
        "Dimensionless",
        "Ohms (\\( \\Omega \\))"
    ],
    correct_answer_index=1,
    feedback_correct="Correct. \\( R \\) is in \\( \\Omega \\) and \\( L \\) is in H \\( = \\Omega \\cdot \\text{s} \\), so \\( R/L \\) has units \\( \\Omega/(\\Omega\\cdot\\text{s}) = \\text{s}^{-1} \\). This is consistent with the requirement that each term in the ODE has the same units as \\( v_C'' \\) (V/s\\(^2\\)).",
    feedback_incorrect="\\( [R/L] = \\Omega/\\text{H} = \\Omega/(\\Omega\\cdot\\text{s}) = \\text{s}^{-1} \\). The coefficient of \\( v_C' \\) must have units of 1/s so that \\( (R/L)v_C' \\) has the same units as \\( v_C'' \\) (V/s\\(^2\\)).",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
  dict(
    title="Numerical ODE coefficient calculation",
    question_text="A series RLC circuit has \\( R = 10\\,\\Omega \\), \\( L = 0.5\\,\\text{H} \\), \\( C = 10\\,\\text{mF} \\), \\( V_s = 12\\,\\text{V} \\). What is the coefficient of \\( v_C'(t) \\) in the normalized ODE?",
    choices=[
        "\\( 5\\,\\text{s}^{-1} \\)",
        "\\( 20\\,\\text{s}^{-1} \\)",
        "\\( 200\\,\\text{s}^{-1} \\)",
        "\\( 2\\,\\text{s}^{-1} \\)"
    ],
    correct_answer_index=1,
    feedback_correct="Correct. \\( R/L = 10/0.5 = 20\\,\\text{s}^{-1} \\).",
    feedback_incorrect="The coefficient of \\( v_C' \\) is \\( R/L = 10\\,\\Omega / 0.5\\,\\text{H} = 20\\,\\text{s}^{-1} \\).",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
]

Q[5] = [
  dict(
    title="Definition of damping coefficient alpha",
    question_text="For a series RLC circuit, the damping coefficient \\( \\alpha \\) is defined as:",
    choices=[
        "\\( \\alpha = R/L \\)",
        "\\( \\alpha = R/(2L) \\)",
        "\\( \\alpha = 1/\\sqrt{LC} \\)",
        "\\( \\alpha = RC/2 \\)"
    ],
    correct_answer_index=1,
    feedback_correct="Correct. \\( \\alpha = R/(2L) \\). The factor of 2 comes from writing the characteristic roots as \\( s_{1,2} = -a/2 \\pm \\sqrt{(a/2)^2 - b} \\) where \\( a = R/L \\).",
    feedback_incorrect="From the characteristic equation, the roots are \\( s_{1,2} = -(R/L)/2 \\pm \\cdots = -R/(2L) \\pm \\cdots \\). The neper frequency is defined as \\( \\alpha = R/(2L) \\).",
    bloom_level="Remember", difficulty=2, katex_present=1,
  ),
  dict(
    title="Definition of natural frequency omega_0",
    question_text="The undamped natural frequency \\( \\omega_0 \\) of a series RLC circuit is:",
    choices=[
        "\\( \\omega_0 = R/(2L) \\)",
        "\\( \\omega_0 = \\sqrt{RC} \\)",
        "\\( \\omega_0 = 1/\\sqrt{LC} \\)",
        "\\( \\omega_0 = 1/(2\\sqrt{LC}) \\)"
    ],
    correct_answer_index=2,
    feedback_correct="Correct. \\( \\omega_0 = 1/\\sqrt{LC} \\) is the resonant frequency that would result with zero resistance (undamped oscillation).",
    feedback_incorrect="From the characteristic polynomial \\( s^2 + (R/L)s + 1/(LC) = 0 \\), the constant term is \\( \\omega_0^2 = 1/(LC) \\), so \\( \\omega_0 = 1/\\sqrt{LC} \\).",
    bloom_level="Remember", difficulty=2, katex_present=1,
  ),
  dict(
    title="Numerical alpha and omega_0",
    question_text="A series RLC circuit has \\( R = 4\\,\\Omega \\), \\( L = 2\\,\\text{H} \\), \\( C = 0.5\\,\\text{F} \\). Compute \\( \\alpha \\) and \\( \\omega_0 \\).",
    choices=[
        "\\( \\alpha = 1\\,\\text{s}^{-1},\\; \\omega_0 = 1\\,\\text{rad/s} \\)",
        "\\( \\alpha = 2\\,\\text{s}^{-1},\\; \\omega_0 = 1\\,\\text{rad/s} \\)",
        "\\( \\alpha = 1\\,\\text{s}^{-1},\\; \\omega_0 = \\sqrt{2}\\,\\text{rad/s} \\)",
        "\\( \\alpha = 0.5\\,\\text{s}^{-1},\\; \\omega_0 = 1\\,\\text{rad/s} \\)"
    ],
    correct_answer_index=0,
    feedback_correct="Correct. \\( \\alpha = R/(2L) = 4/(2\\times 2) = 1\\,\\text{s}^{-1} \\). \\( \\omega_0 = 1/\\sqrt{LC} = 1/\\sqrt{2\\times 0.5} = 1/1 = 1\\,\\text{rad/s} \\). Since \\( \\alpha = \\omega_0 \\), this is critically damped.",
    feedback_incorrect="\\( \\alpha = R/(2L) = 4/(4) = 1\\,\\text{s}^{-1} \\) and \\( \\omega_0 = 1/\\sqrt{2 \\times 0.5} = 1\\,\\text{rad/s} \\). Note \\( \\alpha = \\omega_0 \\) indicates critical damping.",
    bloom_level="Remember", difficulty=2, katex_present=1,
  ),
]

Q[6] = [
  dict(
    title="Physical meaning of transient response",
    question_text="In the decomposition \\( v_C(t) = v_{ss}(t) + v_{tr}(t) \\), what does \\( v_{tr}(t) \\) represent physically?",
    choices=[
        "The final DC value the capacitor charges to.",
        "The short-term behavior following a switching action, which decays to zero as \\( t \\to \\infty \\).",
        "The constant driven by the source that persists indefinitely.",
        "The initial voltage on the capacitor before the switch closes."
    ],
    correct_answer_index=1,
    feedback_correct="Correct. The transient response captures the temporary deviation of \\( v_C \\) from steady state caused by the switching event. By definition, \\( \\lim_{t\\to\\infty}v_{tr}(t)=0 \\).",
    feedback_incorrect="The transient \\( v_{tr}(t) \\) is the part of the solution that dies out. The long-term behavior is \\( v_{ss}(t) \\), which is what remains after the transient vanishes.",
    bloom_level="Understand", difficulty=2, katex_present=1,
  ),
  dict(
    title="Identifying transient in RC step response",
    question_text="In the RC step response \\( v_C(t) = V_s + (v_C(0^+) - V_s)e^{-t/RC} \\), which term is the transient response \\( v_{tr}(t) \\)?",
    choices=[
        "\\( V_s \\)",
        "\\( (v_C(0^+) - V_s)e^{-t/RC} \\)",
        "\\( v_C(0^+) \\)",
        "\\( V_s e^{-t/RC} \\)"
    ],
    correct_answer_index=1,
    feedback_correct="Correct. The term \\( (v_C(0^+)-V_s)e^{-t/RC} \\) decays to zero as \\( t\\to\\infty \\), so it is the transient. The steady-state part is \\( V_s \\).",
    feedback_incorrect="The transient must satisfy \\( v_{tr} \\to 0 \\) as \\( t\\to\\infty \\). Only \\( (v_C(0^+)-V_s)e^{-t/RC} \\) decays to zero; \\( V_s \\) is the steady-state.",
    bloom_level="Understand", difficulty=2, katex_present=1,
  ),
  dict(
    title="Asymptotic requirement on transient",
    question_text="Why must \\( \\lim_{t\\to\\infty} v_{tr}(t) = 0 \\) in a stable series RLC circuit?",
    choices=[
        "Because the inductor blocks DC in steady state.",
        "So that the complete response \\( v_C(t) \\to v_{ss}(t) \\) as \\( t\\to\\infty \\), matching the long-term behavior of the circuit.",
        "Because \\( v_{ss}(t) \\) grows without bound if the transient does not decay.",
        "Because the capacitor voltage must equal zero at large \\( t \\)."
    ],
    correct_answer_index=1,
    feedback_correct="Correct. Since \\( v_C = v_{ss} + v_{tr} \\), requiring \\( v_{tr}\\to 0 \\) ensures \\( v_C \\to v_{ss} \\) as \\( t\\to\\infty \\), which is the physical definition of steady state.",
    feedback_incorrect="The decomposition \\( v_C = v_{ss} + v_{tr} \\) is only useful if \\( v_{tr} \\to 0 \\); otherwise, \\( v_C \\) would not approach \\( v_{ss} \\) at large times, violating the meaning of 'steady state'.",
    bloom_level="Understand", difficulty=2, katex_present=1,
  ),
]

Q[7] = [
  dict(
    title="Finding v_ss by setting derivatives to zero",
    question_text="To find the steady-state response \\( v_{ss} \\) for a series RLC circuit, which mathematical condition is applied?",
    choices=[
        "Set \\( v_C'(t)=0 \\) only.",
        "Assume \\( v_{ss} \\) is a constant (so \\( v_{ss}'=v_{ss}''=0 \\)) and substitute into the normalized ODE.",
        "Set \\( v_C(t)=0 \\) and \\( v_C'(t)=0 \\) simultaneously.",
        "Set \\( s=0 \\) in the characteristic polynomial."
    ],
    correct_answer_index=1,
    feedback_correct="Correct. For a DC source, \\( v_{ss} \\) is a constant. With \\( v_{ss}'=v_{ss}''=0 \\), the ODE becomes \\( (1/LC)v_{ss} = V_s/(LC) \\), giving \\( v_{ss} = V_s \\).",
    feedback_incorrect="Setting all time-derivatives of \\( v_{ss} \\) to zero (since the steady state is a constant) simplifies the ODE to \\( (1/LC)v_{ss} = V_s/(LC) \\Rightarrow v_{ss} = V_s \\).",
    bloom_level="Apply", difficulty=2, katex_present=1,
  ),
  dict(
    title="Steady-state value for series RLC step response",
    question_text="For a series RLC circuit driven by a constant source \\( V_s \\), the normalized ODE is \\( v_C'' + (R/L)v_C' + (1/LC)v_C = V_s/(LC) \\). What is \\( v_{ss} \\)?",
    choices=[
        "\\( v_{ss} = V_s/(LC) \\)",
        "\\( v_{ss} = 0 \\)",
        "\\( v_{ss} = V_s \\)",
        "\\( v_{ss} = LC \\cdot V_s \\)"
    ],
    correct_answer_index=2,
    feedback_correct="Correct. Substituting a constant \\( v_{ss} \\) with all derivatives zero: \\( (1/LC)v_{ss} = V_s/(LC) \\Rightarrow v_{ss} = V_s \\). Physically, the capacitor charges to the supply voltage at DC steady state.",
    feedback_incorrect="With \\( v_{ss}' = v_{ss}'' = 0 \\): \\( (1/LC)v_{ss} = V_s/(LC) \\). Multiplying both sides by \\( LC \\): \\( v_{ss} = V_s \\).",
    bloom_level="Apply", difficulty=2, katex_present=1,
  ),
  dict(
    title="Physical interpretation of v_ss = V_s",
    question_text="Why does the steady-state capacitor voltage equal \\( V_s \\) (the source voltage) in a series RLC step response?",
    choices=[
        "Because the inductor and capacitor voltage divider gives \\( V_s/2 \\) to each.",
        "At DC steady state, the capacitor is fully charged and no current flows; with zero current, \\( v_R = v_L = 0 \\), so KVL gives \\( v_C = V_s \\).",
        "Because the inductor blocks all current, forcing \\( v_C = V_s \\) at all times.",
        "Because \\( v_C(\\infty) = 0 \\) and \\( V_s = 0 \\) at steady state."
    ],
    correct_answer_index=1,
    feedback_correct="Correct. In DC steady state: the capacitor is an open circuit (no current flows), the inductor is a short circuit (zero voltage). KVL: \\( V_s - 0 - v_C - 0 = 0 \\Rightarrow v_C = V_s \\).",
    feedback_incorrect="At DC steady state, \\( i = 0 \\) (capacitor open circuit). Then \\( v_R = Ri = 0 \\) and \\( v_L = Li' = 0 \\). KVL yields \\( v_C = V_s \\).",
    bloom_level="Apply", difficulty=2, katex_present=1,
  ),
]

Q[8] = [
  dict(
    title="ODE satisfied by the transient response",
    question_text="After writing \\( v_{tr} = v_C - v_{ss} \\), which ODE does \\( v_{tr} \\) satisfy?",
    choices=[
        "\\( v_{tr}'' + (R/L)v_{tr}' + (1/LC)v_{tr} = V_s/(LC) \\)",
        "\\( v_{tr}'' + (R/L)v_{tr}' + (1/LC)v_{tr} = 0 \\)",
        "\\( v_{tr}'' + (1/LC)v_{tr} = 0 \\)",
        "\\( v_{tr}' + (1/LC)v_{tr} = 0 \\)"
    ],
    correct_answer_index=1,
    feedback_correct="Correct. Because \\( v_{ss} \\) is a constant, \\( v_{tr}'' = v_C'' \\) and \\( v_{tr}' = v_C' \\). Substituting into the full ODE and using \\( (1/LC)v_{ss} = V_s/(LC) \\) cancels the right-hand side, giving the homogeneous equation.",
    feedback_incorrect="Since \\( v_{ss} \\) is constant, its derivatives vanish. Substituting \\( v_C = v_{tr} + v_{ss} \\) into the ODE and cancelling \\( (1/LC)v_{ss} = V_s/(LC) \\) leaves \\( v_{tr}'' + (R/L)v_{tr}' + (1/LC)v_{tr} = 0 \\).",
    bloom_level="Understand", difficulty=3, katex_present=1,
  ),
  dict(
    title="Why v_ss constant implies zero derivatives",
    question_text="A key step in showing \\( v_{tr} \\) satisfies the homogeneous ODE is that \\( v_{ss}'' = v_{ss}' = 0 \\). Why?",
    choices=[
        "The source \\( V_s \\) decays to zero at large \\( t \\).",
        "\\( v_{ss} \\) is a constant function of time, so all of its time derivatives are identically zero.",
        "The capacitor prevents DC from passing in steady state.",
        "The inductor acts as a short circuit at DC."
    ],
    correct_answer_index=1,
    feedback_correct="Correct. \\( v_{ss} = V_s \\) is a constant (independent of \\( t \\)). The derivative of any constant is zero: \\( v_{ss}' = 0 \\), \\( v_{ss}'' = 0 \\).",
    feedback_incorrect="The steady-state response is \\( v_{ss} = V_s \\), a constant. The derivative of a constant is zero, regardless of what \\( V_s \\) equals.",
    bloom_level="Understand", difficulty=3, katex_present=1,
  ),
  dict(
    title="Asymptotic condition on transient: physical meaning",
    question_text="The transient response must satisfy \\( \\lim_{t\\to\\infty}v_{tr}(t) = 0 \\). For a stable series RLC circuit, this is guaranteed because:",
    choices=[
        "The homogeneous ODE has purely imaginary roots.",
        "The characteristic roots have negative real parts, so all exponential terms in \\( v_{tr} \\) decay to zero.",
        "The source \\( V_s \\) is turned off after a long time.",
        "The capacitor voltage is bounded above by \\( V_s \\)."
    ],
    correct_answer_index=1,
    feedback_correct="Correct. For a physically realistic series RLC circuit with \\( R,L,C > 0 \\), all characteristic roots have negative real parts (\\( \\text{Re}(s) < 0 \\)), so every term \\( e^{st} \\to 0 \\) as \\( t\\to\\infty \\).",
    feedback_incorrect="Stability requires \\( \\text{Re}(s_{1,2}) < 0 \\). Since \\( \\text{Re}(s) = -\\alpha \\) and \\( \\alpha = R/(2L) > 0 \\) for a physical circuit, all transient terms decay exponentially to zero.",
    bloom_level="Understand", difficulty=3, katex_present=1,
  ),
]

Q[9] = [
  dict(
    title="Derivation of characteristic polynomial",
    question_text="Substituting \\( v_{tr}(t) = e^{st} \\) into \\( v_{tr}'' + av_{tr}' + bv_{tr} = 0 \\) and factoring \\( e^{st} \\neq 0 \\) gives:",
    choices=[
        "\\( se^{st} + ase^{st} + be^{st} = 0 \\quad \\Rightarrow\\quad s + a + b = 0 \\)",
        "\\( s^2e^{st} + ase^{st} + be^{st} = 0 \\quad \\Rightarrow\\quad s^2 + as + b = 0 \\)",
        "\\( e^{st}(s + a)(s + b) = 0 \\quad \\Rightarrow\\quad s = -a \\text{ or } s = -b \\)",
        "\\( s^2 + a + b = 0 \\)"
    ],
    correct_answer_index=1,
    feedback_correct="Correct. With \\( v_{tr}' = se^{st} \\) and \\( v_{tr}'' = s^2e^{st} \\): \\( e^{st}(s^2+as+b)=0 \\). Since \\( e^{st}\\neq 0 \\), the characteristic polynomial \\( s^2+as+b=0 \\) must hold.",
    feedback_incorrect="\\( v_{tr}'' = s^2e^{st} \\) (not \\( se^{st} \\)). Factoring \\( e^{st} \\) gives \\( e^{st}(s^2+as+b)=0 \\), so the characteristic polynomial is \\( s^2+as+b=0 \\).",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
  dict(
    title="Superposition principle for homogeneous solutions",
    question_text="If \\( e^{s_1 t} \\) and \\( e^{s_2 t} \\) both satisfy \\( v_{tr}''+av_{tr}'+bv_{tr}=0 \\), then which expression is also a solution?",
    choices=[
        "Only one of \\( e^{s_1 t} \\) or \\( e^{s_2 t} \\) can be physical.",
        "\\( A_1 e^{s_1 t} + A_2 e^{s_2 t} \\) for any constants \\( A_1, A_2 \\).",
        "The product \\( e^{(s_1+s_2)t} \\).",
        "\\( e^{s_1 t} - e^{s_2 t} \\) only."
    ],
    correct_answer_index=1,
    feedback_correct="Correct. The homogeneous ODE is linear, so any linear combination of solutions is also a solution (superposition principle). The two free constants \\( A_1, A_2 \\) are then fixed by the two initial conditions.",
    feedback_incorrect="For a linear homogeneous ODE, if \\( f_1 \\) and \\( f_2 \\) are solutions, then \\( \\alpha f_1 + \\beta f_2 \\) is also a solution for any constants \\( \\alpha,\\beta \\). This gives us the general solution \\( A_1e^{s_1t}+A_2e^{s_2t} \\).",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
  dict(
    title="Characteristic polynomial for specific RLC circuit",
    question_text="For a series RLC circuit with \\( R=10\\,\\Omega \\), \\( L=0.5\\,\\text{H} \\), \\( C=5\\,\\text{mF} \\), the normalized ODE coefficients are \\( a=R/L=20 \\) and \\( b=1/(LC)=40 \\). What is the characteristic polynomial?",
    choices=[
        "\\( s^2 + 40s + 20 = 0 \\)",
        "\\( s^2 + 20s + 40 = 0 \\)",
        "\\( s + 20 + 40 = 0 \\)",
        "\\( s^2 + 20 + 40s = 0 \\)"
    ],
    correct_answer_index=1,
    feedback_correct="Correct. The characteristic polynomial is \\( s^2 + as + b = s^2 + 20s + 40 = 0 \\). Its roots give the natural frequencies of the circuit.",
    feedback_incorrect="The characteristic polynomial is \\( s^2 + as + b \\) where \\( a=R/L=20 \\) and \\( b=1/(LC)=40 \\), giving \\( s^2 + 20s + 40 = 0 \\).",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
]

Q[10] = [
  dict(
    title="Classifying damping regime from R, L, C",
    question_text="A series RLC circuit has \\( R=20\\,\\Omega \\), \\( L=1\\,\\text{H} \\), \\( C=100\\,\\text{mF} \\). Compute \\( \\alpha \\) and \\( \\omega_0 \\) and classify the damping regime.",
    choices=[
        "\\( \\alpha=5\\,\\text{s}^{-1},\\;\\omega_0=10\\,\\text{rad/s} \\); underdamped",
        "\\( \\alpha=10\\,\\text{s}^{-1},\\;\\omega_0\\approx 3.16\\,\\text{rad/s} \\); overdamped",
        "\\( \\alpha=10\\,\\text{s}^{-1},\\;\\omega_0\\approx 3.16\\,\\text{rad/s} \\); critically damped",
        "\\( \\alpha=20\\,\\text{s}^{-1},\\;\\omega_0\\approx 3.16\\,\\text{rad/s} \\); overdamped"
    ],
    correct_answer_index=1,
    feedback_correct="Correct. \\( \\alpha = 20/(2\\times1)=10\\,\\text{s}^{-1} \\). \\( \\omega_0 = 1/\\sqrt{1\\times 0.1}=1/\\sqrt{0.1}\\approx 3.16\\,\\text{rad/s} \\). Since \\( \\alpha > \\omega_0 \\), the circuit is overdamped.",
    feedback_incorrect="\\( \\alpha = R/(2L) = 10\\,\\text{s}^{-1} \\) and \\( \\omega_0 = 1/\\sqrt{LC} = 1/\\sqrt{0.1} \\approx 3.16\\,\\text{rad/s} \\). Because \\( \\alpha > \\omega_0 \\), the regime is overdamped.",
    bloom_level="Apply", difficulty=2, katex_present=1,
  ),
  dict(
    title="Overdamped condition in terms of R, L, C",
    question_text="The overdamped condition \\( \\alpha > \\omega_0 \\) is equivalent to which inequality in terms of \\( R \\), \\( L \\), and \\( C \\)?",
    choices=[
        "\\( R < 2\\sqrt{L/C} \\)",
        "\\( R > 2\\sqrt{L/C} \\)",
        "\\( R = 2\\sqrt{L/C} \\)",
        "\\( R^2 > L/C \\)"
    ],
    correct_answer_index=1,
    feedback_correct="Correct. \\( \\alpha > \\omega_0 \\Leftrightarrow R/(2L) > 1/\\sqrt{LC} \\Leftrightarrow R > 2L/\\sqrt{LC} = 2\\sqrt{L/C} \\).",
    feedback_incorrect="Starting from \\( R/(2L) > 1/\\sqrt{LC} \\), multiply both sides by \\( 2L \\): \\( R > 2L/\\sqrt{LC} = 2\\sqrt{L^2/LC} = 2\\sqrt{L/C} \\).",
    bloom_level="Apply", difficulty=2, katex_present=1,
  ),
  dict(
    title="Identifying underdamped circuit values",
    question_text="Which set of values produces an underdamped series RLC circuit?",
    choices=[
        "\\( R=100\\,\\Omega,\\;L=1\\,\\text{H},\\;C=10\\,\\text{mF} \\quad(\\alpha=50,\\;\\omega_0=10) \\)",
        "\\( R=2\\,\\Omega,\\;L=1\\,\\text{H},\\;C=0.25\\,\\text{F} \\quad(\\alpha=1,\\;\\omega_0=2) \\)",
        "\\( R=4\\,\\Omega,\\;L=1\\,\\text{H},\\;C=0.25\\,\\text{F} \\quad(\\alpha=2,\\;\\omega_0=2) \\)",
        "\\( R=8\\,\\Omega,\\;L=1\\,\\text{H},\\;C=0.25\\,\\text{F} \\quad(\\alpha=4,\\;\\omega_0=2) \\)"
    ],
    correct_answer_index=1,
    feedback_correct="Correct. For option B: \\( \\alpha=R/(2L)=1\\,\\text{s}^{-1} \\) and \\( \\omega_0=1/\\sqrt{0.25}=2\\,\\text{rad/s} \\). Since \\( \\alpha < \\omega_0 \\), the circuit is underdamped.",
    feedback_incorrect="Underdamped requires \\( \\alpha < \\omega_0 \\). Check each: A: \\( 50>10 \\) (overdamped); B: \\( 1<2 \\) (underdamped ✓); C: \\( 2=2 \\) (critically damped); D: \\( 4>2 \\) (overdamped).",
    bloom_level="Apply", difficulty=2, katex_present=1,
  ),
]

Q[11] = [
  dict(
    title="General form of overdamped solution",
    question_text="The general step response for an overdamped series RLC circuit is:",
    choices=[
        "\\( v_C(t) = e^{-\\alpha t}(D_1\\cos\\omega_d t + D_2\\sin\\omega_d t) + v_C(\\infty) \\)",
        "\\( v_C(t) = A_1 e^{s_1 t} + A_2 e^{s_2 t} + v_C(\\infty) \\)",
        "\\( v_C(t) = (B_1 + B_2 t)e^{-\\alpha t} + v_C(\\infty) \\)",
        "\\( v_C(t) = A_1 e^{j\\omega_d t} + A_2 e^{-j\\omega_d t} + v_C(\\infty) \\)"
    ],
    correct_answer_index=1,
    feedback_correct="Correct. In the overdamped case, \\( s_1 \\) and \\( s_2 \\) are distinct real negative numbers. The general solution \\( A_1e^{s_1t}+A_2e^{s_2t}+v_C(\\infty) \\) contains two free constants fixed by the initial conditions.",
    feedback_incorrect="For overdamped (\\( \\alpha>\\omega_0 \\)), the roots \\( s_{1,2} \\) are real and distinct. The solution is \\( A_1e^{s_1t}+A_2e^{s_2t}+v_C(\\infty) \\). The cosine/sine form belongs to the underdamped case; the \\( te^{-\\alpha t} \\) form belongs to critically damped.",
    bloom_level="Remember", difficulty=2, katex_present=1,
  ),
  dict(
    title="Nature of overdamped characteristic roots",
    question_text="In the overdamped regime (\\( \\alpha > \\omega_0 \\)), the characteristic roots \\( s_{1,2} = -\\alpha \\pm \\sqrt{\\alpha^2-\\omega_0^2} \\) are:",
    choices=[
        "Complex conjugates with negative real part.",
        "Real, distinct, and positive.",
        "Real, distinct, and negative.",
        "Equal negative real numbers."
    ],
    correct_answer_index=2,
    feedback_correct="Correct. Since \\( \\alpha > \\omega_0 \\), the square root is real and less than \\( \\alpha \\). Both \\( s_1 = -\\alpha + \\sqrt{\\alpha^2-\\omega_0^2} \\) and \\( s_2 = -\\alpha - \\sqrt{\\alpha^2-\\omega_0^2} \\) are negative real numbers.",
    feedback_incorrect="With \\( \\alpha>\\omega_0 \\): \\( \\sqrt{\\alpha^2-\\omega_0^2} < \\alpha \\), so \\( s_1 = -\\alpha + \\text{(something less than }\\alpha\\text{)} < 0 \\) and \\( s_2 < s_1 < 0 \\). Both roots are real and negative.",
    bloom_level="Remember", difficulty=2, katex_present=1,
  ),
  dict(
    title="What determines A1 and A2 in overdamped solution",
    question_text="In \\( v_C(t) = A_1e^{s_1t} + A_2e^{s_2t} + v_C(\\infty) \\), what determines the constants \\( A_1 \\) and \\( A_2 \\)?",
    choices=[
        "The component values \\( R \\), \\( L \\), \\( C \\) alone.",
        "The initial capacitor voltage \\( v_C(0^+) \\) and initial inductor current \\( i_L(0^+) \\) (which equals \\( i_C(0^+) \\)).",
        "The steady-state voltage \\( v_C(\\infty) \\) only.",
        "The characteristic roots \\( s_1 \\) and \\( s_2 \\) alone."
    ],
    correct_answer_index=1,
    feedback_correct="Correct. The component values determine \\( s_1,s_2 \\) and \\( v_C(\\infty) \\), but \\( A_1 \\) and \\( A_2 \\) are fixed by the two initial conditions: \\( v_C(0^+) \\) and \\( i_C(0^+)/C = v_C'(0^+) \\).",
    feedback_incorrect="\\( s_1 \\) and \\( s_2 \\) come from \\( R,L,C \\). The free constants \\( A_1,A_2 \\) are determined by evaluating the solution and its derivative at \\( t=0 \\), which requires knowing \\( v_C(0^+) \\) and \\( i_L(0^+) \\).",
    bloom_level="Remember", difficulty=2, katex_present=1,
  ),
]

Q[12] = [
  dict(
    title="Second equation for overdamped IC system",
    question_text="For \\( v_C(t) = A_1e^{s_1t}+A_2e^{s_2t}+v_C(\\infty) \\), the condition \\( v_C(0^+) \\) provides one equation: \\( A_1+A_2 = v_C(0^+)-v_C(\\infty) \\). What provides the second equation?",
    choices=[
        "Evaluating \\( v_C''(0) \\).",
        "Using \\( i_C(0^+) = Cv_C'(0^+) \\) to equate \\( C(s_1A_1+s_2A_2) \\) to \\( i_C(0^+) \\).",
        "Applying KVL at \\( t\\to\\infty \\).",
        "Substituting the roots back into the characteristic polynomial."
    ],
    correct_answer_index=1,
    feedback_correct="Correct. Differentiating: \\( v_C'(t) = s_1A_1e^{s_1t}+s_2A_2e^{s_2t} \\). At \\( t=0 \\): \\( v_C'(0^+) = s_1A_1+s_2A_2 = i_C(0^+)/C \\). This gives the second equation.",
    feedback_incorrect="Differentiate \\( v_C \\) to get \\( v_C'(t) = s_1A_1e^{s_1t}+s_2A_2e^{s_2t} \\). At \\( t=0^+ \\): \\( i_C(0^+) = Cv_C'(0^+) = C(s_1A_1+s_2A_2) \\). This is the second equation needed alongside the voltage condition.",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
  dict(
    title="IC system: computing A1+A2",
    question_text="For an overdamped circuit with \\( v_C(0^+)=0 \\), \\( v_C(\\infty)=10\\,\\text{V} \\), \\( i_C(0^+)=0 \\), \\( s_1=-2 \\), \\( s_2=-8 \\), what does the voltage initial condition give?",
    choices=[
        "\\( A_1 + A_2 = 10 \\)",
        "\\( A_1 + A_2 = -10 \\)",
        "\\( A_1 + A_2 = 0 \\)",
        "\\( A_1 + A_2 = -20 \\)"
    ],
    correct_answer_index=1,
    feedback_correct="Correct. \\( A_1+A_2 = v_C(0^+)-v_C(\\infty) = 0-10 = -10\\,\\text{V} \\).",
    feedback_incorrect="The voltage IC gives \\( A_1+A_2 = v_C(0^+)-v_C(\\infty) = 0-10 = -10 \\).",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
  dict(
    title="Solving the 2x2 IC system for overdamped coefficients",
    question_text="For the overdamped example in the notes (\\( s_1=-8.8,\\;s_2=-71.2 \\)), the IC system is: \\( A_1+A_2=-16 \\) and \\( -8.8A_1-71.2A_2=0 \\). From the current equation, what relationship follows?",
    choices=[
        "\\( A_1 = -A_2 \\)",
        "\\( A_1 = -(71.2/8.8)A_2 \\)",
        "\\( A_1 = (8.8/71.2)A_2 \\)",
        "\\( A_1 = -8.8A_2 \\)"
    ],
    correct_answer_index=1,
    feedback_correct="Correct. From \\( -8.8A_1 = 71.2A_2 \\Rightarrow A_1 = -(71.2/8.8)A_2 \\approx -8.09A_2 \\). Substituting into \\( A_1+A_2=-16 \\) gives \\( A_2=2.25\\,\\text{V} \\) and \\( A_1=-18.25\\,\\text{V} \\).",
    feedback_incorrect="Rearrange \\( -8.8A_1-71.2A_2=0 \\) as \\( -8.8A_1 = 71.2A_2 \\), so \\( A_1 = -(71.2/8.8)A_2 \\). Substituting into the first equation resolves \\( A_1 \\) and \\( A_2 \\) individually.",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
]

Q[13] = [
  dict(
    title="Continuity of capacitor voltage",
    question_text="In a series RLC circuit, which quantity is guaranteed to equal its pre-switch value immediately after the switch closes at \\( t=0 \\)?",
    choices=[
        "The current through the capacitor.",
        "The voltage across the resistor.",
        "The voltage across the capacitor.",
        "The voltage across the inductor."
    ],
    correct_answer_index=2,
    feedback_correct="Correct. Capacitor voltage cannot change instantaneously because \\( i_C = C\\,dv_C/dt \\); a finite current cannot charge \\( C \\) to a different voltage in zero time. Hence \\( v_C(0^+) = v_C(0^-) \\).",
    feedback_incorrect="Only energy-storing elements obey continuity: capacitor voltage and inductor current cannot jump instantaneously. Resistor voltage and capacitor current can change instantaneously.",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
  dict(
    title="Initial conditions for at-rest RLC circuit",
    question_text="A series RLC circuit is at rest before \\( t=0 \\) (no initial energy stored). What are \\( v_C(0^+) \\) and \\( i_C(0^+) \\)?",
    choices=[
        "\\( v_C(0^+)=V_s,\\;i_C(0^+)=0 \\)",
        "\\( v_C(0^+)=0,\\;i_C(0^+)=0 \\)",
        "\\( v_C(0^+)=0,\\;i_C(0^+)=V_s/R \\)",
        "\\( v_C(0^+)=V_s,\\;i_C(0^+)=V_s/R \\)"
    ],
    correct_answer_index=1,
    feedback_correct="Correct. No initial energy means \\( v_C(0^-)=0 \\) and \\( i_L(0^-)=0 \\). By continuity: \\( v_C(0^+)=0 \\) and \\( i_L(0^+)=i_C(0^+)=0 \\) (since L and C are in series).",
    feedback_incorrect="With no initial energy: \\( v_C(0^-)=0 \\) (uncharged capacitor) and \\( i_L(0^-)=0 \\) (no current in inductor). Continuity gives \\( v_C(0^+)=0 \\) and \\( i_C(0^+)=i_L(0^+)=0 \\).",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
  dict(
    title="Why not use i_C(0-) for initial condition",
    question_text="The notes warn against using \\( i_C(0^-) \\) directly as the initial current condition. Why?",
    choices=[
        "Because capacitor current is zero at DC, making \\( i_C(0^-)=0 \\) always useless.",
        "Because current through a capacitor CAN change instantaneously, so \\( i_C(0^-)\\neq i_C(0^+) \\) in general.",
        "Because the initial condition should be on voltage, not current.",
        "Because \\( i_C(0^-) \\) is undefined in a series circuit."
    ],
    correct_answer_index=1,
    feedback_correct="Correct. Unlike voltage (which cannot jump), capacitor current can change instantaneously. Instead, we use inductor-current continuity: \\( i_L(0^+)=i_L(0^-) \\), and since \\( i_L=i_C \\) in series, \\( i_C(0^+)=i_L(0^-) \\).",
    feedback_incorrect="Energy storage in a capacitor is \\( \\frac{1}{2}Cv_C^2 \\) — only voltage is continuous. The current through a capacitor is \\( i_C=Cv_C' \\) and can jump. Use \\( i_L(0^+)=i_L(0^-) \\) (inductor continuity) to get \\( i_C(0^+) \\).",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
]

Q[14] = [
  dict(
    title="Computing alpha for the overdamped example",
    question_text="For the overdamped example in the notes: \\( V_s=16\\,\\text{V} \\), \\( R=64\\,\\Omega \\), \\( L=0.8\\,\\text{H} \\), \\( C=2\\,\\text{mF} \\). What is \\( \\alpha \\)?",
    choices=[
        "\\( \\alpha = 40\\,\\text{s}^{-1} \\)",
        "\\( \\alpha = 80\\,\\text{s}^{-1} \\)",
        "\\( \\alpha = 25\\,\\text{s}^{-1} \\)",
        "\\( \\alpha = 8.8\\,\\text{s}^{-1} \\)"
    ],
    correct_answer_index=0,
    feedback_correct="Correct. \\( \\alpha = R/(2L) = 64/(2\\times0.8) = 64/1.6 = 40\\,\\text{s}^{-1} \\). With \\( \\omega_0=25\\,\\text{rad/s} \\), we confirm \\( \\alpha>\\omega_0 \\) (overdamped).",
    feedback_incorrect="\\( \\alpha = R/(2L) = 64/(1.6) = 40\\,\\text{s}^{-1} \\). Note: \\( R/L = 80\\,\\text{s}^{-1} \\) is the ODE coefficient, not \\( \\alpha \\).",
    bloom_level="Apply", difficulty=4, katex_present=1,
  ),
  dict(
    title="Steady-state value for overdamped example",
    question_text="For the overdamped example (\\( V_s=16\\,\\text{V} \\), solution \\( v_C(t)=-18.25e^{-8.8t}+2.25e^{-71.2t}+16 \\)), what does \\( v_C \\) approach as \\( t\\to\\infty \\)?",
    choices=[
        "\\( 0\\,\\text{V} \\)",
        "\\( 18.25\\,\\text{V} \\)",
        "\\( 16\\,\\text{V} \\)",
        "\\( -16\\,\\text{V} \\)"
    ],
    correct_answer_index=2,
    feedback_correct="Correct. Both \\( e^{-8.8t}\\to 0 \\) and \\( e^{-71.2t}\\to 0 \\) as \\( t\\to\\infty \\), leaving \\( v_C(\\infty) = 16\\,\\text{V} = V_s \\).",
    feedback_incorrect="Both exponential terms decay to zero (negative exponents). The only term that survives is the constant 16 V, confirming \\( v_C(\\infty)=V_s=16\\,\\text{V} \\).",
    bloom_level="Apply", difficulty=4, katex_present=1,
  ),
  dict(
    title="Computing i_C(t) for overdamped example",
    question_text="For the overdamped example, \\( v_C(t) = -18.25e^{-8.8t}+2.25e^{-71.2t}+16\\,\\text{V} \\) and \\( C=2\\,\\text{mF} \\). Which expression gives \\( i_C(t) \\) for \\( t>0 \\)?",
    choices=[
        "\\( i_C(t) = 0.32(e^{8.8t}-e^{71.2t})\\,\\text{A} \\)",
        "\\( i_C(t) = 0.32(e^{-8.8t}-e^{-71.2t})\\,\\text{A} \\)",
        "\\( i_C(t) = 0.32(e^{-8.8t}+e^{-71.2t})\\,\\text{A} \\)",
        "\\( i_C(t) = 160(e^{-8.8t}-e^{-71.2t})\\,\\text{A} \\)"
    ],
    correct_answer_index=1,
    feedback_correct="Correct. \\( v_C'(t) = (-8.8)(-18.25)e^{-8.8t}+(-71.2)(2.25)e^{-71.2t} \\approx 160.6e^{-8.8t}-160.2e^{-71.2t} \\). Then \\( i_C = Cv_C' \\approx 0.32(e^{-8.8t}-e^{-71.2t})\\,\\text{A} \\).",
    feedback_incorrect="Differentiate \\( v_C \\): \\( v_C'= 160.6e^{-8.8t}-160.2e^{-71.2t} \\). Multiply by \\( C=0.002\\,\\text{F} \\): \\( i_C \\approx 0.32(e^{-8.8t}-e^{-71.2t})\\,\\text{A} \\). Both exponents remain negative.",
    bloom_level="Apply", difficulty=4, katex_present=1,
  ),
]

# ── DB helpers ─────────────────────────────────────────────────────────────

def now():
    return datetime.datetime.utcnow().isoformat() + "Z"

def init_db(con):
    with open(SCHEMA) as f:
        con.executescript(f.read())
    t = now()
    for m in MODULES:
        con.execute("INSERT OR IGNORE INTO modules(id,number,title,course,created_at) VALUES(?,?,?,?,?)",
                    (*m, t))
    for c in CHAPTERS:
        con.execute("INSERT OR IGNORE INTO chapters(id,module_id,number,title) VALUES(?,?,?,?)", c)
    for tp in TOPICS:
        con.execute("INSERT OR IGNORE INTO topics(id,chapter_id,row_number,title,subtopic,learning_objective,bloom_level,difficulty) VALUES(?,?,?,?,?,?,?,?)", tp)
    con.commit()

def ch_mod(chapter_id):
    return CH_MOD[chapter_id]

def insert_topic_questions(con, topic_record, qlist):
    tid = topic_record[0]
    ch_id = topic_record[1]
    mod_id = ch_mod(ch_id)
    diff = topic_record[7]
    bloom = topic_record[6]
    # check existing
    cnt = con.execute("SELECT COUNT(*) FROM questions WHERE topic_id=? AND status!='failed'", (tid,)).fetchone()[0]
    if cnt >= 3:
        print(f"  [EXISTS] topic {tid} — skipping")
        return 0
    inserted = 0
    for i, q in enumerate(qlist, 1):
        con.execute("""
            INSERT INTO questions(topic_id,question_number,type,title,question_text,choices,
                correct_answer_index,points,tolerance,feedback_correct,feedback_incorrect,
                bloom_level,difficulty,katex_present,status,created_at,module_id,chapter_id)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (tid, i, "multiple_choice", q["title"], q["question_text"],
             json.dumps(q["choices"]), q["correct_answer_index"],
             1, 0.0, q["feedback_correct"], q["feedback_incorrect"],
             q.get("bloom_level", bloom), q.get("difficulty", diff),
             q["katex_present"], "draft", now(), mod_id, ch_id))
        inserted += 1
    con.commit()
    print(f"  [OK] topic {tid} ({topic_record[3]}: {topic_record[4]}) — {inserted} questions inserted")
    return inserted

# ── main ───────────────────────────────────────────────────────────────────

def main():
    con = sqlite3.connect(DB)
    init_db(con)
    print("DB initialized.\nGenerating Module 1, Chapters 1-3 (topics 1-14)...\n")
    total = 0
    for tp in TOPICS:
        tid = tp[0]
        if tid in Q:
            total += insert_topic_questions(con, tp, Q[tid])
    con.close()
    print(f"\nDone. {total} questions inserted this run.")

if __name__ == "__main__":
    main()
