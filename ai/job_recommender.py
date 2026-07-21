def recommend_jobs(skills):

    jobs = []

    skills = [skill.lower() for skill in skills]

    if "python" in skills:
        jobs.append(("Python Developer",95))

    if "flask" in skills:
        jobs.append(("Flask Developer",92))

    if "sql" in skills or "mysql" in skills:
        jobs.append(("Database Developer",90))

    if "javascript" in skills:
        jobs.append(("Frontend Developer",88))

    if "html" in skills and "css" in skills:
        jobs.append(("Web Developer",90))

    if "machine learning" in skills:
        jobs.append(("AI Engineer",96))

    return jobs