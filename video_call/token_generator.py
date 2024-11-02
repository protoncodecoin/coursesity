"""Video Call Generator"""

import random
import time
from typing import Optional
from django.conf import settings

from agora_token_builder import RtcTokenBuilder, RtmTokenBuilder

ALPHABETS: list[str] = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
]


def video_token_generator() -> str:
    """Generate a short unique token for a video conference"""
    token: str = str()

    for index in range(1, 10):
        if index != 9 and index % 3 == 0:
            chosen_letter = random.choice(ALPHABETS)
            token += f"{chosen_letter}-"
        else:
            chosen_letter = random.choice(ALPHABETS)
            token += chosen_letter
    return token


def buildRTCToken(
    channel_name: str,
    uid: int,
    expTimeInSeconds: Optional[int] = 3600 * 24,
    user_role: Optional[int] = 1,
) -> str:
    appId: str = settings.APP_ID
    appCertificate: str = settings.APP_CERTIFICATE
    channelName: str = channel_name
    uid: str = uid
    expirationTimeInSeconds: int = expTimeInSeconds
    currentTimeStamp: int = time.time()
    privilegeExpiredTs: float = currentTimeStamp + expirationTimeInSeconds
    role: int = user_role  # host
    # account = request.user.email

    token: str = RtcTokenBuilder.buildTokenWithUid(
        appId, appCertificate, channelName, uid, role, privilegeExpiredTs
    )

    return token
