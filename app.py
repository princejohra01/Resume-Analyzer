from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

SKILLS = [
    "python", "java", "c++", "c", "javascript", "typescript",
    "react", "node.js", "html", "css", "sql", "mysql",
    "mongodb", "git", "github", "docker", "aws", "azure",
    "machine learning", "deep learning", "artificial intelligence",
    "pandas", "numpy", "tensorflow", "pytorch", "flask",
    "django", "spring", "figma", "excel", "power bi"
]

def analyze_resume(text):
    text = re.sub(r"\s+", " ", text).strip()
    lower = text.lower()

    skills = sorted(set(
        skill for skill in SKILLS
        if skill in lower
    ))

    email = bool(
        re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text)
    )

    phone = bool(
        re.search(r"\b\d{10}\b", text)
    )

    linkedin = "linkedin.com" in lower
    github = "github.com" in lower

    sections = {
        "Summary": any(x in lower for x in
                       ["summary", "objective", "profile"]),

        "Education": "education" in lower,

        "Experience": any(x in lower for x in
                          ["experience", "internship", "employment"]),

        "Projects": "project" in lower,

        "Skills": "skills" in lower,

        "Certifications": any(x in lower for x in
                              ["certification", "certificate"]),

        "Achievements": any(x in lower for x in
                           ["achievement", "award"])
    }

    action_words = [
        "built", "developed", "created",
        "designed", "implemented", "optimized",
        "automated", "improved", "managed"
    ]

    action_count = sum(
        lower.count(word) for word in action_words
    )

    metrics = bool(
        re.search(r"\b\d+(?:%|x|k|m)\b", lower)
    )

    checks = [
        email,
        phone,
        sections["Summary"],
        sections["Education"],
        sections["Projects"],
        sections["Skills"],
        linkedin,
        github,
        action_count >= 3,
        metrics
    ]

    score = round(sum(checks) / len(checks) * 100)

    suggestions = []

    if not email:
        suggestions.append(
            "Add a professional email address."
        )

    if not phone:
        suggestions.append(
            "Add your phone number."
        )

    if not sections["Summary"]:
        suggestions.append(
            "Add a short professional summary."
        )

    if not sections["Projects"]:
        suggestions.append(
            "Add 2–4 relevant projects."
        )

    if not linkedin:
        suggestions.append(
            "Add your LinkedIn profile."
        )

    if not github:
        suggestions.append(
            "Add GitHub or portfolio if applying for tech jobs."
        )

    if action_count < 3:
        suggestions.append(
            "Use stronger action words such as Built, Developed, "
            "Implemented and Optimized."
        )

    if not metrics:
        suggestions.append(
            "Add numbers and measurable results to your achievements."
        )

    strengths = []

    if skills:
        strengths.append(
            f"{len(skills)} technical skills detected."
        )

    if sections["Projects"]:
        strengths.append(
            "Projects section detected."
        )

    if sections["Education"]:
        strengths.append(
            "Education section detected."
        )

    if linkedin:
        strengths.append(
            "LinkedIn profile detected."
        )

    if github:
        strengths.append(
            "GitHub profile detected."
        )

    return {
        "score": score,
        "skills": skills,
        "sections": sections,
        "suggestions": suggestions,
        "strengths": strengths,
        "word_count": len(text.split())
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    if "resume" not in request.files:
        return jsonify({
            "error": "Please upload your resume."
        }), 400

    file = request.files["resume"]

    if not file.filename:
        return jsonify({
            "error": "Please select a resume."
        }), 400

    try:

        text = file.read().decode(
            "utf-8",
            errors="ignore"
        )

        if not text.strip():
            return jsonify({
                "error":
                "Could not read this file. "
                "For this demo, upload a TXT resume."
            }), 400

        result = analyze_resume(text)

        return jsonify(result)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
)
