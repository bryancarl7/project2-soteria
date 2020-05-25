import requests
from data.apiHandler import apiHandler
from flask_restful import Resource
from collections import OrderedDict
from data.bestPlace import bestPlace

PADDING = 10 #
'''if we try to insert into an hour with <PADDING minutes left and need to
    add remaining time to the next, we instead ignore it. Mostly for elegance: 
    stops situations where you get a schedule of "go to location from 10:58 to 11:43".
'''

class hour(object):
    def __init__(self, id):
        self.id = id
        self.locations = []
        self.timeleft = 60
        # keeps track if an event bleeds over from a prior hour to this, or from this to the hour after.
        self.hasbefore = False
        self.hasafter = False

    def insert(self, location, time):
        # Check if we have space for an event at this hour, and inserts if available.
        if((self.timeleft - time) < 0 ):
            print("false")
            return False
        if(len (self.locations) == 0):
            last_time = 0
        else:
            last_time = self.locations[-1][2] 
        self.locations.append( [location, last_time, last_time + time])
        self.timeleft = self.timeleft - time
        print("true, time remaining: " + str(self.timeleft))
        return True
    
    def adjust_insert(self, location, time):
        # as insert, but inserts at the start of the hour instead of the end.
        # used for events that rollover hours.
        if ((self.timeleft - time) < 0):
            ''' shifting would result in pushing an event out of this list, say no
             potential TODO: Return list of events pushed out for rescheduling? Probably not, since pushed out groups have
             a higher priority than the inserted group.'''
            print("could not shift locations, despite checking we could?? ")
            return False
        print("Before adjustions: ")
        print(self.locations)
        for triplet in self.locations:
            #shift every location up
            triplet[1] += time
            triplet[2] += time
        self.locations.insert(0, [location, 0, time])
        print("Adjusted list: ")
        print(self.locations)
        return True
 
    def __str__(self):
        if(self.id > 12):
            hour = self.id - 12
            ending = "pm"
        else:
            hour = self.id
            ending = "am"
        out = ("For {} {}, ".format(hour, ending))
        if(len(self.locations) > 0):
            things = []
            for tup in self.locations:
                end_hour = hour
                minutes = tup[2]
                if tup[2] == 60:
                    minutes = 0
                    end_hour += 1
                    if(end_hour == 24):
                        end_hour = 0
                things.append("at {0} from {1}:{2} - {3}:{4} {5}".format(tup[0], hour, str(tup[1]).zfill(2), end_hour, str(minutes).zfill(2), ending))
            out += "there are events: " + ",".join(things)
        else:
            out += "there is nothing scheduled"
        return out

class scheduleObj(object):
    '''
    Schedule object, handles the logic for trying to insert a given time. 
    if STRICT: events will not be allowed to go across hour objects. Otherwise, the scheduler will attempt to reshuffle
    '''
    def __init__(self, STRICT = True):
        self.strict = STRICT
        self.hours = {}
        for x in range(24):
            self.hours[x] = hour(x)

    def insert(self, location, hour, time, closedtimes):
        print("attempting insert of place " + location + " at hour " + str(hour) + " with duration " + str(time), end = '.')
        hourobj = self.hours[hour]
        if(self.strict):
            return hourobj.insert(location, time)
        else:
            if(hourobj.insert(location, time)):
                # same logic as strict: If we can fully insert now, do so
                return True
            if hourobj.timeleft <= PADDING:
                print("padding killed it")
                return False
            if (self.recursive_insert(location, hour+1, ( time - hourobj.timeleft), closedtimes) ):
                return hourobj.insert(location, hourobj.timeleft)


    def recursive_insert(self, location, hour, time, closedtimes):
        hourobj = self.hours[hour]
        if hour in closedtimes:
            # business is closed at this hour, send failure back up the list
            print(location + " is closed at " + str(hour))
            return False
        if time <= hourobj.timeleft:
            #try insertion. *should* work.
            return hourobj.adjust_insert(location, time)
        if (hourobj.timeleft == 60 and hour <23):
            # we're too big for this timeslot, BUT we can completely occupy this slot and bleed into the next hour. Does not allow for schedules spanning two days.
            if (self.recursive_insert(location, hour+1, time-60, closedtimes)):
                # we were able to insert into later time slots; now, insert ourselves fully into this slot.
                return hourobj.insert(location, 60)


    def __str__(self):
        slist = []
        for x in range(24):
            slist.append(str(self.hours[x]))
        return('\n'.join(slist))

class scheduler(Resource):
    def __init__(self, api_handler):
        self.apiHandler = api_handler
        self.id = ""
        self.table = []

    def get(self):
        return '', 200

    def post(self):
        return '', 200

    def delete(self):
        return '', 200

    def create(self):
        return '', 200
    
    @staticmethod
    def build_greedy_list(curr_locations, day, test_dict = None):
        '''
        List(placeids), string, optional dict(placeid: list[popularity]) -> list
        helper method. Builds a sorted list of best hours within a given priority. 
        example:
            place x and place y share same priority; x's min popularity is 4 at 6 am , and y's is 6 at 7 am.
            So, the list would look like: [('x', 6, 4), ('y', 7, 6), ....]
            this allows the caller to iterate over the list until the minimum available hour is selected 
            for all locations. If the caller reaches the end of this list without an available space, we are
            unable to allocate that location in the schedule.
            also creates a dictionary of location:closedtimes, for insertion purposes.
        '''
        tempdict = bestPlace.get_best_place(curr_locations, day, test_dict)
        tuplelist = []
        closed_hours = {x:[] for x in curr_locations}
        for k in tempdict.keys():
            for hour, pop in tempdict[k]:
                tuplelist.append( (k, hour, pop) )
                if pop == 0:
                    closed_hours[k].append(hour)
        return closed_hours, sorted(tuplelist, key = lambda triple: 1000 if triple[2] == 0 else triple[2])


    @classmethod
    def optimize_schedule(cls, schedule, day, test_dict=None, strict = True):
        '''
        Dict(location:(priority, time??)), String, optional dict(location:(hour, ratio)) -> dict(location:(time??))
        time?? is either (from_time and to_time), or the duration in minutes you would be at a location(pending implementation on frontend)
        
        Given an initial user-defined schedule and the weekday the schedule would be followed, tries to optimize it to ensure as little human contact as possible.
        User-defined priority represents the order to select places: Users are asked to rate places with higher average customers closer to 1
        '''
        sched = scheduleObj(strict)
        #build a list of priorities; the sentinel guarantees the last priority is run through the following loop.
        by_priority = sorted(schedule.items(), key = lambda pair: pair[1][0])
        sentinel = ("dummy", (999,999))
        by_priority.append(sentinel)
        
        #initial variables. By priority: (location, (priority, time))
        curr_locations = [by_priority[0][0]]
        curr_priority = by_priority[0][1][0]
        curr_times = {by_priority[0][0]: by_priority[0][1][1]}
        for key, (priority, time) in by_priority[1:]:
            
            if (priority == curr_priority) and (key != "dummy"):
                curr_locations.append(key)
                curr_times[key] = time
                continue


            print("stepping into allocations with list: ")
            print(str(curr_locations))
            print("")
            #priority has changed, try to add previous to schedule.
            test_subset = None
            if test_dict != None:
                test_subset = {x:test_dict[x] for x in curr_locations}
            closedlist, glist = cls.build_greedy_list(curr_locations, day, test_subset)
            successful_inserts = []
            for (location, hour, popularity) in glist:
                if(popularity == 0):
                    # location is closed
                    continue
                if len(successful_inserts) == len(curr_locations):
                    # we've allocated everything, get out of the loop!
                    break
                if location in successful_inserts:
                    # this location already exists in the schedule; ignore it.
                    continue
                
                if sched.insert(location, hour, curr_times[location], closedlist[location]):
                    successful_inserts.append(location)
                    print(successful_inserts)
            
            #Check if we inserted everything in this priority level
            if len(successful_inserts) != len(curr_locations):
                raise Exception #todo: better error descriptor

            #previous priority has been handled, setup new priority
            curr_priority = priority
            curr_locations = [key] 
            curr_times = {key: time}
        return sched