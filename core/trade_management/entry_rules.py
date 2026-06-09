# core/trade_management/entry_rules.py

class EntryRules:
    @staticmethod
    def can_enter_position(
        position_manager,
        symbol: str,
        direction: str,
    ) -> bool:

        position = position_manager.get_open_positions().get(symbol)

        if position is None:
            return True

        if position.side.upper() == direction.upper():
            return False

        return True
