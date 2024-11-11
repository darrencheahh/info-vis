import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import time
import random

matplotlib.use('TkAgg')

# Setting all the Parameters
num_trials = 6
heatmap_trials = 3
scatter_trials = 3
trial_index = 0 # starts at 0, up till num_trials 
start_time = None
response_times = []
results = []  # stores the results of each trial
trial_cid = None  # this is for connecting events
current_trial_type = None
point_size = 80
colors = plt.colormaps.get_cmap('tab10').colors

num_schools = 10
num_days = 5
num_months = 12
month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

trial_order = random.sample(["heatmap"] * heatmap_trials + ["scatter"] * scatter_trials, num_trials)

def generate_heatmap_data():
    return np.random.randint(0, 151, size=(num_schools, num_months))


def generate_scatter_data():
    x = np.arange(1, num_months + 1)
    y_data = [np.random.randint(0, 250, num_months) for _ in range(num_schools)]
    return x, y_data


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
    global trial_index, current_trial_type
    if trial_index < num_trials:
        current_trial_type = trial_order[trial_index]
        if current_trial_type == "heatmap":
            start_heatmap_trial()
        else:
            start_scatter_trial()
    else:
        plt.close()


def start_heatmap_trial():
    global trial_index, start_time, trial_cid
    plt.clf()
    data = generate_heatmap_data()
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
    global trial_index, start_time, trial_cid
    if event.inaxes and event.inaxes == plt.gca():
        row, col = int(event.ydata), int(event.xdata)
        
        # valid answer check
        if 0 <= row < num_schools and 0 <= col < num_months:
            response_time = time.time() - start_time
            response_times.append(response_time)
            fig.canvas.mpl_disconnect(trial_cid)
            trial_index += 1
            show_ready_screen()


def start_scatter_trial():
    global trial_index, start_time, trial_cid, y_data
    plt.clf()
    x, y_data = generate_scatter_data()
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
    trial_cid = fig.canvas.mpl_connect('button_press_event', lambda event: on_click_scatter(event, scatter_points))
    plt.draw()


def on_click_scatter(event, scatter_points):
    global trial_index, start_time, trial_cid
    if event.inaxes:
        x_clicked, y_clicked = event.xdata, event.ydata
        x_tolerance, y_tolerance = 0.5, 0.7

        # valid answer check
        for x_vals, y_vals in scatter_points:
            for x, y in zip(x_vals, y_vals):
                # Check both x and y tolerances
                if abs(x - x_clicked) <= x_tolerance and abs(y - y_clicked) <= y_tolerance:
                    response_time = time.time() - start_time
                    response_times.append(response_time)
                    fig.canvas.mpl_disconnect(trial_cid)
                    trial_index += 1
                    show_ready_screen()
                    return


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
