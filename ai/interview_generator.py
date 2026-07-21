from question_bank.python import python_questions
from question_bank.java import java_questions
from question_bank.sql import sql_questions
from question_bank.hr import hr_questions


def generate_questions(skills):

    questions = []

    if "Python" in skills:
        questions.extend([
            "What is Python?",
            "Difference between List and Tuple?",
            "What is OOP?",
            "Explain Flask.",
            "What is NumPy?",
            "What is Pandas?",
            "Explain Decorators.",
            "What is Lambda Function?",
            "What is Generator?",
            "Explain Exception Handling."
        ])

    if "Java" in skills:
        questions.extend([
            "What is Java?",
            "Difference between JDK, JRE and JVM?",
            "Explain OOP.",
            "What is Inheritance?",
            "What is Polymorphism?",
            "What is Interface?",
            "What is Abstract Class?",
            "Difference between ArrayList and LinkedList?",
            "Explain Exception Handling.",
            "What is Spring Boot?"
        ])

    if "SQL" in skills or "MySQL" in skills:
        questions.extend([
            "What is SQL?",
            "Explain JOIN.",
            "Difference between DELETE and TRUNCATE?",
            "What is GROUP BY?",
            "What is HAVING?",
            "What is Primary Key?",
            "What is Foreign Key?",
            "Find Second Highest Salary.",
            "What is Index?",
            "What is View?"
        ])

    return questions