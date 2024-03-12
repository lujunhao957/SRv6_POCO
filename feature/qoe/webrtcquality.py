from feature.qoe.webrtcjitterBD import get_jitter_BD
from feature.qoe.webrtcjitterCBD import get_jitter_CBD
from feature.qos.qos_calc import  get_qos_parameter
from path.pathinfo import pathinfo


def path_meet_webrtc_quality(path,webrtcquality):
    # qos_data=multi_vpath_qos_cal(path)
    resolution=webrtcquality['resolution']
    fps=webrtcquality['fps']
    buffer_duration=webrtcquality['buffer_duration']
    buffer_duration_probability = webrtcquality['buffer_duration_probability']
    continuous_playback_duration = webrtcquality['continuous_playback_duration']
    continuous_playback_duration_probability = webrtcquality['continuous_playback_duration_probability']
    bdp=cal_buffer_duration_probability(path,resolution,fps,buffer_duration)
    cpdp=cal_continuous_playback_duration_probability(path,resolution,fps,continuous_playback_duration)
    path_info=pathinfo(path,bdp,cpdp)
    return path_info


def cal_buffer_duration_probability(path,resolution,fps,buffer_duration):
    qos_parameter=get_qos_parameter(path)
    bdp=get_jitter_BD(qos_parameter.get_std(),qos_parameter.get_avg(),fps,resolution,buffer_duration)
    return bdp

def cal_continuous_playback_duration_probability(path,resolution,fps,continuous_playback_duration):
    qos_parameter = get_qos_parameter(path)
    cpdp = get_jitter_CBD(qos_parameter.get_std(), qos_parameter.get_avg(), fps, resolution, continuous_playback_duration)
    return cpdp