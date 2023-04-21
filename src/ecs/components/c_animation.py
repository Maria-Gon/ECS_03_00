from typing import List


class CAnimation:
    def __init__(self, animations: dict) -> None:
        self.number_frames = animations['number_frames']
        self.animations_list: List[AnimationData] = []
        for anim in animations['list']:
            anim_data = AnimationData(anim['name'],anim['start'],
                                      anim['end'],anim['framerate'])
            self.animations_list.append(anim_data)

        self.cur_anim = 0
        self.cur_anim_time  = 0
        self.curr_frame = self.animations_list[self.cur_anim].start

class AnimationData:
    def __init__(self, name: str, start: int, end: int, framerate: float) -> None:
        self.name = name
        self.start = start
        self.end = end
        self.framerate = 1.0/framerate