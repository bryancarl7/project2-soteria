from data.apiHandler import apiKeyLoader
from flask_restful import Resource, request
import datetime, calendar, json
from data.bestPlace import bestPlace
from copy import deepcopy

PADDING = 0
'''if we try to insert into an hour with <PADDING minutes left and need to
    add remaining time to the next, we instead ignore it. Mostly for elegance: 
    stops situations where you get a schedule of "go to location from 10:58 to 11:43".
'''
MAX_RECURSION = 3
'''
number of locations to bruteforce insert into a schedule at the same time.
Higher = more optimized lists, but much slower run speeds.

'''


class hour(object):
    def __init__(self, id):
        self.id = id
        self.locations = []
        self.timeleft = 60
        self.last_open_time = 0
        # keeps track if an event bleeds over from a prior hour to this, or from this to the hour after.
        self.hasafter = False

    def insert(self, location, time):
        # Check if we have space for an event at this hour, and inserts if available.
        if (self.timeleft - time) < 0:
            print("false")
            return False
        if self.hasafter:
            # final thing in list is an event that goes into next hour; we need to preserve it's pos at the end of the list
            # for processing purposes. 
            self.locations.insert(-1, [location, self.last_open_time, self.last_open_time + time])
        else:
            self.locations.append( [location, self.last_open_time, self.last_open_time + time])
        self.timeleft -= time
        self.last_open_time += time
        print("true, time remaining: " + str(self.timeleft))
        return True
    
    def adjust_insert(self, location, time):
        # as insert, but inserts at the start of the hour instead of the end.
        # used for events that rollover hours.
        if (self.timeleft - time) < 0:
            ''' shifting would result in pushing an event out of this list, say no
             potential TODO: Return list of events pushed out for rescheduling? Probably not, since pushed out groups have
             a higher priority than the inserted group.'''
            print("could not shift locations, despite checking we could?? ")
            return False
        print("Before adjustions: ")
        print(self.locations)
        for triplet in self.locations:
            # Shift every location up
            triplet[1] += time
            triplet[2] += time
        self.locations.insert(0, [location, 0, time])
        self.timeleft -= time
        self.last_open_time += time
        print("Adjusted list: ")
        print(self.locations)
        return True
 
    def insert_end(self, location, time):
        # as insert, but we're instead appending to the end of this hour. (bleedover from next hour to this one)
        if self.hasafter:
            # We're already bled over! Don't make us invalid!
            return False
        if (self.timeleft - time) < 0:
            # can't fit
            return False
        self.hasafter = True
        self.locations.append([location, 60-time, 60])
        self.timeleft -= time
        return True

    def as_minutes(self):
        '''
        returns a representation where each item in location is (60*our hour)+minutes. Used for representing multi-hour events.
        '''
        out = []
        offset = 60*self.id
        for loc, start, end in self.locations:
            out.append([loc, start+offset, end+offset])
        return out


    def __str__(self):
        if self.id > 12:
            hour = self.id - 12
            ending = "pm"
        else:
            hour = self.id
            ending = "am"
        out = ("For {} {}, ".format(hour, ending))
        if len(self.locations) > 0:
            things = []
            for tup in self.locations:
                end_hour = hour
                minutes = tup[2]
                if tup[2] == 60:
                    minutes = 0
                    end_hour += 1
                    if end_hour == 24:
                        end_hour = 0
                things.append("at {0} from {1}:{2} - {3}:{4} {5}".format(tup[0], hour, str(tup[1]).zfill(2), end_hour,
                                                                         str(minutes).zfill(2), ending))
            out += "there are events: " + ",".join(things)
        else:
            out += "there is nothing scheduled"
        return out

LEFT = 0
RIGHT = 1

class scheduleObj(object):
    '''
    Schedule object, handles the logic for trying to insert a given time. 
    if STRICT: events will not be allowed to go across hour objects. Otherwise, the scheduler will attempt to reshuffle
    '''
    def __init__(self, STRICT = True):
        self.strict = STRICT
        self.hours = []
        for x in range(24):
            self.hours.append(hour(x))

    def insert(self, location, hour, time, closedtimes, pop_times, direction = None):
        print("attempting insert of place " + location + " at hour " + str(hour) + " with duration " + str(time), end='.')
        hourobj = self.hours[hour]
        if self.strict:
            return hourobj.insert(location, time)
        else:
            if hourobj.insert(location, time):
                # same logic as strict: If we can fully insert now, do so
                return True
            if hourobj.timeleft <= PADDING:
                return False

            success, dir = self.recursive_insert(location, hour, ( time - hourobj.timeleft), closedtimes, pop_times, direction)
            
            if success == False:
                return False
            if dir == LEFT: 
                # we inserted to the left; adjust all other times in currhour so we can insert ourselves
                return hourobj.adjust_insert(location, hourobj.timeleft)
            else:
                return hourobj.insert(location, hourobj.timeleft)


    def recursive_insert(self, location, hour, time, closedtimes, pop_times, direction = None):
        # we don't compute the zscore for this hour: it will be the same, left or right
        # time = remaining time to process.

        if direction == None:
            #only check if we need to
            score, direction = self.generate_zscore(location, hour, time, closedtimes, pop_times)

        if direction == LEFT: 
            return ( self.insert_left(location, hour-1, time, closedtimes), LEFT )
        else:
            return (self.insert_right(location, hour+1, time, closedtimes), RIGHT )

    def insert_right(self, location, hour, timeleft, closedtimes):
        hourobj = self.hours[hour]
        if hour in closedtimes:
            # business is closed at this hour, send failure back up the list
            print(location + " is closed at " + str(hour))
            return False
        if timeleft <= hourobj.timeleft:
            # We can insert into this slot! 
                return hourobj.adjust_insert(location, timeleft)
        if hourobj.timeleft == 60 and hour < 23:
            # we're too big for this timeslot, BUT we can completely occupy this slot and bleed into the next hour.
            # Does not allow for schedules spanning two days.
            if self.insert_right(location, hour+1, timeleft-60, closedtimes, start_time):
                # we were able to insert into later time slots; now, insert ourselves fully into this slot.
                return hourobj.insert(location, 60)
        else:
            return False

    def insert_left(self, location, hour, timeleft, closedtimes):
        hourobj = self.hours[hour]
        if hour in closedtimes:
            # business is closed at this hour, send failure back up the list
            print(location + " is closed at " + str(hour))
            return False
        if timeleft <= hourobj.timeleft:
            # We can insert into this slot! 
                return hourobj.insert_end(location, timeleft)
        if hourobj.timeleft == 60 and hour < 23:
            # we're too big for this timeslot, BUT we can completely occupy this slot and bleed into the next hour.
            # Does not allow for schedules spanning two days.
            if self.insert_left(location, hour-1, timeleft-60, closedtimes):
                # we were able to insert into later time slots; now, insert ourselves fully into this slot.
                return hourobj.insert(location, 60)
        else:
            return False

    def generate_zscore(self, location, hour, time, closedtimes, pop_times):

        left_score = self.generate_zscore_left(location, hour-1, time, closedtimes, pop_times)
        right_score = self.generate_zscore_right(location, hour+1, time, closedtimes, pop_times)
        if (left_score == 0) and (right_score == 0):
            # neither direction works! signal we couldn't continue.
            return (0, RIGHT)
        # 144001 is an impossible score (max possible is 144000)
        if left_score <= 0:
            left_score = 144001
        if right_score <= 0:
            right_score = 144001

        if left_score < right_score: #bias ->, for good looking schedules more than anything.
            return (left_score, LEFT)
        else:
            return (right_score, RIGHT)

    def generate_zscore_left(self, location, hour, time, closedtimes, pop_times):
        if (hour < 0) or (hour > 23):
            #OOB
            return 0 
        hourobj = self.hours[hour]
        if hour in closedtimes:
            # business is closed at this hour, send failure back up the list
            #print(location + " is closed at " + str(hour))
            return 0  
        if hourobj.hasafter:
            #print("hour " + str(hour) + " already has event crossing over, cannot insert")
            return 0
        if time <= hourobj.timeleft:
            #print("successfully finished zscore at: ", str(hour))
            return time * (pop_times[hour])
        if hourobj.timeleft == 60 and hour > 0:
            # we're too big for this timeslot, BUT we can completely occupy this slot and bleed into the previous hour.
            # Does not allow for schedules spanning two days.
            #print("we were too big, but can bleed over into previous hour")
            z_score = self.generate_zscore_left(location, hour-1, time-60, closedtimes, pop_times)
            if z_score > 0:
                # we were able to insert into previous time slots; now, calculate cost of this slot.
                return z_score + (60 * pop_times[hour])
        #We couldn't finish insertion here and cannot continue to the previous hour; failed!
        print("what?")
        return 0

        print("what?")
        print(location + ": " + str(hour) + " " + str(time))

    def generate_zscore_right(self, location, hour, time, closedtimes, pop_times):
        if (hour < 0) or (hour > 23):
            #OOB
            return 0 
        hourobj = self.hours[hour]
        if hour in closedtimes:
            # business is closed at this hour, send failure back up the list
            #print(location + " is closed at " + str(hour))
            return 0  
        if time <= hourobj.timeleft:
            #print("successfully finished zscore at: ", str(hour))
            return time * (pop_times[hour])
        if hourobj.timeleft == 60 and hour < 23:
            # we're too big for this timeslot, BUT we can completely occupy this slot and bleed into the next hour.
            # Does not allow for schedules spanning two days.
            #print("we were too big, but can bleed over into next hour")
            z_score = self.generate_zscore_right(location, hour+1, time-60, closedtimes, pop_times)
            if z_score != 0:
                # we were able to insert into later time slots; now, insert ourselves fully into this slot.
                return z_score + (60 * pop_times[hour])
            else:
                return 0
       #We couldn't finish insertion here and cannot continue to the previous hour; failed!
        print("what?")
        return 0

    def __str__(self):
        slist = []
        for x in range(24):
            slist.append(str(self.hours[x]))
        return '\n'.join(slist)

    def to_list(self):
        internal = []
        for x in range(0, 23):
            cur = self.hours[x].as_minutes()
            if(len(cur) == 0):
                continue
            if(len(internal) == 0):
                internal = cur
                continue
            if (internal[-1][0] == cur[0][0]):
                '''
                if same location, concatenate
                so [a, 0, 60] + [a, 0, 30] => [a,0,90] which will get turned back into hours after processing.
                This allows for multi-hour events to get correctly concatenated, whil being processible for strings
                '''
                internal[-1][2] = cur[0][2] 
                internal += cur[1:]
            else:
                internal += cur
        return internal

    def current_zscore(self, pop_dict):
        zscore = 0
        for x in range[24]:
            hour = self.hours[x]
            for loc, start, end in hour.locations:
                zscore += (end - start)*pop_dict[location][x]
        return zscore


class scheduler(Resource):
    def post(self):
        # Take the JSON from the request
        json_dump = request.get_json()
        print(json.dumps(json_dump, indent=4))

        # Setup Place_ID
        place_id = json_dump['place']  # add extra indexes to the end to sub-index the JSON

        # Setup the day of the week
        today = datetime.datetime.today()
        day = calendar.day_name[today.weekday()]

        return place_id, 200
    
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
        resorted_dict = {}
        for k in tempdict.keys():
            resorted_dict[k] = [0 for x in range(24)]
            for hour, pop in tempdict[k]:
                tuplelist.append( (k, hour, pop) )
                resorted_dict[k][hour] = pop
                if pop == 0:
                    closed_hours[k].append(hour)
        for k in tempdict.keys():
            resorted_dict[k] = sorted(tempdict[k], key = lambda pair: pair[0])
        return resorted_dict, closed_hours, sorted(tuplelist, key = lambda triple: 1000 if triple[2] == 0 else triple[2])


    @classmethod
    def bruteforce_helper(cls, sched_obj, locations, curr_times, closed_times,  pop_dict):
        lowest_score = 144001 # zscore = popularity in hour * minutes in the slot, max = 24 * 60 * 100 = 144000.
        final_schedule = None
        if len(locations) == 0:
            return 0, sched_obj
        for loc in locations:
            schedule = deepcopy(sched_obj)
            best_hour_score = 144001
            best_hour = 0
            best_hour_dir = LEFT
            best_bleed = False
            for x in range(24):
                print("for hour "+ str(x)+ ":")
                print("pop count is "+ str(pop_dict[loc][x]))
                print("inserting here solely costs " + str(curr_times[loc] * pop_dict[loc][x]))
                if x in closed_times[loc]:
                    #closed at this time, ignore it
                    continue
                hourobj = schedule.hours[x]
                time_at_hour = None
                Must_bleed = False
                if ( hourobj.timeleft == 0):
                    #we're full!
                    continue
                if (( hourobj.timeleft < curr_times[loc]) ):
                    # not enough space in hour; need to bleed over into next hour.
                    time_at_hour = hourobj.timeleft
                    Must_bleed = True
                else:
                    #enough space for us here.
                    time_at_hour = curr_times[loc]


                score = pop_dict[loc][x] * time_at_hour #base score
                part_score, direction = schedule.generate_zscore(loc, x, curr_times[loc] - time_at_hour, closed_times[loc], pop_dict[loc])
                if (Must_bleed and part_score == 0) or (Must_bleed == False and score == 0):
                    #We couldn't insert recursively and needed to. This hour is invalid
                    print("reeee")
                    continue
                score += part_score

                #print("score is " + str(score))
                if score < best_hour_score:
                    #print("and was better than previous: " + str(best_hour_score) + " at "+ str(best_hour))
                    best_hour_score = score
                    #print(best_hour_score)
                    best_hour = x
                    best_hour_dir = direction
                    best_bleed = Must_bleed

            if best_hour_score == 144001:
                #unable to insert this location *at all*!!
                #invalid schedule; will never be considered over base
                return 144001, None
            #at this point, we know what the best hour is to insert this loc: now recursively build lower ones
            #print(best_hour_score)
            #print(best_hour)
            #insert's logic handles shifts
            truth = schedule.insert(loc, best_hour, curr_times[loc], closed_times[loc], pop_dict[loc], best_hour_dir)

            #otherwise, recurse
            rec_score, rec_schedule = cls.bruteforce_helper(schedule, [x for x in locations if x != loc], curr_times, closed_times, pop_dict)
            best_hour_score += rec_score
            if best_hour_score < lowest_score:
                lowest_score = best_hour_score
                final_schedule = rec_schedule
        
        return lowest_score, final_schedule




    @classmethod
    def optimize_schedule(cls, schedule, day, test_dict=None, strict = True, bruteforce = False):
        '''
        Dict(location:(priority, time)), String, optional dict(location:(hour, ratio)) -> dict(location:(time??))
        time?? is either (from_time and to_time), or the duration in minutes you would be at a location(pending implementation on frontend)
        
        Given an initial user-defined schedule and the weekday the schedule would be followed, tries to optimize it to ensure as little human contact as possible.
        User-defined priority represents the order to select places: Users are asked to rate places with higher average customers closer to 1
        '''
        sched = scheduleObj(strict)
        #builds a list of priorities; the sentinel guarantees the last priority is run through the following loop.
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
            # Priority has changed, try to add previous to schedule.
            test_subset = None
            if test_dict is not None:
                test_subset = {x:test_dict[x] for x in curr_locations}
            poplist, closedlist, glist = cls.build_greedy_list(curr_locations, day, test_subset)
            successful_inserts = []
            if (strict == True) or (bruteforce == False):
                # this algorithm is faster *and* is guaranteed to be optimal for a strict ruleset
                # letting bruteforce == false allows for testing optimizations
                for (location, hour, popularity) in glist:
                    if popularity == 0:
                        # Location is closed
                        continue
                    if len(successful_inserts) == len(curr_locations):
                        # We've allocated everything, get out of the loop!
                        break
                    if location in successful_inserts:
                        # This location already exists in the schedule; ignore it.
                        continue
                    
                    if sched.insert(location, hour, curr_times[location], closedlist[location], poplist[location]):
                        successful_inserts.append(location)
                        print(successful_inserts)
                
                # Check if we inserted everything in this priority level
                if len(successful_inserts) != len(curr_locations):
                    raise Exception  # TODO: better error descriptor
            else:
                #recursion guarantees we'll be the most optimal, within our set.
                for x in range(0, len(curr_locations), MAX_RECURSION):
                    loc_subset = curr_locations[x:x+MAX_RECURSION]
                    cost, sched = cls.bruteforce_helper(sched, loc_subset, curr_times, closedlist, poplist)

            # Previous priority has been handled, setup new priority
            curr_priority = priority
            curr_locations = [key] 
            curr_times = {key: time}
        schedlist = sched.to_list()
        failed_to_schedule = []
 
        if len(schedlist) < len(schedule):
            failed_to_schedule = list(schedule)
            for x in schedlist:
                loc = x[0]
                print(loc)
                if loc in failed_to_schedule:
                    failed_to_schedule.remove(loc)
        return sched.to_list(), failed_to_schedule

