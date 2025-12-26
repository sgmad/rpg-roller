from view import RollerView, StatRow, DiceRow, ModRow
from model import RollerModel

class RollerController:
    # Coordinates logic between the Model and View, managing character stats and dice rolls.
    def __init__(self):
        # Initialize the data model and user interface components
        self.model = RollerModel()
        self.view = RollerView()

        # Connect UI signals to controller methods
        self.view.add_stat_btn.clicked.connect(self.create_stat)
        self.view.add_dice_btn.clicked.connect(self.create_dice)
        self.view.add_mod_btn.clicked.connect(self.create_mod)
        self.view.roll_requested.connect(self.perform_roll)
        
        # Load character stats from file and initialize with a default dice row
        for s in self.model.load_stats_from_file():
            self.create_stat(s["name"], s["value"])
        self.create_dice()

    def create_stat(self, name="", value=10):
        # Adds a character stat row and defines its modifier generation logic
        row = StatRow(name if not isinstance(name, bool) else "", value)
        row.delete_clicked.connect(lambda: self._remove(row, self.view.stats_layout))
        row.use_clicked.connect(lambda n, v: self.create_mod(f"{n} Modifier", (v-10)//2))
        self.view.add_stat_row(row)

    def create_dice(self):
        # Adds a new dice configuration row to the main container
        row = DiceRow()
        row.delete_clicked.connect(lambda: self._remove(row, self.view.dice_layout))
        self.view.add_dice_row(row)

    def create_mod(self, name="", value=0):
        # Adds a manual modifier row to the calculation list
        row = ModRow(name if not isinstance(name, bool) else "", value)
        row.delete_clicked.connect(lambda: self._remove(row, self.view.mod_layout))
        self.view.add_mod_row(row)

    def _remove(self, widget, layout):
        # Removes a row from the layout and triggers geometry updates
        layout.removeWidget(widget)
        widget.deleteLater()
        self.view.adjustSize()
        if isinstance(widget, StatRow):
            self.save_stats()

    def save_stats(self):
        # Collects current character stats and saves them to local storage
        data = []
        for i in range(self.view.stats_layout.count()):
            w = self.view.stats_layout.itemAt(i).widget()
            if isinstance(w, StatRow): 
                data.append(w.get_data())
        self.model.save_stats_to_file(data)

    def perform_roll(self):
        # Calculates the total sum of all active dice and modifiers
        grand_total = 0
        log_html = ""
        
        # Sum results from all active dice pools
        for i in range(self.view.dice_layout.count()):
            w = self.view.dice_layout.itemAt(i).widget()
            if isinstance(w, DiceRow):
                count, faces = w.get_values()
                total, rolls, _ = self.model.roll_dice(count, faces)
                grand_total += total
                rolls_str = ", ".join(map(str, rolls))
                log_html += f"<div>🎲 <b>{count}d{faces}</b>: [{rolls_str}] = <b>{total}</b></div>"

        # Apply all active modifiers to the total
        for i in range(self.view.mod_layout.count()):
            w = self.view.mod_layout.itemAt(i).widget()
            if isinstance(w, ModRow):
                name, val = w.get_values()
                grand_total += val
                name_str = name if name else "Modifier"
                color = "#4cd137" if val >= 0 else "#ff5555"
                sign = "+" if val >= 0 else ""
                log_html += f"<div>• {name_str}: <span style='color:{color}'>{sign}{val}</span></div>"

        # Finalize the HTML entry and update the scrollable output log
        log_html += f"<div style='margin-top:4px; border-top:1px solid #333; padding-top:2px; font-size:14px; color:#d4af37'><b>RESULT: {grand_total}</b></div><br>"
        
        self.view.log.append(log_html)
        sb = self.view.log.verticalScrollBar()
        sb.setValue(sb.maximum())

    def run(self):
        # Displays the main application window
        self.view.show()