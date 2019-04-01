# Emitter() Animation

*By Steve Mulanax 4/1/2019*

A strip animation written in Python with particle system emitters.

Watch a video demo describing the use of this class here:
[https://www.youtube.com/watch?v=_UtHC1IhKxg](https://www.youtube.com/watch?v=_UtHC1IhKxg)

#### Sample YAML Project

```yaml
# emitter_sample.yml
#
# Command line:
# bp emitter_sample.yml

shape: 32

palettes:
  rocket: ['gold 4', [70,10,0], 'red 4']
  blues:  [
            [130, 130, 227],
            [46, 46, 209],
            [25, 25, 112],
            [18, 18, 84],
            [14, 14, 63],
            [9, 9, 42],
            [5, 5, 21],
          ]

animation:
  typename: $bpa.strip.Emitter
  bgcolor:  [0, 0, 2] # deep blue
  emitters: [
              # e_pos  e_dir  e_vel  e_range  e_color  p_pallete
              # -----  -----  -----  -------  -------  ---------
              [ 0,     1,     -0.25, 4,       null,    rocket    ],
              [ 0,     -1,    0.5,   5,       200,     blues     ],
              [ 0,     0,     0.33,  2.5,     green,   green     ],
            ]
  aperture: 0.75
  starts_at_once: 5
  bd_mean: -32
  bd_mu: 10
```

