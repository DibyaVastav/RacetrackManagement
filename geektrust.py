from datetime import time
from sys import argv

timeslots =[]
bookedvehicles={}
viptimeslots = []
bookingcostsreg=[]
bookingcostsvip=[]
addcostsreg=[]
addcostsvip=[]


def getcost(veh_type, track_type):
    if track_type == "reg":
        if veh_type == "CAR":
            cost = 120 * 3
            return (cost)
        elif veh_type == "SUV":
            cost= 200 * 3
            return (cost)
        elif veh_type == "BIKE":
            cost = 60 * 3
            return (cost)
    else:
        if veh_type == "CAR":
            cost = 250 * 3
            return (cost)
        elif veh_type == "SUV":
            cost= 300 * 3
            return (cost)

def getcostadd (time1, time2):

    timemin1 = time1.hour * 60 + time1.minute
    timemin2 = time2.hour * 60 + time2.minute
    timediff = timemin2 - timemin1
    
    g = timediff//60
    if (timediff< 15):
        cost = 0
    elif (15 < timediff < 60):
        cost = 50
    elif timediff/60 > timediff//60:
        cost= ((g+1) * 50)
        
    else:
        cost = (g * 50)

    return cost


def bookingregtrack(req_time, endtime, veh_type, reg_no, req_type):
    time1 = req_time
    time2 = endtime
    s=(time1, time2)
    timeslots.append(s)
    bookdict = {reg_no : s}
    bookedvehicles.update(bookdict)
    if req_type == "BOOK":
        bookingcostsreg.append(getcost(veh_type, "reg"))
    else:
        addcostsreg.append(getcostadd(time1, time2))
    return ("SUCCESS")

def bookingviptrack(req_time, endtime, veh_type, reg_no, req_type):
    time1 = req_time
    time2 = endtime
    s=(time1, time2)
    viptimeslots.append(s)
    bookdict = {reg_no : s}
    bookedvehicles.update(bookdict)
    if req_type == "BOOK":
        bookingcostsvip.append(getcost(veh_type, "vip"))
    else:
        addcostsvip.append(getcostadd(time1, time2))
    return ("SUCCESS")


def timeavailability(req_time, endtime, req1):
    count = 0
    temp1 = []
    for y,x in enumerate(timeslots):
        if x[0] < req_time < x[1]:
            count+=1
            temp1.append(y)
        elif x[0] < endtime < x[1]:
            if y not in temp1:
                count += 1
                temp1.append(y)
        else:
            return(bookingregtrack(req_time, endtime, req1['veh_type'], req1['reg_no'], req1['req_type']))
            
        
    if count<2 and (req1['veh_type'] in ("CAR", "SUV")):
        return(bookingregtrack(req_time, endtime, req1['veh_type'], req1['reg_no'], req1['req_type']))

    elif (count<4 and req1['veh_type']=="BIKE"):
        return(bookingregtrack(req_time, endtime, req1['veh_type'], req1['reg_no'], req1['req_type']))

    elif count==2 and (req1['veh_type'] in ("CAR", "SUV")):
        for m in viptimeslots:
            if m[0] < req_time < m[1] or m[0] < req_time <m[1]:
                return ("RACETRACK_FULL")
        return(bookingviptrack(req_time, endtime, req1['veh_type'], req1['reg_no'], req1['req_type']))

    else:
        return ("RACETRACK_FULL")



def booking(booking_requests):
    booking_output=[]
    x=0
    while (x < len(booking_requests)):
        req1= booking_requests[x]
        z= req1['time_req'].split(":")
        req_time=time(hour= int (z[0]), minute= int (z[1]))
        endtime = time(req_time.hour+3, req_time.minute)
        if req_time < time(13,00) or req_time > time(17, 00):
            booking_output.append("INVALID_ENTRY_TIME")
        elif req1['reg_no'] in bookedvehicles:
            booking_output.append("Vehicle already has a racetrack booked, ask for additional time")
        else:
            booking_output.append(timeavailability(req_time, endtime, req1))

        x+=1    
    return booking_output

def booking_add(additional_requests):
    additional_output =[]
    #if len(additional_requests)==0:
        #return (additional_output)
    x = 0
    while (x< len(additional_requests)):
        req2= additional_requests[x]
        if req2['reg_no'] in bookedvehicles:
            z = req2['exit_time'].split(":")
            exit_timereq = time (hour = int(z[0]), minute = int(z[1]))
            m = req2['end_time'].split(":")
            endtime = time (hour = int(m[0]), minute = int(m[1]))
            if exit_timereq < time(20,00):
                additional_output.append(timeavailability(endtime, exit_timereq, req2))
            else:
                additional_output.append("INVALID_EXIT_TIME")
        else:
            additional_output.append("NO_BOOKING")
        x+=1
    return additional_output        





def main():
    
    
   
    if len(argv) != 2:
        raise Exception("File path not entered")
    file_path1 = argv[1]
    f1 = open(file_path1, 'r')
    Lines1 = f1.read().splitlines()
    Lines2= []
    remlines=[]
    for r, line in enumerate (Lines1):
        if line[0]== 'A':
            remlines.append(Lines1[r])
    for z in remlines:
        Lines1.remove(z)
        Lines2.append(z)
    Lines1.pop()
    f1.close
    

    dictkeys1 = ['req_type','veh_type','reg_no','time_req']
    dictkeys2 = ['req_type', 'reg_no', 'exit_time', 'veh_type', 'end_time']
    x = 0
    y=0
    
    booking_requests=[]
    additional_requests =[]

    while x < len(Lines1):
        dictvalues1= (Lines1[x].split(" "))
        my_dict1 = {key:value for (key, value) in zip(dictkeys1, dictvalues1)}
        booking_requests.append(my_dict1)
        x+=1
    
    while y < len(Lines2):
        dictvalues2 = (Lines2[y].split(" "))
        regnum = dictvalues2[1]
        for k in booking_requests:
            
            if k['reg_no'] == regnum:
                dictvalues2.append(k['veh_type'])
                dictvalues2.append(k['time_req'])
            else:
                continue
        #print (dictvalues2)    
        my_dict2 = {key:value for (key, value) in zip(dictkeys2, dictvalues2)}
        additional_requests.append(my_dict2)
        y+=1
    #print (additional_requests)
    booking_outlist = booking (booking_requests)
    add_outlist = booking_add(additional_requests) 
    revregtrack = sum(bookingcostsreg) + sum(addcostsreg)
    revviptrack = sum(bookingcostsvip) + sum(addcostsvip)

    for z in range(len(Lines1)):
        #print (Lines1[z] + "  " + booking_outlist[z])
        print (booking_outlist[z])
    
    for z in range(len(Lines2)):
        #print (Lines2[z] + "  " + add_outlist[z])
        print (add_outlist[z])

    print (str(revregtrack) + " " + str(revviptrack))

    #print ("Total Revenue from Regular Track:" + str(revregtrack))
    #print ("Total Revenue from VIP Track:" + str(revviptrack))
    
    



    
    """
    //Add your code here to process the input commands
    """
    
if __name__ == "__main__":
    main()


