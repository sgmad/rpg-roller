# RPG Roller

Most online dice rollers limit you to a standard set of d4s, d6s, or d20s. They often only allow a single modifier, forcing you to manually calculate stacking bonuses from items, spells, and base stats. **RPG Roller** is designed to eliminate that manual math by providing a highly customizable interface where the user defines the rules.

## The Problem

Standard tools like Google's "Roll Dice" feature are great for simple games but fail in complex tabletop RPGs. When you have multiple modifiers stacking up, you shouldn't have to add them up yourself before inputting a single variable.

## The Solution

This application provides total control over your RNG environment:

* **Unlimited Dice Customization**: Roll any number of dice with any number of faces. If you need to roll a d15 or a d1000, you can do it instantly.
* **Stacking Modifiers**: Add as many modifier rows as needed for your roll. Each one can be labeled so you can track specifically why you have a +2 from a "Bless" spell and a -1 from "Exhaustion."
* **Custom Stats Panel**: A collapsible panel allows you to input and save your character stats. Unlike other apps, these are not pre-labeled (like STR or INT). You define the names and values yourself, and they persist across sessions.
* **Dynamic UI**: The interface is built to be compact. The stats panel can be collapsed to save screen space, and the window automatically snaps to fit only the active rows, ensuring no dead space on your desktop.

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/sgmad/rpg-roller.git
cd rpg-roller

```

**2. Install dependencies**
This project requires Python 3.x and PyQt6.

```bash
pip install PyQt6

```

**3. Run the application**

```bash
python main.py

```

## How to Use

**Character Stats**
Input your stat names and values in the top panel. These are saved to a `stats.json` file automatically whenever you delete or add a row. Clicking the green arrow next to a stat will automatically calculate the standard RPG modifier `(Value - 10) / 2` and add it to your current roll list.

**Dice and Modifiers**
Add as many dice pools as you need. Each pool allows you to set the number of dice and the number of faces. Use the **+ Modifier** button to add flat bonuses or penalties to the final total.

**Results Log**
The log at the bottom provides a detailed breakdown of every roll. It shows the individual results of each die in a pool, each active modifier, and the final grand total.
