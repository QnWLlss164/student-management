from abc import ABC, abstractmethod

class GradeStrategy(ABC):
    @abstractmethod
    def calculate(self, midterm: float, final: float) -> float:
        """Trả về điểm tổng kết cuối cùng (0-10)."""
        pass

class WeightedAverageStrategy(GradeStrategy):
    # ví dụ: 40% giữa kỳ + 60% cuối kỳ
    def calculate(self, midterm, final):
        return round(midterm * 0.4 + final * 0.6, 2)

class MaxScoreStrategy(GradeStrategy):
    # ví dụ: lấy điểm cao nhất giữa kỳ / cuối kỳ
    def calculate(self, midterm, final):
        return round(max(midterm, final), 2)

class StrictStrategy(GradeStrategy):
    # ví dụ: nếu 1 trong 2 <4 thì rớt
    def calculate(self, midterm, final):
        if midterm < 4 or final < 4:
            return 3.9  # rớt
        return round((midterm + final) / 2, 2)

class GradeContext:
    """Context nắm giữ strategy hiện tại."""
    def __init__(self, strategy: GradeStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: GradeStrategy):
        self.strategy = strategy

    def get_final_grade(self, midterm, final):
        return self.strategy.calculate(midterm, final)

def classify_grade(score: float) -> str:
    """Phân loại học lực theo thang điểm VN."""
    if score >= 8.5:
        return "Giỏi"
    elif score >= 7.0:
        return "Khá"
    elif score >= 5.0:
        return "Trung bình"
    else:
        return "Yếu"
