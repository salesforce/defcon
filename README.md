# defcon
SR Defcon Status Board

A HackDay project by C.J. Mihelich & Paulson McIntyre

## Install Instructions
_These instructions do NOT cover basic RPi hardening_
1) Enable internet access
1) (as root) apt-get update
1) (as root) apt-get upgrade (recommended but not required)
1) (as root) apt-get install -y git vim python-numpy python-pygame python-requests python-dateutil fonts-roboto 
1) (as pi) Unzip https://github.com/Salesforce/defcon/archive/master.zip to /home/pi
1) (as pi) Rename /home/pi/defcon-master to /home/pi/defcon
1) (as pi) Copy the [unicorn_hat_sim folder](https://github.com/jayniz/unicorn-hat-sim/tree/master/unicorn_hat_sim) to /home/pi/defcon/src/
1) (as root) pip install -r /home/pi/defcon/requirements.txt
1) (as root) cp /home/pi/defcon/defcon.service /lib/systemd/system/defcon.service 
1) (as root) chmod 644 /lib/systemd/system/defcon.service
1) (as root) chown root:root /lib/systemd/system/defcon.service 
1) (as root) systemctl daemon-reload
1) (as root) systemctl enable defcon
1) (as root) systemctl start defcon

## Running The App
_Note: The app auto starts on boot using systemd_
1) (as root) systemctl start defcon

## Dependencies

### Software
* fonts-roboto
* [Unicorn Hat Sim](https://github.com/jayniz/unicorn-hat-sim)
* See requirements.txt

### Hardware
* [Pimoroni Unicorn HAT HD](https://www.adafruit.com/product/3580)
* Raspberry Pi 3 Model B
* Micro SD Card >= 4GB
* M2.5 10mm Standoffs (recommended)

### Network
* Access to https://api.status.salesforce.com/v1
* DHCP
* Can be wired or wireless

## Data Source
* [https://api.status.salesforce.com/v1](https://api.status.salesforce.com/v1)

## Scoring
### Overview
```Score = ( <Impact Type> * <Instance Count Mult> ) + ( <Maintenance Type> * <Availability Multi> )```


### Level vs Color vs Score
| Level | Color  | Score     |
|-------|--------|-----------|
| 5     | Blue   | 0         |
| 4     | Green  | 1-127     |
| 3     | Yellow | 128-1023  |
| 2     | Orange | 1024-2047 |
| 1     | Red    | 2048-4095 |
| 0     | Black  | >=4096    |

### Impact
#### Impact Type
| Type | Score |
|------|-------|
| serviceDisruption | 2048 |
| intermittentPageLoadErrors | 1024 | 
| intermittentLoginErrors | 1024 | 
| performanceDegradation | 1024 | 
| pageLoadDelays | 1024 | 
| slowDataProcessing | 1024 | 
| performanceDegradationAsynchronousProcessingSubset | 1024 | 
| performanceDegradationAsynchronousProcessing | 1024 | 
| disruptionReadOnlySsOverRun | 512 | 
| disruptionReadOnlyInstanceRefreshOverrun | 512 |


#### Instance Count
| Count | Impact Type Score Multiplier |
|-----|---|
| 1   | 1 |
| 2+ | 2 |

### Maintenance
#### Maintenance Type
| Type                 | Score |
|----------------------|-------|
| scheduledMaintenance | 8     | 
| emergencyMaintenance | 16    | 
| switch               | 16    | 
| release              | 32    | 

#### Availability
| Type                 | Maintenance Type Score Multiplier |
|----------------------|-----------------------------------|
| unavailable | 2 | 
| readOnly | 1 | 
| available | 0 | 
| availabilityGenerallyAvailableInRead | 1 | 
| availabilityLiveAgentNotAvailable | 0.5 | 
| availabilityChatternowNotAvailable | 0.5 | 
| availabilityIntermittentReadOnly | 0.5 | 
| bulkOrgMigration | 0 | 
| availabilityBULKORGMIG-ROFORAFFECTEDORGONLY | 0 | 
| readOnlySiteSwitch | 1 | 
| readOnlyContinuousSiteSwitch | 1 | 
| eMaint | 1 | 
| fullyAvailable | 0 | 
