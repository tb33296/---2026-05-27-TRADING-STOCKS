from core.positions.position import Position


class TrailingStopManager:
    """
    Multi-stage R based trailing.

    LONG

    1R -> breakeven
    2R -> lock 1R
    3R -> lock 2R

    SHORT

    1R -> breakeven
    2R -> lock 1R
    3R -> lock 2R
    """

    def update(
        self,
        position: Position,
        current_price: float,
    ) -> None:

        if position.initial_stop_loss <= 0:
            return

        if position.side == "LONG":
            self._update_long(position, current_price)

        elif position.side == "SHORT":
            self._update_short(position, current_price)

    # -------------------------------------------------

    def _update_long(
        self,
        position: Position,
        current_price: float,
    ) -> None:

        risk = position.entry_price - position.initial_stop_loss

        if risk <= 0:
            return

        rr = int((current_price - position.entry_price) / risk)

        if rr <= position.highest_rr_achieved:
            return

        if rr >= 1:
            new_stop = position.entry_price + (rr - 1) * risk

            if new_stop > position.stop_loss:
                position.stop_loss = round(new_stop, 2)

                position.highest_rr_achieved = rr

    # -------------------------------------------------

    def _update_short(
        self,
        position: Position,
        current_price: float,
    ) -> None:

        risk = position.initial_stop_loss - position.entry_price

        if risk <= 0:
            return

        rr = int((position.entry_price - current_price) / risk)

        if rr <= position.highest_rr_achieved:
            return

        if rr >= 1:
            new_stop = position.entry_price - (rr - 1) * risk

            if new_stop < position.stop_loss:
                position.stop_loss = round(new_stop, 2)

                position.highest_rr_achieved = rr
