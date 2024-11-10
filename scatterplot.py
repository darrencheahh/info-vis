import matplotlib.pyplot as plt
import numpy as np
import time


num_charts = 10
num_months = 12
response_times = []
fig, ax = plt.subplots()
start_time = 0
current_chart = 0
month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def generate_random_data():
    x = np.arange(1, num_months + 1)
    y = np.random.randint(0, 250, num_months)
    return x, y


def generate_scatterplot(x, y):
    ax.clear()
    scatter = ax.scatter(x, y)
    ax.set_title('School Absences by Month')
    ax.set_xlabel('Month')
    ax.set_ylabel('Number of Students Absent')
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 275)
    ax.set_xticks(np.arange(1, 13))
    ax.set_xticklabels(month_names)
    ax.set_yticks(np.arange(0, 251, 50))
    return scatter


def on_click(event):
    global current_chart, start_time, scatter, x, y
    if current_chart < num_charts:
        contains, _ = scatter.contains(event)

        if contains:
            end_time = time.time()
            response_times.append(end_time - start_time)

            mouse_y = event.ydata
            y_value_clicked = mouse_y

            max_absences = np.max(y)  # the outlier is the highest absences value

            tolerance = 2
            if  abs(y_value_clicked - max_absences) <= tolerance:
                print(f"Chart {current_chart + 1}: Correct, Response time: {response_times[-1]:.2f} seconds")
            else:
                print(f"Chart {current_chart + 1}: Incorrect, Response time: {response_times[-1]:.2f} seconds")

            current_chart += 1

            x, y = generate_random_data()
            scatter = generate_scatterplot(x, y)

            start_time = time.time()

            plt.draw()
            time.sleep(1)  # 1 second pause before next chart

            if current_chart == num_charts:
                plt.close()


def run_test():
    global start_time, scatter, x, y
    start_time = time.time()
    
    x, y = generate_random_data()
    scatter = generate_scatterplot(x, y)

    fig.canvas.mpl_connect('button_press_event', on_click)

    plt.show()


run_test()