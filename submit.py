import time
import math

#do not modify the function names
#You are given L and M as input
#Each of your functions should return the minimum possible L value alongside the marker positions
#Or return -1,[] if no solution exists for the given L

def get_marker_diffs(markers):
    """

    :param markers: golomb markers
    :return: returns a list of differences between all elements of the markers
    """

    diffs = list()
    for idx1 in range(0, len(markers)):
        for idx2 in range(idx1 + 1, len(markers)):
            current_diff = int(math.fabs(markers[idx1] - markers[idx2]))
            #if current_diff not in diffs:
            diffs.append(current_diff)

    return diffs


def set_domains_after_ac3(last_val, L, markers, cp_excluded_vals):
    """

    :param last_val: last value set to golomb ruler
    :param L: length of proposed ruler
    :return: reduced domain values using arc consistency
    """
    #unoptimized domain values
    domain_values = [i for i in range(last_val + 1, L + 1)] # now domain values start from next of last val of markers.

    #current set of diffs
    diffs = get_marker_diffs(markers)
    unique_diffs = set(diffs)

    #print "initial domain values >>>> ", domain_values
    #print "initial diffs >>>> ", diffs
    #print "markers >>>> ", markers


    for i in range(2,len(markers)):                 # first 2 are extreme values
        for udiff in unique_diffs:
            excluded_val = int(markers[i] + udiff)
            if excluded_val <= markers[1]:           # value to be excluded should optimally be <= than markers
                cp_excluded_vals.append(excluded_val)

    #unique_cp_excluded_vals = set(cp_excluded_vals)
    #print "cp_excluded_vals >>>> ", cp_excluded_vals
    #print "----------------------------------------------"

    return cp_excluded_vals


def csp_bt_cp_verify(L, M):
    """

    reduce the domain values in each iteration to maintain arc consistency (ac3)
    :param L: Length of ruler to verify
    :param M: Number of Markers to verify
    :return: Whether such a golomb ruler exists (-1 = 'does not exists',  1 = 'exists')
    """

    backtrack = False

    # basic validation
    if L == 0 :
        return -1 , []

    markers = list()
    markers.append(0) # assuming m1=0
    markers.append(L)  # assuming m-last=L as largest distance between 2 marks is length of golomb ruler

    if M == 2 and L == 1:
        return L, markers

    excluded = list()
    last_val = 0

    # next variable to be added to the markers list
    while True:

        cp_excluded_vals = list()
        if len(markers) == 0:
            break

        if backtrack:
            last_val = markers[len(markers) - 1]
            # remove last value
            markers.remove(last_val)

        # gather all the allowed values based on length

        domain_values = [i for i in range(last_val + 1, L + 1)] # now domain values start from next of last val of markers.

        for val in domain_values:

            # fetch next value if it is already present in existing markers
            # ---- CP : making sure that domain values in excluded list (cp_excluded_vals) are not iterated.
            if val in markers or val in cp_excluded_vals:
                continue


            value_absent = True

            #get a list of differences between all elements of the markers
            diffs = get_marker_diffs(markers)

            #constraint satisfaction check
            for marker in markers:
                val_diff = math.fabs(val - marker)
                if val_diff in diffs:
                    value_absent = False
                    break

            # value diff with each marker does not exist in the diffs between markers (constraint)
            if value_absent == True:
                markers.append(val)

                # gathering the list of excluded values for the next iteration based on
                #current domain values, markers and their difference.
                cp_excluded_vals = set_domains_after_ac3(last_val, L, markers, cp_excluded_vals)

                # if all markers found and count matches M then return , terminating condition
                if len(markers) == M:
                    # check if these markers are valid
                    final_diffs = get_marker_diffs(markers)
                    if len(final_diffs) == len(set(final_diffs)):
                        return L, markers

        # backtrack once all domain values looped over
        #print "current markers >>>> ", markers
        backtrack = True

    #all else fails
    return -1, []


def csp_bt_verify(L, M):
    """

    :param L: Length of ruler to verify
    :param M: Number of Markers to verify
    :return: Whether such a golomb ruler exists (-1 = 'does not exists',  1 = 'exists')
    """

    backtrack = False

    # basic validation
    if L == 0 :
        return -1 , []

    markers = list()
    markers.append(0) # assuming m1=0
    markers.append(L)  # assuming m-last=L as largest distance between 2 marks is length of golomb ruler

    if M == 2 and L == 1:
        return L, markers

    excluded = list()
    last_val = 0

    # next variable to be added to the markers list
    while True:

        if len(markers) == 0:
            break

        if backtrack:
            last_val = markers[len(markers) - 1]
            # remove last value
            markers.remove(last_val)

        # gather all the allowed values based on length

        domain_values = [i for i in range(last_val + 1, L + 1)] # now domain values start from next of last val of markers.

        for val in domain_values:

            # fetch next value if it is already present in existing markers
            if val in markers:
                continue


            value_absent = True

            #get a list of differences between all elements of the markers
            diffs = get_marker_diffs(markers)

            #constraint satisfaction check
            for marker in markers:
                val_diff = math.fabs(val - marker)
                if val_diff in diffs:
                    value_absent = False
                    break

            # value diff with each marker does not exist in the diffs between markers (constraint)
            if value_absent == True:
                markers.append(val)
                # if all markers found and count matches M then return , terminating condition
                if len(markers) == M:
                    # check if these markers are valid
                    final_diffs = get_marker_diffs(markers)
                    if len(final_diffs) == len(set(final_diffs)):
                        return L, markers

        # backtrack once all domain values looped over
        backtrack = True

    #all else fails
    return -1, []

#Your backtracking function implementation
def BT(L, M):
    """

    :param L: Length of the ruler
    :param M: Number of marks
    :return: Verify if a Golomb ruler for this combination of (L,M) actually exists or not.

    Note:   CSP can only tell us whether or not there is a ruler of fixed length L for M marks.
            To find an optimal length, the value of L must be decreased until no solution exists using CSP.
    """
    "*** YOUR CODE HERE ***"

    #golombLength, markers =csp_bt_verify(L, M)
    #return golombLength, markers

    # base case: if L = 0 or golomb ruler for given inputs does not exist, then return -1, []
    if L == 0:           #or golombLength == -1:
        return -1, []

    # if golomb ruler for L exists but not L -1, the optimal length is L. Return that along with markers

    golombLength, markers = csp_bt_verify(L, M)
    prev_markers = markers
    last_good_markers = markers

    while L > 0:
        L -= 1
        golombLength, markers = csp_bt_verify(L, M)

        if golombLength == -1:
            last_good_markers = prev_markers # the previous marker was most optimal, return that
        else:
            print "\n **** Found a solution with BT only ***** ", markers
            print "checking for more optimal solutions.........."
            prev_markers = markers

    if len(last_good_markers) > 0:
        return sorted(last_good_markers)[-1], last_good_markers
    else:
        return -1, []
#returns all possible distances between the selected values 
def getDistances(values):
    l = []
    for i in range(0, len(values)):
        for j in range(i + 1, len(values)):
            l.append(values[i] - values[j])
    return list(set(l))


def setFirstAndLastMark(marks_domain, marks):
    """
    set the first mark and the last mark by default
    """
    domain = marks_domain['mark0']
    for i in range(0, len(domain)):
        if (i != 0):
            marks_domain['mark0'].remove(i)


def checkIfSafe(final_marks, position):
    """
    check if the current selected value satisfy the constraints or not by
    calculating the possible distances between all value and they should be unique
    return True if unique else False
    """

    finalmarks = []
    for i in range(0, len(final_marks)):
        finalmarks.append(final_marks[i])
    finalmarks.append(position)

    diffs = []
    for idx1 in range(0, len(finalmarks)):
        for idx2 in range(idx1 + 1, len(finalmarks)):
            current_diff = abs(finalmarks[idx1] - finalmarks[idx2])
            # if current_diff not in diffs:
            diffs.append(current_diff)
    if len(diffs) == len(set(diffs)):
        return True
    else:
        return False


def backtracking(marks_domain, length, marks, final_marks, dictionary_distances, currentmark):  
    # function to perform backtracking along with forward checking
    """

    :param L: Length of ruler to verify
    :param M: Number of Markers to verify
    :return: Whether such a golomb ruler exists (-1 = 'does not exists',  1 = 'exists' using backtracking and forward checking)
    """

    if (len(final_marks) == marks): #all marks have been assigned a value satisfying the constraint
        print "\n *********** Found a solution with BT+FC ************ ", final_marks
        print "checking for more optimal solutions.........."
        return sorted(final_marks) #sorted the marks 
    # return
    result = ''

    currentMarklist = marks_domain['mark' + str(currentmark)] #gets the domain for a corresponding mark
    flag = True #flag defines whether all the constraints have been satisfied or not for selected values.
    for i in range(0, len(currentMarklist)): #traverse for values one by one and checks for constraint satisfaction
        count = 0
        position = currentMarklist[i]
        # final_marks.append(position)
        dictionary_distances = getDistances(final_marks) # for selected marks get all the distances possible
        for j in range(0, len(final_marks)):
            flag = True
            # count=0/
            d = abs(final_marks[j] - position)
            if (d not in dictionary_distances): #checks if a new selected value satisfies all the constraints 
                count += 1
                dictionary_distances.append(d) 
            else:
                flag = False

                # dictionary_distances = dictionary_distances[:len(dictionary_distances) - count]
                dictionary_distances = dictionary_distances[:len(dictionary_distances) - count] #if the value doesnt satisfy constraints remove the distance added by that value
                break
        if (flag):
            if len(final_marks) == 0:
                dictionary_distances.append(0) #value selected satidfies all constraint, add to list
            # if(checkIfSafe(final_marks, position)):
            final_marks.append(position)

            newD = []
            # Forward checking : domains of subsequent marks being explored
            if (currentmark + 1 < marks): #check if marks left to be filled
                domain = marks_domain['mark' + str(currentmark + 1)]
                dependence = False
                for d in domain:
                    dependence = False
                    for value in final_marks:
                        dist = abs(d - value)
                        if dist in dictionary_distances: # checking for constraints againts domsin of subsequent marks| forward checking
                            dependence = True
                    if (not dependence):
                        newD.append(d)

            for i in range(0, marks):
                if (i > currentmark):
                    marks_domain['mark' + str(i)] = newD; # forward checking, updating the domain of subsequent marks removing values generating the distances already generated by the domain of selected marks
            # if(len(marks_domain['mark'+str(currentmark)])):
            result = backtracking(marks_domain, length, marks, final_marks, dictionary_distances, currentmark + 1) # backtrack called after adding a mark value that satisfies the constraints

            if (len(result) != marks): #backtracking called here
                final_marks.remove(position)#if the selected value doesnot provide adequate result, value is removed and  next value is selected and checked
                dictionary_distances = dictionary_distances[:len(dictionary_distances) - count] #remove the distances added by the previous selected value 
                for i in range(0, marks):
                    if (i > currentmark):
                        marks_domain['mark' + str(i)] = marks_domain['mark' + str(currentmark)];# set the updated domain for the subsequent marks
            else:
                return result
    return result

#Your backtracking+Forward checking function implementation
def FC(l, M):
    """
    ""*** YOUR CODE HERE ***"

    :param L: Length of ruler to verify
    :param M: Number of Markers to verify
    :return: Whether such a golomb ruler exists (-1 = 'does not exists',  1 = 'exists' using backtracking and forward checking)
    """
    length, marks = l, M
    dictionary_distances = [] #stores uniques distances between all finalmark values
    marks_domain = {} #stores domain for mark values
    final_marks = [] #final list of selected marks

    for i in range(0, marks):
        domain = []
        for j in range(0, length + 1):
            domain.append(j)
        marks_domain['mark' + str(i)] = domain
    # print marks_domain

    result = backtracking(marks_domain, length, marks, final_marks, dictionary_distances, 0) # calling backtracking with forwardChecking
    if (result == None):
        print "\n No solution found for BT+FC"
        return -1, []
    else:
        return result


#Bonus: backtracking + constraint propagation
def CP(L, M):
    """
    "*** YOUR CODE HERE ***"
        :param L: Length of the ruler
        :param M: Number of marks
        :return: Verify if a Golomb ruler for this combination of (L,M) actually exists or not.

        Note:   CSP can only tell us whether or not there is a ruler of fixed length L for M marks.
                To find an optimal length, the value of L must be decreased until no solution exists using CSP.
    "*** YOUR CODE HERE ***"
    """


    # golombLength, markers =csp_bt_verify(L, M)
    # return golombLength, markers

    # base case: if L = 0 or golomb ruler for given inputs does not exist, then return -1, []
    if L == 0:  # or golombLength == -1:
        return -1, []

    # if golomb ruler for L exists but not L -1, the optimal length is L. Return that along with markers

    golombLength, markers = csp_bt_cp_verify(L, M) # calling the BT with CP method
    prev_markers = markers
    last_good_markers = markers

    while L > 0:
        L -= 1
        golombLength, markers = csp_bt_cp_verify(L, M)

        if golombLength == -1:
            last_good_markers = prev_markers  # the previous marker was most optimal, return that
        else:
            print "\n **** Found a solution with BT and CP ***** ", markers
            print "checking for more optimal solutions with BT and CP .........."
            prev_markers = markers

    if len(last_good_markers) > 0:
        return sorted(last_good_markers)[-1], last_good_markers
    else:
        return -1, []



if __name__ == "__main__":


    num_markers = 3
    length = 1



    print "\n------------------- Inputs  ----------------------------"
    print " length >> ", length
    print " markers >> ", num_markers
    print "\n------------------- Backtracking only solution  ----------------------------"
    t0 = time.time()
    l, markers = BT(length, num_markers)

    if len(markers) > 0:
        sorted_markers = sorted(markers)
        print "\n Shortest possible length ", sorted_markers[
            len(sorted_markers) - 1], " with Backtracking only is possible for marker positions ", sorted_markers
        print " Calculation took ", (time.time() - t0), " seconds."
    else:
        print " No shortest possible length exists for ", num_markers, " markers of length ", length
        print " Calculation took ", (time.time() - t0), " seconds."



    print " \n\n------------------- Backtracking with Forward Checking solution  ----------------------------"
    t0 = time.time()
    results = []
    startlength = int((num_markers*(num_markers-1))/2) # min start length for golomb ruler is m(m-1)/2
    #print "startlength >> ", startlength
    for i in range(length, startlength-1, -1):
        res = FC(i, num_markers)
        if (res != ''):
            results.append(res)
    if (len(results) == 0):
        print " No shortest possible length exists for ", num_markers, " markers of length ", length
        print " Calculation took ", (time.time() - t0), " seconds."
    else:
        print "-----------------------------------------------------"
        print "\n Shortest possible length using Backtracking with Forward Checking have marker positions ", results[len(results) - 1]
        print " Calculation took ", (time.time() - t0), " seconds."




    print "\n------------------- Backtracking with Constraint Propagation solution  ----------------------------"
    t0 = time.time()
    markers = CP(length, num_markers)

    if len(markers) > 0:
        sorted_markers = sorted(markers)
        print "\n Shortest possible length ", sorted_markers[
            len(sorted_markers) - 1], " with Backtracking and Constraint Propagation only is possible for marker positions ", sorted_markers
        print " Calculation took ", (time.time() - t0), " seconds."
    else:
        print " No shortest possible length exists for ", num_markers, " markers of length ", length
        print " Calculation took ", (time.time() - t0), " seconds."

print "\n------------------- End  ----------------------------"