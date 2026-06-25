# ENG17: Circuits I — Learning Objectives
## Topic: Thevenin & Norton Equivalence + Maximum Power Transfer

**Source:** `ENG17_unit3_thevenin_norton_equivalence/main.tex`  
**Format:** Beamer slide deck (Unit 3)  
**Course:** ENG17: Circuits I  
**Instructor:** Anthony Thomas  

> **Note on source style:** This document is a slide-deck presentation, not a detailed derivation note. Slides serve as an outline; the instructor delivers mathematical detail verbally and at the board. Learning objectives below are inferred from slide structure and topic context, with standard circuit-theory content filled in as needed to make the objectives actionable.

---

## 1. Motivation: Abstraction and Modularity

- Explain why **abstraction** is essential in modern engineering: real systems (e.g., smartphones, precision ADCs) are too complex to reason about in full detail simultaneously.
- Define the concept of an **interface**: a description of a component's behavior at its terminals that is sufficient to use it without knowing its internal implementation.
- Articulate the engineering value of circuit equivalence: it allows complex sub-circuits to be replaced by simple models that "appear identical" to the rest of the circuit.

---

## 2. Thevenin's Theorem

### 2a. Statement

- State **Thevenin's Theorem**: any linear circuit, viewed from two output terminals, can be replaced by an equivalent circuit consisting of a single voltage source $v_{th}$ in **series** with a single resistor $R_{th}$.

$$\boxed{\text{Thevenin equivalent} = v_{th} \text{ (series) } R_{th}}$$

- Define "appears the same" precisely: for *any* load $R_L$ connected to the terminals, the equivalent circuit delivers the same terminal voltage and the same current as the original circuit.
- State the **linearity requirement**: Thevenin's theorem applies only to circuits composed of linear elements (resistors, linear dependent sources) and independent sources. Nonlinear elements (diodes, transistors in general) violate this.

### 2b. Finding $v_{th}$: Open-Circuit Voltage

- Recognize that $v_{th}$ equals the **open-circuit voltage** $v_{oc}$ at the output terminals:
$$v_{th} = v_{oc}$$
- **Reasoning:** When the load terminals are open ($R_L \to \infty$, so $i_L = 0$), no current flows through $R_{th}$ (no voltage drop across it), so the terminal voltage equals $v_{th}$ directly. Therefore $v_{th}$ can be found by computing the terminal voltage with the load disconnected.
- Apply KVL, KCL, nodal analysis, mesh analysis, or superposition to find $v_{oc}$ for a given circuit.

### 2c. Finding $R_{th}$: Three Methods

The appropriate method depends on whether the circuit contains **only independent sources**, or also **dependent sources**.

#### Method 1 — Short-Circuit Method
- Applicable when the circuit has **independent sources only**.
- Find the **short-circuit current** $i_{sc}$: connect a wire (short circuit) across the output terminals and compute the resulting current.
- Then:
$$R_{th} = \frac{v_{oc}}{i_{sc}} = \frac{v_{th}}{i_{sc}}$$
- This is equivalent to computing the Norton current $i_N = i_{sc}$ and using $R_{th} = v_{th}/i_N$.

#### Method 2 — Equivalent-Resistance Method (Source Deactivation)
- Applicable when the circuit has **independent sources only** (no dependent sources).
- **Deactivate** all independent sources:
  - Replace every **independent voltage source** with a **short circuit** (wire).
  - Replace every **independent current source** with an **open circuit** (gap).
- Compute the equivalent resistance seen looking into the output terminals using series/parallel combinations.
$$R_{th} = R_{eq}\big|_{\text{sources deactivated}}$$
- Note: dependent sources must *not* be deactivated — they depend on circuit variables and remain active.

#### Method 3 — External-Source (Test-Source) Method
- Required when the circuit contains **dependent sources** (in addition to, or instead of, independent sources).
- Deactivate all **independent** sources (same rules as Method 2).
- Apply an external **test voltage** $v_x$ or **test current** $i_x$ at the output terminals.
- Compute the resulting current $i_x$ (if voltage applied) or voltage $v_x$ (if current applied).
- Then:
$$R_{th} = \frac{v_x}{i_x}$$
- Either a test voltage or test current may be used; pick whichever makes the algebra simpler.

---

## 3. Norton Equivalence

### 3a. Statement

- State **Norton's Theorem**: any linear circuit, viewed from two output terminals, can be replaced by an equivalent circuit consisting of a single current source $i_N$ in **parallel** with a single resistor $R_N$.

$$\boxed{\text{Norton equivalent} = i_N \text{ (parallel) } R_N}$$

### 3b. Derivation from Thevenin via Source Transformation

- Apply **source transformation** to the Thevenin equivalent:
  - A voltage source $v_{th}$ in series with $R_{th}$ is equivalent (at its terminals) to a current source $i_N$ in parallel with $R_N$, where:
$$i_N = \frac{v_{th}}{R_{th}}, \qquad R_N = R_{th}$$

- Conversely:
$$v_{th} = i_N R_N, \qquad R_{th} = R_N$$

- The three quantities $v_{th}$, $i_N$, $R_{th}$ are not independent — any two determine the third:

| Known | Derived |
|---|---|
| $v_{th}$, $R_{th}$ | $i_N = v_{th}/R_{th}$ |
| $i_N$, $R_{th}$ | $v_{th} = i_N R_{th}$ |
| $v_{th}$, $i_N$ | $R_{th} = v_{th}/i_N$ |

### 3c. Self-Derivation Exercise

> The slides pose this as a **"Test Yourself"** problem: given a Thevenin equivalent, derive the Norton equivalent. Students are expected to produce the source transformation and the parameter relationships above independently.

---

## 4. Source Transformation (Prerequisite/Tool)

- State the source transformation equivalence: a voltage source $V_s$ in series with resistance $R$ is equivalent (at external terminals) to a current source $I_s = V_s/R$ in parallel with the same $R$, and vice versa.
- Apply source transformation iteratively to simplify circuits before finding Thevenin/Norton equivalents.
- Recognize the constraint: source transformation is valid only for resistors in series with voltage sources or in parallel with current sources — not for ideal sources alone.

---

## 5. Maximum Power Transfer

### 5a. Problem Setup

- Model a practical source (or any active sub-circuit) by its Thevenin equivalent: voltage source $v_s$ in series with source resistance $R_s$.
- Connect a variable passive load $R_L$ to the terminals.
- Express the **power delivered to the load**:

The load current is:
$$i_L = \frac{v_s}{R_s + R_L}$$

Therefore:
$$p_L = i_L^2 R_L = \frac{v_s^2\, R_L}{(R_s + R_L)^2}$$

### 5b. Optimization

- Maximize $p_L$ over $R_L > 0$ by differentiating and setting $dp_L/dR_L = 0$:

$$\frac{dp_L}{dR_L} = v_s^2 \cdot \frac{(R_s + R_L)^2 - R_L \cdot 2(R_s + R_L)}{(R_s + R_L)^4} = v_s^2 \cdot \frac{R_s - R_L}{(R_s + R_L)^3} = 0$$

- This is zero if and only if $R_s = R_L$, confirming the condition.
- Verify it is a maximum (not minimum) by checking the second derivative or by inspecting boundary behavior ($p_L \to 0$ as $R_L \to 0$ or $R_L \to \infty$).

### 5c. Result

$$\boxed{p_L^* = \frac{v_s^2}{4R_L}\bigg|_{R_L = R_s} = \frac{v_s^2}{4R_s}}$$

- State the **Maximum Power Transfer Theorem**: maximum power is delivered to a load $R_L$ from a Thevenin equivalent ($v_s$, $R_s$) when:
$$R_L = R_s$$

> The slide poses "where did this come from?" as an explicit prompt — students are expected to reconstruct the optimization derivation above.

### 5d. Efficiency at Maximum Power Transfer

- At $R_L = R_s$, the total power supplied by $v_s$ is:
$$p_{total} = \frac{v_s^2}{R_s + R_L} \cdot \frac{v_s}{R_s + R_L} \cdot (R_s + R_L) = \frac{v_s^2}{2R_s}$$
- Power dissipated in $R_s$: $p_{R_s} = i_L^2 R_s = \frac{v_s^2}{4R_s}$
- Therefore the **efficiency** at maximum power transfer is exactly **50%** — the source dissipates as much power as the load receives. This is why maximum power transfer is not the same as maximum efficiency.

---

## 6. Practical Interpretation and Limits

- Recognize that Thevenin/Norton equivalents are valid only at the **terminal pair** at which they are defined — internal voltages and currents within the original circuit are not preserved by the equivalent.
- Understand that the equivalent changes if the terminal pair changes.
- Identify which method to use for $R_{th}$ based on the circuit:
  - Independent sources only → Method 1 (short-circuit) or Method 2 (source deactivation)
  - Contains dependent sources → Method 3 (external test source) required

---

## Summary of Key Relations

| Quantity | Expression |
|---|---|
| Thevenin voltage | $v_{th} = v_{oc}$ (open-circuit voltage) |
| Thevenin resistance (methods 1–3) | $R_{th} = v_{oc}/i_{sc}$ or $R_{eq}$ (sources off) or $v_x/i_x$ (test source) |
| Norton current | $i_N = i_{sc} = v_{th}/R_{th}$ |
| Norton resistance | $R_N = R_{th}$ |
| Load power (general) | $p_L = v_s^2 R_L / (R_s + R_L)^2$ |
| Max power condition | $R_L = R_s$ |
| Max power delivered | $p_L^* = v_s^2 / (4R_s)$ |
| Efficiency at MPT | $50\%$ |

---

## Implicit Prerequisites

Students are expected to be fluent in:

- KVL, KCL, Ohm's law
- Node-voltage and mesh-current methods
- Series and parallel resistor combinations
- Basic calculus: derivative of a rational function, setting derivative to zero
- Concept of a linear circuit element
- Source transformation (voltage $\leftrightarrow$ current source equivalence)

---

## Pedagogical Notes on This Source

This is a **slide deck** (Beamer), not a derivation document. Several slides are deliberately incomplete:

- *"Finding $v_{th}$"* — poses the question "how can we use this?" without answering it; instructor elicits the open-circuit argument interactively.
- *"Norton Equivalence"* — posts a "Test Yourself" prompt for students to derive it from Thevenin.
- *"Maximum Power Transfer — Where did this come from?"* — blank slide; instructor derives the optimization at the board.

This contrasts with the series RLC derivation notes (Unit 1), which provided full step-by-step derivations in the source document.
