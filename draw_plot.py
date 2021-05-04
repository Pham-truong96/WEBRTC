import matplotlib.pyplot as plt
# %matplotlib inline
# plt.gca().set_color_cycle(['red', 'green', 'blue', 'yellow'])


DUMS = [0, 5, 10, 15, 20,]# 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80]
COLOR = ["green", "blue", "red", "black", "yellow", "brown", "orange", "pink"]
bandwidths = [0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 1, 2, 3, 4, 5, 15, 30, 50]


def data_dum(data=[]):
    res = []
    for i in DUMS:
        res.append(DUMS[i])
    return res


def draw(data=[], title="", keyword="", ylabel="fps"):
    index = 0
    for i in bandwidths:
        plt.plot(
            DUMS,
            data_dum(data["bw_{}".format(i)]]["average"][keyword]),
            'o-',
            color=COLOR[index],
            label='{} mbit'.format(i)
        )
        index += 1

    plt.title(title)
    plt.xlabel('time')
    plt.ylabel(ylabel)
    plt.legend(loc='best')
    plt.grid()
    plt.savefig("{}.png".format(keyword))


def draw_percen_max_time(data=[]):
    index = 0
    percen = []
    for i in bandwidths:
        percen.append(data["bw_{}".format(i)]]["percen_max_time"])

    plt.plot(
        percen,
        bandwidths,
        'o-',
        color="green",
    )
    
    plt.title("Phần trăm hời gian đạt chất lượng video cao nhât")
    plt.xlabel('băng thông')
    plt.ylabel("phân trăm")
    plt.legend(loc='best')
    plt.grid()
    plt.savefig("phantram.png")

json_file = open("data.json")
json_data = json.load(json_file)

draw(data=json_data, json_data="Tốc độ khung hinh theo thời gian", keyword="googFrameRateReceived", ylabel="fps")
draw(data=json_data, json_data="Độ phân giải khung hinh theo thời gian", keyword="googFrameWidthReceived", ylabel="fps")
draw(data=json_data, json_data="Độ trễ trong phiên", keyword="googCurrentDelayMs", ylabel="fps")
draw(data=json_data, json_data="Tốc độ bit theo thời gian", keyword="bitsReceivedPerSecond", ylabel="fps")

draw_percen_max_time(data)
