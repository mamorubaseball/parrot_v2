from olympe.messages import gimbal

def set_gimbal(drone,angle):
    drone(gimbal.set_target(
    gimbal_id=0,
    control_mode="position",
    yaw_frame_of_reference="none",   # None instead of absolute
    yaw=0.0,
    pitch_frame_of_reference="absolute",
    pitch=-angle,
    roll_frame_of_reference="none",     # None instead of absolute
    roll=0.0,
)).wait()
