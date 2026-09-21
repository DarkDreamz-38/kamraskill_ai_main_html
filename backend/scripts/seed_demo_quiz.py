"""
Seed a demo quiz (id=1) with 20 MCQs so the frontend quiz page
(quiz.html?quizId=1) works out of the box.

Run from the backend directory:
    python scripts/seed_demo_quiz.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from database import SessionLocal  # noqa: E402
from models import Competency, LearningMaterial, Quiz, QuizQuestion  # noqa: E402


QUESTIONS = [
    ("A histogram is best used to visualize which type of data?",
     {"A": "Continuous numerical distributions", "B": "Categorical counts", "C": "Geographic coordinates", "D": "Time series trends"},
     "A", "Easy"),
    ("Which measure of central tendency is most affected by outliers?",
     {"A": "Median", "B": "Mode", "C": "Mean", "D": "Range"},
     "C", "Easy"),
    ("What does a p-value below 0.05 conventionally indicate?",
     {"A": "The null hypothesis is true", "B": "Statistically significant evidence against the null", "C": "A large effect size", "D": "Data collection bias"},
     "B", "Medium"),
    ("In hypothesis testing, a Type I error occurs when we...",
     {"A": "Reject a true null hypothesis", "B": "Fail to reject a false null hypothesis", "C": "Use the wrong test statistic", "D": "Sample too few observations"},
     "A", "Medium"),
    ("Which chart is most appropriate to show composition over time?",
     {"A": "Pie chart", "B": "Scatter plot", "C": "Stacked area chart", "D": "Histogram"},
     "C", "Medium"),
    ("What is the primary purpose of a box plot?",
     {"A": "Displaying correlation matrices", "B": "Showing distribution, median and outliers", "C": "Tracking cumulative totals", "D": "Comparing part-to-whole ratios"},
     "B", "Easy"),
    ("Correlation does not imply causation because...",
     {"A": "Correlation coefficients are always wrong", "B": "A third variable or reverse causality may explain the association", "C": "Correlation only applies to categorical data", "D": "Causation cannot ever be established"},
     "B", "Medium"),
    ("Which sampling method gives every member an equal, independent chance of selection?",
     {"A": "Convenience sampling", "B": "Snowball sampling", "C": "Judgmental sampling", "D": "Simple random sampling"},
     "D", "Easy"),
    ("A confidence interval that includes zero for a mean difference implies...",
     {"A": "The effect is statistically significant", "B": "The sample size was too large", "C": "No statistically significant difference at that level", "D": "The data must be non-linear"},
     "C", "Medium"),
    ("Standard deviation measures...",
     {"A": "The spread of values around the mean", "B": "The most frequent value", "C": "The midpoint of the data", "D": "The steepest slope of a regression line"},
     "A", "Easy"),
    ("In linear regression, R-squared represents...",
     {"A": "The slope of the fitted line", "B": "The proportion of variance explained by the model", "C": "The number of predictors", "D": "The residual sum of squares"},
     "B", "Medium"),
    ("Which normalization scales values to a fixed 0-1 range?",
     {"A": "Z-score standardization", "B": "Log transformation", "C": "Min-max scaling", "D": "Rank transformation"},
     "C", "Medium"),
    ("A left-skewed distribution has...",
     {"A": "A long tail on the right side", "B": "A long tail on the left side", "C": "Two equal tails", "D": "No tail at all"},
     "B", "Medium"),
    ("What is the first step in a structured data analysis workflow?",
     {"A": "Build a dashboard", "B": "Define the question and success metrics", "C": "Choose a chart type", "D": "Deploy a model to production"},
     "B", "Easy"),
    ("Which plot best examines the relationship between two continuous variables?",
     {"A": "Bar chart", "B": "Scatter plot", "C": "Stacked bar chart", "D": "Donut chart"},
     "B", "Easy"),
    ("Selection bias primarily threatens which aspect of a study?",
     {"A": "Internal validity of conclusions", "B": "Visual appeal of charts", "C": "Compute cost", "D": "Model interpretability only"},
     "A", "Hard"),
    ("The central limit theorem states that...",
     {"A": "All populations are normal", "B": "Sample means approach normality as sample size grows", "C": "Variance always decreases with more data", "D": "Medians converge to the mean"},
     "B", "Hard"),
    ("Which of the following is a measure of dispersion?",
     {"A": "Mean", "B": "Mode", "C": "Interquartile range", "D": "Median"},
     "C", "Easy"),
    ("Overfitting in a predictive model means...",
     {"A": "The model captures noise instead of the underlying pattern", "B": "The model is too simple", "C": "The training loss is too high", "D": "There are too few features"},
     "A", "Hard"),
    ("A KPI dashboard should prioritize...",
     {"A": "As many metrics as possible", "B": "3D visuals for impact", "C": "Decision-relevant metrics with clear baselines and targets", "D": "Raw data dumps"},
     "C", "Medium"),
]


def main() -> None:
    db = SessionLocal()
    try:
        existing = db.query(Quiz).filter(Quiz.id == 1).first()
        if existing:
            print("Quiz 1 already exists — nothing to do.")
            return

        material = db.query(LearningMaterial).first()
        if not material:
            material = LearningMaterial(
                filename="data_viz_guide.pdf",
                title="Data Visualization Fundamentals",
                extracted_text="Demo study material covering statistics and data visualization fundamentals.",
                pages=1,
            )
            db.add(material)
            db.flush()

        competency = db.query(Competency).order_by(Competency.id).first()

        quiz = Quiz(
            material_id=material.id,
            title="Data Analysis Certification Assessment",
            number_of_questions=len(QUESTIONS),
        )
        db.add(quiz)
        db.flush()

        for question, options, correct, difficulty in QUESTIONS:
            db.add(QuizQuestion(
                quiz_id=quiz.id,
                question=question,
                option_a=options["A"],
                option_b=options["B"],
                option_c=options["C"],
                option_d=options["D"],
                correct_answer=correct,
                explanation="",
                difficulty=difficulty,
                competency_id=competency.id if competency else None,
            ))

        db.commit()
        print(f"Seeded quiz id={quiz.id} with {len(QUESTIONS)} questions.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
