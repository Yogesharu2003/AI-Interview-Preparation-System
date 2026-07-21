def get_response(message):

    message = message.lower().strip()

    responses = {

        # Python
        "what is python":
        "Python is a high-level, interpreted, object-oriented programming language known for its simplicity and readability.",

        "difference between list and tuple":
        "Lists are mutable, whereas tuples are immutable. Lists use [], tuples use ().",

        "what is oop":
        "Object-Oriented Programming is a programming paradigm based on classes and objects. It includes encapsulation, inheritance, polymorphism, and abstraction.",

        "what is class":
        "A class is a blueprint for creating objects.",

        "what is object":
        "An object is an instance of a class.",

        "what is inheritance":
        "Inheritance allows one class to inherit properties and methods from another class.",

        "what is polymorphism":
        "Polymorphism allows the same method to behave differently for different objects.",

        "what is encapsulation":
        "Encapsulation is wrapping data and methods together in a single unit while restricting direct access.",

        "what is abstraction":
        "Abstraction hides implementation details and shows only essential features.",

        "what is decorator":
        "A decorator is a function that modifies the behavior of another function.",

        "what is lambda":
        "A lambda function is an anonymous function written using the lambda keyword.",

        "what is generator":
        "A generator returns values one at a time using the yield keyword.",

        "what is exception handling":
        "Exception handling manages runtime errors using try, except, finally, and raise.",

        "what is numpy":
        "NumPy is a Python library for numerical computing and arrays.",

        "what is pandas":
        "Pandas is a Python library used for data manipulation and analysis.",

        "what is flask":
        "Flask is a lightweight Python web framework used to build web applications.",

        "what is django":
        "Django is a high-level Python web framework that follows the MVT architecture.",

        # SQL
        "what is sql":
        "SQL (Structured Query Language) is used to manage relational databases.",

        "what is primary key":
        "A Primary Key uniquely identifies each record in a table.",

        "what is foreign key":
        "A Foreign Key creates a relationship between two database tables.",

        "what is join":
        "JOIN combines rows from two or more tables using a related column.",

        "types of joins":
        "The main JOIN types are INNER JOIN, LEFT JOIN, RIGHT JOIN, and FULL OUTER JOIN.",

        "difference between delete and truncate":
        "DELETE removes selected rows and can be rolled back. TRUNCATE removes all rows quickly and resets identity values.",

        "what is group by":
        "GROUP BY groups rows with the same values into summary rows.",

        "what is having":
        "HAVING filters grouped records after GROUP BY.",

        "what is index":
        "An Index improves the speed of data retrieval from a database.",

        "what is view":
        "A View is a virtual table based on the result of a SQL query.",

        "what is normalization":
        "Normalization organizes database tables to reduce redundancy.",

        # HTML
        "what is html":
        "HTML stands for HyperText Markup Language and is used to create web pages.",

        # CSS
        "what is css":
        "CSS stands for Cascading Style Sheets and is used to style HTML pages.",

        # JavaScript
        "what is javascript":
        "JavaScript is a scripting language used to make web pages interactive.",

        # API
        "what is api":
        "An API (Application Programming Interface) allows different software applications to communicate.",

        # HR
        "tell me about yourself":
        "Introduce yourself with your education, skills, projects, and career goals.",

        "why should we hire you":
        "Highlight your skills, willingness to learn, problem-solving ability, and enthusiasm.",

        "what are your strengths":
        "Mention strengths like quick learning, teamwork, communication, and problem-solving.",

        "what are your weaknesses":
        "Mention a genuine weakness and explain how you're improving it.",

        "why do you want to join our company":
        "Talk about the company's reputation, learning opportunities, and how your skills match the role."
    }

    if message in responses:
        return responses[message]

    for key in responses:
        if key in message:
            return responses[key]

    return (
        "Sorry, I couldn't find an exact answer.\n\n"
        "Try asking questions like:\n"
        "• What is Python?\n"
        "• Difference between List and Tuple\n"
        "• What is OOP?\n"
        "• What is Flask?\n"
        "• What is SQL?\n"
        "• What is JOIN?\n"
        "• What is Primary Key?\n"
        "• Tell me about yourself.\n"
        "• Why should we hire you?"
    )