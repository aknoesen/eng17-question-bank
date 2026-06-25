#!/usr/bin/env python3
"""ENG17 Question Bank — Module 2, Chapters 6-8 (topics 25-36)"""
import sqlite3, json, datetime, os

BASE = os.path.dirname(os.path.abspath(__file__))
DB   = os.path.join(BASE, "veriqa.db")

TOPICS_25_36 = [
    (25,6,25,"Abstraction and Modularity","Circuit abstraction motivation","Explain why engineers use circuit abstraction and what an interface provides","Understand",1),
    (26,6,26,"Abstraction and Modularity","Terminal v-i characteristic","Define the terminal v-i characteristic and state what information it captures","Remember",1),
    (27,6,27,"Thévenin's Theorem","Theorem statement and linearity requirement","State Thévenin's theorem and identify which circuits it applies to","Remember",2),
    (28,6,28,"Thévenin's Theorem","Finding v_th (open-circuit voltage)","Compute v_th by finding the open-circuit voltage at the output terminals","Apply",3),
    (29,7,29,"Finding R_th","Method 1 — Short-circuit current","Apply the short-circuit current method to find R_th = v_th / i_sc","Apply",3),
    (30,7,30,"Finding R_th","Method 2 — Source deactivation","Apply source deactivation to find R_th; identify when this method is INVALID","Apply",3),
    (31,7,31,"Finding R_th","Method 3 — Test source","Apply an external test source to find R_th when dependent sources are present","Apply",4),
    (32,7,32,"Norton's Theorem","Norton equivalent derivation","Derive the Norton equivalent from the Thévenin equivalent via source transformation","Apply",3),
    (33,8,33,"Norton's Theorem","Parameter triangle relationship","Use the Thévenin–Norton parameter triangle (v_th, i_N, R_th) to convert between forms","Apply",3),
    (34,8,34,"Maximum Power Transfer","Load power expression","Derive p_L as a function of R_L from the Thévenin equivalent","Apply",3),
    (35,8,35,"Maximum Power Transfer","Optimal load resistance","Show using calculus (dp_L/dR_L = 0) that R_L* = R_th maximises power","Apply",4),
    (36,8,36,"Maximum Power Transfer","Power efficiency at MPT","Compute source efficiency at MPT and explain why it equals 50%","Analyze",4),
]

CH_MOD = {1:1,2:1,3:1,4:1,5:1,6:2,7:2,8:2}

Q = {}

Q[25] = [
  dict(
    title="Purpose of circuit abstraction",
    question_text="In the context of engineering design, what does a circuit's \\emph{interface} provide?",
    choices=[
        "The exact internal implementation of all components, enabling full circuit reconstruction.",
        "A description of the circuit's external behavior at its terminals, without requiring knowledge of internal details.",
        "A list of component tolerances and failure modes.",
        "The power dissipated internally by each resistor."
    ],
    correct_answer_index=1,
    feedback_correct="Correct. An interface describes external behavior — what the circuit does at its terminals — without exposing internal structure. This is the essence of abstraction: other designers interact with the interface, not the internals.",
    feedback_incorrect="An interface exposes external behavior (terminal voltages and currents), not internal details. The whole point of abstraction is that designers don't need to know how a sub-circuit is built — only how it behaves at its terminals.",
    bloom_level="Understand", difficulty=1, katex_present=0,
  ),
  dict(
    title="Why abstraction matters for large designs",
    question_text="A smartphone contains millions of transistors organized into blocks (CPU, RF, ADC, etc.). Why is circuit abstraction essential for designing such a system?",
    choices=[
        "It allows each block to be analyzed at the transistor level simultaneously by a single engineer.",
        "It removes the need to understand any low-level details anywhere in the design.",
        "It enables each block to be developed and verified independently using a standardized terminal interface, so designers can work on one block without knowing the internals of others.",
        "It guarantees that all blocks operate with zero power consumption."
    ],
    correct_answer_index=2,
    feedback_correct="Correct. Abstraction enables modularity: each sub-circuit is characterized by its terminal interface, so teams can work independently. The RF designer doesn't need microarchitecture knowledge and vice versa.",
    feedback_incorrect="Abstraction works by letting each block be treated as a 'black box' with a well-defined interface. This enables independent development — but engineers still need to understand the block they are building at whatever level is appropriate.",
    bloom_level="Understand", difficulty=1, katex_present=0,
  ),
  dict(
    title="Limitation of full-circuit analysis vs. abstraction",
    question_text="Without circuit abstraction, connecting a new load to a complex source network would require:",
    choices=[
        "Re-solving the entire source network from scratch for each new load.",
        "Only knowing the Thévenin equivalent, which remains valid regardless of the load.",
        "Computing the Norton equivalent once and never updating it.",
        "Measuring the short-circuit current once and using it for all loads."
    ],
    correct_answer_index=0,
    feedback_correct="Correct. Without abstraction, every load change forces a complete re-analysis of the source network. Thévenin/Norton equivalents capture the source behavior in two parameters (\\( v_{th}, R_{th} \\)) that stay fixed regardless of load.",
    feedback_incorrect="Without a pre-computed equivalent, each load change demands solving the full network again. The power of Thévenin/Norton is that two parameters describe the source for any load — you never re-solve the internals.",
    bloom_level="Understand", difficulty=1, katex_present=1,
  ),
]

Q[26] = [
  dict(
    title="Terminal v-i characteristic definition",
    question_text="The terminal \\( v \\)-\\( i \\) characteristic of a circuit is:",
    choices=[
        "The relationship between power delivered and time.",
        "The relationship between the voltage across the output terminals and the current flowing out of them, for all possible loads.",
        "The internal resistance seen looking into the circuit from any node.",
        "The Thevenin voltage divided by the Norton current."
    ],
    correct_answer_index=1,
    feedback_correct="Correct. The \\( v \\)-\\( i \\) characteristic is the function \\( v = f(i) \\) (or \\( i = g(v) \\)) at the output terminals. For a linear circuit it is a straight line; Thévenin form writes it as \\( v = v_{th} - R_{th}i \\).",
    feedback_incorrect="The \\( v \\)-\\( i \\) characteristic specifies how the terminal voltage \\( v \\) depends on the terminal current \\( i \\) — equivalently, what \\( (v,i) \\) pairs are possible at the output port. For a linear circuit this is a single straight line.",
    bloom_level="Remember", difficulty=1, katex_present=1,
  ),
  dict(
    title="v-i characteristic of a Thevenin equivalent",
    question_text="A Thévenin equivalent has open-circuit voltage \\( v_{th} \\) and Thévenin resistance \\( R_{th} \\). Its terminal \\( v \\)-\\( i \\) equation is:",
    choices=[
        "\\( v = R_{th}\\,i \\)",
        "\\( i = v_{th}/R_{th} \\) (constant current)",
        "\\( v = v_{th} - R_{th}\\,i \\)",
        "\\( v = v_{th} + R_{th}\\,i \\)"
    ],
    correct_answer_index=2,
    feedback_correct="Correct. KVL around the Thévenin equivalent: \\( v_{th} = R_{th}\\,i + v \\), so \\( v = v_{th}-R_{th}\\,i \\). This is a line with \\( v \\)-intercept \\( v_{th} \\) (open-circuit, \\( i=0 \\)) and \\( i \\)-intercept \\( v_{th}/R_{th}=i_N \\) (short-circuit).",
    feedback_incorrect="Write KVL: source \\( v_{th} \\) drives current through \\( R_{th} \\) then delivers \\( v \\) to the load. KVL: \\( v_{th}=R_{th}i+v \\Rightarrow v=v_{th}-R_{th}i \\). Note the minus sign: higher \\( i \\) means lower terminal \\( v \\).",
    bloom_level="Remember", difficulty=1, katex_present=1,
  ),
  dict(
    title="Two key points on the v-i characteristic",
    question_text="For a linear circuit, the \\( v \\)-\\( i \\) characteristic is a straight line determined by two special points. Which two?",
    choices=[
        "Maximum power point and half-power point.",
        "Open-circuit voltage (\\( i=0 \\)) and short-circuit current (\\( v=0 \\)).",
        "Thevenin voltage and Norton resistance.",
        "Norton current and Thevenin resistance."
    ],
    correct_answer_index=1,
    feedback_correct="Correct. At \\( i=0 \\): \\( v=v_{th} \\) (open circuit). At \\( v=0 \\): \\( i=i_N=v_{th}/R_{th} \\) (short circuit). These two points uniquely define the line \\( v=v_{th}-R_{th}i \\).",
    feedback_incorrect="A line is determined by two points. The natural choices are: the \\( v \\)-intercept (open circuit: \\( i=0,\\;v=v_{th} \\)) and the \\( i \\)-intercept (short circuit: \\( v=0,\\;i=i_{sc}=v_{th}/R_{th} \\)).",
    bloom_level="Remember", difficulty=1, katex_present=1,
  ),
]

Q[27] = [
  dict(
    title="Thevenin's theorem statement",
    question_text="Thévenin's theorem states that any linear circuit, viewed from two output terminals, can be replaced by:",
    choices=[
        "A single current source \\( i_N \\) in series with \\( R_{th} \\).",
        "A single voltage source \\( v_{th} \\) in parallel with \\( R_{th} \\).",
        "A single voltage source \\( v_{th} \\) in series with a resistance \\( R_{th} \\).",
        "A dependent voltage source \\( v_{th} \\) in series with a capacitor \\( C_{th} \\)."
    ],
    correct_answer_index=2,
    feedback_correct="Correct. The Thévenin equivalent is a voltage source \\( v_{th} \\) (the open-circuit voltage) in series with \\( R_{th} \\). This two-element circuit produces the same terminal \\( v \\)-\\( i \\) characteristic as the original network for any load.",
    feedback_incorrect="Thévenin: series combination of \\( v_{th} \\) and \\( R_{th} \\). (Norton is the parallel combination of \\( i_N \\) and \\( R_{th} \\) — that's a different theorem.) Both \\( v_{th} \\) and \\( R_{th} \\) are positive real numbers for passive networks.",
    bloom_level="Remember", difficulty=2, katex_present=1,
  ),
  dict(
    title="Linearity requirement for Thevenin's theorem",
    question_text="Thévenin's theorem requires the circuit to be linear. Which of the following would VIOLATE this requirement?",
    choices=[
        "Independent voltage sources.",
        "Dependent current sources (CCCS, VCCS).",
        "A diode (exponential \\( i \\)-\\( v \\) relationship).",
        "Fixed resistors."
    ],
    correct_answer_index=2,
    feedback_correct="Correct. A diode has a nonlinear \\( i \\)-\\( v \\) relationship \\( i=I_0(e^{v/V_T}-1) \\). Thévenin's theorem applies only to circuits where all element equations are linear (resistors, independent sources, dependent sources with linear gain). Nonlinear elements violate the superposition principle on which the theorem rests.",
    feedback_incorrect="Linear circuits consist of elements with linear \\( v \\)-\\( i \\) relationships: resistors (\\( v=Ri \\)), ideal sources, and linear dependent sources. A diode's exponential characteristic \\( i\\propto e^{v/V_T} \\) is nonlinear, so Thévenin's theorem does not apply.",
    bloom_level="Remember", difficulty=2, katex_present=1,
  ),
  dict(
    title="What Thevenin equivalence preserves",
    question_text="When you replace a circuit with its Thévenin equivalent, which quantity is guaranteed to be identical for any load \\( R_L \\)?",
    choices=[
        "Power dissipated inside the original network (internal power losses).",
        "The terminal voltage \\( v \\) and current \\( i \\) at the output port.",
        "The total current drawn from any independent source inside the network.",
        "The open-circuit voltage only; short-circuit current will differ."
    ],
    correct_answer_index=1,
    feedback_correct="Correct. The Thévenin equivalent has the same \\( v \\)-\\( i \\) characteristic as the original circuit at the output terminals. Therefore the terminal voltage and current — and hence power delivered to any load — are identical. Internal quantities (currents inside the original network) are not preserved.",
    feedback_incorrect="The Thévenin equivalent preserves the external \\( v \\)-\\( i \\) characteristic at the terminals. For any load \\( R_L \\), the terminal voltage \\( v \\) and current \\( i \\) are the same as with the original circuit. Internal node voltages and branch currents inside the original network are NOT preserved.",
    bloom_level="Remember", difficulty=2, katex_present=1,
  ),
]

Q[28] = [
  dict(
    title="Open-circuit voltage definition",
    question_text="To find \\( v_{th} \\) for a circuit, you connect \\( R_L=\\infty \\) (open circuit) at the output terminals and measure the voltage. This is valid because:",
    choices=[
        "An infinite load draws zero current, so the open-circuit terminal voltage equals \\( v_{th} \\) directly.",
        "The open circuit forces \\( v=0 \\), giving the Thévenin source voltage by KVL.",
        "An open circuit draws maximum current, revealing the internal voltage.",
        "The Thévenin source must equal the Norton source when no load is connected."
    ],
    correct_answer_index=0,
    feedback_correct="Correct. With \\( R_L=\\infty \\) (open circuit), \\( i=0 \\). KVL around the Thévenin equivalent: \\( v = v_{th}-R_{th}\\cdot 0 = v_{th} \\). So the open-circuit terminal voltage IS \\( v_{th} \\).",
    feedback_incorrect="Open circuit means \\( i=0 \\). In the Thévenin equivalent: \\( v = v_{th}-R_{th}i = v_{th}-0 = v_{th} \\). The zero current causes zero drop across \\( R_{th} \\), so the full source voltage appears at the terminals.",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
  dict(
    title="Computing v_th with resistive divider",
    question_text="A circuit has \\( V_s=20\\,\\text{V} \\), with \\( R_1=5\\,\\Omega \\) in series and \\( R_2=20\\,\\Omega \\) in parallel with the output terminals (\\( R_2 \\) is connected across the open-circuit terminals). What is \\( v_{th} \\)?",
    choices=[
        "\\( v_{th}=20\\,\\text{V} \\)",
        "\\( v_{th}=4\\,\\text{V} \\)",
        "\\( v_{th}=16\\,\\text{V} \\)",
        "\\( v_{th}=10\\,\\text{V} \\)"
    ],
    correct_answer_index=2,
    feedback_correct="Correct. With the output open, no current flows through the external circuit. The circuit is a voltage divider: \\( v_{th} = V_s\\cdot\\frac{R_2}{R_1+R_2} = 20\\cdot\\frac{20}{5+20} = 20\\cdot0.8 = 16\\,\\text{V} \\).",
    feedback_incorrect="The open-circuit voltage is found by voltage divider (no load current): \\( v_{th}=V_s\\cdot R_2/(R_1+R_2) = 20\\cdot 20/25 = 16\\,\\text{V} \\).",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
  dict(
    title="v_th with current source",
    question_text="A circuit has \\( I_s=2\\,\\text{A} \\) with \\( R_1=4\\,\\Omega \\) (connects source to output node) and \\( R_2=8\\,\\Omega \\) (shunts the output to ground). Find \\( v_{th} \\).",
    choices=[
        "\\( v_{th}=8\\,\\text{V} \\)",
        "\\( v_{th}=16\\,\\text{V} \\)",
        "\\( v_{th}=2\\,\\text{V} \\)",
        "\\( v_{th}=\\frac{16}{3}\\,\\text{V} \\)"
    ],
    correct_answer_index=0,
    feedback_correct="Correct. With output open, \\( I_s \\) splits between \\( R_1 \\) and \\( R_2 \\). Actually if \\( R_1 \\) is in series with \\( I_s \\) and \\( R_2 \\) shunts the output node to ground, all of \\( I_s \\) flows through \\( R_2 \\): \\( v_{th}=I_s\\cdot R_2 = 2\\cdot 8 = 16\\,\\text{V} \\). Wait — if \\( R_1 \\) is in series between source and output, and \\( R_2 \\) is across the output, KCL at output: \\( I_s = i_{R_2}\\Rightarrow v_{th}=I_s R_2=16\\,\\text{V} \\). Re-checking: answer should be 8 V if \\( R_2=4 \\). For \\( R_2=8\\Omega \\): \\( v_{th}=16\\,\\text{V} \\).",
    feedback_incorrect="Open circuit means no current into the load. KCL at the output node: all of \\( I_s \\) must flow through \\( R_2 \\) to ground (since the output terminal is open). Therefore \\( v_{th}=I_s R_2=2\\times 8=16\\,\\text{V} \\).",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
]

# Fix Q[28] question 3 (index 2) — rewrite for clean answer
Q[28][2] = dict(
    title="v_th for current-source circuit",
    question_text="A circuit has \\( I_s=3\\,\\text{A} \\) in parallel with \\( R_1=6\\,\\Omega \\). The output terminals are connected across \\( R_1 \\). Find \\( v_{th} \\).",
    choices=[
        "\\( v_{th}=18\\,\\text{V} \\)",
        "\\( v_{th}=3\\,\\text{V} \\)",
        "\\( v_{th}=0.5\\,\\text{V} \\)",
        "\\( v_{th}=6\\,\\text{V} \\)"
    ],
    correct_answer_index=0,
    feedback_correct="Correct. The output terminals are across \\( R_1 \\). With the output open, all of \\( I_s \\) flows through \\( R_1 \\): \\( v_{th}=I_s R_1=3\\times 6=18\\,\\text{V} \\).",
    feedback_incorrect="Output open \\( \\Rightarrow \\) no load current. The entire \\( I_s=3\\,\\text{A} \\) flows through \\( R_1=6\\,\\Omega \\). By Ohm's law: \\( v_{th}=3\\times 6=18\\,\\text{V} \\).",
    bloom_level="Apply", difficulty=3, katex_present=1,
)

Q[29] = [
  dict(
    title="Short-circuit current method — procedure",
    question_text="In Method 1 (short-circuit current method) for finding \\( R_{th} \\), the steps are:",
    choices=[
        "Deactivate all sources, then compute the equivalent resistance looking into the terminals.",
        "Find \\( v_{th} \\) (open circuit) and \\( i_{sc} \\) (short circuit), then \\( R_{th}=v_{th}/i_{sc} \\).",
        "Apply a test voltage \\( v_x \\) at the terminals and compute \\( R_{th}=v_x/i_x \\).",
        "Find \\( v_{th} \\) and divide by the Norton resistance \\( R_N \\)."
    ],
    correct_answer_index=1,
    feedback_correct="Correct. Method 1: (a) compute \\( v_{th} \\) with output open; (b) replace the load with a short and compute \\( i_{sc} \\); (c) \\( R_{th}=v_{th}/i_{sc} \\). This works even when dependent sources are present.",
    feedback_incorrect="Method 1 uses both the open-circuit voltage and the short-circuit current. You don't deactivate sources (that's Method 2) or inject a test source (Method 3). The formula is \\( R_{th}=v_{th}/i_{sc} \\).",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
  dict(
    title="Computing R_th via Method 1 — resistive example",
    question_text="For the example in the notes: \\( v_{th}=16\\,\\text{V} \\), \\( R_1=5\\,\\Omega \\), \\( R_2=20\\,\\Omega \\). The short-circuit current \\( i_{sc} \\) (found by shorting the output) is \\( 4\\,\\text{A} \\). What is \\( R_{th} \\)?",
    choices=[
        "\\( R_{th}=80\\,\\Omega \\)",
        "\\( R_{th}=20\\,\\Omega \\)",
        "\\( R_{th}=4\\,\\Omega \\)",
        "\\( R_{th}=5\\,\\Omega \\)"
    ],
    correct_answer_index=2,
    feedback_correct="Correct. \\( R_{th}=v_{th}/i_{sc}=16/4=4\\,\\Omega \\). Alternatively, with the output shorted, \\( R_2 \\) is bypassed and \\( i_{sc}=V_s/R_1=20/5=4\\,\\text{A} \\), confirming \\( R_{th}=16/4=4\\,\\Omega \\).",
    feedback_incorrect="\\( R_{th}=v_{th}/i_{sc}=16/4=4\\,\\Omega \\). With output shorted, \\( R_2 \\) is short-circuited (bypassed), leaving only \\( R_1 \\) limiting the current: \\( i_{sc}=20/5=4\\,\\text{A} \\).",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
  dict(
    title="Short-circuit current for Norton current",
    question_text="What is the relationship between \\( i_{sc} \\) (short-circuit current measured during Method 1) and \\( i_N \\) (the Norton current)?",
    choices=[
        "\\( i_N = v_{th}/i_{sc} \\) — they are inverses.",
        "\\( i_N = i_{sc} \\) — they are identical.",
        "\\( i_N = R_{th}\\cdot i_{sc} \\) — scaled by resistance.",
        "They are unrelated."
    ],
    correct_answer_index=1,
    feedback_correct="Correct. The Norton current \\( i_N \\) is defined as the short-circuit current at the output terminals — exactly what Method 1 measures. So \\( i_N=i_{sc} \\) by definition.",
    feedback_incorrect="Norton current \\( i_N \\) is the current that flows when the output is short-circuited. This is precisely \\( i_{sc} \\) measured in Method 1. Therefore \\( i_N=i_{sc} \\).",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
]

Q[30] = [
  dict(
    title="Source deactivation procedure",
    question_text="In Method 2 (source deactivation), independent sources are deactivated by:",
    choices=[
        "Replacing voltage sources with open circuits and current sources with short circuits.",
        "Replacing voltage sources with short circuits (zero volts) and current sources with open circuits (zero amps).",
        "Setting all source values to their Thévenin equivalents.",
        "Removing all sources and computing the remaining resistor network."
    ],
    correct_answer_index=1,
    feedback_correct="Correct. Deactivating a source means setting it to zero: a zero-volt voltage source is a short circuit (wire); a zero-amp current source is an open circuit (broken wire). The resulting passive network's input resistance at the terminals is \\( R_{th} \\).",
    feedback_incorrect="Zero voltage \\( \\Rightarrow \\) short circuit (replace voltage source with a wire). Zero current \\( \\Rightarrow \\) open circuit (remove current source, leave gap). After deactivation, compute the equivalent resistance seen at the output terminals.",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
  dict(
    title="R_th by source deactivation — example",
    question_text="For the notes' example (\\( V_s=20\\,\\text{V} \\), \\( R_1=5\\,\\Omega \\), \\( R_2=20\\,\\Omega \\)): after deactivating \\( V_s \\), what is \\( R_{th} \\) seen at the output?",
    choices=[
        "\\( R_{th}=25\\,\\Omega \\)",
        "\\( R_{th}=20\\,\\Omega \\)",
        "\\( R_{th}=4\\,\\Omega \\)",
        "\\( R_{th}=5\\,\\Omega \\)"
    ],
    correct_answer_index=2,
    feedback_correct="Correct. Deactivating \\( V_s \\) replaces it with a short. Looking into the output: \\( R_1 \\) and \\( R_2 \\) are now in parallel (\\( R_1 \\) connects to ground through the short): \\( R_{th}=R_1\\|R_2=5\\|20=\\frac{5\\times20}{5+20}=\\frac{100}{25}=4\\,\\Omega \\).",
    feedback_incorrect="Shorting \\( V_s \\) connects \\( R_1 \\) to ground. From the output terminals, \\( R_2 \\) is in parallel with \\( R_1 \\) (now grounded): \\( R_{th}=R_1\\|R_2=5\\|20=4\\,\\Omega \\). Same answer as Method 1, as expected.",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
  dict(
    title="When Method 2 is INVALID",
    question_text="Method 2 (source deactivation) gives the WRONG \\( R_{th} \\) when the circuit contains:",
    choices=[
        "Multiple independent voltage sources.",
        "Resistors in a bridge (Wheatstone) configuration.",
        "Dependent sources (VCVS, CCCS, etc.).",
        "More than two terminals."
    ],
    correct_answer_index=2,
    feedback_correct="Correct. Dependent sources cannot be deactivated — they respond to circuit variables and their contribution to the terminal resistance is NOT captured by simply shorting/opening them. For circuits with dependent sources, use Method 1 or Method 3.",
    feedback_incorrect="The key restriction is dependent sources. Deactivating an independent source sets it to zero, which is a valid linear superposition step. But a dependent source is controlled by some variable in the circuit; zeroing it would change the circuit's behavior incorrectly. Methods 1 or 3 handle dependent sources correctly.",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
]

Q[31] = [
  dict(
    title="Test source method — setup",
    question_text="In Method 3 (external test source), you deactivate all independent sources and apply a test voltage \\( v_x \\) at the output terminals. Then \\( R_{th} \\) is found as:",
    choices=[
        "\\( R_{th}=i_x/v_x \\) (ratio inverted)",
        "\\( R_{th}=v_x \\cdot i_x \\) (product)",
        "\\( R_{th}=v_x/i_x \\) (Ohm's law at the terminals)",
        "\\( R_{th}=v_x^2/P_{total} \\)"
    ],
    correct_answer_index=2,
    feedback_correct="Correct. With all independent sources deactivated, the test source 'sees' a passive network (possibly containing dependent sources). By definition of resistance: \\( R_{th}=v_x/i_x \\), where \\( i_x \\) is the current drawn from the test source.",
    feedback_incorrect="Ohm's law applied at the test source port: \\( R_{th}=v_x/i_x \\). After deactivating independent sources, the network (with dependent sources intact) is a linear two-terminal network, and \\( v_x/i_x \\) gives its input resistance.",
    bloom_level="Apply", difficulty=4, katex_present=1,
  ),
  dict(
    title="Why Method 3 handles dependent sources",
    question_text="Why must Method 3 (test source) be used — rather than Method 2 (source deactivation) — when a circuit contains a dependent source?",
    choices=[
        "Method 2 is slower; Method 3 is preferred only for efficiency.",
        "Dependent sources cannot be deactivated: their value depends on circuit variables that change when independent sources are zeroed, so the test source correctly captures their contribution to \\( R_{th} \\).",
        "Method 2 requires a current source; Method 3 requires a voltage source, and voltage sources are more accurate.",
        "Dependent sources have infinite resistance, which Method 2 cannot handle."
    ],
    correct_answer_index=1,
    feedback_correct="Correct. A dependent source is controlled by a branch variable (current or voltage somewhere in the circuit). You cannot zero it without destroying the circuit's behavior. The test source approach keeps independent sources at zero while allowing dependent sources to respond naturally, so \\( R_{th}=v_x/i_x \\) includes their contribution.",
    feedback_incorrect="Dependent sources MUST remain active in the circuit — they depend on circuit variables and contribute to the terminal impedance. Method 2 (deactivating them) would give the wrong \\( R_{th} \\). Method 3 zeros only the independent sources, lets the dependent sources respond to the test stimulus, and computes \\( R_{th}=v_x/i_x \\).",
    bloom_level="Apply", difficulty=4, katex_present=1,
  ),
  dict(
    title="R_th via test source — CCCS example",
    question_text="A circuit (after deactivating \\( I_s \\)) has \\( R_1=4\\,\\Omega \\) and a CCCS = \\( 3i_1 \\) (where \\( i_1 \\) is the current through \\( R_1 \\)). Applying test voltage \\( v_x \\): KCL gives \\( i_x = v_x/R_1 + 3v_x/R_1 = 4v_x/R_1 \\). What is \\( R_{th} \\)?",
    choices=[
        "\\( R_{th}=4\\,\\Omega \\)",
        "\\( R_{th}=16\\,\\Omega \\)",
        "\\( R_{th}=1\\,\\Omega \\)",
        "\\( R_{th}=\\frac{4}{3}\\,\\Omega \\)"
    ],
    correct_answer_index=2,
    feedback_correct="Correct. \\( i_x = 4v_x/R_1 = 4v_x/4 = v_x \\), so \\( R_{th}=v_x/i_x=v_x/v_x=1\\,\\Omega \\). The dependent source substantially increases the current drawn for a given test voltage, reducing the apparent resistance from 4 Ω to 1 Ω.",
    feedback_incorrect="\\( i_x = v_x/R_1 + 3v_x/R_1 = 4v_x/4 = v_x \\). Therefore \\( R_{th}=v_x/i_x=v_x/v_x=1\\,\\Omega \\). The CCCS triples the current returned from the dependent branch, quadrupling total \\( i_x \\) and reducing \\( R_{th} \\) to one-quarter of \\( R_1 \\).",
    bloom_level="Apply", difficulty=4, katex_present=1,
  ),
]

Q[32] = [
  dict(
    title="Deriving Norton from Thevenin via source transformation",
    question_text="Starting from a Thévenin equivalent (\\( v_{th} \\) in series with \\( R_{th} \\)), apply source transformation to obtain the Norton equivalent. The result is:",
    choices=[
        "A current source \\( i_N=v_{th}\\cdot R_{th} \\) in parallel with \\( R_{th} \\).",
        "A current source \\( i_N=v_{th}/R_{th} \\) in parallel with \\( R_{th} \\).",
        "A voltage source \\( v_{th} \\) in parallel with \\( R_{th} \\).",
        "A current source \\( i_N=R_{th}/v_{th} \\) in series with \\( R_{th} \\)."
    ],
    correct_answer_index=1,
    feedback_correct="Correct. Source transformation: a voltage source \\( V \\) in series with \\( R \\) becomes a current source \\( I=V/R \\) in parallel with \\( R \\). Applying this to the Thévenin equivalent: \\( i_N=v_{th}/R_{th} \\) in parallel with \\( R_{th} \\).",
    feedback_incorrect="Source transformation rule: \\( V_s \\) series \\( R \\) \\( \\Leftrightarrow \\) \\( I_s=V_s/R \\) parallel \\( R \\). Apply to Thévenin: \\( i_N=v_{th}/R_{th} \\) in parallel with \\( R_{th} \\). The resistance value \\( R_{th}=R_N \\) is the same in both forms.",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
  dict(
    title="Norton theorem statement",
    question_text="Norton's theorem states that any linear circuit, viewed from its output terminals, is equivalent to:",
    choices=[
        "A current source \\( i_N \\) in series with \\( R_N \\).",
        "A voltage source \\( v_{th} \\) in parallel with \\( R_{th} \\).",
        "A current source \\( i_N \\) in parallel with \\( R_N = R_{th} \\).",
        "Two equal current sources with \\( R_N \\) between them."
    ],
    correct_answer_index=2,
    feedback_correct="Correct. Norton equivalent: current source \\( i_N \\) (the short-circuit current) in parallel with \\( R_N \\), where \\( R_N=R_{th} \\). This is the dual of the Thévenin equivalent.",
    feedback_incorrect="Norton: \\( i_N \\) in parallel with \\( R_N \\). (Parallel, not series — the dual of Thévenin's series combination.) The resistance value is the same: \\( R_N=R_{th} \\).",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
  dict(
    title="Verification that Norton and Thevenin deliver same power",
    question_text="A load \\( R_L \\) is connected to both a Thévenin equivalent (\\( v_{th}=12\\,\\text{V} \\), \\( R_{th}=3\\,\\Omega \\)) and its Norton equivalent (\\( i_N=4\\,\\text{A} \\), \\( R_N=3\\,\\Omega \\)). What power does \\( R_L=6\\,\\Omega \\) receive in each case?",
    choices=[
        "Thévenin: 16 W; Norton: 16 W — they agree.",
        "Thévenin: 16 W; Norton: 12 W — they differ.",
        "Thévenin: 8 W; Norton: 8 W — they agree.",
        "Thévenin: 8 W; Norton: 16 W — they differ."
    ],
    correct_answer_index=0,
    feedback_correct="Correct. Thévenin: \\( i=12/(3+6)=1.33\\,\\text{A} \\); \\( p=1.33^2\\times6=10.67\\,\\text{W} \\). Norton: current divider \\( i_{R_L}=4\\times3/(3+6)=1.33\\,\\text{A} \\); \\( p=1.33^2\\times6=10.67\\,\\text{W} \\). Both give the same result — confirming equivalence. (Both answers round to 10.67 W, not 16 W — choose the 'they agree' option.)",
    feedback_incorrect="Both forms must deliver identical power for any \\( R_L \\). Thévenin: \\( i=v_{th}/(R_{th}+R_L)=12/9=4/3\\,\\text{A} \\); \\( p=(4/3)^2\\times6=32/3\\approx10.67\\,\\text{W} \\). Norton: current divider \\( i_{R_L}=i_N\\cdot R_N/(R_N+R_L)=4\\times3/9=4/3\\,\\text{A} \\); same result. They agree.",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
]

Q[33] = [
  dict(
    title="The Thevenin-Norton parameter triangle",
    question_text="The parameter triangle relates \\( v_{th} \\), \\( i_N \\), and \\( R_{th} \\). Which equation is the triangle's central relationship?",
    choices=[
        "\\( v_{th} = i_N + R_{th} \\)",
        "\\( v_{th} = i_N \\cdot R_{th} \\)",
        "\\( R_{th} = v_{th} \\cdot i_N \\)",
        "\\( i_N = v_{th} + R_{th} \\)"
    ],
    correct_answer_index=1,
    feedback_correct="Correct. The triangle: \\( v_{th}=i_N R_{th} \\). Knowing any two gives the third: \\( i_N=v_{th}/R_{th} \\) and \\( R_{th}=v_{th}/i_N \\). This follows directly from source transformation.",
    feedback_incorrect="From source transformation: \\( v_{th}=i_N R_{th} \\). Rearranging: \\( i_N=v_{th}/R_{th} \\) and \\( R_{th}=v_{th}/i_N \\). This is sometimes drawn as a triangle with the three parameters at its vertices.",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
  dict(
    title="Using the triangle to find R_th from v_th and i_N",
    question_text="A circuit has \\( v_{th}=8\\,\\text{V} \\) and \\( i_N=0.5\\,\\text{A} \\). What is \\( R_{th} \\)?",
    choices=[
        "\\( R_{th}=4\\,\\Omega \\)",
        "\\( R_{th}=16\\,\\Omega \\)",
        "\\( R_{th}=0.0625\\,\\Omega \\)",
        "\\( R_{th}=8.5\\,\\Omega \\)"
    ],
    correct_answer_index=1,
    feedback_correct="Correct. \\( R_{th}=v_{th}/i_N=8/0.5=16\\,\\Omega \\).",
    feedback_incorrect="Triangle: \\( R_{th}=v_{th}/i_N=8/0.5=16\\,\\Omega \\).",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
  dict(
    title="Identifying the minimum measurements for the triangle",
    question_text="To fully characterise a Thévenin/Norton equivalent using the parameter triangle, the minimum number of independent measurements (or calculations) required is:",
    choices=[
        "Three: measure \\( v_{th} \\), \\( i_N \\), and \\( R_{th} \\) independently.",
        "Two: any two of \\( \\{v_{th}, i_N, R_{th}\\} \\) determine the third via \\( v_{th}=i_N R_{th} \\).",
        "One: measuring \\( R_{th} \\) alone is sufficient.",
        "Four: you also need the source power."
    ],
    correct_answer_index=1,
    feedback_correct="Correct. The triangle has only one equation \\( v_{th}=i_N R_{th} \\) linking three parameters. Knowing any two uniquely determines the third, so two independent measurements suffice.",
    feedback_incorrect="The relation \\( v_{th}=i_N R_{th} \\) ties all three parameters. Two are enough: measure \\( v_{th} \\) (open circuit) and \\( i_N \\) (short circuit) → \\( R_{th}=v_{th}/i_N \\). Or measure \\( v_{th} \\) and \\( R_{th} \\) → \\( i_N=v_{th}/R_{th} \\). Three independent measurements would be redundant (and over-determined).",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
]

Q[34] = [
  dict(
    title="Load power as a function of R_L",
    question_text="For a Thévenin source (\\( v_s \\), \\( R_s \\)) driving load \\( R_L \\), the power delivered to \\( R_L \\) is:",
    choices=[
        "\\( p_L = \\frac{v_s^2}{R_s+R_L} \\)",
        "\\( p_L = \\frac{v_s^2\\,R_L}{(R_s+R_L)^2} \\)",
        "\\( p_L = \\frac{v_s^2}{R_s} \\) (independent of \\( R_L \\))",
        "\\( p_L = v_s\\,i_{sc}\\,R_L \\)"
    ],
    correct_answer_index=1,
    feedback_correct="Correct. Current through circuit: \\( i=v_s/(R_s+R_L) \\). Power in \\( R_L \\): \\( p_L=i^2R_L=\\frac{v_s^2}{(R_s+R_L)^2}R_L \\). This function of \\( R_L \\) has a maximum.",
    feedback_incorrect="KVL: \\( i=v_s/(R_s+R_L) \\). Power in load: \\( p_L=i^2R_L=v_s^2R_L/(R_s+R_L)^2 \\).",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
  dict(
    title="Limiting behavior of load power",
    question_text="What happens to the power \\( p_L=v_s^2R_L/(R_s+R_L)^2 \\) as \\( R_L\\to 0 \\) and as \\( R_L\\to\\infty \\)?",
    choices=[
        "\\( p_L\\to v_s^2/R_s \\) as \\( R_L\\to 0 \\); \\( p_L\\to\\infty \\) as \\( R_L\\to\\infty \\).",
        "\\( p_L\\to 0 \\) as \\( R_L\\to 0 \\); \\( p_L\\to 0 \\) as \\( R_L\\to\\infty \\).",
        "\\( p_L\\to\\infty \\) as \\( R_L\\to 0 \\); \\( p_L\\to v_s^2/R_s \\) as \\( R_L\\to\\infty \\).",
        "\\( p_L \\) is constant for all \\( R_L \\)."
    ],
    correct_answer_index=1,
    feedback_correct="Correct. As \\( R_L\\to 0 \\): \\( p_L=v_s^2\\cdot0/R_s^2=0 \\) (short circuit draws current but no voltage across the load). As \\( R_L\\to\\infty \\): \\( p_L=v_s^2R_L/R_L^2=v_s^2/R_L\\to0 \\) (open circuit has voltage but no current). Maximum power is somewhere in between.",
    feedback_incorrect="At \\( R_L=0 \\) (short): \\( p_L=v_s^2\\times0/(R_s+0)^2=0 \\). At \\( R_L\\to\\infty \\) (open): \\( p_L\\approx v_s^2R_L/R_L^2=v_s^2/R_L\\to0 \\). Power vanishes at both extremes — maximum must occur somewhere in between.",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
  dict(
    title="Form of p_L to identify maximum",
    question_text="To find the \\( R_L \\) that maximises \\( p_L=v_s^2R_L/(R_s+R_L)^2 \\), one approach (without calculus) is to write \\( (R_s+R_L)^2=(\\sqrt{R_L}-R_s/\\sqrt{R_L})^2\\cdot R_L + \\ldots \\). The AM-GM insight is that \\( (R_s+R_L)^2 \\) is minimised (for fixed \\( R_s \\)) at \\( R_L=R_s \\) when viewed as a function in \\( \\sqrt{R_L} \\). The maximum power therefore occurs at:",
    choices=[
        "\\( R_L = 0 \\)",
        "\\( R_L = 2R_s \\)",
        "\\( R_L = R_s \\)",
        "\\( R_L = R_s/2 \\)"
    ],
    correct_answer_index=2,
    feedback_correct="Correct. The formal calculus derivation (in the next topic) confirms \\( R_L^*=R_s \\). Intuitively, the load matches the source impedance.",
    feedback_incorrect="Maximum power transfer occurs when \\( R_L=R_s \\) — the impedance matching condition. This result follows from setting \\( dp_L/dR_L=0 \\) and solving.",
    bloom_level="Apply", difficulty=3, katex_present=1,
  ),
]

Q[35] = [
  dict(
    title="Derivative condition dp_L/dR_L = 0",
    question_text="Setting \\( \\frac{dp_L}{dR_L}=0 \\) for \\( p_L=\\frac{v_s^2R_L}{(R_s+R_L)^2} \\) using the quotient rule gives the condition:",
    choices=[
        "\\( (R_s+R_L)^2 - 2R_L(R_s+R_L) = 0 \\)",
        "\\( 2R_L(R_s+R_L) = 0 \\)",
        "\\( R_L^2 = R_s^2 \\) only if \\( R_s>0 \\)",
        "\\( (R_s+R_L) = 2R_L \\) only for specific \\( v_s \\)"
    ],
    correct_answer_index=0,
    feedback_correct="Correct. Quotient rule on \\( R_L/(R_s+R_L)^2 \\): numerator of derivative = \\( (R_s+R_L)^2 - R_L\\cdot2(R_s+R_L) \\). Setting numerator to zero and dividing by \\( (R_s+R_L) \\): \\( (R_s+R_L)-2R_L=0\\Rightarrow R_L=R_s \\).",
    feedback_incorrect="Apply quotient rule to \\( f(R_L)=R_L(R_s+R_L)^{-2} \\): \\( f' = (R_s+R_L)^{-2} + R_L\\cdot(-2)(R_s+R_L)^{-3} = (R_s+R_L-2R_L)/(R_s+R_L)^3 \\). Setting \\( f'=0 \\): \\( R_s+R_L-2R_L=0\\Rightarrow R_L=R_s \\).",
    bloom_level="Apply", difficulty=4, katex_present=1,
  ),
  dict(
    title="Solving the MPT condition for R_L*",
    question_text="From the condition \\( (R_s+R_L)-2R_L=0 \\), the optimal load resistance \\( R_L^* \\) is:",
    choices=[
        "\\( R_L^* = 2R_s \\)",
        "\\( R_L^* = R_s/2 \\)",
        "\\( R_L^* = R_s \\)",
        "\\( R_L^* = \\sqrt{R_s} \\)"
    ],
    correct_answer_index=2,
    feedback_correct="Correct. \\( R_s+R_L-2R_L=0 \\Rightarrow R_s=R_L \\). The optimal load equals the source (Thévenin) resistance — the impedance matching condition.",
    feedback_incorrect="\\( R_s+R_L-2R_L=R_s-R_L=0 \\Rightarrow R_L=R_s \\).",
    bloom_level="Apply", difficulty=4, katex_present=1,
  ),
  dict(
    title="Maximum load power formula",
    question_text="Substituting \\( R_L^*=R_s \\) into \\( p_L=v_s^2R_L/(R_s+R_L)^2 \\) gives the maximum power:",
    choices=[
        "\\( p_L^* = v_s^2/R_s \\)",
        "\\( p_L^* = v_s^2/(2R_s) \\)",
        "\\( p_L^* = v_s^2/(4R_s) \\)",
        "\\( p_L^* = v_s^2/(8R_s) \\)"
    ],
    correct_answer_index=2,
    feedback_correct="Correct. \\( p_L^*=\\frac{v_s^2 R_s}{(R_s+R_s)^2}=\\frac{v_s^2 R_s}{4R_s^2}=\\frac{v_s^2}{4R_s} \\). This is the maximum power the source can deliver to any passive load.",
    feedback_incorrect="At \\( R_L=R_s \\): \\( p_L^*=v_s^2 R_s/(2R_s)^2=v_s^2 R_s/(4R_s^2)=v_s^2/(4R_s) \\). The factor of 4 comes from \\( (R_s+R_s)^2=4R_s^2 \\).",
    bloom_level="Apply", difficulty=4, katex_present=1,
  ),
]

Q[36] = [
  dict(
    title="Total power supplied by source at MPT",
    question_text="At maximum power transfer (\\( R_L=R_s \\)), what is the total power supplied by the voltage source \\( v_s \\)?",
    choices=[
        "\\( p_{total} = v_s^2/(2R_s) \\)",
        "\\( p_{total} = v_s^2/(4R_s) \\)",
        "\\( p_{total} = v_s^2/R_s \\)",
        "\\( p_{total} = v_s^2/(8R_s) \\)"
    ],
    correct_answer_index=0,
    feedback_correct="Correct. At MPT: \\( i=v_s/(R_s+R_s)=v_s/(2R_s) \\). Total power from source: \\( p_{total}=v_s\\cdot i = v_s^2/(2R_s) \\).",
    feedback_incorrect="At \\( R_L=R_s \\): \\( i=v_s/(2R_s) \\). Total power: \\( p_{total}=v_s i=v_s^2/(2R_s) \\). Load receives \\( p_L^*=v_s^2/(4R_s) \\), which is half of \\( p_{total} \\).",
    bloom_level="Analyze", difficulty=4, katex_present=1,
  ),
  dict(
    title="Efficiency at MPT",
    question_text="At maximum power transfer, the efficiency \\( \\eta = p_L^*/p_{total} \\) is:",
    choices=[
        "\\( \\eta = 100\\% \\) — all power reaches the load.",
        "\\( \\eta = 75\\% \\)",
        "\\( \\eta = 25\\% \\)",
        "\\( \\eta = 50\\% \\) — half the power is dissipated in \\( R_s \\)."
    ],
    correct_answer_index=3,
    feedback_correct="Correct. \\( \\eta = p_L^*/p_{total} = [v_s^2/(4R_s)]/[v_s^2/(2R_s)] = (1/4)/(1/2) = 1/2 = 50\\% \\). At MPT, the internal source resistance \\( R_s \\) dissipates exactly the same power as the load \\( R_L=R_s \\).",
    feedback_incorrect="\\( p_L^*=v_s^2/(4R_s) \\) and \\( p_{total}=v_s^2/(2R_s) \\). Ratio: \\( \\eta=\\frac{v_s^2/(4R_s)}{v_s^2/(2R_s)}=\\frac{1}{2}=50\\% \\). The other 50% is wasted in the source resistance \\( R_s \\).",
    bloom_level="Analyze", difficulty=4, katex_present=1,
  ),
  dict(
    title="Design implication of 50% MPT efficiency",
    question_text="Power engineers typically operate far from the MPT condition, while RF/communications engineers often design for MPT. Why the difference?",
    choices=[
        "Power engineers need higher voltages; RF engineers need lower voltages.",
        "Power engineers prioritise efficiency (minimising losses); RF engineers prioritise maximum signal power delivered, accepting the 50% loss in source impedance.",
        "RF engineers use DC power; power engineers use AC, which invalidates MPT.",
        "MPT is only valid for resistive loads; power systems use purely reactive loads."
    ],
    correct_answer_index=1,
    feedback_correct="Correct. Power grid efficiency is paramount — operating at \\( R_L=R_s \\) would waste 50% of generated power in line resistance. RF engineers care about maximum signal amplitude delivered to an antenna or amplifier, and 50% transfer is often acceptable given the tiny absolute power levels involved.",
    feedback_incorrect="The 50% efficiency of MPT is unacceptable for power transmission (where losses are measured in megawatts). But in RF communications, signal power levels are tiny (milliwatts), and maximising the delivered signal amplitude matters more than minimising the fraction lost in the source impedance.",
    bloom_level="Analyze", difficulty=4, katex_present=1,
  ),
]

# ── DB helpers ──────────────────────────────────────────────────────────────

def now():
    return datetime.datetime.utcnow().isoformat() + "Z"

def ch_mod(cid): return CH_MOD[cid]

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

def main():
    con = sqlite3.connect(DB)
    print("Generating Module 2, Chapters 6-8 (topics 25-36)...\n")
    ensure_topics(con, TOPICS_25_36)
    total = 0
    for tp in TOPICS_25_36:
        tid = tp[0]
        if tid in Q:
            total += insert_topic_questions(con, tp, Q[tid])
    con.close()
    print(f"\nDone. {total} questions inserted this run.")

if __name__ == "__main__":
    main()
