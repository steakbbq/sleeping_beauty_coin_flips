import random
import sys
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# set the style
plt.style.use('seaborn-v0_8-darkgrid')

# initialize variables
x_vals = []
tails_vals = []
heads_vals = []
random_vals = []
tails_wins = 0
heads_wins = 0
random_wins = 0
number_of_flips = 0
index = 0


# define what happens each frame
def animate(i):
    # allow access to the global variables
    global tails_wins
    global heads_wins
    global random_wins
    global index

    # using count keep track of current x index
    x_vals.append(index)
    index += 1

    # first flip
    coin = flip_a_coin()  # 0 = tails, 1 = heads
    # count total number of flips for percentage
    increase_number_of_flips()

    # tails came up
    if coin == 0:

        # add 1 to tails_wins
        tails_won()

        #  check if random strategy won and add 1 to random_wins
        calculate_random(coin)

        # since tails came up flip a coin on tuesday
        tuesday_coin = flip_a_coin()

        # count another total flip for tuesday
        increase_number_of_flips()

        # if tuesday is tails, add 1 to tails_wins
        if tuesday_coin == 0:
            tails_wins = 1 + tails_wins  # extra win

            # if random strategy won update random_wins
            update_random(tuesday_coin)
        else:

            # even though heads came up on tuesday, random could still get a win
            update_random(tuesday_coin)

    # heads came up
    elif coin == 1:

        # add 1 to heads_wins
        heads_won()

        # check if random strategy won and add 1 to random_wins
        calculate_random(coin)

    # clear plot axis
    plt.cla()

    # plot the data
    plt.plot(x_vals, tails_vals, label="Tails Strategy ({})".format(calculate_percentage(tails_wins, number_of_flips)))
    plt.plot(x_vals, heads_vals, label="Heads Strategy ({})".format(calculate_percentage(heads_wins, number_of_flips)))
    plt.plot(x_vals, random_vals,
             label="Random Strategy ({})".format(calculate_percentage(random_wins, number_of_flips)))

    # show the legend
    plt.legend()
    # use tight layout
    plt.tight_layout()


def calculate_percentage(part, whole):
    percentage = 100 * float(part) / float(whole)
    return str(int(percentage)) + '%'


def increase_number_of_flips():
    global number_of_flips
    number_of_flips = number_of_flips + 1


def update_random(coin):
    coin_random = flip_a_coin()
    if coin_random == coin:
        random_vals[-1] = random_vals[-1] + 1


def calculate_random(coin):
    coin_random = flip_a_coin()
    if coin_random == coin:
        random_won()
    else:
        random_lost()


def flip_a_coin():
    return random.SystemRandom().randint(0, 1)


def tails_won():
    global tails_wins
    tails_wins = 1 + tails_wins
    tails_vals.append(tails_wins)
    heads_vals.append(heads_wins)


def heads_won():
    global heads_wins
    heads_wins = 1 + heads_wins
    heads_vals.append(heads_wins)
    tails_vals.append(tails_wins)


def random_won():
    global random_wins
    random_wins = 1 + random_wins
    random_vals.append(random_wins)


def random_lost():
    random_vals.append(random_wins)


def on_close(event):
    # close the program
    sys.exit(0)


# call Functional Animation
ani = FuncAnimation(plt.gcf(), animate, interval=100)

# get the current figure
fig = plt.gcf()
fig.canvas.manager.set_window_title('Coin Flip')
# listen for close event on current figure and call on_close function
fig.canvas.mpl_connect('close_event', on_close)

plt.show()
