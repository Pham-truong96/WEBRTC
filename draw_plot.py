import matplotlib.pyplot as plt
import json

from kpi import KPIresolution, KPIfps
# %matplotlib inline
# plt.gca().set_color_cycle(['red', 'green', 'blue', 'yellow'])


DUMS = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 79]
COLOR = ["green", "blue", "red", "black", "yellow", "brown", "orange", "pink"]
# bandwidths = [0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 1, 2, ]

bandwidths = [ 1, 2, 3, 4, 5, 15, 30, 50]

def _average(data=[]):
    cnt = 0
    Sum = 0
    # print(len(data))
    for i in data:
        cnt +=1
        Sum += i
    return Sum/cnt


def data_dum(data=[]):
    res = []
    # print(len(data))
    for i in DUMS:
        # if data[i] > 60:
        #     data[i] = 60
        res.append(data[i] /1)
    return res


def draw(data=[], title="", keyword="", ylabel="fps"):
    index = 0
    print(DUMS)

    for i in bandwidths:
        print(data_dum(data["bw_{}".format(i)]["average"][keyword]))
        plt.plot(
            DUMS,
            data_dum(data["bw_{}".format(i)]["average"][keyword]),
            'o-',
            color=COLOR[index],
            label='{} mbit'.format(i)
        )
        index += 1

    plt.title(title)
    plt.xlabel('second')
    plt.ylabel(ylabel)
    plt.legend(loc='best')
    plt.grid()
    plt.savefig("{}.png".format(keyword))


def draw_send_received(data=[], title="", 
        keyword1="googFrameWidthSent", keyword2="googFrameWidthReceived", ylabel="pixel"):
    index = 0

    plt.plot(
        DUMS,
        data_dum(data["bw_{}".format(0.25)]["average"][keyword1]),
        'o-',
        color=COLOR[0],
        label=keyword1
    )

    plt.plot(
        DUMS,
        data_dum(data["bw_{}".format(0.25)]["average"][keyword2]),
        'o-',
        color=COLOR[2],
        label=keyword2
    )
    print(data_dum(data["bw_{}".format(0.25)]["average"][keyword1]))
    print(data_dum(data["bw_{}".format(0.25)]["average"][keyword2]))
    plt.title(title)
    plt.xlabel('second')
    plt.ylabel(ylabel)
    plt.legend(loc='best')
    plt.grid()
    plt.savefig("sendreceid.png")


def draw_percen_max_time(data=[]):
    index = 0
    percen = []
    for i in bandwidths:
        percen.append(data["bw_{}".format(i)]["percen_max_time"])

    print(percen)
    plt.plot(
        bandwidths,
        percen,
    )
    
    plt.title("Phần trăm hời gian đạt chất lượng video cao nhât")
    plt.xlabel('băng thông')
    plt.ylabel("phân trăm")
    plt.legend(loc='best')
    plt.grid()
    plt.savefig("phantram.png")


def draw_average_time(data=[],title="", keyword="", ylabel="fps"):
    index = 0
    kpi = []
    for i in bandwidths:
        kpi.append(KPIresolution(data["bw_{}".format(i)]["percen_max_time"]))

    plt.plot(
        bandwidths,
        kpi,
    )
    
    plt.title("KPI")
    plt.xlabel('băng thông')
    plt.ylabel("fps")
    plt.legend(loc='best')
    plt.grid()
    plt.savefig("KPIresolution.png")

def draw_kpi_fps(data=[],title="", ylabel="fps"):
    index = 0
    kpi = []
    for i in bandwidths:
        kpi.append(KPIfps(_average(data_dum(data["bw_{}".format(i)]["average"]["googFrameRateReceived"]))))

    plt.plot(
        bandwidths,
        kpi,
    )
    
    plt.title("KPI")
    plt.xlabel('băng thông')
    plt.ylabel("KPI")
    plt.legend(loc='best')
    plt.grid()
    plt.savefig("KPIfps.png")

json_file = open("data.json")
json_data = json.load(json_file)

# draw(data=json_data, title="Tốc độ khung hinh theo thời gian", keyword="googFrameRateReceived", ylabel="fps")
# draw(data=json_data, title="Độ phân giải khung hinh theo thời gian", keyword="googFrameWidthReceived", ylabel="pixel")
# draw(data=json_data, title="Độ trễ trong phiên", keyword="googCurrentDelayMs", ylabel="ms")
# draw(data=json_data, title="", keyword="bitsReceivedPerSecond", ylabel="kbit/s")
# draw_average_time(data=json_data, title="Tốc độ khung hinh theo thời gian", keyword="googFrameRateReceived", ylabel="fps")
# draw_send_received(data=json_data, title="", keyword1="googFrameRateSent",keyword2="googFrameRateReceived", ylabel="fps")
draw_send_received(data=json_data, title="", keyword1="googFrameWidthSent",keyword2="googFrameWidthReceived", ylabel="pixel")

# draw_percen_max_time(json_data)

# draw_kpi_fps(json_data)