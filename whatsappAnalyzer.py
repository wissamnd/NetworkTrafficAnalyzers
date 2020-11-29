import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv("data/whatsappCall.csv", sep=",", encoding="ISO-8859-1")
ListOfTimeStamps = data.Time.values
ListOfProtocols = data.Protocol.values
ListOfInfos = data.Info.values

TCPpackets = list(map(lambda  p: 1 if "TCP" in p else 0, ListOfProtocols))
UDPpackets = list(map(lambda  p: 1 if "UDP" in p or "STUN" in p or "DNS" in p  else 0, ListOfProtocols))


def detectWhenCallsWereEnded():
    timestamps = []
    UnknownRequestInfoPackets = list(map(lambda  i: 1 if "Unknown Request" in i else 0, ListOfInfos))
    count = 0
    for i in range(len(UnknownRequestInfoPackets)):
        if UnknownRequestInfoPackets[i] == 1 and ListOfProtocols[i] == "STUN":
            count += 1
            if count == 5:
                timestamps.append(ListOfTimeStamps[i-4])
        else:
            count = 0
    return timestamps
def detectWhenCallsWereAnswered():
    timestamps = []
    SuccessRequestInfoPackets = list(map(lambda  i: 1 if "Allocate Success Response" in i else 0, ListOfInfos))
    count = 0
    for i in range(len(SuccessRequestInfoPackets)):
        if SuccessRequestInfoPackets[i] == 1 and ListOfProtocols[i] == "STUN" :
            count += 1
            if count == 10 and ListOfProtocols[i+1] == "UDP":
                timestamps.append(ListOfTimeStamps[i-4])
        else:
            count = 0
    return timestamps

StartOfCallTimeStamps = detectWhenCallsWereAnswered()
EndOfCallTimeStamps = detectWhenCallsWereEnded()    
for i in range(len(StartOfCallTimeStamps)):
    print("A call started after %.2f seconds and lasted for %.2f seconds"%(StartOfCallTimeStamps[i],EndOfCallTimeStamps[i] -StartOfCallTimeStamps[i]))
def countNumberOfPackets(packets,timestamps, cap):
    returnedpackets = []
    returnedtimestamps = []
    count = 0
    time = 0
    timePrev = 0
    for i in range(timestamps.size):
        time = float(timestamps[i])
        protocol = packets[i]
        if((time - timePrev) >= 0.1):
            if(count > cap):
                count = cap
            returnedpackets.append(count)
            returnedtimestamps.append(time)
            count = 0
        if(protocol):
            count += 1
        timePrev = time
    returnedpackets.append(count)
    returnedtimestamps.append(time)   
    return returnedpackets, returnedtimestamps
#ip.dst_host contains "whatsapp" || ip.dst_host contains "facebook" ||ip.src_host contains "whatsapp" || ip.src_host contains "facebook"
TCPpackets,timestamps = countNumberOfPackets(TCPpackets,ListOfTimeStamps, 200)
UDPpackets, timestamps = countNumberOfPackets(UDPpackets,ListOfTimeStamps, max(TCPpackets) +40)
plt.plot(timestamps,TCPpackets, color ="blue", label ="TCP")
plt.plot(timestamps,UDPpackets,color ="pink", label ="UDP")

for t in StartOfCallTimeStamps:
    plt.plot(t,0,'go')
    plt.axvline(t, 0, 100, label='Start Of Call', color = "green", linewidth=2)

for t in EndOfCallTimeStamps:
    plt.plot(t,0,'ro')
    plt.axvline(t, 0, 100, label='End Of Call', color = "red", linewidth=2)



plt.ylabel('Number of packets')
plt.xlabel('Time in seconds')
plt.legend(loc="upper left")
plt.title('Packets recorded during a VoIP call')
plt.margins(0,0.05,tight =True)
plt.xticks(np.arange(0, int(timestamps[len(timestamps)-1]),5))
plt.ylim(bottom=0)


plt.show()