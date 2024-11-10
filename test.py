import matplotlib.pyplot as plt
import numpy as np
import time

# Setting all the Parameters
num_trials = 5
trial_index = 0 # starts at 0, up till num_trials 
start_time = None
response_times = []
trial_cid = None  # this is for connecting events

def generate_random_data():
    return np.random.randint(0, 50, size=(5, 12))  # this is randomised, i want set questions

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
    start_trial()

# the loop for actual trials
def start_trial():
    global trial_index, start_time, trial_cid

    if trial_index < num_trials:
        # Generate and display heatmap data
        data = generate_random_data()
        plt.clf()
        ax = plt.gca()
        cax = ax.matshow(data, cmap="viridis")
        plt.colorbar(cax)
        
        # setting labels
        ax.set_xticks(np.arange(12))
        ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], rotation=90)
        ax.set_yticks(np.arange(5))
        ax.set_yticklabels(["Mon", "Tue", "Wed", "Thu", "Fri"])
        
        # Title for each trial
        ax.set_title(f"Trial {trial_index + 1}")
        
        # Timer and correct/incorrect
        start_time = time.time()
        trial_cid = fig.canvas.mpl_connect('button_press_event', on_click)
        plt.draw()
    else:
        plt.close()

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
