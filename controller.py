from view import RollerView, StatRow, DiceRow, ModRow
from model import RollerModel

class RollerController:
    # Manages application logic and triggers UI size updates on row changes.
    def __init__(self):
        self.model = RollerModel()
        self.view = RollerView()

        self.view.add_stat_btn.clicked.connect(self.create_stat)
        self.view.add_dice_btn.clicked.connect(self.create_dice)
        self.view.add_mod_btn.clicked.connect(self.create_mod)
        self.view.roll_requested.connect(self.perform_roll)
        self.view.clear_requested.connect(self.clear_all_rows)
        
        for s in self.model.load_stats_from_file():
            self.create_stat(s["name"], s["value"])
        self.create_dice()

    def create_stat(self, name="", value=10):
        # Adds a new stat row and refreshes the window size
        row = StatRow(name if not isinstance(name, bool) else "", value)
        row.delete_clicked.connect(lambda: self._remove(row, self.view.stats_layout))
        row.use_clicked.connect(lambda n, v: self.create_mod(f"{n} Modifier", (v-10)//2))
        self.view.add_stat_row(row)
        self.view.update_window_size()

    def create_dice(self):
        # Adds a new dice row and refreshes the window size
        row = DiceRow()
        row.delete_clicked.connect(lambda: self._remove(row, self.view.dice_layout))
        self.view.add_dice_row(row)
        self.view.update_window_size()

    def create_mod(self, name="", value=0):
        # Adds a new modifier row and refreshes the window size
        row = ModRow(name if not isinstance(name, bool) else "", value)
        row.delete_clicked.connect(lambda: self._remove(row, self.view.mod_layout))
        self.view.add_mod_row(row)
        self.view.update_window_size()

    def clear_all_rows(self):
        # Immediately removes widgets from layout to ensure sizeHint updates correctly
        for layout in [self.view.dice_layout, self.view.mod_layout]:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
        
        self.create_dice()
        self.view.update_window_size()

    def _remove(self, widget, layout):
        # Removes a specific row and updates geometry
        layout.removeWidget(widget)
        widget.deleteLater()
        self.view.update_window_size()
        if isinstance(widget, StatRow):
            self.save_stats()

    def save_stats(self):
        # Serializes stats data to local storage
        data = []
        for i in range(self.view.stats_layout.count()):
            w = self.view.stats_layout.itemAt(i).widget()
            if isinstance(w, StatRow): 
                data.append(w.get_data())
        self.model.save_stats_to_file(data)

    def perform_roll(self):
        # Processes all active dice and modifiers for the final sum log
        grand_total = 0
        log_html = "<div style='margin-bottom: 5px;'>"
        
        for i in range(self.view.dice_layout.count()):
            w = self.view.dice_layout.itemAt(i).widget()
            if isinstance(w, DiceRow):
                count, faces = w.get_values()
                total, rolls, _ = self.model.roll_dice(count, faces)
                grand_total += total
                rolls_str = ", ".join(map(str, rolls))
                log_html += (f"<div style='color: #e0e0e0;'>🎲 <b>{count}d{faces}</b>: "
                            f"<span style='color: #888;'>[{rolls_str}]</span> = <b>{total}</b></div>")

        for i in range(self.view.mod_layout.count()):
            w = self.view.mod_layout.itemAt(i).widget()
            if isinstance(w, ModRow):
                name, val = w.get_values()
                grand_total += val
                name_str = name if name else "Modifier"
                color = "#4cd137" if val >= 0 else "#ff5555"
                sign = "+" if val >= 0 else ""
                log_html += (f"<div style='color: #bbb;'>• {name_str}: "
                            f"<span style='color:{color};'>{sign}{val}</span></div>")

        log_html += (f"<div style='margin-top: 4px; border-top: 1px solid #333; padding-top: 2px; "
                    f"font-size: 14px; color: #d4af37;'><b>TOTAL: {grand_total}</b></div>"
                    f"</div><br>")
        
        self.view.log.append(log_html)
        sb = self.view.log.verticalScrollBar()
        sb.setValue(sb.maximum())

    def run(self):
        self.view.show()
