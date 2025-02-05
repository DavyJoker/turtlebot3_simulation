import rclpy
from rclpy.node import Node

from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import OccupancyGrid
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
import random

import sys

class GoalPublisher(Node):
    def __init__(self):
        super().__init__('GoalPublisher')
        self.publisher_ = self.create_publisher(PoseStamped, 'goal_pose', 10)
        self.get_logger().info('The navigation node is started.')

        self.costmap = None
        self.map_width = 0
        self.map_height = 0
        self.goal_sent = False

        self.create_subscription(OccupancyGrid, '/global_costmap/costmap', self.map_callback, 10)
        self.action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        self.get_logger().info('Waiting for map data...')

        self.timer = self.create_timer(2.0, self.random_goal)

    def map_callback(self, msg):
        self.costmap = msg.data
        self.map_width = msg.info.width
        self.map_height = msg.info.height

        self.get_logger().info('Map data received and processed.')
 
    def random_goal(self):
        if self.costmap is None or self.goal_sent:
            return

        while True:
            x = random.randint(0, self.map_width - 1)
            y = random.randint(0, self.map_height - 1)

            if self.costmap[y * self.map_width + x] == 0:
                world_x = x * 0.05
                world_y = y * 0.05

                self.send_goal(world_x, world_y)
                break

    def send_goal(self, x, y):
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.pose.position.x = float(x)
        goal_msg.pose.pose.position.y = float(y)
        goal_msg.pose.pose.orientation.w = 1.0

        self.goal_sent = True
        self.get_logger().info(f'Sent goal: x={x}, y={y}')

        self.action_client.wait_for_server()
        self.send_goal_future = self.action_client.send_goal_async(goal_msg)
        self.send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected.')
            self.goal_sent = False
            return

        self.get_logger().info('Goal accepted.')
        self.result_future = goal_handle.get_result_async()
        self.result_future.add_done_callback(self.goal_result_callback)
    
    def goal_result_callback(self, future):
        result = future.result()
        if result:
            self.get_logger().info('Goal reached, generating new goal...')
            self.goal_sent = False

def main(args=None):
    rclpy.init(args=args)
    navigation_node = GoalPublisher()
    rclpy.spin(navigation_node)
    navigation_node.destroy_node()
    rclpy.shutdown()
if __name__ == '__main__':
    main()