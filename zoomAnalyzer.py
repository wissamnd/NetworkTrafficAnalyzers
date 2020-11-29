import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def UsedProtocols(protocols):
    listOfProtocolNames = []
    for p in ListOfProtocols:
        if p not in listOfProtocolNames:
            listOfProtocolNames.append(p)
    return listOfProtocolNames


#Client Key Exchange, Change Cipher Spec, Encrypted Handshake Message
def detectWhenTheMeetingWasStrated():
    timestamps = []
    SuccessRequestInfoPackets = list(map(lambda  i: 1 if "Client Key Exchange, Change Cipher Spec, Encrypted Handshake Message" in str(i) else 0, ListOfProtocolInformation))
    UDPPackets = list(map(lambda  p: 1 if "UDP" in p else 0, ListOfProtocols))
    for i in range(len(SuccessRequestInfoPackets)):
        if SuccessRequestInfoPackets[i] == 1:
            timestamps.append(ListOfTimeStamps[i-4])
    count = 0
    startTime = 0
    lastUDPPacketTimeStamp = 0
    for t in timestamps:
        if count == 0:
            plt.plot(t,0,'go')
            plt.axvline(t, 0, 100, label='Zoom Call Started', color = "red", linewidth=2)
            startTime = t
        
        count+=1
    count = 0
    for t in ListOfTimeStamps:
        if UDPPackets[count] == 0:
            if(lastUDPPacketTimeStamp == 0):
                lastUDPPacketTimeStamp = t
        elif UDPPackets[count] == 1:
            lastUDPPacketTimeStamp = 0
        count+=1
    print("Meeting Started at: "+ str(startTime)+" seconds")
    
    if(lastUDPPacketTimeStamp > 0):
        plt.axvline(lastUDPPacketTimeStamp, 0, 100, label='Zoom Call Ended', color = "cyan", linewidth=2)
        print("Meeting Ended at: "+ str(lastUDPPacketTimeStamp)+" seconds")
        print("The User entered the meeting for %.2f seconds"%((lastUDPPacketTimeStamp - startTime)))
    else:
        print("End of meeting not detected!")

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

SAMPLING_RATE = 0.02
SAMPLING_CAP = 1400
# reading csv file
data = pd.read_csv("data/zoomCall6.2.csv", sep=",", encoding="ISO-8859-1")

# extracting the Time, Protocol and Info column values
ListOfTimeStamps = data.Time.values
ListOfProtocols = data.Protocol.values
ListOfPacketsLengths = data.Length.values
ListOfProtocolInformation = data.Info.values


def plotGraphByNumberOfPacketsVersusTime(protocols, plotColors):

    # plotting packs
    for i in range(len(protocols)):
        protocolPackets = list(map(lambda p: 1 if protocols[i] in p else 0, ListOfProtocols))
        protocolPackets, timestamps = samplePackets(protocolPackets,ListOfTimeStamps,SAMPLING_CAP, SAMPLING_RATE)
        plt.plot(timestamps, protocolPackets, color=plotColors[i], label=protocols[i], linewidth=1)
    detectWhenTheMeetingWasStrated()
    plt.ylabel('Number of packets')
    plt.xlabel('Time in seconds')
    plt.legend(loc="upper right")
    plt.title('Traffic recorded during a Zoom call')
    plt.margins(0,0.05,tight=True)
    plt.xticks(np.arange(0, int(timestamps[len(timestamps)-1]), 15))
    plt.ylim(bottom=0)
    plt.show()

def plotGraphByLengthOfPacketsVersusTime(protocols, plotColors):
    # plotting packs
    for i in range(len(protocols)):
        plt.plot(ListOfTimeStamps, ListOfPacketsLengths, color=plotColors[i], label=protocols[i], linewidth=0.09)

    detectWhenTheMeetingWasStrated()
    plt.ylabel('Length of packets')
    plt.xlabel('Time in seconds')
    plt.legend(loc="upper right")
    plt.suptitle('Traffic recorded during a Zoom call')
    plt.margins(0,0.05,tight=True)
    plt.xticks(np.arange(0, int(ListOfTimeStamps[len(ListOfTimeStamps)-1]), 15))
    plt.ylim(bottom=0)
    
    plt.show()

# plot TCP and UDP packets

plotGraphByLengthOfPacketsVersusTime(protocols=["TCP","UDP"],plotColors=["blue","green"])
# plotGraphByNumberOfPacketsVersusTime(protocols=["TCP","UDP"],plotColors=["blue","green"])


# plot UDP Packets 

#plotGraphByLengthOfPacketsVersusTime(protocols=["UDP"],plotColors=["blue"])
# plotGraphByNumberOfPacketsVersusTime(protocols=["UDP"],plotColors=["blue"])
