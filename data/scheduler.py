import requests
from data.apiHandler import apiHandler
from flask_restful import Resource
from collections import OrderedDict
from data.bestPlace import bestPlace

class hour(object):
    def __init__(self, id):
        self.id = id
        self.locations = []
        self.timeleft = 60

    def try_insert(self, location, time):
        # Check if we have space for an event at this hour, and
        if((self.timeleft - time) < 0 ):
            print("false")
            return False
        if(len (self.locations) == 0):
            last_time = 0
        else:
            last_time = self.locations[-1][2] 
        self.locations.append( (location, last_time, last_time + time))
        self.timeleft = self.timeleft - time
        print("true, time remaining: " + str(self.timeleft))
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
                things.append("{0} from {1}:{2} - {1}:{3} {4}".format(tup[0], hour, tup[1], tup[2], ending))
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

    def insert(self, location, hour, time_at):
        print("attempting insert of place " + location + " at hour " + str(hour) + " with duration" + str(time_at), end = '')
        if(self.strict):
            return self.hours[hour].try_insert(location, time_at)
        else:
            raise NotImplementedError

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
            unable to allocate that location in the schedule
        '''
        tempdict = bestPlace.get_best_place(curr_locations, day, test_dict)
        returnlist = []
        for k in tempdict.keys():
            returnlist = returnlist + ( [(k, hour, pop) for hour, pop in tempdict[k] ] )
        return sorted(returnlist, key = lambda triple: triple[2])


    @classmethod
    def optimize_schedule(cls, schedule, day, test_dict=None):
        '''
        Dict(location:(priority, time??)), String, optional dict(location:(hour, ratio)) -> dict(location:(time??))
        time?? is either (from_time and to_time), or the duration in minutes you would be at a location(pending implementation on frontend)
        
        Given an initial user-defined schedule and the weekday the schedule would be followed, tries to optimize it to ensure as little human contact as possible.
        User-defined priority represents the order to select places: Users are asked to rate places with higher average customers closer to 1
        '''
        sched = scheduleObj()
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
            test_subset = {x:test_dict[x] for x in curr_locations}
            glist = cls.build_greedy_list(curr_locations, day, test_subset)
            successful_inserts = []
            for (location, hour, popularity) in glist:
                if len(successful_inserts) == len(curr_locations):
                    # we've allocated everything, get out of the loop!
                    break
                if location in successful_inserts:
                    # this location already exists in the schedule; ignore it.
                    continue
                
                if sched.insert(location, hour, curr_times[location]):
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

            
if __name__ == "__main__":
    print(scheduler.scheduler.build_greedy_list(["ChIJnwXa6yF2vlQRmB-51fHUrIo","ChIJ0X3bxN4CwVQRk22GqgCurPY"], 
    "Tuesday", 
    test_dict = {
        "ChIJnwXa6yF2vlQRmB-51fHUrIo": 
        [13, 70, 41, 22, 49, 37, 39, 2, 48, 6, 74, 26, 99, 31, 27, 83, 82, 88, 53, 78, 43, 87, 47, 54], 
        "ChIJ0X3bxN4CwVQRk22GqgCurPY": 
        [1, 81, 77, 22, 27, 13, 12, 24, 69, 74, 80, 96, 9, 64, 26, 10, 95, 62, 90, 97, 53, 0, 7, 89]
        }
        ) 
        )