import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import time
import random

from numpy.ma.core import argmax

matplotlib.use('TkAgg')

# Setting all the Parameters
num_trials = 6
heatmap_trials = 3
scatter_trials = 3
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

num_schools = 10
num_days = 5
num_months = 12
month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

trial_order = random.sample(["heatmap"] * heatmap_trials + ["scatter"] * scatter_trials, num_trials)

questions = [
    {
        "question": "Identify the month with the highest absences for a school",
        "correct_answer": None
    },
    {
        "question": "Identify the month with the lowest absences for a school",
        "correct_answer": None
    },
    {
        "question": "Identify the school with the highest absence in month 1",
        "correct_answer": None
    },
    {
        "question": "Identify the school with the lowest absence in month 3",
        "correct_answer": None
    },
    {
        "question": "Identify the school with the least variance in absences",
        "correct_answer": None
    },
    {
        "question": "Identify the school with the most variance in absences",
        "correct_answer": None
    }
]

trial_questions = random.sample(questions, num_trials)

def generate_heatmap_data():
    data = np.random.randint(0, 151, size=(num_schools, num_months))
    max_value_index = np.unravel_index(np.argmax(data, axis=None), data.shape)
    min_value_index = np.unravel_index(np.argmin(data, axis=None), data.shape)


    answers = {
        "Identify the month with the highest absences for a school": max_value_index,
        "Identify the month with the lowest absences for a school": min_value_index,
        "Identify the school with the highest absences in month 1": np.argmax(data[:, 0]),
        "Identify the school with the lowest absences in month 3": np.argmin(data[:, 2]),
        "Identify the school with the least variance in absences": np.argmin(np.var(data, axis=1)),
        "Identify the school with the most variance in absences": np.argmax(np.var(data, axis=1))
    }

    return data, answers


def generate_scatter_data():
    x = np.arange(1, num_months + 1)
    y_data = np.random.randint(0, 250, size=(num_schools, num_months))
    max_value_index = np.unravel_index(np.argmax(y_data, axis=None), y_data.shape)
    min_value_index = np.unravel_index(np.argmin(y_data, axis=None), y_data.shape)

    answers = {
        "Identify the month with the highest absences for a school": max_value_index[1],  # Month index
        "Identify the month with the lowest absences for a school": min_value_index[1],  # Month index
        "Identify the school with the highest absence in month 1": np.argmax(y_data[:, 0]),
        "Identify the school with the lowest absence in month 3": np.argmin(y_data[:, 2]),
        "Identify the school with the least variance in absences": np.argmin(np.var(y_data, axis=1)),
        "Identify the school with the most variance in absences": np.argmax(np.var(y_data, axis=1))
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

        # Check if the user's click matches the correct answer
        is_correct = False
        if isinstance(correct_answer, tuple):
            correct_row, correct_col = correct_answer
            if row == correct_row and col == correct_col:
                print("Correct!")
                is_correct = True
            else:
                print("Incorrect.")
        elif isinstance(correct_answer, int):
            if question_text.startswith("Identify the school"):
                if row == correct_answer:
                    print("Correct!")
                    is_correct = True
                else:
                    print("Incorrect.")
            elif question_text.startswith("Identify the month"):
                if col == correct_answer:
                    print("Correct!")
                    is_correct = True
                else:
                    print("Incorrect.")

        # Record response time and correctness
        response_time = time.time() - start_time
        response_times.append(response_time)
        results.append(is_correct)

        # Move to the next trial
        fig.canvas.mpl_disconnect(trial_cid)
        trial_index += 1
        show_ready_screen()
        
        # # valid answer check
        # if 0 <= row < num_schools and 0 <= col < num_months:
        #     response_time = time.time() - start_time
        #     response_times.append(response_time)
        #     fig.canvas.mpl_disconnect(trial_cid)
        #     trial_index += 1
        #     show_ready_screen()


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
    global trial_index, start_time, trial_cid
    if event.inaxes:
        x_clicked, y_clicked = event.xdata, event.ydata
        x_tolerance, y_tolerance = 0.4, 0.6

        if isinstance(correct_answer, tuple):
            correct_x, correct_y = correct_answer
            if abs(x_clicked - correct_x) <= x_tolerance and abs(y_clicked - correct_y) <= y_tolerance:
                print("Correct!")
                is_correct = True
            else:
                print("Incorrect.")
                is_correct = False
        else:
            is_correct = False

        # Record response time and correctness
        response_time = time.time() - start_time
        response_times.append(response_time)
        results.append(is_correct)

        # Move to the next trial
        fig.canvas.mpl_disconnect(trial_cid)
        trial_index += 1
        show_ready_screen()

        # valid answer check
        # for x_vals, y_vals in scatter_points:
        #     for x, y in zip(x_vals, y_vals):
        #         # Check both x and y tolerances
        #         if abs(x - x_clicked) <= x_tolerance and abs(y - y_clicked) <= y_tolerance:
        #             response_time = time.time() - start_time
        #             response_times.append(response_time)
        #             fig.canvas.mpl_disconnect(trial_cid)
        #             trial_index += 1
        #             show_ready_screen()
        #             return

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
print("Experiment Complete. Results:")
for i, response_time in enumerate(response_times, 1):
    print(f"Trial {i}: Response Time: {response_time:.2f} seconds")

print_results()
