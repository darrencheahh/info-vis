import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np
import time
import random
import re

matplotlib.use('TkAgg')

# Setting all the Parameters
num_trials = 6
heatmap_trials = 3
scatter_trials = 3
num_schools = 10
num_days = 5
num_months = 12
trial_index = 0 # starts at 0, up till num_trials 
start_time = None
response_times = []
results = []  # stores the results of each trial
trial_types = []
trial_cid = None  # this is for connecting events
current_trial_type = None
point_size = 80
colors = plt.colormaps.get_cmap('tab10').colors
current_question = {"question": "", "correct_answer": None}
month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

trial_order = random.sample(["heatmap"] * heatmap_trials + ["scatter"] * scatter_trials, num_trials)

questions = [
    {
        "question": "For school 5, select the month with the highest absences",
        "correct_answer": None
    },
    {
        "question": "For school 6, select the month with the second highest absences",
        "correct_answer": None
    },
    {
        "question": "Identify the school with the highest absence in January",
        "correct_answer": None
    },
    {
        "question": "Identify the school with the lowest absence in March",
        "correct_answer": None
    },
    {
        "question": "Compare schools 1 and 2 in January for higher absences",
        "correct_answer": None
    },
    {
        "question": "Identify schools 2 and 5, which had the highest decrease in absences in February",
        "correct_answer": None
    }
]

trial_questions = random.sample(questions, num_trials)

def generate_heatmap_data():
    data = np.random.randint(0, 151, size=(num_schools, num_months))

    answers = {
        "For school 5, select the month with the highest absences": np.argmax(data[4, :]),
        "For school 6, select the month with the second highest absences": np.argsort(data[5, :])[-2],
        "Identify the school with the highest absence in January": np.argmax(data[:, 0]),
        "Identify the school with the lowest absence in March": np.argmin(data[:, 2]),
        "Compare schools 1 and 2 in January for higher absences": "School 1" if data[0,0] > data[1,0] else "School 2",
        "Identify schools 2 and 5, which had the highest decrease in absences in February": "School 2" if (data[1, 1] - data[1, 2]) > (data[4, 1] - data[4, 2]) else "School 5"
    }

    return data, answers


def generate_scatter_data():
    x = np.arange(1, num_months + 1)
    y_data = np.random.randint(0, 250, size=(num_schools, num_months))

    answers = {
        "For school 5, select the month with the highest absences": np.argmax(y_data[4, :]),
        "For school 6, select the month with the second highest absences": np.argsort(y_data[5, :])[::-1][1],
        "Identify the school with the highest absence in January": np.argmax(y_data[:, 0]),
        "Identify the school with the lowest absence in March": np.argmin(y_data[:, 2]),
        "Compare schools 1 and 2 in January for higher absences": "School 1" if y_data[0, 0] > y_data[1, 0] else "School 2",
        "Identify schools 2 and 5, which had the highest decrease in absences in February": "School 2" if (y_data[1, 1] - y_data[1, 2]) > (y_data[4, 1] - y_data[4, 2]) else "School 5"
    }

    return x, y_data, answers


# this shows the 'Begin Test' screen
def start_experiment(event):
    fig.canvas.mpl_disconnect(begin_cid) 
    show_ready_screen()  


# this is the 1 second window between trials
def show_ready_screen():
    plt.clf()
    plt.text(0.5, 0.5, "Ready", ha="center", va="center", fontsize=24, color='blue')
    plt.axis("off")
    plt.pause(1)
    show_next_trial()

# Start a trial based on the trial type
def show_next_trial():
    global trial_index, current_trial_type, current_question
    if trial_index < num_trials:
        current_trial_type = trial_order[trial_index]
        current_question = trial_questions[trial_index]  # Get the question info

        # Set the current question text and reset the correct answer
        current_question["question"] = current_question["question"]
        current_question["correct_answer"] = None  # This will be set in the trial function

        # Display the question
        plt.clf()
        plt.text(0.5, 0.5, current_question["question"], ha="center", va="center", fontsize=16, wrap=True)
        plt.axis("off")
        plt.pause(2)  # Pause to show the question before starting the trial

        if current_trial_type == "heatmap":
            start_heatmap_trial()
        else:
            start_scatter_trial()
    else:
        plt.close()


def start_heatmap_trial():
    global trial_index, start_time, trial_cid, current_question

    trial_types.append("heatmap")

    plt.clf()
    data, answers = generate_heatmap_data()

    question_text = current_question["question"]
    correct_answer = answers.get(question_text, None)
    current_question["correct_answer"] = correct_answer

    ax = plt.gca()
    cax = ax.matshow(data, cmap="viridis")
    plt.colorbar(cax)
    ax.set_xticks(np.arange(num_months))
    ax.set_xticklabels(month_names, rotation=90)
    ax.set_yticks(np.arange(num_schools))
    ax.set_yticklabels([f"School {i+1}" for i in range(num_schools)])
    ax.set_title(f"Heatmap Trial {trial_index + 1}")

    start_time = time.time()
    trial_cid = fig.canvas.mpl_connect('button_press_event', on_click_heatmap)
    plt.draw()


def on_click_heatmap(event):
    global trial_index, start_time, trial_cid, current_question

    if event.inaxes and event.inaxes == plt.gca():
        row, col = int(event.ydata), int(event.xdata)
        question_text = current_question["question"]
        correct_answer = current_question["correct_answer"]

        # Debug output
        print(f"Question: {question_text}")
        print(f"Clicked: (row={row}, col={col}), Correct Answer: {correct_answer}")

        is_correct = False
        if "For school 5, select the month with the highest absences" in question_text:
            is_correct = (row == 4 and col == correct_answer)
        elif "For school 6, select the month with the second highest absences" in question_text:
            is_correct = (row == 5 and col == correct_answer)
        elif "Identify the school with the highest absence in January" in question_text:
            is_correct = (col == 0 and row == correct_answer)
        elif "Identify the school with the lowest absence in March" in question_text:
            is_correct = (col == 2 and row == correct_answer)
        elif "Compare schools 1 and 2 in January for higher absences" in question_text:
            is_correct = (col == 0 and (row == 0 or row == 1))
        elif "Identify schools 2 and 5, which had the highest decrease in absences in February" in question_text:
            is_correct = (col == 1 and (row == 1 or row == 4))

        # Record response time and correctness
        response_time = time.time() - start_time
        response_times.append(response_time)
        results.append(is_correct)

        # Move to the next trial
        fig.canvas.mpl_disconnect(trial_cid)
        trial_index += 1
        show_ready_screen()

def start_scatter_trial():
    global trial_index, start_time, trial_cid, y_data, current_question

    trial_types.append("scatterplot")

    plt.clf()
    x, y_data, answers = generate_scatter_data()

    question_text = current_question["question"]
    correct_answer = answers[question_text]
    current_question["correct_answer"] = correct_answer

    ax = plt.gca()
    scatter_points = []
    
    for i, y in enumerate(y_data):
        scatter = ax.scatter(x, y, color=colors[i], label=f'School {i + 1}', s=point_size)
        scatter_points.append((x, y))
    
    ax.set_title(f"Scatter Trial {trial_index + 1}")
    ax.set_xlabel("Month")
    ax.set_ylabel("Absences")
    ax.set_xticks(x)
    ax.set_xticklabels(month_names)
    ax.legend(title="Schools", bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0.5)

    start_time = time.time()
    trial_cid = fig.canvas.mpl_connect('button_press_event', lambda event: on_click_scatter(event, scatter_points, correct_answer))
    plt.draw()


def on_click_scatter(event, scatter_points, correct_answer):
    global trial_index, start_time, trial_cid, current_question
    if event.inaxes:
        x_clicked, y_clicked = event.xdata, event.ydata
        correct_x_tolerance, correct_y_tolerance = 0.5, 10  # month, absences

        question_text = current_question["question"]

        # Debug output
        print(f"Question: {question_text}")
        print(f"Clicked: (x={x_clicked:.2f}, y={y_clicked:.2f}), Correct Answer: {correct_answer}")

        is_correct = False

        # Handling month-based questions
        if isinstance(correct_answer, int):
            # Check if the x-coordinate of the click is close to the correct month
            if abs(x_clicked - (correct_answer + 1)) <= correct_x_tolerance:
                is_correct = True

        # Handling comparison questions between schools
        elif isinstance(correct_answer, str) and "School" in correct_answer:
            # Extract school numbers from the question using regular expressions
            school_numbers = list(map(int, re.findall(r'\d+', question_text)))
            if len(school_numbers) == 2:
                school_1, school_2 = school_numbers

                # Retrieve absences for both schools in January (or any relevant month)
                month_index = 0  # Default to January for now; adjust based on the question
                if "February" in question_text:
                    month_index = 1
                elif "March" in question_text:
                    month_index = 2

                school_1_absence = y_data[school_1 - 1, month_index]  # Adjust for 0-based index
                school_2_absence = y_data[school_2 - 1, month_index]

                # Determine which school has higher absences
                correct_school = school_1 if school_1_absence > school_2_absence else school_2

                # Validate if the user's click is near the correct school's data point for the specified month
                if correct_answer == f"School {correct_school}":
                    # Get the x-coordinate for the month and y-coordinate for the correct school's absences
                    correct_x = month_index + 1  # +1 because x values are 1-based (January is 1, February is 2, etc.)
                    correct_y = y_data[correct_school - 1, month_index]

                    # Check if the click is within the tolerance range of the correct point
                    if abs(x_clicked - correct_x) <= correct_x_tolerance and abs(y_clicked - correct_y) <= correct_y_tolerance:
                        is_correct = True

        # Record response time and correctness
        response_time = time.time() - start_time
        response_times.append(response_time)
        results.append(is_correct)

        # Move to the next trial
        fig.canvas.mpl_disconnect(trial_cid)
        trial_index += 1
        show_ready_screen()

# Function to print results at the end of the experiment
def print_results():
    print("\nExperiment Complete. Results:")
    for i, (response_time, is_correct, trial_type) in enumerate(zip(response_times, results, trial_types), 1):
        status = "Correct" if is_correct else "Wrong"
        print(f"Trial {i} ({trial_type}): Response Time: {response_time:.2f} seconds - {status}")


# this is so its all within 1 ui window
fig, ax = plt.subplots()
ax.text(0.5, 0.5, 'Click to Begin Test', ha='center', va='center', fontsize=20)
ax.axis("off")
begin_cid = fig.canvas.mpl_connect('button_press_event', start_experiment) 
plt.show()

# print results
print_results()