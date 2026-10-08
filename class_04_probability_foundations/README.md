# Class 04: Probability Foundations (+ learning to use AI)

**Topics:** probability concepts · conditional probability · independence · Bayes' theorem · random variables · probability distributions
**Second theme:** a workflow for using AI on quantitative problems — **Understand → Prompt → Run → Verify → Reflect** — with simulation as the verification tool.

## 📂 Notebooks (`notebooks/`)
| File | Who | Purpose |
|---|---|---|
| `01_INSTRUCTOR_concepts.ipynb` | **you** | Screen-share demo of all 6 topics, notes + pacing inside, pre-rendered |
| `01_STUDENT_concepts.ipynb` | students | Same code with predict boxes, no notes |
| `02_INSTRUCTOR_ai_demo.ipynb` | **you** | You solve **3 tasks live with AI** (Bayes, Poisson, Monty Hall twist) showing weak vs strong prompts and verification |
| `02_STUDENT_ai_demo_followalong.ipynb` | students | Workflow + tasks, AI-log template |
| `03_STUDENT_ai_tasks.ipynb` | students | **3 tasks they solve with AI** (spam filter, casino game, exam curve). Deliberately *no* pre-built code: only hints, empty cells, and an AI log |
| `03_INSTRUCTOR_ai_tasks_solutions.ipynb` | **you** | Solutions, likely AI traps, rubric, spot-check questions |
| `CLASS_LESSON_PLAN.md` | **you** | Suggested timeline and logistics |

Rebuild everything: `cd scripts && python create_class4_notebooks.py` (reuses `nbtools.py` from Class 03). Edit the script, not the `.ipynb` files.

## 🧭 Design notes
* Student task notebook follows the Class 03 feedback: *little pre-built*, students write the code, verification is mandatory and graded.
* The AI-demo notebook intentionally contains **no fake AI transcripts**: you run the prompts live with whichever AI you use, and verification cells hold the ground truth. Each task targets a real, common AI failure: base rates (Task 1), off-by-one ≥ vs > and distribution choice (Task 2), pattern-matching the famous problem instead of reading it (Task 3).
