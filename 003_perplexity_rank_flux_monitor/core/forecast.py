import numpy as np

class RankForecaster:
    @staticmethod
    def predict_shift(history: list[int]) -> dict:
        """Simple probability forecasting based on historical rank trends."""
        if len(history) < 3:
            return {"probability": 50, "direction": "STABLE"}
        
        # Calculate moving average and momentum
        avg = np.mean(history)
        momentum = history[-1] - history[0]
        
        prob = 50 + (abs(momentum) * 5)
        prob = min(max(prob, 1), 99)
        
        direction = "UP" if momentum < 0 else "DOWN" if momentum > 0 else "STABLE"
        
        return {
            "probability": int(prob),
            "direction": direction,
            "next_day_estimate": max(1, int(avg + (momentum * 0.2)))
        }
