# Module 2 Topics — Thevenin & Norton Equivalence + Maximum Power Transfer

## Chapter 1 — Thevenin's Theorem (chapter_id = 6)

| Row | Topic | Subtopic | Learning Objective | Bloom Level | Difficulty |
|-----|-------|----------|--------------------|-------------|------------|
| 1 | Abstraction | Circuit equivalence motivation | Explain why circuit equivalence enables modular engineering design and define what "appears the same at the terminals" means in terms of terminal voltage and current | Understand | 2 |
| 2 | Thevenin's Theorem | Theorem statement | State Thevenin's theorem: any linear two-terminal circuit can be replaced by a voltage source \(v_{th}\) in series with a resistor \(R_{th}\) | Remember | 1 |
| 3 | Thevenin's Theorem | Linearity requirement | Identify which circuit elements satisfy the linearity condition required for Thevenin's theorem, and explain why nonlinear elements violate it | Understand | 2 |
| 4 | Thevenin's Theorem | Finding v_th — open-circuit voltage | Determine \(v_{th}\) by computing the open-circuit terminal voltage with the load disconnected, and explain why this equals \(v_{oc}\) | Apply | 2 |
| 5 | Thevenin's Theorem | R_th — short-circuit method | Apply the short-circuit method to find \(R_{th} = v_{oc}/i_{sc}\) by computing the current with terminals shorted | Apply | 3 |
| 6 | Thevenin's Theorem | R_th — source deactivation method | Apply the source deactivation method (voltage sources to shorts, current sources to opens) to find \(R_{th}\) as \(R_{eq}\), and explain why this method is invalid when dependent sources are present | Apply | 3 |
| 7 | Thevenin's Theorem | R_th — external test-source method | Apply the external test-source method to find \(R_{th} = v_x/i_x\) when dependent sources are present, and explain why independent sources must be deactivated first | Apply | 4 |

## Chapter 2 — Norton Equivalence and Source Transformation (chapter_id = 7)

| Row | Topic | Subtopic | Learning Objective | Bloom Level | Difficulty |
|-----|-------|----------|--------------------|-------------|------------|
| 8 | Norton Equivalence | Theorem statement and derivation | State Norton's theorem and derive the Norton equivalent from the Thevenin equivalent using source transformation, showing that \(i_N = v_{th}/R_{th}\) and \(R_N = R_{th}\) | Apply | 3 |
| 9 | Norton Equivalence | Parameter relationships | Apply the relationships \(v_{th} = i_N R_{th}\), \(i_N = v_{th}/R_{th}\), and \(R_{th} = v_{oc}/i_{sc}\) to convert between Thevenin and Norton equivalent forms | Apply | 2 |

## Chapter 3 — Maximum Power Transfer (chapter_id = 8)

| Row | Topic | Subtopic | Learning Objective | Bloom Level | Difficulty |
|-----|-------|----------|--------------------|-------------|------------|
| 10 | Maximum Power Transfer | Load power expression | Derive the expression \(p_L = v_s^2 R_L/(R_s + R_L)^2\) for power delivered to a load \(R_L\) from a Thevenin equivalent \((v_s, R_s)\) | Apply | 3 |
| 11 | Maximum Power Transfer | Optimization and result | Differentiate \(p_L\) with respect to \(R_L\) and show that maximum power \(p_L^* = v_s^2/(4R_s)\) is delivered when \(R_L = R_s\) | Apply | 4 |
| 12 | Maximum Power Transfer | Efficiency at MPT | Calculate that efficiency is exactly 50% at maximum power transfer, and distinguish engineering contexts (power systems vs. communications) where MPT vs. high efficiency is the priority | Analyze | 3 |
