# PetDraw

![petdraw.png](https://github.com/Kolhun/PetDraw/blob/master/petdraw.png)
![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)

# Description 

Thesis on the Django framework for Urbana University using AI technology [IOPaint](https://github.com/Sanster/IOPaint?ysclid=m2iwl121js750648984)

# Quick Start

To install, just enter the following commands into the console
```
pip install -r requirements.txt
```
or
```
pip install django
pip install iopaint
```
The download will be long, be patient...
That's enough, now you can click on the link from the terminal with django and try the project in action
Now run the Django wrapper separately in the configuration (help-at the top in Pycharm) using the run with the **runserver** parameter. After that, enter the following command through the console
```
iopaint start --model=lama --device=cpu --port=5000
```
That's it, you can start using IOPaint by opening [http://localhost:5000](http://localhost:5000) in your web browser.

All models will be loaded automatically at startup. If you want to change the download directory, you can add --model-dir. Additional documentation can be found [here](https://www.iopaint.com/install/download_model)
