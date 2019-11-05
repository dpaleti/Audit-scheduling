#from __future__ import absolute_import
#from __future__ import division
from __future__ import print_function
from ortools.sat.python import cp_model
import numpy as np
from ortools.linear_solver import pywraplp

class AuditorsScheduleSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, assignments, num_auditors, num_sites, sols):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._assignments = assignments
        self._num_auditors = num_auditors
        self._num_sites = num_sites
        self._solutions = set(sols)
        self._solution_count = 0

    def on_solution_callback(self):
        if self._solution_count in self._solutions:
            print('Solution %i' % self._solution_count)
            for n in range(self._num_auditors):
                is_working = False
                for s in range(self._num_sites):
                    if self.Value(self._assignments[(n, s)]):
                        is_working = True
                        print('  Auditor %i audits Site %i' % (n, s))
                if not is_working:
                    print('  Auditor {} does not audit'.format(n))
            print()
        self._solution_count += 1

    def solution_count(self):
        return self._solution_count


#Strucutre of the program
# 1.Creates cp model
# 2.Declares variables
# 3.Add constraints to the model
# 4. Defines Objective functin(minimize)
# 5.Runs the solver

#10/22
# Program should provide the schedule a month out based on sites to audit and their due dates
# Every site has a time to audit in days,
# Assignment table
# auditor | site | distance | timetoaudit | next30dayssequence | calendardate


def main():

    num_sites = 8
    num_auditors = 3
    sites = range(num_sites)
    auditors = range(num_auditors)
    num_days = 31

    audit_limit_monthly = 3 # per month, max audits an auditor can conduct in a month --> assignments per audit less than audit_limit



    # all_days = range(1, num_days)
    # for x in all_days:
    #     print(x)
    #
    # x = 1
    # # x = 11
    #
    # print(range(x,x+9))
    # for n in range(x,x+9):
    #     print (n)
    # print(all_days[x-1:x+8])

    # Creates Model
    model = cp_model.CpModel()

    #Declare Variables
    # Assigning Audits evenly across Auditors , ie. Each Auditor gets same # of audits to complete

    # min_shifts_per_nurse is the largest integer such that every nurse
    # can be assigned at least that many shifts. If the number of nurses doesn't
    # divide the total number of shifts over the schedule period,
    # some nurses have to work one more shift, for a total of
    # min_shifts_per_nurse + 1.
    # Its could always be at most one extra audit per auditor after evenly distributing the audits
    # Objective could be to minimize the total distance travelled by the Auditors

    # Build a dictionary with all Auditor-Site assignment possible combinations
    # Distance between Auditor and Site are randomly assigned between 50 and 300 mile range
    # Days to audit for each site is randomly assigned between 6 and 60 days
    assignments = {}
    # np.random.seed(np.random.randint(1, 100))

    daysdue = np.random.randint(1, 100) # setting a random seed to generate random timetoaudit in days
    for n in auditors:
        np.random.seed(daysdue)           # setting a random seed for every program run and also to be same days to audit per site, in belwo assignment matirx across auditors
        for s in sites:
                assignments[(n, s)] = [model.NewBoolVar('auditor%i_site%i' % (n, s)),np.random.randint(50, 300), np.random.randint(4, 30) ]


    for key, value in assignments.items():
        print (key, value[1], value[2])
    ##############################################################################
    # Constraints:
    # Each site can only have one assignment,
    # Each auditor can have a min of 2 assignments and max of 3 assignments lets say
    #
    # Each Site can be audited only once, ie.can be assigned only one Auditor
    # An audit takes 2 days to complete, so Each Auditor gets assigned atmost one Site every two weeks
    for s in sites:
        model.Add(sum(assignments[(n, s)][0] for n in auditors) == 1)

    # Assignments for auditors are equally spaced out over a month
    # audit_limit_monthly
    # time = [day10,day20,day30]
    # x = 1
    # for t in range(all_days[x-1:x+8]):
    #     x = x + 10
    # week = ['week1,week2,week3']
    # for wk in week:
    # print (type(assignments[(n, s)]))
    #     model.Add(sum(assignments[(n, s)][0] for s in sites) == 1)


    min_audits_per_auditor = (num_sites) // num_auditors
    # max_audits_per_auditor = min_audits_per_auditor + 1
    max_audits_per_auditor = audit_limit_monthly
    for n in auditors:
        num_audits_assigned = sum(
            assignments[(n, s)][0] for s in sites)
        model.Add(min_audits_per_auditor <= num_audits_assigned)
        model.Add(num_audits_assigned <= max_audits_per_auditor)


    # Prioritize site assigment overall or per auditor ?









    # get the assignment array per auditor
    # auditor_travel = {}
    # for n in auditors:
    #     auditor_travel[(n, s)] = (assignments[(n, s)] for s in sites)
    #
    # for key, value in auditor_travel.items():
    #     print (key, "::::", value)
    #
    # print(type(distance))
    # print(type(final_assigned))
    # print (sum(assignments[(n, s)][1] for n in auditors for s in sites))
    # print(sum(assignments[(n, s)][1] for s in sites))
    # for item in gen():
    #     print(item)

    # Minimize the total distance travelled by the auditors, need not be the minimum distance travelled by individual auditor
    # print(sum(assignments[(n, s)][1] for s in sites))

    model.Minimize(
        sum(assignments[(n, s)][1] * assignments[(n, s)][0] for n in auditors for s in sites))
        # sum(assignments[(n, s)][1] for n in auditors for s in sites))
    # sum(distance[(n, s)] * assignments[(n, s)] for n in auditors for s in sites))

    # Calling the solver

    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    if status == cp_model.FEASIBLE:
        print ('FEASIBLE')
    elif status == cp_model.OPTIMAL:
        print ('OPTIMAL - Minimizing Total distance travelled by all auditors')
    elif status == cp_model.INFEASIBLE:
        print ('INFEASBILE')
    elif status == cp_model.MODEL_INVALID:
        print ('MODEL_INVALID')
    else:
        print('SOLUTION UNKNOWN')

    for n in auditors:
        for s in sites:
            if solver.Value(assignments[(n, s)][0]) == 1:
                print('Auditor', n, 'audits Site', s, 'daystoaudit', assignments[(n, s)][2])
    print()



    # Statistics.
    print()
    print('Statistics')
    print('  - conflicts       : %i' % solver.NumConflicts())
    print('  - branches        : %i' % solver.NumBranches())
    print('  - wall time       : %f s' % solver.WallTime())
    # print('  - solutions found : %i' % solution_printer.solution_count())
########################################################################################

if __name__ == '__main__':
    main()












