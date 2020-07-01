# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------- class: Video ------------------------------------------------------------- #

class Video:

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        post_dict: Dict
    ):
        self.video_url = None
        self.duration = None
        self.height = None
        self.width = None
        self.audio_url = None

        vid_res = self.__get_video(post_dict)

        if vid_res is None:
            return

        self.video_url = vid_res[0].strip('?source=fallback')
        self.duration = vid_res[1]
        self.height = vid_res[2]
        self.width = vid_res[3]
        self.audio_url = self.video_url.rsplit('/', 1)[0] + '/audio'


    # ------------------------------------------------------- Private methods -------------------------------------------------------- #

    def __get_video(self, post_dict: Dict) -> Optional[Tuple[str, int, int, int]]:
        try:
            video = post_dict['media']['reddit_video']
        except:
            try:
                video = post_dict['preview']['reddit_video_preview']
            except:
                return None

        try:
            return video['fallback_url'], video['duration'], video['height'], video['width']
        except:
            return None


# ---------------------------------------------------------------------------------------------------------------------------------------- #