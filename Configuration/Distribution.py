# standard library
import os 
import yaml as yaml

# ROS
from rclpy.node import Node
import rclpy

# ROS messages
from motion_msgs.msg import LinkGroup, JointGroup, LinearParams, Home

class ParamDistributor(Node):

    # Publishers

    link_config_pub : rclpy.publisher.Publisher = None
    joint_config_pub : rclpy.publisher.Publisher = None
    linear_config_pub : rclpy.publisher.Publisher = None
    home_config_pub : rclpy.publisher.Publisher = None

    # File configuratio
    path : str = None
    config_file : dict = None
    config : dict = None

    def __init__(self, *args, **kwargs):
        super().__init__("Distributor")
        self.get_logger().info("Distribution initialized")

        self.path = os.getcwd()
        self.path = os.path.join(self.path,"src","command_gui", "Configuration", "config.yaml")

        self.link_config = self.create_publisher(
            LinkGroup,
            "config_link_group",
            10)

        self.joint_config = self.create_publisher(
            JointGroup,
            "config_joint_group",
            10)

        self.linear_config = self.create_publisher(
            LinearParams,
            "config_linear_params",
            10)

        self.home_config = self.create_publisher(
            Home,
            "config_home",
            10)

        self.config_file = open(self.path, "r")
        self.config = yaml.safe_load(self.config_file)

    def publish_config(self):

        self.get_logger().info("Publishing configuration")
        self.publish_link_config()
        self.publish_joint_config()
        self.publish_linear_config()
        self.publish_home_config()

    def write_config(self, config : dict = None):

        if config is None:
            config = self.config

        self.get_logger().info("Writing configuration to file")
        with open(self.path, "w") as f:
            yaml.dump(config, f)

    def publish_link_config(self):

        link_config = LinkGroup()

        link_config.l1 = self.config["links"]["l1"]
        link_config.l2 = self.config["links"]["l2"]
        link_config.l3 = self.config["links"]["l3"]

        self.link_config.publish(link_config)

    def publish_joint_config(self):

        joint_config = JointGroup()

        joint_config.j1.min = self.config["joint_limits"]["j1"]["min"]
        joint_config.j1.max = self.config["joint_limits"]["j1"]["max"]

        joint_config.j2.min = self.config["joint_limits"]["j2"]["min"]
        joint_config.j2.max = self.config["joint_limits"]["j2"]["max"]

        joint_config.j3.min = self.config["joint_limits"]["j3"]["min"]
        joint_config.j3.max = self.config["joint_limits"]["j3"]["max"]

        joint_config.j4.min = self.config["joint_limits"]["j4"]["min"]
        joint_config.j4.max = self.config["joint_limits"]["j4"]["max"]

        joint_config.j5.min = self.config["joint_limits"]["j5"]["min"]
        joint_config.j5.max = self.config["joint_limits"]["j5"]["max"]

        self.joint_config.publish(joint_config)

    def publish_linear_config(self):

        linear_config = LinearParams()

        linear_config.p = self.config["linear_IK_params"]["P"]
        linear_config.i = self.config["linear_IK_params"]["I"]
        linear_config.d = self.config["linear_IK_params"]["D"]

        self.linear_config.publish(linear_config)

    def publish_home_config(self):

        home_config = Home()

        home_config.home.t1 = self.config["home_position"]["j1"]
        home_config.home.t2 = self.config["home_position"]["j2"]
        home_config.home.t3 = self.config["home_position"]["j3"]
        home_config.home.t4 = self.config["home_position"]["j4"]
        home_config.home.t5 = self.config["home_position"]["j5"]

        self.home_config.publish(home_config)

    def set_link_config(self, l1 : float, l2 : float, l3 : float):

        self.config["links"]["l1"] = l1
        self.config["links"]["l2"] = l2
        self.config["links"]["l3"] = l3

    def set_joint_config(self, joint_id : int, min : float, max : float):

        self.config["joint_limits"][f"j{joint_id}"]["min"] = min
        self.config["joint_limits"][f"j{joint_id}"]["max"] = max

    def set_linear_config(self, p : float, i : float, d : float):

        self.config["linear_IK_params"]["P"] = p
        self.config["linear_IK_params"]["I"] = i
        self.config["linear_IK_params"]["D"] = d

    def set_home_config(self, j1 : float, j2 : float, j3 : float, j4 : float, j5 : float):

        self.config["home_position"]["j1"] = j1
        self.config["home_position"]["j2"] = j2
        self.config["home_position"]["j3"] = j3
        self.config["home_position"]["j4"] = j4
        self.config["home_position"]["j5"] = j5