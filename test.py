import matplotlib.pyplot as plt
import numpy as np
import time

# Parameters
num_trials = 5
trial_index = 0
start_time = None
response_times = []
trial_cid = None  # Initialize trial_cid for managing event connections

def generate_random_data():
    """Generate random data for heatmap."""
    return np.random.randint(0, 50, size=(5, 12))  # Example data dimensions

def start_experiment(event):
    """Handle click on the 'Begin Test' screen to start trials."""
    fig.canvas.mpl_disconnect(begin_cid)  # Disconnect 'Begin Test' screen click event
    show_ready_screen()  # Start with a ready screen before the first trial

def show_ready_screen():
    """Display a 1-second ready screen between trials."""
    plt.clf()
    plt.text(0.5, 0.5, "Ready", ha="center", va="center", fontsize=24, color='blue')
    plt.axis("off")
    plt.pause(1)
    start_trial()

def start_trial():
    """Display a heatmap for each trial."""
    global trial_index, start_time, trial_cid

    if trial_index < num_trials:
        # Generate and display heatmap data
        data = generate_random_data()
        plt.clf()
        ax = plt.gca()
        cax = ax.matshow(data, cmap="viridis")
        plt.colorbar(cax)
        
        # Set labels
        ax.set_xticks(np.arange(12))
        ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], rotation=90)
        ax.set_yticks(np.arange(5))
        ax.set_yticklabels(["Mon", "Tue", "Wed", "Thu", "Fri"])
        
        # Title for each trial
        ax.set_title(f"Trial {trial_index + 1}")
        
        # Start timing and connect click event for answer selection
        start_time = time.time()
        trial_cid = fig.canvas.mpl_connect('button_press_event', on_click)
        plt.draw()
    else:
        plt.close()  # Close after all trials completed

def on_click(event):
    """Handle clicks on the heatmap to record responses."""
    global trial_index, start_time, trial_cid
    
    if event.inaxes:  # Ensure the click is within the plot area
        response_time = time.time() - start_time
        response_times.append(response_time)
        
        # Move to next trial
        trial_index += 1
        fig.canvas.mpl_disconnect(trial_cid)  # Disconnect trial click event
        show_ready_screen()  # Show ready screen before next trial

# Set up the figure and show the 'Begin Test' screen
fig, ax = plt.subplots()
ax.text(0.5, 0.5, 'Click to Begin Test', ha='center', va='center', fontsize=20)
ax.axis("off")
begin_cid = fig.canvas.mpl_connect('button_press_event', start_experiment)  # Connect start event to 'Begin Test' screen
plt.show()

# Print results after experiment
print("Experiment Complete. Results:")
for i, response_time in enumerate(response_times, 1):
    print(f"Trial {i}: Response Time: {response_time:.2f} seconds")
