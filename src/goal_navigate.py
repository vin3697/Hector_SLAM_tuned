#!/usr/bin/python3
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from math import radians, degrees
from actionlib_msgs.msg import *
from geometry_msgs.msg import Point   

class NavigateToGoal:
    """ This is a class that encorporates the functionality to navigate the robot to its
    goal location by sending coordinates to the ROS move_base server.
    """    

    def __init__(self, xGoal,yGoal,xOri,yOri,zOri,wOri):
        self.xGoal = xGoal
        self.yGoal = yGoal
        self.xOri = xOri
        self.yOri = yOri
        self.zOri = zOri
        self.wOri = wOri
        
    def movebase_client(self):
        """ This method creates a SimpleActionClient instance and associates with it the goal 
        coordinates for the robots navigation. It sends goal and notifies the status.
        """        
        #Create a actionlib client object.
        client = actionlib.SimpleActionClient('move_base', MoveBaseAction)

        while (not client.wait_for_server(rospy.Duration.from_sec(10.0))):
            rospy.loginfo ("Waiting for the move_base action server to come up")

        goal = MoveBaseGoal()

        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()

        #Associate goal location to move_base server.
        goal.target_pose.pose.position = Point(self.xGoal, self.yGoal, 0)
        goal.target_pose.pose.orientation.x = self.xOri
        goal.target_pose.pose.orientation.y = self.yOri
        goal.target_pose.pose.orientation.z = self.zOri
        goal.target_pose.pose.orientation.w = self.wOri

        rospy.loginfo ("Sending goal location to ohmni")
        client.send_goal(goal)

        client.wait_for_result()

        if (client.get_state() == GoalStatus.SUCCEEDED):
            rospy.loginfo("Ohmni Goal Reached !")
        else:
            rospy.loginfo("Ohmni Failed to reach the destination")
