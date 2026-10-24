"""HVF Sovereign C2 // Native 4-Window C2 Deck Contract (CAGE: 1AHA8)"""
class ChronosNativeQuadDeck:
    def __init__(self, cage_code: str = "1AHA8", presenter: str = "CEO Jeffery Humphrey", **kw) -> None:
        self.cage_code = cage_code
        self.presenter = presenter
        self.geom = {
            "Q1_TOP_LEFT": (0, 0, 960, 540),
            "Q2_BOTTOM_LEFT": (0, 540, 960, 540),
            "Q3_TOP_RIGHT": (960, 0, 960, 540),
            "Q4_BOTTOM_RIGHT": (960, 540, 960, 540),
        }
