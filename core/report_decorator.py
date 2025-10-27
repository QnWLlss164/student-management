from abc import ABC, abstractmethod
from core.grading_strategy import GradeContext, WeightedAverageStrategy, classify_grade

class ReportComponent(ABC):
    @abstractmethod
    def build_report(self, student) -> dict:
        """Trả về dict thông tin báo cáo cho sinh viên."""
        pass

class BasicReport(ReportComponent):
    def build_report(self, student):
        # dùng default strategy: WeightedAverageStrategy
        grade_context = GradeContext(WeightedAverageStrategy())
        final_score = grade_context.get_final_grade(student.midterm, student.final)

        return {
            "name": student.name,
            "student_id": student.student_id,
            "classroom": student.classroom,
            "midterm": student.midterm,
            "final": student.final,
            "final_score": final_score,
            "rank": classify_grade(final_score)
        }

class ReportDecorator(ReportComponent):
    def __init__(self, component: ReportComponent):
        self._component = component

    def build_report(self, student):
        return self._component.build_report(student)

class GPAReportDecorator(ReportDecorator):
    def build_report(self, student):
        data = super().build_report(student)
        # ví dụ GPA tạm tính
        data["gpa_estimate"] = round(data["final_score"] / 2.5, 2)
        return data

class WarningReportDecorator(ReportDecorator):
    def build_report(self, student):
        data = super().build_report(student)
        data["academic_warning"] = data["final_score"] < 5.0
        return data
