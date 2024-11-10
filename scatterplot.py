import numpy as np
import matplotlib.pyplot as plt
import time

def generate_absence_data():
    months = np.arange(1, 13)           
    absences = np.random.randint(5,50, size=12)
    correct_month = np.argmax(absences) + 1
    return months, absences, correct_month

selected_month = None

def on_click(event, months, absences):
    global selected_month
    if event.inaxes:
        distances = [(month, abs - event.ydata) for month, abs in zip(months, absences)]
        closest_month, closest_distance = min(distances, key=lambda x: abs(x[1]))

        if abs(closest_distance) < 5:
            selected_month = closest_month
            plt.close()

def create_scatterplot(months, absences):
    global selected_month
    selected_month = None

    fig, ax = plt.subplots(figsize=(8,6))

    plt.scatter(months, absences, color='blue')
    plt.xlabel('Month')
    plt.ylabel('Number of Absences')
    plt.title('Pupil Absences over the School Year')
    plt.xticks(months,['Jan','Feb','Mar','Apr', 'May', 'Jun', 'Jul','Aug', 'Sep', 'Oct','Nov','Dec'])
    plt.ylim(0,60)

    cid = fig.canvas.mpl_connect('button_press_event', lambda event: on_click(event, months, absences))

    plt.show()

    fig.canvas.mpl_disconnect(cid)


def show_blank_screen(duration=1):
    fig, ax = plt.subplots(figsize=(8,6))
    ax.set_facecolor("white")  # Blank white screen
    ax.axis("off")  # Hide axes
    plt.pause(duration)  # Display the blank screen for the specified duration
    plt.close(fig)  # Close the blank screen figure

def trial():
    months, absences, correct_month = generate_absence_data()
    create_scatterplot(months, absences)
    
    is_correct = (selected_month == correct_month) 
    plt.close()
    show_blank_screen()
    response_time = time.time()
    return is_correct, response_time

def run_experiment(num_trials=10):
    result = []
    for _ in range(num_trials):
        is_correct, response_time = trial()
        result.append((is_correct, response_time))
    return result


result = run_experiment()
print("Experiment results: ", result)