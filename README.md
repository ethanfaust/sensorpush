# What is it
Using temp sensor devices from Amazon, show how to print out sensor values
* Sensor: https://www.amazon.com/SensorPush-HTP-xw-Thermometer-Hygrometer-Water-Resistant/dp/B08PKVRJJX
* Gateway: https://www.amazon.com/SensorPush-G1-WiFi-Gateway-Anywhere/dp/B01N17RWWV

# This can be done for way cheaper
Yes. I like that they make it in USA and that they are durable
I have left these outside for years, they work great.

# Credential setup

create file in same directory `sensorpush_credentials.json`

```
{
    "username": "<to be filled>",
    "password": "<to be filled>"
}
```

## Usage
```
./print_temps.py
```

## Example Output
```
$ ./print_temps.py
current date utc: 2025-11-05T02:39:12Z
Deck Box            :  54.3  54.2  54.2  54.1  54.1 °F as of 2025-11-05T02:38:59.000Z
Mud Room            :  57.8  57.8  57.8  57.8  57.8 °F as of 2025-11-05T02:37:28.000Z
Well                :  47.8  47.7  47.7  47.7  47.7 °F as of 2025-11-05T02:38:04.000Z
Inside Parlor       :  59.0  59.0  58.9  59.0  59.0 °F as of 2025-11-05T02:39:01.000Z
```
