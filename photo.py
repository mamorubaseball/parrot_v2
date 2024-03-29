from cmath import pi
from dataclasses import _DefaultFactory
from olympe.messages.camera import (
    set_camera_mode,
    set_photo_mode,
    take_photo,
    photo_progress,
)
from olympe.media import download_media, indexing_state
from logging import getLogger
import olympe
import os
import re
import tempfile
import xml.etree.ElementTree as ET
from olympe.messages import gimbal
import math

DRONE_IP = "192.168.42.1"
SKYCTRL_IP = "192.168.53.1"

olympe.log.update_config({
    "loggers": {
        "olympe": {"level": "INFO"},
        "photo_example": {
            "level": "INFO",
            "handlers": ["console"],
        },
    }
})

logger = getLogger("photo_example")

# Drone IP
DRONE_IP = os.environ.get("DRONE_IP", "192.168.42.1")
DRONE_MEDIA_PORT = os.environ.get("DRONE_MEDIA_PORT", "80")

XMP_TAGS_OF_INTEREST = (
    "CameraRollDegree",
    "CameraPitchDegree",
    "CameraYawDegree",
    "CaptureTsUs",
    # NOTE: GPS metadata is only present if the drone has a GPS fix
    # (i.e. they won't be present indoor)
    "GPSLatitude",
    "GPSLongitude",
    "GPSAltitude",
)


def take_photo_burst(drone):
    # take a photo burst and get the associated media_id
    photo_saved = drone(photo_progress(result="photo_saved", _policy="wait"))
    drone(take_photo(cam_id=0)).wait()
    if not photo_saved.wait(_timeout=30).success():
        assert False, "take_photo timedout"
    photo_progress_info = photo_saved.received_events().last().args
    media_id = photo_progress_info["media_id"]
    photo_count = photo_progress_info["photo_count"]
    # download the photos associated with this media id
    drone.media.download_dir = tempfile.mkdtemp(prefix="olympe_photo_example")
    logger.info(
        "Download photo burst resources for media_id: {} in {}".format(
            media_id,
            drone.media.download_dir,
        )
    )
    media_download = drone(download_media(media_id, integrity_check=True))
    # Iterate over the downloaded media on the fly
    resources = media_download.as_completed(expected_count=photo_count, timeout=60)
    resource_count = 0
    for resource in resources:
        logger.info(f"Resource: {resource.resource_id}")
        if not resource.success():
            logger.error(f"Failed to download {resource.resource_id}")
            continue
        resource_count += 1
        # parse the xmp metadata
        with open(resource.download_path, "rb") as image_file:
            image_data = image_file.read()
            image_xmp_start = image_data.find(b"<x:xmpmeta")
            image_xmp_end = image_data.find(b"</x:xmpmeta")
            if image_xmp_start < 0 or image_xmp_end < 0:
                logger.error(f"Failed to find XMP photo metadata {resource.resource_id}")
                continue
            image_xmp = ET.fromstring(image_data[image_xmp_start: image_xmp_end + 12])
            for image_meta in image_xmp[0][0]:
                xmp_tag = re.sub(r"{[^}]*}", "", image_meta.tag)
                xmp_value = image_meta.text
                # only print the XMP tags we are interested in
                if xmp_tag in XMP_TAGS_OF_INTEREST:
                    logger.info(f"{resource.resource_id} {xmp_tag} {xmp_value}")
    logger.info(f"{resource_count} media resource downloaded")
    assert resource_count == 14, f"resource count == {resource_count} != 14"
    assert media_download.wait(1.).success(), "Photo burst media download"


def setup_photo_burst_mode(drone):
    drone(set_camera_mode(cam_id=0, value="photo")).wait()
    # For the file_format: jpeg is the only available option
    # dng is not supported in burst mode
    assert drone(
        set_photo_mode(
            cam_id=0,
            mode="burst",
            format="rectilinear",
            file_format="jpeg",
            burst="burst_14_over_1s",
            bracketing="preset_1ev",
            capture_interval=0.0,
        )
    ).wait().success()

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

def _take_photo(drone):
    # drone.connect()
    assert drone.media(
        indexing_state(state="indexed")
    ).wait(_timeout=60).success()
    setup_photo_burst_mode(drone)
    take_photo_burst(drone)
    # drone.disconnect()

if __name__ == "__main__":
    _take_photo()