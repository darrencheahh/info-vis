import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import time

matplotlib.use('TkAgg')

# Setting all the Parameters
num_trials = 5
trial_index = 0 # starts at 0, up till num_trials 
start_time = None
response_times = []
trial_cid = None  # this is for connecting events
current_experiment = "heatmap"

num_schools = 10
num_days = 5
num_months = 12
# absences_data = np.random.randint(0, 151, size=(num_days, num_months))

def generate_heatmap_data(trial_index):
    return np.random.randint(0, 151, size=(num_schools, num_months))

def generate_scatter_data(trial_index):
    y = np.random.randint(0, 151, size=num_months)
    x = np.arange(1, num_months + 1)
    return x, y

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

    if current_experiment == "heatmap":
        start_heatmap_trial()
    else:
        start_scatter_trial()

def start_heatmap_trial():
    global trial_index, start_time, trial_cid

    if trial_index < num_trials:
        # Generate and display heatmap data
        data = generate_heatmap_data(trial_index)
        plt.clf()
        ax = plt.gca()
        cax = ax.matshow(data, cmap="viridis")
        plt.colorbar(cax)

        # setting labels
        ax.set_xticks(np.arange(num_months))
        ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], rotation=90)
        ax.set_yticks(np.arange(num_schools))
        ax.set_yticklabels(["School 1", "School 2", "School 3", "School 4", "School 5", "School 6", "School 7", "School 8", "School 9", "School 10"])

        # Title for each trial
        ax.set_title(f"Heatmap Trial {trial_index + 1}")

        # Timer and correct/incorrect
        start_time = time.time()
        trial_cid = fig.canvas.mpl_connect('button_press_event', on_click)
        plt.draw()
    else:
        switch_to_scatter_trials()

# the click function
def on_click(event):
    global trial_index, start_time, trial_cid
    
    if event.inaxes:  # need to modify this because its designed for heatmap
        response_time = time.time() - start_time
        response_times.append(response_time)
        
        # on to next trial
        trial_index += 1
        fig.canvas.mpl_disconnect(trial_cid)  
        show_ready_screen()  # flash ready screen

# Function to switch to scatterplot trials
def switch_to_scatter_trials():
    global trial_index, current_experiment
    trial_index = 0  # reset trial index
    current_experiment = "scatter"  # update experiment type
    show_ready_screen()


def start_scatter_trial():
    global trial_index, start_time, trial_cid

    if trial_index < num_trials:
        # Generate and display scatterplot data
        x, y = generate_scatter_data(trial_index)
        plt.clf()
        ax = plt.gca()
        scatter = ax.scatter(x, y, c=y, cmap='viridis')
        plt.colorbar(scatter)

        # Title for each trial
        ax.set_title(f"Scatter Trial {trial_index + 1}")
        ax.set_xlabel("Month")
        ax.set_ylabel("Absences")

        # Timer
        start_time = time.time()
        trial_cid = fig.canvas.mpl_connect('button_press_event', on_click)
        plt.draw()
    else:
        plt.close()

# this is so its all within 1 ui window
fig, ax = plt.subplots()
ax.text(0.5, 0.5, 'Click to Begin Test', ha='center', va='center', fontsize=20)
ax.axis("off")
begin_cid = fig.canvas.mpl_connect('button_press_event', start_experiment) 
plt.show()

# Print results
print("Experiment Complete. Results:")
for i, response_time in enumerate(response_times, 1):
    print(f"Trial {i}: Response Time: {response_time:.2f} seconds")
