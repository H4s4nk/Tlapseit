# Tlapseit
## V1.5.4
[English](#English)
[فارسی](#فارسی)

### English
**time lapse app for you and more**

> When you can't find the program you want, create(code) it.

this app helps you to creat timelapse of your pc screen when you are working or even playing video game.

**Python 3.8** & [Requirements](/requirements.txt) 

***How to use***

It has 3 modes:
1. Infinit capture
    - In this mode app will capture infinit number of images until you press end capture
2. Clip limit
    - In this mode app will capture images based on your final clip; eg: you wants 30s final clip whit 15fps and 10s of interval, so app will run fo 4500s or 75min and 450 of screenshots.
3. Work limit
    - like the previuse mode, this mode will capture for exact time exept its based on your work time not the clip. It means you gonna work for 2 hours and you sat interval of 10 and fps on 15, so your final clip will be 48s.

- For those who wants to know:
    clip lentgh(second) = work time(seconds) * fps 
    number of screenshots = clip lentgh(second) * fps
    work time(second) = clip lentgh(second) * fps * interval

Feel free to share bugs-ask for features and more...

### to Do:
- [ ] creat logo :sad:
- [ ] change app theme 
- [ ] save and load setting
- [ ] creat time lapse frome captured images
- [ ] add more video encoder
- [ ] delet temp images after merge
- [ ] calculate final video size