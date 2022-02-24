# main file for camera
from cam.src.personCounter import personCounter
import uuid

perCount = personCounter(uuid.uuid4(), roomId=1)

perCount.run()
