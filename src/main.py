from flask import Flask, render_template, request, redirect, send_file
from stackoverflow import get_jobs as get_so_jobs
from indeed import get_jobs as get_indeed_jobs
from export import save_to_file

app = Flask("SuperScrapper")

db = {}

@app.route("/")
def home():
  return render_template("home.html")

@app.route("/report")
def report():
  word = request.args.get("word")
  if word:
    word = word.lower()

    existingJobs = db.get(word)
    if existingJobs:
      jobs = existingJobs
    else:
      so_jobs = get_so_jobs(word)
      indeed_jobs = get_indeed_jobs(word)
      jobs = so_jobs + indeed_jobs
      db[word] = jobs
      # save_to_file(jobs, word)
  else:
    return redirect("/")
  return render_template(
    "report.html", 
    searchingBy=word, 
    resultsNumber=len(jobs),
    jobs=jobs)

@app.route("/export")
def export():
  try:
    word = request.args.get("word")
    if not word:
      raise Exception();
    word = word.lower()
    jobs = db.get(word)
    if not jobs:
      raise Exception()
    save_to_file(jobs, word)
    
    return send_file(f"{word}.csv")
  except:
    return redirect("/")

  if word:
    word = word.lower()

app.run(host="0.0.0.0")