import operator
import csv
import sys

sub_time_slots = []
rooms = []

with open(sys.argv[1], newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\t')
    for row in spamreader:
        sub_time_slots.append(list(filter(None, row[0].split(','))))
        
rooms=sub_time_slots.pop(-1)

print (sys.argv[1])

c_s_p = {}

sujectIterator = -1

subjects = []

for i in range(len(sub_time_slots)):
    subjects.append(sub_time_slots[i][0])

print (subjects)

for i in range(len(sub_time_slots)):
    c_s_p[sub_time_slots[i][0]] = sub_time_slots[i][1::]

print (c_s_p)
print (rooms)

numOfRooms = len(rooms)


def findSlotConflictValue(subject, timeSlot, csp):
    constraintVal = 0
    numOfOptionals = 0
    for k in csp.keys():
        for z in range(1, len(csp[k])):
            if timeSlot == csp[k][z]:
                if csp[subject][0] == "o" and csp[k][0] == "o":
                    constraintVal += 1
                    numOfOptionals += 1
                else:
                    constraintVal += 1               
    return (constraintVal, numOfOptionals) 

def getOrderedTimeSlot(subject, assignment, csp):
    timeSlotsForSubject = csp[subject][1::]      
    slot_constraint_assignment = {}
    for slot in timeSlotsForSubject:
        slot_constraint_assignment[slot] = findSlotConflictValue(subject, slot, csp)
    ordered_list = sorted(slot_constraint_assignment.items(), key=operator.itemgetter(1))  
    return [ordered_list[i][0] for i in range(len(ordered_list))]


def isComplete(assignment):
    if "null" in assignment.values():
        return False
    else:
        return True

def isConsistent(slot, assignment):
    if slot not in assignment.values():
        return True
    elif slot in assignment.values():
        count = 0
        for sub, tSlot in assignment.items():    
            if (tSlot == slot) and (sub[1] == "o"):
                count += 1
        if (count > 0) and (count < numOfRooms):
            return True
        else:
            return False                       

def removeAssignedTimeSlot(csp, subject, slot):
    if subject[1] == "c":
        for k in csp.keys():
            if slot in csp[k]:
                csp[k].remove(slot)
    return csp

def printAssignment(assignment):
    slot_duplicate = {}
    finalOutput = []
    for sub, tSlot in assignment.items():
        if tSlot not in slot_duplicate:
            slot_duplicate[tSlot] = 1
        else:
            slot_duplicate[tSlot] += 1
    with open(sys.argv[2], 'w') as csvfile:
        fieldnames = ['SUBJECT', 'TIME_SLOT', 'ROOM']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for sub in assignment.keys():
            finalOutput.append([sub[0], assignment[sub], "R"+str(slot_duplicate[assignment[sub]])])
            writer.writerow({'SUBJECT': sub[0], 'TIME_SLOT': assignment[sub], 'ROOM': "R"+str(slot_duplicate[assignment[sub]])})
            slot_duplicate[assignment[sub]] -= 1
    print(finalOutput)
    return finalOutput
                       
def Backtracking(assignment, csp):
    if isComplete(assignment):
        return True
    else:
        try:
            subject = selectSubject()
        except:
            return False
        for slot in getOrderedTimeSlot(subject, assignment, csp):
            if isConsistent(slot, assignment):
                assignment[(subject, csp[subject][0])] = slot
                temp = csp
                csp = removeAssignedTimeSlot(csp, (subject, csp[subject][0]), slot)
                if Backtracking(assignment, csp):
                    return True
                else:
                    assignment[(subject, csp[subject][0])] = "null"               
    return False 
    
def assignTimeSlots(csp):
    assignment = {}
    for subject in csp:
        assignment[(subject, csp[subject][0])] = "null"
    if Backtracking(assignment, csp) == True:
        printAssignment(assignment) 
    else:
        print ("Cannot assign time slots!!")
        with open('output.csv', 'w') as csvfile:
            fieldnames = ['Cannot assign time slots!!']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()


def selectSubject():
    global sujectIterator
    sujectIterator+=1
    print (sujectIterator)
    return subjects[sujectIterator]
    

# print (selectSubject())
# print (selectSubject())
# print (selectSubject())
# print (subjects[0])


assignTimeSlots(c_s_p)


