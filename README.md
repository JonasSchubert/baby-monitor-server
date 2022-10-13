<div style="text-align: center;">
<img height="128" src="./app.png">
</div>

# Baby Monitor - Server

> !!!\
> The [ui](https://code.sinthu-und-jonas.de/jsa/baby-monitor/ui) project is a good start to display the API provided data.\
> !!!

This projects aims to be the server for my baby monitor. It utilizes [gstreamer](https://gstreamer.freedesktop.org/), [Grove SHT31 Temperature Humidity Sensor](https://github.com/Seeed-Studio/Grove_SHT31_Temp_Humi_Sensor), a simple USB microphone with some python code to provide a video and audio stream with an sensor API to check on our newborn. Additionaly I am using the command line interface for VLC to play some lullabies.

## Instructions

### Raspberry Pi

#### Hardware

I had my old [Snips Voice Interaction Base Kit](https://wiki.seeedstudio.com/Snips_Voice_Interaction_Base_Kit/) laying in one of my drawers, so I reused all this stuff to build this baby monitor. I slightly adjusted the used devices.

- I removed the Relay (had no use for this)
- My set came with a [ReSpeaker 4 Mic Linear Array](https://wiki.seeedstudio.com/ReSpeaker_4-Mic_Linear_Array_Kit_for_Raspberry_Pi/) - but I replaced this with a [simple USB microphone](https://makersportal.com/shop/usb-microphone-for-raspberry-pi); I wanted the microphone be closer to our baby, but the Raspberry Pi further away
- I added the default [Raspberry Pi Camera module](https://projects.raspberrypi.org/en/projects/getting-started-with-picamera)

#### Software

I used the awesome [Raspberry Pi Sleep Monitor](https://github.com/srinathava/raspberry-pi-sleep-monitor) by [Srinathava](https://github.com/srinathava) as a starting point. It covered a lot, actually a little bit more then I needed. So I adjusted it.

I am using the drivers for the [seeed-voicecard](https://github.com/HinTak/seeed-voicecard), the [Grove sensors](https://github.com/Seeed-Studio/grove), command line tools for VLC. Checkout the [install script](./install.sh) for more details. Gstream provides the camera stream. Twisted is used to build the API.

Everyting is running directly on the Raspberry Pi - no container or any kind of virtualization.

### API

The server itself provides six API endpoints. VLC provides an endpoint to access the audio stream:

#### Camera

The camera can be accessed under `http://<your-local-ip>:8080/stream.mjpeg`.
It provides a stream of images provided by Gstreamer.

#### Audio

An audio stream is provided by the VLC command line tool. It starts streaming when the application starts on port `8081`.

You can subscribe to this using following URL: `http://<your-local-ip>:8081`

#### Single Picture

If you want a single picture and always the latest one, this can be accessed under `http://<your-local-ip>:8080/latest.jpeg`.

#### Climate

To read the current sensor data regarding humidity and temperature, perform a `GET` request against `http://<your-local-ip>:8080/climate`.

You will receive following object:

```json
{
  "humidity": {
    "sensor": "number",
    "unit": "%"
  },
  "temperature": {
    "cpu": "number",
    "gpu": "number",
    "sensor": "number",
    "unit": "°C"
  }
}
```

The units are always `%` for humidity and `°C` for temperature.

- `sensor` contains the actual values from `Grove` sensor
- `cpu` and `gpu` are the current temperatures for the processor - read with two different [commands](./src/ClimateResource.py)

#### Lullabies

There are two endpoints to handle lullabies.

##### GET List

The first endpoint will return a list of files under the defined path (`/mnt/lullaby-songs/`).

Read them with a `GET` request against `http://<your-local-ip>:8080/lullaby-list`.

You will receive a list of strings representing the file paths on your machine.

```json
[
  "string"
]
```

##### Handle Song

The second endpoint allows to play or stop songs, adjust the volume or mute/unmute.

You can perform a `GET` and a `POST` request against  `http://<your-local-ip>:8080/lullaby-song`.

1. `GET`

This endpoint returns the current state:

```json
{
  "mute": boolean,
  "status": "string",
  "track": "string",
  "volume": number
}
```

2. `POST`

If you want to play or stop a song you perform a `POST` request. Same for setting the volume or mute/unmute.

The body has to have the same structure as the response from the `GET` request and will return the same format:

```json
{
  "mute": boolean,
  "status": "string",
  "track": "string",
  "volume": number
}
```

To play a song, fill the property `track` with a path from the lullaby string list, set `mute` to `false` and the `volume` to something between `0...100`. (The `status` is a readonly field and has no effect) E.g.:

```json
{
  "mute": false,
  "status": "",
  "track": "/mnt/lullaby-songs/babys-favorite-lullaby.mp3",
  "volume": 35
}
```

If the song exists it will start playing. If a song is already being played this will be stopped first.

To stop a song, simply send a request body with an empty string for the track:

```json
{
  "mute": false,
  "status": "",
  "track": "",
  "volume": 35
}
```

To mute a song, but keep it playing, send a similar body:

```json
{
  "mute": true,
  "status": "",
  "track": "/mnt/lullaby-songs/babys-favorite-lullaby.mp3",
  "volume": 35
}
```

To change the volume, but keep a song playing, send a similar body:

```json
{
  "mute": false,
  "status": "",
  "track": "/mnt/lullaby-songs/babys-favorite-lullaby.mp3",
  "volume": 42
}
```

> !!!\
> Whenever the server receives a body with an empty track, it will stop playing! Always send the track, if you want to keep the song playing. Even if you just want to mute/unmute or set the volume! \
> !!!

#### Healthcheck

The server provides a simple healthcheck endpoint. Either you will have a result or none :P

```json
{
  "status": "up"
}
```

You can request the status under `http://<your-local-ip>:8080/healthcheck`.

## Author

| [<img alt="JonasSchubert" src="https://secure.gravatar.com/avatar/835215bfb654d58acb595c64f107d052?s=180&d=identicon" width="117"/>](https://code.sinthu-und-jonas.de/jonas-schubert) |
| :---------------------------------------------------------------------------------------------------------------------------------------: |
| [Jonas Schubert](https://code.sinthu-und-jonas.de/jonas-schubert) |

## License

`Baby Monitor - Server` is distributed under the MIT license. [See LICENSE](LICENSE) for details.

```
MIT License

Copyright (c) 2022 Jonas Schubert

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
