import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import time
import random
from matplotlib.colors import ListedColormap
import matplotlib.patches as patches

matplotlib.use('TkAgg')

# Color Universal Design (CUD) colors
cud_colors = ['#377eb8', '#ff7f00', '#4daf4a', '#f781bf', '#a65628', '#984ea3', '#999999', '#e41a1c', '#dede00']
cud_cmap = ListedColormap(cud_colors)


matplotlib_colors = plt.get_cmap('tab10').colors

# Setting all the Parameters
num_trials = 10
num_schools = 10
num_days = 5
num_months = 12
trial_index = 0
start_time = None
response_times = []
results = []
trial_types = []
selected_chart_type = None  # Stores user's choice of chart
current_trial_type = None
trial_cid = None
point_size = 80
month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

questions = [
    {"question": "For school 5, select the month with the highest absences", "correct_answer": None},
    {"question": "For school 6, select the month with the second highest absences", "correct_answer": None},
    {"question": "Identify the school with the highest absence in January", "correct_answer": None},
    {"question": "Identify the school with the lowest absence in March", "correct_answer": None},
    {"question": "Compare schools 1 and 2 in January for higher absences", "correct_answer": None},
    {"question": "Compare school 3 and 8 in June, which of them had lower absences", "correct_answer": None},
    {"question": "For school 8, select the month with the fourth highest absences", "correct_answer": None},
    {"question": "Identify the sixth highest absences in the month of August", "correct_answer": None},
    {"question": "Compare school 9 and 10 in April, which of them had a lower absences", "correct_answer": None},
    {"question": "Identify the school with the lowest absence in November", "correct_answer": None},
]

trial_questions = random.sample(questions, num_trials)

# Data generation functions
def generate_heatmap_data():
    data = np.random.randint(0, 151, size=(num_schools, num_months))
    answers = { "For school 5, select the month with the highest absences": np.argmax(data[4, :]),
                "For school 6, select the month with the second highest absences": np.argsort(data[5, :])[-2],
                "Identify the school with the highest absence in January": (np.argmax(data[:, 0]), 0),
                "Identify the school with the lowest absence in March": (np.argmin(data[:, 2]), 2),
                "Compare schools 1 and 2 in January for higher absences": "School 1" if data[0, 0] > data[1, 0] else "School 2",
                "Compare school 3 and 8 in June, which of them had lower absences": "School 3" if data[2, 5] < data[7, 5] else "School 8",
                "For school 8, select the month with the fourth highest absences": np.argsort(data[7, :])[-4],
                "Identify the sixth highest absences in the month of August": np.argsort(data[:, 7])[-6],
                "Compare school 9 and 10 in April, which of them had a lower absences": "School 9" if data[8, 3] < data[9, 3] else "School 10",
                "Identify the school with the lowest absence in November": (np.argmin(data[:, 10]), 10),
    }

    return data, answers

def generate_scatter_data():
    x = np.arange(1, num_months + 1)
    y_data = np.random.randint(0, 250, size=(num_schools, num_months))

    answers = {"For school 5, select the month with the highest absences": np.argmax(y_data[4, :]) + 1,
               "For school 6, select the month with the second highest absences": np.argsort(y_data[5, :])[-2] + 1,
               "Identify the school with the highest absence in January": (np.argmax(y_data[:, 0]), 1),
               "Identify the school with the lowest absence in March": (np.argmin(y_data[:, 2]), 3),
               "Compare schools 1 and 2 in January for higher absences": "School 1" if y_data[0, 0] > y_data[1, 0] else "School 2",
               "Compare school 3 and 8 in June, which of them had lower absences": "School 3" if y_data[2, 5] < y_data[7, 5] else "School 8",
               "For school 8, select the month with the fourth highest absences": np.argsort(y_data[7, :])[-4] + 1,
               "Identify the sixth highest absences in the month of August": np.argsort(y_data[:, 7])[-6] + 1,
               "Compare school 9 and 10 in April, which of them had a lower absences": "School 9" if y_data[8, 3] < y_data[9, 3] else "School 10",
               "Identify the school with the lowest absence in November": (np.argmin(y_data[:, 10]), 11),
               }
    return x, y_data, answers

# Homepage to select trial type
def show_homepage():
    plt.clf()
    plt.text(0.5, 0.6, "Select Chart Type for the Test", ha="center", va="center", fontsize=24, color='blue')
    plt.text(0.3, 0.4, "Heatmap", ha="center", va="center", fontsize=20, color='green')
    plt.text(0.7, 0.4, "Scatterplot", ha="center", va="center", fontsize=20, color='purple')
    plt.text(0.5, 0.2, "Click to Choose", ha="center", va="center", fontsize=16, color='grey')
    plt.axis("off")

    ax = plt.gca()
    heatmap_box = patches.Rectangle((0.15, 0.35), 0.3, 0.1, linewidth=2, edgecolor='green', facecolor='none')
    scatterplot_box = patches.Rectangle((0.52, 0.35), 0.35, 0.1, linewidth=2, edgecolor='purple', facecolor='none')
    ax.add_patch(heatmap_box)
    ax.add_patch(scatterplot_box)

    plt.draw()

def on_homepage_click(event):
    global selected_chart_type, begin_cid

    # Detect clicks on heatmap or scatterplot
    if event.xdata and event.ydata:
        if 0.2 < event.xdata < 0.4 and 0.35 < event.ydata < 0.45:
            selected_chart_type = "heatmap"
        elif 0.6 < event.xdata < 0.8 and 0.35 < event.ydata < 0.45:
            selected_chart_type = "scatterplot"

        if selected_chart_type:
            fig.canvas.mpl_disconnect(begin_cid)
            start_experiment()  # Start trials for the selected chart type

# Start experiment based on chart selection
def start_experiment():
    show_ready_screen()

# Ready screen between trials
def show_ready_screen():
    plt.clf()
    plt.text(0.5, 0.5, "Ready", ha="center", va="center", fontsize=24, color='blue')
    plt.axis("off")
    plt.pause(1)
    show_next_trial()

# Display the next trial
def show_next_trial():
    global trial_index, current_question

    if trial_index < num_trials:
        current_question = trial_questions[trial_index]

        # Set the current question text and reset the correct answer
        current_question["question"] = current_question["question"]
        current_question["correct_answer"] = None  # This will be set in the trial function


        # Display the question
        plt.clf()
        plt.text(0.5, 0.5, current_question["question"], ha="center", va="center", fontsize=16, wrap=True)
        plt.axis("off")
        plt.pause(2)

        if selected_chart_type == "heatmap":
            start_heatmap_trial()
        elif selected_chart_type == "scatterplot":
            start_scatter_trial()
    else:
        plt.close()

# Heatmap trial
def start_heatmap_trial():
    global trial_index, start_time, trial_cid, current_question

    trial_types.append("heatmap")

    plt.clf()
    data, answers = generate_heatmap_data()
    current_question["correct_answer"] = answers.get(current_question["question"])

    ax = plt.gca()
    cax = ax.matshow(data, cmap=cud_cmap)
    plt.colorbar(cax)
    ax.set_xticks(np.arange(num_months))
    ax.set_xticklabels(month_names, rotation=90)
    ax.set_yticks(np.arange(num_schools))
    ax.set_yticklabels([f"School {i+1}" for i in range(num_schools)])
    ax.set_title(current_question["question"])

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
            is_correct = (row == correct_answer[0] and col == correct_answer[1])
        elif "Identify the school with the lowest absence in March" in question_text:
            is_correct = (row == correct_answer[0] and col == correct_answer[1])
        elif "Compare schools 1 and 2 in January for higher absences" in question_text:
            is_correct = (col == 0 and (row == 0 or row == 1))
        elif "Compare school 3 and 8 in June, which of them had lower absences" in question_text:
            is_correct = (col == 5 and (row == 2 or row == 7))
        elif "For school 8, select the month with the fourth highest absences" in question_text:
            is_correct = (row == 7 and col == correct_answer)
        elif "Identify the sixth highest absences in the month of August" in question_text:
            is_correct = (col == 7 and row == correct_answer)
        elif "Compare school 9 and 10 in April, which of them had a lower absences" in question_text:
            is_correct = (col == 3 and (row == 8 or row == 9))
        elif "Identify the school with the lowest absence in November" in question_text:
            is_correct = (row == correct_answer[0] and col == correct_answer[1])

        # Record response time and correctness
        response_time = time.time() - start_time
        response_times.append(response_time)
        results.append(is_correct)

        # Move to the next trial
        fig.canvas.mpl_disconnect(trial_cid)
        trial_index += 1
        show_ready_screen()

# Scatterplot trial
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
        scatter = ax.scatter(x, y, color=matplotlib_colors[i], label=f'School {i + 1}', s=point_size)
        scatter_points.append((x, y))
    
    ax.set_title(question_text)
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

        # Handle each question type
        if "For school 5, select the month with the highest absences" in question_text:
            correct_x = correct_answer
            correct_y = y_data[4, correct_x - 1]
            is_correct = (abs(x_clicked - correct_x) <= correct_x_tolerance and
                          abs(y_clicked - correct_y) <= correct_y_tolerance)
        elif "For school 6, select the month with the second highest absences" in question_text:
            correct_x = correct_answer
            correct_y = y_data[5, correct_x - 1]
            is_correct = (abs(x_clicked - correct_x) <= correct_x_tolerance and abs(y_clicked - correct_y) <= correct_y_tolerance)
        elif "Identify the school with the highest absence in January" in question_text:
            school_index = correct_answer[0]
            correct_x = 1 # January corresponds to x = 1
            correct_y = y_data[school_index, 0]
            is_correct = (abs(x_clicked - correct_x) <= correct_x_tolerance and abs(y_clicked - correct_y) <= correct_y_tolerance)
        elif "Identify the school with the lowest absence in March" in question_text:
            school_index = correct_answer[0]
            correct_x = 3 # March corresponds to x = 3
            correct_y = y_data[school_index, correct_x - 1]
            is_correct = (abs(x_clicked - correct_x) <= correct_x_tolerance and abs(y_clicked - correct_y) <= correct_y_tolerance)
        elif "Compare schools 1 and 2 in January for higher absences" in question_text:
            correct_x = 1 # January
            if (abs(x_clicked - correct_x) <= correct_x_tolerance and
                    (abs(y_clicked - y_data[0, 0]) <= correct_y_tolerance or abs(y_clicked - y_data[1, 0]) <= correct_y_tolerance)):
                correct_school = "School 1" if y_data[0, 0] > y_data[1, 0] else "School 2"
                is_correct = (correct_answer == correct_school)
        elif "Compare school 3 and 8 in June, which of them had lower absences" in question_text:
            correct_x = 6 # June
            if (abs(x_clicked - correct_x) <= correct_x_tolerance and
                    (abs(y_clicked - y_data[2, 5]) <= correct_y_tolerance or abs(y_clicked - y_data[7, 5]) <= correct_y_tolerance)):
                correct_school = "School 3" if y_data[2, 5] < y_data[7, 5] else "School 8"
                is_correct = (correct_answer == correct_school)
        elif "For school 8, select the month with the fourth highest absences" in question_text:
            correct_x = correct_answer
            correct_y = y_data[7, correct_x - 1]
            is_correct = (abs(x_clicked - correct_x) <= correct_x_tolerance and abs(y_clicked - correct_y) <= correct_y_tolerance)
        elif "Identify the sixth highest absences in the month of August" in question_text:
            correct_x = 8 # August
            correct_y = y_data[:, correct_x - 1][correct_answer - 1]
            is_correct = (abs(x_clicked - correct_x) <= correct_x_tolerance and abs(y_clicked - correct_y) <= correct_y_tolerance)
        elif "Compare school 9 and 10 in April, which of them had a lower absences" in question_text:
            correct_x = 4 # April
            if (abs(x_clicked - correct_x) <= correct_x_tolerance and
                    (abs(y_clicked - y_data[8, 3]) <= correct_y_tolerance or
                     abs(y_clicked - y_data[9, 3]) <= correct_y_tolerance)):
                correct_school = "School 9" if y_data[8, 3] < y_data[9, 3] else "School 10"
                is_correct = (correct_answer == correct_school)
        elif "Identify the school with the lowest absence in November" in question_text:
            school_index = correct_answer[0]
            correct_x = 11 # November
            correct_y = y_data[school_index, correct_x - 1]
            is_correct = (abs(x_clicked - correct_x) <= correct_x_tolerance and abs(y_clicked - correct_y) <= correct_y_tolerance)

        # Record response time and correctness
        response_time = time.time() - start_time
        response_times.append(response_time)
        results.append(is_correct)

        # Move to the next trial
        fig.canvas.mpl_disconnect(trial_cid)
        trial_index += 1
        show_ready_screen()


def print_results():
    print("\nExperiment Complete. Results:")
    for i, (response_time, is_correct, trial_type) in enumerate(zip(response_times, results, trial_types), 1):
        status = "Correct" if is_correct else "Wrong"
        print(f"Trial {i} ({trial_type}): Response Time: {response_time:.2f} seconds - {status}")


# Initial UI setup
fig, ax = plt.subplots()
begin_cid = fig.canvas.mpl_connect('button_press_event', on_homepage_click)
show_homepage()
plt.show()

print_results()
