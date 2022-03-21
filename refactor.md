This is the note when I'm working on the code.

### Working on *main.py*
It seems that the class name Main doesn't represent the purpose, I rename it to *Autodrive*.
And put the default `if __name__=='__main__'`: in the main code below.
> commit

Rename main method to start to make it easier to understand.
> commit

It turns out that we need to install some python modules.
So I create "requirements.txt" so we can use 'pip install -r requirements.txt" to install all module dependencies.
> commit

Refactor print_train_info method out to make the long print statement easier to read
> commit

3/18/2022
### main.py
* add some comments while reading the code
* move signal_speed_dict as class constant

* create Screenshot.py for everything to do with screenshot (capture screenshot, OCR, detect color, get throttle position to get current speed)
* changing several methods in Autodrive class

3/19/2022
### main.py
In determine_following_speed method, I think there is no need to keep self.approaching_station in this class.
Now, we can read this directly from Screenshot. So let's remove them by doing the following.
* move screen_shot object to __init__ so we can access it anywhere in Autodrive class.
* replace self.approaching_station with self.screen_shot.is_approaching_station()
This will make code slower because self.screen_shot.is_approaching_station() will call OCR.
But the code is cleaner and easier to understand. We'll solve the problem of slowness in the next step.
> commit

TODO: create some caching mechanisms in Screenshot so we don't have to call OCR which is pretty slow.
I'll use a dictionary to keep cache values and reset every time we capture a new screen shot.

Fix small bug of screen_shot.get_distance_till_next_station() distance not being numeric but running "self.cache['distance_till_next_station'] = distance" anyways, causing an error.

Fix bug of Autodrive.print_train_info() running screen_shot.is_approaching_station() running OCR before the screenshot is captured.

* Small cleanups
    Remove unused imports in Main.py and Follow_speed_limit.py
    Removed unused Autodrive.is_require_AWS_aknowledge() (because now use ScreenShot.get_current_speed())
    Removed unused Follow_speed.get_current_speed() (because now use ScreenShot.get_current_speed())

3/20/2022
### screen_shot.py

3/21/2022
self.loading อาจจะไม่จำเป็น
ถ้าอ่านเอาจาก need_load กับ need_close โดยตรง
เราก็จะไม่จำเป็นต้องมีข้อมูลชุดนี้อีก

แล้วไปแทนที่ self.loading ด้วยข้อมูลอื่นแทน

ดูแล้ว change_speed กับ follow_speed น่าจะยุบมารวมใน Autodrive ได้
เพราะดูชื่อแล้วไม่เหมือนเป็น class หรือ object
ยังไม่ได้ implement ใส่ไว้เป็น plan เอาไว้ก่อน

