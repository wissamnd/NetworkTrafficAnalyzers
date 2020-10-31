import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def UsedProtocols(protocols):
    listOfProtocolNames = []
    for p in ListOfProtocols:
        if p not in listOfProtocolNames:
            listOfProtocolNames.append(p)
    return listOfProtocolNames

def plotPacketByProtocol(protocolName, lineColor, lineWidth, samplingRate,cap):
    protocolPackets = list(map(lambda p: 1 if protocolName in p else 0, ListOfProtocols))
    protocolPackets, timestamps = samplePackets(protocolPackets,ListOfTimeStamps,cap, samplingRate)
    plt.plot(timestamps, protocolPackets, color=lineColor, label=protocolName, linewidth=lineWidth)
    return timestamps


def samplePackets(packets,timestamps, cap, samplingRate):
    returnedPackets = []
    returnedTimeStamps = []
    count = 0
    time = 0
    timePrev = 0
    for i in range(timestamps.size):
        time = float(timestamps[i])
        protocol = packets[i]
        if (time - timePrev) >= samplingRate:
            if count > cap:
                count = cap
            returnedPackets.append(count)
            returnedTimeStamps.append(time)
            count = 0
        if protocol:
            count += 1
        timePrev = time
    returnedPackets.append(count)
    returnedTimeStamps.append(time)
    return returnedPackets, returnedTimeStamps

SAMPLING_RATE = 0.07
SAMPLING_CAP = 200

# reading csv file
data = pd.read_csv("data/zoomCall2.csv", sep=",", encoding="ISO-8859-1")

# extracting the Time, Protocol and Info column values
ListOfTimeStamps = data.Time.values
ListOfProtocols = data.Protocol.values
ListOfProtocolInformation = data.Info.values

# plotting packs
timestamps = plotPacketByProtocol(protocolName="TCP",lineColor="blue",lineWidth=1, cap=SAMPLING_CAP, samplingRate= SAMPLING_RATE)
plotPacketByProtocol(protocolName="UDP",lineColor="green",lineWidth=1, cap=SAMPLING_CAP, samplingRate= SAMPLING_RATE)
plotPacketByProtocol(protocolName="WireGuard",lineColor="red",lineWidth=1, cap=SAMPLING_CAP, samplingRate= SAMPLING_RATE)
plotPacketByProtocol(protocolName="DNS",lineColor="olive",lineWidth=1, cap=SAMPLING_CAP, samplingRate= SAMPLING_RATE)

# printing used protocols
print(UsedProtocols(ListOfProtocols))

plt.ylabel('Number of packets')
plt.xlabel('Time in seconds')
plt.legend(loc="upper right")
plt.title('Packets recorded during a VoIP call')
plt.margins(0,0.05,tight=True)
plt.xticks(np.arange(0, int(timestamps[len(timestamps)-1]), 5))
plt.ylim(bottom=0)
plt.show()
