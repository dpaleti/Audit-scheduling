# Audit-scheduling
A Optimization algorithm to Assign and Schedule Auditors to Site locations for conducting audits. 
Using google OR tool set https://developers.google.com/optimization/introduction/overview

      #Strucutre of the Algorithm
      # 1.Creates cp model
      # 2.Declares variables
      # 3.Add constraints to the model
      # 4. Defines Objective functin(minimize)
      # 5.Runs the solver

      # Problem - There are Sites to audit on a montly basis and Auditors (typically lesser than # of Sites to audit) that need to be assigned
      # to conduct the audits. Also, Assignment for each Auditor should have a schedule based on the urgency (due date) of Sites to be audited
      # There are two dimensions to this problem, One is the DISTANCE an auditor needs to travel to the Sites, and a TIME dimension, the sites # need to prioritized based on the Due days

      # The algorithm should provide the schedule a month out, based on sites to audit and their due dates 
      # Every site has a time to audit in days,
      # Assignment table
      # auditor | site | distance | timetoaudit | next30dayssequence | calendardate



      # Assumptions
      # Assigning Audits evenly across Auditors , ie. Each Auditor gets same # of audits to complete
      # Its could always be at most one extra audit per auditor after evenly distributing the audits
      # Build a dictionary with all Auditor-Site assignment possible combinations
      # Distance between Auditor and Site are randomly assigned between 50 and 300 mile range
      # Days to audit for each site is randomly assigned between 6 and 60 days


      # Constraints:
      # Each site can only have one assignment,
      # Each auditor can have a min of 2 assignments and max of 3 assignments lets say
      # Each Site can be audited only once, ie.can be assigned only one Auditor
      # An audit takes 2 days to complete, so Each Auditor gets assigned atmost one Site every two weeks


      # Objective is to to minimize the TOTAL DISTANCE TRAVELLED by the Auditors
      # Minimize the total distance travelled by the auditors, need not be the minimum distance travelled by individual auditor
      
      # Sample Output:
      OPTIMAL - Minimizing Total distance travelled by all auditors
      Auditor 0 audits Site 0 daystoaudit 4
      Auditor 0 audits Site 4 daystoaudit 5
      Auditor 0 audits Site 6 daystoaudit 10
      Auditor 1 audits Site 2 daystoaudit 25
      Auditor 1 audits Site 3 daystoaudit 24
      Auditor 1 audits Site 7 daystoaudit 24
      Auditor 2 audits Site 1 daystoaudit 29
      Auditor 2 audits Site 5 daystoaudit 9


      Statistics
        - conflicts       : 1260
        - branches        : 1391
        - wall time       : 0.031666 s

      Process finished with exit code 0
