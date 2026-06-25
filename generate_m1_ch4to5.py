#!/usr/bin/env python3
"""ENG17 Question Bank — Module 1, Chapters 4-5 (topics 15-24)"""
import sqlite3, json, datetime, os

BASE   = os.path.dirname(os.path.abspath(__file__))
DB     = os.path.join(BASE, "veriqa.db")
SCHEMA = os.path.join(BASE, "schema.sql")

TOPICS_15_24 = [
    (15,4,15,"Underdamped Response","Complex roots and damped frequency","Identify complex-conjugate roots and define the damped natural frequency omega_d","Understand",2),
    (16,4,16,"Underdamped Response","Euler's identity and general form","Apply Euler's identity to convert complex exponentials to real form and write v_C(t)","Apply",3),
    (17,4,17,"Underdamped Response","Initial conditions","Invoke initial conditions to find D1 and D2, using inductor current continuity for i_C(0+)","Apply",3),
    (18,4,18,"Underdamped Response","Amplitude-phase form","Convert D1*cos+D2*sin to amplitude-phase form D3*cos(omega_d*t+phi)","Apply",3),
    (19,4,19,"Underdamped Response","Physical interpretation — envelope","Describe the oscillatory envelope and explain why the solution reaches steady state","Understand",3),
    (20,4,20,"Underdamped Response","Worked example","Given V_s, R, L, C for underdamped circuit, determine alpha, omega_d, D1, D2, write v_C(t)","Apply",4),
    (21,5,21,"Critically Damped Response","Repeated root problem","Explain why A1*e^st+A2*e^st collapses and cannot satisfy both ICs when s1=s2","Understand",3),
    (22,5,22,"Critically Damped Response","General solution form","State and verify v_C(t)=(B1+B2*t)*e^{-alpha*t}+v_C(inf) satisfies the homogeneous ODE","Apply",3),
    (23,5,23,"Critically Damped Response","Initial conditions","Solve for B1=v_C(0)-v_C(inf) and B2=i_C(0)/C+alpha*(v_C(0)-v_C(inf)) from initial conditions","Apply",3),
    (24,5,24,"Damping Regime Comparison","Decay rate comparison","Compare transient decay rates and explain why critically damped decays fastest without oscillation","Analyze",4),
]

CH_MOD = {1:1,2:1,3:1,4:1,5:1,6:2,7:2,8:2}

Q = {}

Q[15] = [
  dict(
    title="Underdamped: form of complex roots",
    question_text="For an underdamped series RLC circuit (\\( \\alpha < \\omega_0 \\)), the characteristic roots \\( s_{1,2} = -\\alpha \\pm \\sqrt{\\alpha^2-\\omega_0^2} \\) simplify to:",
    choices=[
        "Real, distinct, and negative.",
        "Real, equal: \\( s_1=s_2=-\\alpha \\).",
        "Complex conjugates: \\( s_{1,2} = -\\alpha \\pm j\\omega_d \\).",
        "Pure imaginary: \\( s_{1,2} = \\pm j\\omega_0 \\)."
    ],
    correct_answer_index=2,
    feedback_correct="Correct. When \\( \\alpha<\\omega_0 \\), the quantity \\( \\alpha^2-\\omega_0^2<0 \\), so \\( \\sqrt{\\alpha^2-\\omega_0^2}=j\\sqrt{\\omega_0^2-\\alpha^2}=j\\omega_d \\). The roots are complex conjugates \\( -\\alpha\\pm j\\omega_d \\).",
    feedback_incorrect="With \\( \\alpha<\\omega_0 \\): \\( \\alpha^2-\\omega_0^2<0 \\), so the square root is imaginary. Writing \\( \\sqrt{\\alpha^2-\\omega_0^2}=j\\sqrt{\\omega_0^2-\\alpha^2}=j\\omega_d \\) gives complex-conjugate roots \\( s_{1,2}=-\\alpha\\pm j\\omega_d \\).",
    bloom_level="Understand", difficulty=2, katex_present=1,
  ),
  dict(
    title="Damped natural frequency definition",
    question_text="The damped natural frequency \\( \\omega_d \\) is defined as:",
    choices=[
        "\\( \\omega_d = \\sqrt{\\alpha^2+\\omega_0^2} \\)",
        "\\( \\omega_d = \\omega_0 - \\alpha \\)",
        "\\( \\omega_d = \\sqrt{\\omega_0^2-\\alpha^2} \\)",
        "\\( \\omega_d = \\alpha - \\omega_0 \\)"
    ],
    correct_answer_index=2,
    feedback_correct="Correct. \\( \\omega_d = \\sqrt{\\omega_0^2-\\alpha^2} \\). Since \\( \\alpha<\\omega_0 \\) in the underdamped case, \\( \\omega_d \\) is real and positive. It is the actual oscillation frequency of the damped response.",
    feedback_incorrect="From \\( s_{1,2}=-\\alpha\\pm j\\omega_d \\) and \\( s=-\\alpha\\pm\\sqrt{\\alpha^2-\\omega_0^2}=-\\alpha\\pm j\\sqrt{\\omega_0^2-\\alpha^2} \\), we read off \\( \\omega_d=\\sqrt{\\omega_0^2-\\alpha^2} \\).",
    bloom_level="Understand", difficulty=2, katex_present=1,
  ),
  dict(
    title="Computing omega_d numerically",
    question_text="A series RLC circuit has \\( \\alpha=3\\,\\text{s}^{-1} \\) and \\( \\omega_0=5\\,\\text{rad/s} \\). What is \\( \\omega_d \\)?",
    choices=[
        "\\( \\omega_d = 4\\,\\text{rad/s} \\)",
        "\\( \\omega_d = \\sqrt{34}\\,\\text{rad/s} \\)",
        "\\( \\omega_d = 2\\,\\text{rad/s} \\)",
        "\\( \\omega_d = 8\\,\\text{rad/s} \\)"
    ],
    correct_answer_index=0,
    feedback_correct="Correct. \\( \\omega_d = \\sqrt{\\omega_0^2-\\alpha^2} = \\sqrt{25-9} = \\sqrt{16} = 4\\,\\text{rad/s} \\).",
    feedback_incorrect="\\( \\omega_d = \\sqrt{\\omega_0^2-\\alpha^2} = \\sqrt{5^2-3^2} = \\sqrt{25-9} = \\sqrt{16} = 4\\,\\text{rad/s} \\).",
    bloom_level="Understand", difficulty=2, katex_present=1,
  ),
]

Q[16] = [
  dict(
    title="Euler's identity applied to e^{(-alpha+j*omega_d)t}",
    question_text="Applying Euler's identity \\( e^{j\\theta}=\\cos\\theta+j\\sin\\theta \\) to \\( e^{(-\\alpha+j\\omega_d)t} \\) gives:",
    choices=[
        "\\( e^{-\\alpha t}(\\cos\\omega_d t + j\\sin\\omega_d t) \\)",
        "\\( e^{-\\alpha t}(\\cos\\omega_d t - j\\sin\\omega_d t) \\)",
        "\\( \\cos(\\alpha t) + j\\sin(\\omega_d t) \\)",
        "\\( e^{\\alpha t}(\\cos\\omega_d t + j\\sin\\omega_d t) \\)"
    ],
    correct_answer_index=0,
    feedback_correct="Correct. Factor the exponent: \\( e^{(-\\alpha+j\\omega_d)t} = e^{-\\alpha t}\\cdot e^{j\\omega_d t} = e^{-\\alpha t}(\\cos\\omega_d t+j\\sin\\omega_d t) \\).",
    feedback_incorrect="Split the exponent: \\( e^{(-\\alpha+j\\omega_d)t}=e^{-\\alpha t}e^{j\\omega_d t} \\). Then Euler: \\( e^{j\\omega_d t}=\\cos\\omega_d t+j\\sin\\omega_d t \\). Multiplying gives \\( e^{-\\alpha t}(\\cos\\omega_d t+j\\sin\\omega_d t) \\).",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
  dict(
    title="Combining conjugate exponentials into real form",
    question_text="After applying Euler's identity to \\( A_1e^{s_1t}+A_2e^{s_2t} \\) with \\( s_{1,2}=-\\alpha\\pm j\\omega_d \\) and collecting real terms, the result is:",
    choices=[
        "\\( e^{-\\alpha t}(D_1\\cos\\omega_d t+D_2\\sin\\omega_d t) \\) where \\( D_1=A_1+A_2 \\), \\( D_2=j(A_1-A_2) \\).",
        "\\( e^{-\\alpha t}(A_1\\cos\\omega_d t+A_2\\sin\\omega_d t) \\) unchanged.",
        "\\( D_1\\cos\\omega_d t+D_2\\sin\\omega_d t \\) (no exponential).",
        "\\( e^{-\\alpha t}(D_1+D_2)\\cos(\\omega_d t) \\)."
    ],
    correct_answer_index=0,
    feedback_correct="Correct. Expanding both terms and grouping: \\( (A_1+A_2)\\cos\\omega_d t \\) and \\( j(A_1-A_2)\\sin\\omega_d t \\). Setting \\( D_1=A_1+A_2 \\) and \\( D_2=j(A_1-A_2) \\) (which are real for physical circuits) gives the standard real form.",
    feedback_incorrect="Expanding \\( A_1e^{(-\\alpha+j\\omega_d)t}+A_2e^{(-\\alpha-j\\omega_d)t} \\) and collecting cosine and sine terms yields \\( e^{-\\alpha t}[(A_1+A_2)\\cos\\omega_d t+j(A_1-A_2)\\sin\\omega_d t] \\). The combined real constants are \\( D_1=A_1+A_2 \\) and \\( D_2=j(A_1-A_2) \\).",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
  dict(
    title="Underdamped solution behavior as t → ∞",
    question_text="The complete underdamped step response is \\( v_C(t)=e^{-\\alpha t}(D_1\\cos\\omega_d t+D_2\\sin\\omega_d t)+v_C(\\infty) \\). What happens as \\( t\\to\\infty \\)?",
    choices=[
        "\\( v_C \\to v_C(\\infty) \\), because the exponential factor \\( e^{-\\alpha t}\\to 0 \\) kills the oscillatory term.",
        "\\( v_C \\to 0 \\), because both exponential and sinusoidal terms decay.",
        "\\( v_C \\) oscillates forever between \\( \\pm D_3+v_C(\\infty) \\).",
        "\\( v_C \\to D_1+v_C(\\infty) \\), because cosine approaches 1."
    ],
    correct_answer_index=0,
    feedback_correct="Correct. Since \\( \\alpha>0 \\), \\( e^{-\\alpha t}\\to 0 \\) as \\( t\\to\\infty \\). The entire oscillatory term vanishes, and \\( v_C(t)\\to v_C(\\infty)=V_s \\).",
    feedback_incorrect="The factor \\( e^{-\\alpha t}\\to 0 \\) as \\( t\\to\\infty \\) regardless of how \\( \\cos\\omega_d t \\) and \\( \\sin\\omega_d t \\) oscillate. So \\( v_C(t)\\to 0+v_C(\\infty)=v_C(\\infty) \\).",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
]

Q[17] = [
  dict(
    title="Finding D1 from voltage initial condition",
    question_text="For the underdamped solution, evaluating \\( v_C(0) \\) gives \\( D_1+v_C(\\infty) \\). Therefore:",
    choices=[
        "\\( D_1 = v_C(\\infty) \\)",
        "\\( D_1 = v_C(0) - v_C(\\infty) \\)",
        "\\( D_1 = v_C(0) + v_C(\\infty) \\)",
        "\\( D_1 = v_C(0)/v_C(\\infty) \\)"
    ],
    correct_answer_index=1,
    feedback_correct="Correct. At \\( t=0 \\): \\( v_C(0) = e^0(D_1\\cos 0 + D_2\\sin 0)+v_C(\\infty) = D_1+v_C(\\infty) \\). Solving: \\( D_1 = v_C(0)-v_C(\\infty) \\).",
    feedback_incorrect="Set \\( t=0 \\) in the underdamped solution: \\( \\cos(0)=1 \\), \\( \\sin(0)=0 \\), \\( e^0=1 \\), so \\( v_C(0)=D_1+v_C(\\infty) \\). Solving: \\( D_1=v_C(0)-v_C(\\infty) \\).",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
  dict(
    title="Correct source for i_C(0+) in underdamped IC",
    question_text="The notes emphasise that \\( i_C(0^+) \\) should be obtained from inductor current continuity, not by computing \\( Cv_C'(0^-) \\). Why?",
    choices=[
        "Because the formula \\( i_C=Cv_C' \\) is only valid in the overdamped regime.",
        "Because current through a capacitor CAN change instantaneously; only inductor current is continuous. Using \\( i_L(0^+)=i_L(0^-)=i_C(0^+) \\) is correct.",
        "Because \\( v_C'(0^-) \\) cannot be computed from the source values.",
        "Because \\( i_C(0^-)=0 \\) always, making the formula useless."
    ],
    correct_answer_index=1,
    feedback_correct="Correct. Unlike voltage continuity for capacitors, capacitor current can jump. The physically correct initial current comes from inductor continuity: \\( i_L(0^+)=i_L(0^-) \\). Since \\( L \\) and \\( C \\) are in series, \\( i_C(0^+)=i_L(0^+) \\).",
    feedback_incorrect="Capacitor current is \\( i_C=Cv_C' \\) and can change instantaneously (no continuity constraint). Only inductor current is continuous. Therefore use \\( i_C(0^+)=i_L(0^+)=i_L(0^-) \\), obtained from the pre-switch circuit.",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
  dict(
    title="D1 for underdamped example in notes",
    question_text="For the underdamped example: \\( V_s=24\\,\\text{V} \\), initially at rest (\\( v_C(0^-)=0 \\), \\( i_L(0^-)=0 \\)). What is \\( D_1 \\)?",
    choices=[
        "\\( D_1 = 24 \\)",
        "\\( D_1 = -24 \\)",
        "\\( D_1 = 0 \\)",
        "\\( D_1 = 12 \\)"
    ],
    correct_answer_index=1,
    feedback_correct="Correct. \\( D_1 = v_C(0^+)-v_C(\\infty) = 0-24 = -24\\,\\text{V} \\). The capacitor starts uncharged and must eventually charge to \\( V_s=24\\,\\text{V} \\).",
    feedback_incorrect="By voltage continuity: \\( v_C(0^+)=v_C(0^-)=0 \\). The steady state is \\( v_C(\\infty)=V_s=24\\,\\text{V} \\). Therefore \\( D_1=0-24=-24\\,\\text{V} \\).",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
]

Q[18] = [
  dict(
    title="Amplitude D3 in amplitude-phase form",
    question_text="The expression \\( D_1\\cos(\\omega_d t)+D_2\\sin(\\omega_d t) \\) can be written as \\( D_3\\cos(\\omega_d t+\\phi) \\). What is \\( D_3 \\)?",
    choices=[
        "\\( D_3 = D_1 + D_2 \\)",
        "\\( D_3 = |D_1 - D_2| \\)",
        "\\( D_3 = \\sqrt{D_1^2+D_2^2} \\)",
        "\\( D_3 = (D_1+D_2)/2 \\)"
    ],
    correct_answer_index=2,
    feedback_correct="Correct. Matching \\( D_3\\cos(\\omega_d t+\\phi) = D_3\\cos\\phi\\cos\\omega_d t - D_3\\sin\\phi\\sin\\omega_d t \\) with \\( D_1\\cos\\omega_d t+D_2\\sin\\omega_d t \\) gives \\( D_3^2=D_1^2+D_2^2 \\) via the Pythagorean identity.",
    feedback_incorrect="From \\( D_1=D_3\\cos\\phi \\) and \\( D_2=-D_3\\sin\\phi \\): \\( D_1^2+D_2^2 = D_3^2(\\cos^2\\phi+\\sin^2\\phi)=D_3^2 \\). Therefore \\( D_3=\\sqrt{D_1^2+D_2^2} \\).",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
  dict(
    title="Phase angle phi in amplitude-phase form",
    question_text="In the amplitude-phase form \\( D_3\\cos(\\omega_d t+\\phi) \\), the phase \\( \\phi \\) satisfies:",
    choices=[
        "\\( \\phi = \\arctan(D_2/D_1) \\)",
        "\\( \\phi = -\\arctan(D_2/D_1) \\)",
        "\\( \\phi = \\arctan(D_1/D_2) \\)",
        "\\( \\phi = \\arccos(D_1/D_3) \\; \\text{(no sign relationship)} \\)"
    ],
    correct_answer_index=1,
    feedback_correct="Correct. From \\( D_1=D_3\\cos\\phi \\) and \\( D_2=-D_3\\sin\\phi \\): \\( D_2/D_1=-\\tan\\phi \\Rightarrow \\phi=-\\arctan(D_2/D_1) \\).",
    feedback_incorrect="The matching conditions give \\( D_2=-D_3\\sin\\phi \\), so \\( D_2/D_1 = -\\sin\\phi/\\cos\\phi = -\\tan\\phi \\). Solving: \\( \\phi=-\\arctan(D_2/D_1) \\).",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
  dict(
    title="Numerical D3 calculation",
    question_text="For an underdamped circuit with \\( D_1=-3 \\) and \\( D_2=4 \\), compute \\( D_3 \\).",
    choices=[
        "\\( D_3 = 7 \\)",
        "\\( D_3 = 1 \\)",
        "\\( D_3 = 5 \\)",
        "\\( D_3 = 12 \\)"
    ],
    correct_answer_index=2,
    feedback_correct="Correct. \\( D_3=\\sqrt{(-3)^2+4^2}=\\sqrt{9+16}=\\sqrt{25}=5 \\). This is a 3-4-5 right triangle.",
    feedback_incorrect="\\( D_3=\\sqrt{D_1^2+D_2^2}=\\sqrt{9+16}=\\sqrt{25}=5 \\).",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
]

Q[19] = [
  dict(
    title="Envelope description of underdamped transient",
    question_text="The underdamped transient \\( v_{tr}(t)=D_3 e^{-\\alpha t}\\cos(\\omega_d t+\\phi) \\) is best described as:",
    choices=[
        "A cosine wave whose amplitude grows as \\( e^{\\alpha t} \\).",
        "A cosine wave oscillating at \\( \\omega_d \\) rad/s with a decaying amplitude envelope \\( D_3 e^{-\\alpha t} \\).",
        "A monotonically decaying exponential with no oscillation.",
        "A cosine wave oscillating at \\( \\omega_0 \\) rad/s forever."
    ],
    correct_answer_index=1,
    feedback_correct="Correct. The factor \\( D_3e^{-\\alpha t} \\) forms a decaying envelope, and \\( \\cos(\\omega_d t+\\phi) \\) provides the oscillation at the damped frequency \\( \\omega_d \\). As \\( \\alpha>0 \\), the envelope shrinks to zero.",
    feedback_incorrect="The exponential factor has a negative exponent (\\( -\\alpha t \\) with \\( \\alpha>0 \\)), so the amplitude \\( D_3e^{-\\alpha t} \\) decays — it does not grow. The oscillation frequency is \\( \\omega_d \\), not \\( \\omega_0 \\).",
    bloom_level="Understand", difficulty=3, katex_present=1,
  ),
  dict(
    title="Bounds on the underdamped transient",
    question_text="Which inequality correctly bounds the underdamped transient \\( v_{tr}(t) \\) for all \\( t\\geq 0 \\)?",
    choices=[
        "\\( -D_3 e^{-\\alpha t} \\leq v_{tr}(t) \\leq D_3 e^{-\\alpha t} \\)",
        "\\( v_{tr}(t) \\leq D_3 e^{\\alpha t} \\)",
        "\\( v_{tr}(t) = D_3 \\cos(\\omega_d t) \\) for all \\( t \\)",
        "\\( |v_{tr}(t)| = D_3 \\) for all \\( t \\)"
    ],
    correct_answer_index=0,
    feedback_correct="Correct. Since \\( |\\cos(\\omega_d t+\\phi)|\\leq 1 \\), we have \\( |v_{tr}(t)|=D_3e^{-\\alpha t}|\\cos(\\omega_d t+\\phi)|\\leq D_3e^{-\\alpha t} \\). The envelope \\( D_3e^{-\\alpha t} \\) bounds the oscillations from above and below.",
    feedback_incorrect="\\( |\\cos|\\leq 1 \\), so \\( |v_{tr}|=D_3e^{-\\alpha t}|\\cos|\\leq D_3e^{-\\alpha t} \\). The envelope is \\( \\pm D_3e^{-\\alpha t} \\), which decays to zero, confirming \\( v_{tr}\\to 0 \\).",
    bloom_level="Understand", difficulty=3, katex_present=1,
  ),
  dict(
    title="Which parameter controls underdamped decay rate",
    question_text="In the underdamped response \\( v_{tr}(t)=D_3 e^{-\\alpha t}\\cos(\\omega_d t+\\phi) \\), which parameter controls how quickly the oscillations decay toward zero?",
    choices=[
        "The damped frequency \\( \\omega_d \\) (controls oscillation rate).",
        "The natural frequency \\( \\omega_0 \\).",
        "The damping coefficient \\( \\alpha \\) (appears in the exponent \\( e^{-\\alpha t} \\)).",
        "The amplitude \\( D_3 \\)."
    ],
    correct_answer_index=2,
    feedback_correct="Correct. The decay rate is set by \\( \\alpha \\): a larger \\( \\alpha \\) means \\( e^{-\\alpha t} \\) shrinks faster. The time constant of the envelope is \\( \\tau = 1/\\alpha \\).",
    feedback_incorrect="The decay of the envelope is \\( e^{-\\alpha t} \\). Larger \\( \\alpha \\) = faster decay. \\( \\omega_d \\) controls the oscillation frequency, not the decay speed. \\( D_3 \\) is the initial amplitude only.",
    bloom_level="Understand", difficulty=3, katex_present=1,
  ),
]

Q[20] = [
  dict(
    title="Computing alpha for underdamped example",
    question_text="For the underdamped example in the notes: \\( V_s=24\\,\\text{V} \\), \\( R=12\\,\\Omega \\), \\( L=0.3\\,\\text{H} \\), \\( C=0.72\\,\\text{mF} \\). What is \\( \\alpha \\)?",
    choices=[
        "\\( \\alpha = 40\\,\\text{s}^{-1} \\)",
        "\\( \\alpha = 20\\,\\text{s}^{-1} \\)",
        "\\( \\alpha = 10\\,\\text{s}^{-1} \\)",
        "\\( \\alpha = 65\\,\\text{s}^{-1} \\)"
    ],
    correct_answer_index=1,
    feedback_correct="Correct. \\( \\alpha = R/(2L) = 12/(2\\times0.3) = 12/0.6 = 20\\,\\text{s}^{-1} \\). The notes confirm \\( s_{1,2} = -20\\pm65j \\), consistent with \\( \\alpha=20 \\).",
    feedback_incorrect="\\( \\alpha = R/(2L) = 12/0.6 = 20\\,\\text{s}^{-1} \\). Note: \\( R/L=12/0.3=40 \\) is the ODE coefficient \\( a \\), which equals \\( 2\\alpha \\), not \\( \\alpha \\) itself.",
    bloom_level="Apply", difficulty=4, katex_present=1,
  ),
  dict(
    title="Checking v_C(0) from underdamped solution",
    question_text="For the underdamped example, the solution is \\( v_C(t)=e^{-20t}(-24\\cos65t-7.38\\sin65t)+24 \\). What does this give at \\( t=0 \\)?",
    choices=[
        "\\( v_C(0)=24\\,\\text{V} \\)",
        "\\( v_C(0)=-24\\,\\text{V} \\)",
        "\\( v_C(0)=0\\,\\text{V} \\)",
        "\\( v_C(0)=-7.38\\,\\text{V} \\)"
    ],
    correct_answer_index=2,
    feedback_correct="Correct. At \\( t=0 \\): \\( e^0=1 \\), \\( \\cos(0)=1 \\), \\( \\sin(0)=0 \\), so \\( v_C(0)=(-24)(1)+24=0\\,\\text{V} \\). This matches the initial condition for an uncharged capacitor.",
    feedback_incorrect="At \\( t=0 \\): \\( e^{-20(0)}=1 \\), \\( \\cos(0)=1 \\), \\( \\sin(0)=0 \\). Therefore \\( v_C(0)=1\\times(-24\\times1-7.38\\times0)+24=-24+24=0\\,\\text{V} \\). ✓",
    bloom_level="Apply", difficulty=4, katex_present=1,
  ),
  dict(
    title="Finding D2 from current IC",
    question_text="For an underdamped circuit with \\( v_C(0)=0 \\), \\( v_C(\\infty)=10\\,\\text{V} \\), \\( \\alpha=5\\,\\text{s}^{-1} \\), \\( \\omega_d=10\\,\\text{rad/s} \\), and \\( i_C(0^+)=0 \\), compute \\( D_2 \\).",
    choices=[
        "\\( D_2 = 5 \\)",
        "\\( D_2 = 0 \\)",
        "\\( D_2 = -5 \\)",
        "\\( D_2 = -50 \\)"
    ],
    correct_answer_index=2,
    feedback_correct="Correct. \\( D_2=\\frac{1}{\\omega_d}\\left[\\frac{i_C(0)}{C}+\\alpha(v_C(0)-v_C(\\infty))\\right] = \\frac{1}{10}[0+5(0-10)] = \\frac{-50}{10}=-5 \\).",
    feedback_incorrect="Using the formula: \\( D_2=(1/\\omega_d)[i_C(0)/C+\\alpha(v_C(0)-v_C(\\infty))]=(1/10)[0+5(0-10)]=(1/10)(-50)=-5 \\). The factor \\( 1/\\omega_d \\) is essential.",
    bloom_level="Apply", difficulty=4, katex_present=1,
  ),
]

Q[21] = [
  dict(
    title="Why repeated roots give only one free constant",
    question_text="When \\( s_1=s_2=s \\) (critically damped), the naive solution \\( (A_1+A_2)e^{st}=A_3e^{st} \\) is insufficient because:",
    choices=[
        "\\( e^{st} \\) does not satisfy the homogeneous ODE when \\( s_1=s_2 \\).",
        "\\( A_3 \\) is only one free constant, but two initial conditions (\\( v_C(0) \\) and \\( i_C(0) \\)) must be matched independently.",
        "The exponential \\( e^{st} \\) grows to infinity since \\( s>0 \\) in critical damping.",
        "The steady-state term \\( v_C(\\infty) \\) is undefined when \\( \\alpha=\\omega_0 \\)."
    ],
    correct_answer_index=1,
    feedback_correct="Correct. One constant \\( A_3 \\) can match \\( v_C(0) \\) or \\( i_C(0) \\), but not both simultaneously (unless they happen to satisfy the same constraint). A second linearly independent solution is needed.",
    feedback_incorrect="\\( e^{st} \\) still satisfies the ODE. The problem is that merging \\( A_1 \\) and \\( A_2 \\) into \\( A_3=A_1+A_2 \\) leaves only one free constant to match two independent initial conditions—which is generally impossible.",
    bloom_level="Understand", difficulty=3, katex_present=1,
  ),
  dict(
    title="Contradiction from single-constant critically damped solution",
    question_text="With \\( v_C(t)=A_3e^{st}+v_C(\\infty) \\) in the critically damped case, the voltage IC gives \\( A_3=v_C(0)-v_C(\\infty) \\) and the current IC gives \\( A_3=i_C(0)/(sC) \\). These two expressions for \\( A_3 \\) are contradictory unless:",
    choices=[
        "\\( s=0 \\).",
        "\\( v_C(0)-v_C(\\infty) = i_C(0)/(sC) \\), which is not generally true for arbitrary initial conditions.",
        "\\( i_C(0)=0 \\) always in a critically damped circuit.",
        "\\( v_C(0)=v_C(\\infty) \\)."
    ],
    correct_answer_index=1,
    feedback_correct="Correct. The equality \\( v_C(0)-v_C(\\infty)=i_C(0)/(sC) \\) is a special relationship between initial conditions that does not hold in general. A physically valid solution must work for any \\( v_C(0) \\) and \\( i_C(0) \\).",
    feedback_incorrect="The two expressions for \\( A_3 \\) must both be satisfied simultaneously: \\( A_3 = v_C(0)-v_C(\\infty) \\) and \\( A_3 = i_C(0)/(sC) \\). These can only be equal for special initial conditions, not in general. Hence a second free constant is needed.",
    bloom_level="Understand", difficulty=3, katex_present=1,
  ),
  dict(
    title="Second independent solution for repeated root",
    question_text="What additional solution, valid only when \\( s_1=s_2=s \\), resolves the critical-damping degeneracy?",
    choices=[
        "A constant plus the exponential: \\( A_1+A_2e^{st} \\).",
        "The term \\( B_2 te^{st} \\), giving the second linearly independent solution.",
        "A pair of complex exponentials involving \\( \\omega_d \\).",
        "The original \\( A_3e^{st} \\) but with complex \\( A_3 \\)."
    ],
    correct_answer_index=1,
    feedback_correct="Correct. For a repeated root \\( s \\), the second independent solution is \\( te^{st} \\) (not \\( e^{st} \\) again). The general solution becomes \\( (B_1+B_2t)e^{-\\alpha t} \\), which can independently satisfy both initial conditions.",
    feedback_incorrect="When \\( s_1=s_2 \\), the two exponentials \\( e^{s_1t} \\) and \\( e^{s_2t} \\) are not linearly independent. The standard fix is to multiply the repeated solution by \\( t \\): the second independent solution is \\( te^{st} \\).",
    bloom_level="Understand", difficulty=3, katex_present=1,
  ),
]

Q[22] = [
  dict(
    title="Steady-state limit of critically damped solution",
    question_text="The critically damped solution is \\( v_C(t)=(B_1+B_2t)e^{-\\alpha t}+v_C(\\infty) \\). As \\( t\\to\\infty \\), \\( v_C \\) approaches:",
    choices=[
        "\\( 0 \\)",
        "\\( B_1 \\)",
        "\\( v_C(\\infty) \\)",
        "\\( \\infty \\)"
    ],
    correct_answer_index=2,
    feedback_correct="Correct. Since \\( \\alpha>0 \\), \\( e^{-\\alpha t}\\to 0 \\) exponentially fast — faster than \\( (B_1+B_2t) \\) can grow. So \\( (B_1+B_2t)e^{-\\alpha t}\\to 0 \\) and \\( v_C(t)\\to v_C(\\infty) \\).",
    feedback_incorrect="Even though \\( (B_1+B_2t) \\) grows linearly with \\( t \\), the exponential \\( e^{-\\alpha t} \\) decays faster than any polynomial grows. Therefore the product \\( (B_1+B_2t)e^{-\\alpha t}\\to 0 \\), leaving \\( v_C(\\infty) \\).",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
  dict(
    title="Why te^{-alpha*t} decays to zero",
    question_text="In the critically damped transient \\( (B_1+B_2t)e^{-\\alpha t} \\), the linear factor \\( B_2t \\) grows without bound, yet the full term decays to zero. Why?",
    choices=[
        "Because \\( B_2 \\) is always negative in a physical circuit.",
        "Because the exponential \\( e^{-\\alpha t} \\) decays faster than any polynomial grows for \\( \\alpha>0 \\) (L'Hopital's rule confirms \\( te^{-\\alpha t}\\to 0 \\)).",
        "Because \\( B_1 \\) eventually cancels \\( B_2t \\).",
        "Because the polynomial \\( te^{-\\alpha t} \\) is bounded by \\( 1/(e\\alpha) \\) and never grows."
    ],
    correct_answer_index=1,
    feedback_correct="Correct. Applying L'Hopital's rule: \\( \\lim_{t\\to\\infty}te^{-\\alpha t}=\\lim_{t\\to\\infty}t/e^{\\alpha t}=\\lim 1/(\\alpha e^{\\alpha t})=0 \\). Exponential decay dominates polynomial growth.",
    feedback_incorrect="By L'Hopital: \\( \\lim te^{-\\alpha t}=\\lim t/e^{\\alpha t}=\\lim 1/(\\alpha e^{\\alpha t})=0 \\). Exponential decay always beats polynomial growth for \\( \\alpha>0 \\).",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
  dict(
    title="Verification conditions for critically damped solution",
    question_text="To verify that \\( (B_1+B_2t)e^{-\\alpha t} \\) satisfies \\( v_{tr}''+av_{tr}'+bv_{tr}=0 \\) in the critically damped case, one requires both:",
    choices=[
        "\\( s+a=0 \\) alone.",
        "\\( s^2+as+b=0 \\) alone.",
        "\\( s^2+as+b=0 \\) AND \\( a+2s=0 \\) simultaneously.",
        "\\( s=\\sqrt{b} \\) alone."
    ],
    correct_answer_index=2,
    feedback_correct="Correct. Substituting \\( (B_1+B_2t)e^{st} \\) into the ODE yields \\( (B_1+B_2t)(s^2+as+b)+B_2(a+2s)=0 \\). For this to hold for all \\( t \\), both \\( s^2+as+b=0 \\) (coefficient of \\( t \\) and constant) and \\( a+2s=0 \\) must vanish. The second condition identifies the critically damped case.",
    feedback_incorrect="Substituting yields two conditions: (1) \\( s^2+as+b=0 \\) (characteristic polynomial) and (2) \\( a+2s=0 \\Rightarrow s=-a/2=-\\alpha \\). Both must hold simultaneously—this is exactly what singles out the critically damped case where \\( \\alpha=\\omega_0 \\).",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
]

Q[23] = [
  dict(
    title="Finding B1 from voltage IC",
    question_text="From \\( v_C(0)=B_1+v_C(\\infty) \\) (the critically damped solution at \\( t=0 \\)), solving for \\( B_1 \\) gives:",
    choices=[
        "\\( B_1 = v_C(\\infty) \\)",
        "\\( B_1 = v_C(0)+v_C(\\infty) \\)",
        "\\( B_1 = v_C(0)-v_C(\\infty) \\)",
        "\\( B_1 = -v_C(0) \\)"
    ],
    correct_answer_index=2,
    feedback_correct="Correct. At \\( t=0 \\): \\( v_C(0)=(B_1+0)e^0+v_C(\\infty)=B_1+v_C(\\infty) \\). Solving: \\( B_1=v_C(0)-v_C(\\infty) \\).",
    feedback_incorrect="Evaluate the solution at \\( t=0 \\): \\( e^0=1 \\), \\( t=0 \\), so \\( v_C(0)=B_1+v_C(\\infty) \\). Rearranging: \\( B_1=v_C(0)-v_C(\\infty) \\).",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
  dict(
    title="Formula for B2 in critically damped solution",
    question_text="The coefficient \\( B_2 \\) in the critically damped solution is:",
    choices=[
        "\\( B_2 = i_C(0)/C \\)",
        "\\( B_2 = i_C(0)/C + \\alpha(v_C(0)-v_C(\\infty)) \\)",
        "\\( B_2 = \\alpha(v_C(0)-v_C(\\infty)) \\)",
        "\\( B_2 = i_C(0)/(\\alpha C) \\)"
    ],
    correct_answer_index=1,
    feedback_correct="Correct. Differentiating \\( v_C \\) and evaluating at \\( t=0 \\): \\( v_C'(0)=B_2-\\alpha B_1 \\). Since \\( i_C(0)=Cv_C'(0) \\): \\( B_2=i_C(0)/C+\\alpha B_1=i_C(0)/C+\\alpha(v_C(0)-v_C(\\infty)) \\).",
    feedback_incorrect="Differentiating \\( v_C \\) gives \\( v_C'(t)=(B_2-\\alpha B_1-\\alpha B_2t)e^{-\\alpha t} \\). At \\( t=0 \\): \\( v_C'(0)=B_2-\\alpha B_1 \\). Using \\( i_C(0)=Cv_C'(0) \\) and \\( B_1=v_C(0)-v_C(\\infty) \\): \\( B_2=i_C(0)/C+\\alpha(v_C(0)-v_C(\\infty)) \\).",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
  dict(
    title="Numerical B1 and B2 for critically damped circuit",
    question_text="A critically damped circuit has \\( v_C(0)=0 \\), \\( v_C(\\infty)=5\\,\\text{V} \\), \\( i_C(0^+)=0 \\), \\( \\alpha=10\\,\\text{s}^{-1} \\). What are \\( B_1 \\) and \\( B_2 \\)?",
    choices=[
        "\\( B_1=5\\,\\text{V},\\;B_2=50\\,\\text{V/s} \\)",
        "\\( B_1=-5\\,\\text{V},\\;B_2=50\\,\\text{V/s} \\)",
        "\\( B_1=-5\\,\\text{V},\\;B_2=-50\\,\\text{V/s} \\)",
        "\\( B_1=0\\,\\text{V},\\;B_2=-50\\,\\text{V/s} \\)"
    ],
    correct_answer_index=2,
    feedback_correct="Correct. \\( B_1=v_C(0)-v_C(\\infty)=0-5=-5\\,\\text{V} \\). \\( B_2=i_C(0)/C+\\alpha B_1=0+10(-5)=-50\\,\\text{V/s} \\).",
    feedback_incorrect="\\( B_1=0-5=-5\\,\\text{V} \\). Then \\( B_2=i_C(0)/C+\\alpha(v_C(0)-v_C(\\infty))=0+10\\times(-5)=-50\\,\\text{V/s} \\). Both are negative.",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
]

Q[24] = [
  dict(
    title="Critically damped vs. overdamped decay rate",
    question_text="Compared to the overdamped regime, how does the critically damped response decay to steady state?",
    choices=[
        "More slowly, because of the polynomial factor \\( (B_1+B_2t) \\).",
        "At the same rate as one of the two overdamped exponentials.",
        "More rapidly: the overdamped root \\( s_1=-\\alpha+\\sqrt{\\alpha^2-\\omega_0^2} \\) is less negative than \\( -\\alpha \\), so it decays slower than the critically damped term.",
        "At the same rate only when \\( B_2=0 \\)."
    ],
    correct_answer_index=2,
    feedback_correct="Correct. In the overdamped case, \\( s_1=-\\alpha+\\sqrt{\\alpha^2-\\omega_0^2}>-\\alpha \\), meaning the slowest exponential decays slower than \\( e^{-\\alpha t} \\). The critically damped regime achieves the fastest monotonic decay.",
    feedback_incorrect="The overdamped solution contains \\( e^{s_1t} \\) with \\( s_1=-\\alpha+\\sqrt{\\alpha^2-\\omega_0^2} \\). Since \\( s_1>-\\alpha \\), this term decays more slowly than \\( e^{-\\alpha t} \\). So the critically damped response decays faster.",
    bloom_level="Analyze", difficulty=4, katex_present=1,
  ),
  dict(
    title="Oscillation in underdamped vs. other regimes",
    question_text="How does the underdamped transient response differ qualitatively from the critically damped and overdamped responses?",
    choices=[
        "It decays more rapidly because \\( \\alpha<\\omega_0 \\).",
        "It exhibits oscillations (ringing) before reaching steady state, while the other two regimes are monotonic.",
        "It does not decay to zero.",
        "The steady-state voltage differs from \\( V_s \\)."
    ],
    correct_answer_index=1,
    feedback_correct="Correct. In the underdamped regime, the complex roots produce sinusoidal oscillations (damped ringing). The critically and overdamped regimes have real negative roots, giving monotonic exponential decay with no oscillation.",
    feedback_incorrect="Underdamped means the roots are complex: \\( s=-\\alpha\\pm j\\omega_d \\). The imaginary part \\( \\omega_d \\) produces oscillations. Critically and overdamped have purely real roots — no imaginary part, no oscillation.",
    bloom_level="Analyze", difficulty=4, katex_present=1,
  ),
  dict(
    title="Optimal damping regime for fast, non-oscillatory switching",
    question_text="A relay must switch as fast as possible without any overshoot (oscillation). Which damping regime should the designer choose?",
    choices=[
        "Overdamped: two real roots guarantee monotonic decay.",
        "Underdamped: oscillations quickly drive the output to its final value.",
        "Critically damped: the fastest-decaying regime without oscillation.",
        "Underdamped with \\( \\alpha=0 \\): highest oscillation frequency."
    ],
    correct_answer_index=2,
    feedback_correct="Correct. Critically damped is the sweet spot: it decays faster than overdamped (no slow root) and has no oscillation (unlike underdamped). It is the fastest settling time without overshoot.",
    feedback_incorrect="Overdamped decays more slowly than critically damped (one of its roots is closer to zero). Underdamped has overshoot (oscillations). Critical damping minimises settling time while ensuring monotonic response.",
    bloom_level="Analyze", difficulty=4, katex_present=1,
  ),
]

# ── DB helpers (same as in part 1) ─────────────────────────────────────────

def now():
    return datetime.datetime.utcnow().isoformat() + "Z"

CH_MOD = {1:1,2:1,3:1,4:1,5:1,6:2,7:2,8:2}

def ch_mod(cid): return CH_MOD[cid]

def insert_topic_questions(con, tp, qlist):
    tid, ch_id = tp[0], tp[1]
    mod_id = ch_mod(ch_id)
    diff, bloom = tp[7], tp[6]
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
    print(f"  [OK] topic {tid} ({tp[3]}: {tp[4]}) — {inserted} questions inserted")
    return inserted

def ensure_topics(con, topics):
    for tp in topics:
        tid, ch_id, row_num, title, subtopic, lo, bloom, diff = tp
        exists = con.execute("SELECT 1 FROM topics WHERE id=?", (tid,)).fetchone()
        if not exists:
            con.execute("""
                INSERT INTO topics(id,chapter_id,row_number,title,subtopic,
                    learning_objective,bloom_level,difficulty)
                VALUES(?,?,?,?,?,?,?,?)""",
                (tid, ch_id, row_num, title, subtopic, lo, bloom, diff))
            print(f"  [TOPIC] inserted topic {tid}: {title} / {subtopic}")
    con.commit()

def main():
    con = sqlite3.connect(DB)
    print("Generating Module 1, Chapters 4-5 (topics 15-24)...\n")
    ensure_topics(con, TOPICS_15_24)
    total = 0
    for tp in TOPICS_15_24:
        tid = tp[0]
        if tid in Q:
            total += insert_topic_questions(con, tp, Q[tid])
    con.close()
    print(f"\nDone. {total} questions inserted this run.")

if __name__ == "__main__":
    main()
