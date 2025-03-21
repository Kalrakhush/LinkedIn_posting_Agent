from flask import Flask, render_template, request, redirect, url_for, flash
# from linkedin_posting_agent.crew import LinkedInPostingCrew, post_on_linkedin

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Replace with a secure key

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Gather inputs from the form
        inputs = {
            "topic": request.form.get("topic", ""),
            "tone": request.form.get("tone", ""),
            "audience": request.form.get("audience", ""),
            "details": request.form.get("details", ""),
            "hashtags": request.form.get("hashtags", "")
        }
        # Kick off the crew; this triggers the content creation task.
        crew_instance = LinkedInPostingCrew().crew()
        crew_output = crew_instance.kickoff(inputs=inputs)
        post_content = crew_output.tasks_output[0].raw  # Assuming first task returns the post text

        # Now post to LinkedIn using our custom function.
        post_result = post_on_linkedin(post_content)
        flash(post_result, "info")
        return redirect(url_for("index"))
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
