import matplotlib.pyplot as plt
import numpy as np

num_schools = 10
num_months = 12
absences_data = np.random.randint(0, 501, size=(num_schools, num_months))

def show_heatmap(data):
    fig, ax = plt.subplots()
    im = ax.imshow(data)

    for i in range(num_schools):
        for j in range(num_months):
            text = ax.text(j,i, data[i, j], ha="center", va="center", color="w")

    fig.tight_layout()
    plt.show()


show_heatmap(absences_data)



