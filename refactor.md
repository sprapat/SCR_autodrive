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
### ScreenShot.py
Remove the use of OCR in favor of image similarity, I might edit the threash for more accurate result.
And more testing tomorrow needed.

3/21/2022
self.loading อาจจะไม่จำเป็น
ถ้าอ่านเอาจาก need_load กับ need_close โดยตรง
เราก็จะไม่จำเป็นต้องมีข้อมูลชุดนี้อีก

แล้วไปแทนที่ self.loading ด้วยข้อมูลอื่นแทน

ดูแล้ว change_speed กับ follow_speed น่าจะยุบมารวมใน Autodrive ได้
เพราะดูชื่อแล้วไม่เหมือนเป็น class หรือ object
ยังไม่ได้ implement ใส่ไว้เป็น plan เอาไว้ก่อน
=======
### ScreenShot.py
* Fixed ScreenShot.get_distance_till_next_station1() bugs where when the distance is anchored at the left most point, meaning if the distance is have ones digit (1.23), the 1 will be at the same point as the 1 on if the distance is tens digit (16.23).
So I need seperate positions for all digits in each cases.
* Removed unused methods (the old get_distance_till_next_station and OCR)
* get the thresh in ScreenShot.compare_to_existing_image() to be a parameter rather than being hard coded (due to different images requiring different thresh)
* Create ScreenShot.get_min_of_values(mon) for loop of every element and return which one have the lowest image similarity err
*Remove pytessaract import and command location set
## Other
* Change all distance_num photos

3/22/2022

### Screenshot.py
* ScreenShot.get_distance_till_next_station1() -> ScreenShot.get_distance_till_next_station()
* add 80 mph to speed_limits

* ScreenShot.need_close_door() to check under_signal_restriction to not be red
* use convert_to_BW_image()



* 
=======
Papa note
* create a few utility functions
* at first, I think there is only 1 threshold to create a binary image but it turns out that there are more than one. I will try to understand the code and refactor accordingly.
* so I decided to move the cv2.imread from both need_load_passenger_action and need_close_door because we shouldn't reread the file with every comparison. We should read these files once in __init__ and use it later.
* implementing PAPA_MACHINE condition to make code run on papa's machine. (instead of using capturing screen, use saved screenshot instead)
* get_distance_till_next_station1 is a bit strange that not only return distance but also can return False
  code is also complicated. From what I read, the method returns False when the distance is more than 0.2. I think this part can be done somewhere else.
* then I think that perhaps I can use namedtuple to easier understand the mon (4-member list of coordinate and size).

### main.py
 Dew's note
* Change 


self.signal_restricted_speed = self.SIGNAL_SPEED_DICT[self.aspect]
self.under_signal_restriction = self.is_under_signal_restriction()

    to be before 

self.screen_shot.need_close_door(self.under_signal_restriction) 

* add self.type(self.signal_restricted_speed) == bool and self.signal_restricted_speed == False to every "self.signal_restricted_speed == False"
*  add self.type(self.signal_restricted_speed) != bool and self.signal_restricted_speed != False to every "self.signal_restricted_speed != False"
because if self.signal_restricted_speed is equal to 0 then it would be equal to False
* add more info in Autodrive.print_train_info()
*remove "self.type(self.signal_restricted_speed)" bug

3/23/2022
Papa's note
### main.py
back to main.py again and see whether the main loop in start method is clean.
I'd like to remove self.have_AWS because we should be able to read this from screenshot.
So I start to change self.have_AWS to self.screen_shot.is_required_AWS_acknowledge()
> commit

Similar to self.have_AWS, I think we can remove self.aspect as well.
> commit

Now, it's self.under_signal_restriction's turn to be removed.
> commit

The rest is a bit difficult for me to remove. Have to understand more about the code.
Will add comment along the way.

then I read method determine_following_speed.
I see that I can simplify 'if clause' from this
````
# train is approaching station, maximum speed limit will be 45
if self.screen_shot.is_approaching_station() == True:
    if self.speed_limit < 45:
        return self.speed_limit
    return 45
````
to this
````
# train is approaching station, maximum speed limit will be 45
if self.screen_shot.is_approaching_station() == True:
    return min(self.speed_limit, 45)
````
> commit

Then refactor determine_following_speed a bit more to make code look like this.
````
# if train is not approaching a station but under signal_restricted_speed, maximum speed limit will be self.signal_restricted_speed (can be less)
if type(self.signal_restricted_speed) != bool and self.is_under_signal_restriction() != False:
    return min(self.speed_limit, self.signal_restricted_speed)
````

I think that we have this long comparison
`if type(self.signal_restricted_speed) != bool and self.is_under_signal_restriction() != False:`
because self.signal_restricted_speed contains mixed type of value. It can be boolean or real speed value.
I'll see whether I can make it separated.

But I notice that self.disable_control seems to be a synonym of at_station.
We can read it as if we are at station, we must disable control.

So I replace all references to self.disable_control to self.screen_shot.is_at_station()

> commit

### is_under_signal_restriction
is_under_signal_restriction should return either True or False.
And if it's true, then we can ask for the signal restriction.

When read the method is_under_signal_restriction(self), I have to understand self.signal_restricted_speed.
Then I see the source of mixed value, it's **SIGNAL_SPEED_DICT**.
=======
Dew's note
* Fix bugs created by yesterdays' "add self.type(self.signal_restricted_speed) != bool and **self.signal_restricted_speed != False** to every "self.signal_restricted_speed != False"" if the self.signal_restricted_speed is equal to 0 then it should satisfy but it doesn't because it still is equal to False,
So today I remove **self.signal_restricted_speed != False** entirely so it just is self.type(self.signal_restricted_speed) != bool:

* Add more info to print_train_info()

3/24/2022
### main.py
=======
Dew's note
* So today I decided to remove under_signal_restriction entirely cuz it's only used in determine_following_speed() and it's purpose really is to check that AWS had been hit by signal (which I decided to change for the signal_restricted_speed to kick in immediately instead of waiting for AWS) and (to check whether the train is at station (which doesn't matter because the controls would be disable anyways) or the train is loading (which again the controls would disable) or that the AWS had already hit last time (which again doesn't matter))
    TL;DR: it's useless so I remove it
* move self.signal_restricted_speed to signal_restricted_speed in determine_following_speed() as it's the only place that is used
* rewrite Autodrive.start()

3/25/2022
======
Dew's note
* remove unused files

3/26/2022
======
Dew's note
* create self.get_position_for_getting_distance_num() to replace [990,30,___,6] because every number character size is 9 pixel and decimal point size is 4 pixels
* change distance_num numbers size from [990,30,___,6] to [1000,20,___,6]

======
Papa's note
* add code to read environment variable to determine machine.
  So we don't have to change the PAPA_MACHINE inside the code.
  I'll just set os environment 'PAPA_MACHINE' to 1, the code will know that it's PAPA_MACHINE
  