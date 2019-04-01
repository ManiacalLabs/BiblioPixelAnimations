from bibliopixel.animation.strip import Strip
from bibliopixel.colors import COLORS, make, palette
from bibliopixel.colors.arithmetic import color_scale, color_blend
from numpy import random, concatenate

"""
Emitter animation

By Steve Mulanax 4/1/2019

A strip animation with particle system emitters.

Watch a video describing the use of this class here:
https://www.youtube.com/watch?v=_UtHC1IhKxg

Each strip can have multiple emitters with positions and velocities
controlled by the emitters list paramter. Positions and velocities
are float values. The rendering step figures out what is visible at
each integral strip positon for a given frame.

Particles move away from an emitter starting at full brightness of a
randomly selected color. Colors are selected from the palette field
unless a particle palette is specified in the emitters list. The
particle brightness then varies in a random manner. The random
variations are chosen from a list built at initialization. The default
settings should make the particles "sparkle" and fade. The mean, mu,
and sigma fields can be altered to change the effect. The distribution
of random brightness changes is shaped like two peaks around the bd_mean
point, centered at +/-bd_mu, with their widths controlled by bd_sigma.

Particle velocities are random and based on vel_mu and vel_sigma

:param pallete: Each new emitted particle starts at a color picked from
    this list (can be overriden on a per-emittter basis)
:param emitters: List of tuples for each emitter. Each tuple:
    * position - In strip's _start to _end. Default: _start
    * direction - +1 emit toward end, -1 toward start, 0 both ways.
          Default +1
    * velocity - Emitter velocity in positions/step. Default 0
    * range - particles don't travel beyond this dist. Default: _end
    * emitter color - Use None/null if the emitter is invisible
    * particle palette - Pallete/color for particles
:param bgcolor: The background color for the animation
:param wrap: Particles wrap across ends of strip
:param aperture: Render particles within this visible distance
:param starts_at_once: Maximum number of particles that can be emitted
    at each step
:param starts_prob: Probability of a particle being emitted (0.0 never -
    1.0 always)
:param flare_prob: Probability that a particle will re-ignite on the
    strip segment
:param bd_mean: Average fade (negative) or boost (positive) per particle
    per step. The default value is computed (-2 * 256 / _size) if the
    field is not set.
:param bd_mu: Average distance from mean for the positive and negative
    variations.
:param bd_sigma: Standard deviation from mu for variations on the
    positive and negative sides. The default value is computed (mu *
    0.25) if the field is not set.
:param vel_mu: Average velocity of particles. Positive is away from
    emitter.
:param vel_sigma: Standard deviation from mu for particle velocity
"""


class Emitter(Strip):
    COLOR_DEFAULTS = ('palette', 'gold'),

    def make_bd(self):
        "Make a set of 'shaped' random #'s for particle brightness deltas (bd)"
        self.bd = concatenate((
            # These values will dim the particles
            random.normal(
                self.bd_mean - self.bd_mu, self.bd_sigma, 16).astype(int),
            # These values will brighten the particles
            random.normal(
                self.bd_mean + self.bd_mu, self.bd_sigma, 16).astype(int)),
            axis=0)

    def make_vel(self):
        "Make a set of velocities to be randomly chosen for emitted particles"
        self.vel = random.normal(self.vel_mu, self.vel_sigma, 16)
        # Make sure nothing's slower than 1/8 pixel / step
        for i, vel in enumerate(self.vel):
            if abs(vel) < 0.125 / self._size:
                if vel < 0:
                    self.vel[i] = -0.125 / self._size
                else:
                    self.vel[i] = 0.125 / self._size

    def __init__(
            self, *args,

            emitters=None,
            bgcolor=COLORS.black,
            wrap=True,
            aperture=0.5,
            starts_at_once=6,
            starts_prob=0.33,
            flare_prob=0.05,
            bd_mean=None,
            bd_mu=80,
            bd_sigma=None,
            vel_mu=1,
            vel_sigma=0.25,

            **kwds):
        "Process all the arguments and set up for the run"

        super().__init__(*args, **kwds)

        self.half_size = float(self._size) / 2.0

        if emitters is None:
            emitters = [(None, None, None, None, None, None)]
        self.emitters = []
        self.has_e_colors = False
        self.has_moving_emitters = False
        for e_pos, e_dir, e_vel, e_range, e_color_str, e_pal_list in emitters:
            if e_pos is None:
                e_pos = self._start
            if e_dir is None:
                e_dir = 1
            if e_range is None:
                e_range = self._size
            if e_vel is None:
                e_vel = 0
            if e_vel != 0:
                self.has_moving_emitters = True
            if e_pos >= (self._end + 1):
                raise ValueError('Emitter Position %d >= end+1 (%d)' %
                                 (e_pos, self._end + 1))
            if e_pos < self._start:
                raise ValueError('Emitter position %d < start (%d)' %
                                 (e_pos, self._start))
            if e_color_str is not None:
                e_color = make.color(e_color_str)
                self.has_e_colors = True
            else:
                e_color = None
            if e_pal_list is None:
                e_pal = self.palette  # passed in or default
            else:
                e_pal = palette.Palette(make.colors(e_pal_list))
            self.emitters.append(
                (e_pos, e_dir, e_vel, e_range, e_color, e_pal))
        self.bgcolor = bgcolor
        self.wrap = wrap
        if aperture < 0:
            raise ValueError('Render aperture %g < 0' % (aperture))
        self.aperture = aperture
        self.starts_at_once = starts_at_once
        self.starts_prob = starts_prob
        self.flare_prob = flare_prob
        self.step_flare_prob = self.flare_prob // self._size
        if bd_mean is None:
            self.bd_mean = -2 * 256 // self._size
        else:
            self.bd_mean = bd_mean
        self.bd_mu = 80
        if bd_sigma is None:
            self.bd_sigma = self.bd_mu * 0.25
        else:
            self.bd_sigma = bd_sigma
        self.vel_mu = vel_mu
        self.vel_sigma = vel_sigma

        # Random number lists
        self.make_bd()
        self.make_vel()

        # List of tuples for flying/walking particles
        # (velocity, position, steps to live, color, brightness)
        self.particles = []

    def move_particles(self):
        """
        Move each particle by it's velocity, adjusting brightness as we go.
        Particles that have moved beyond their range (steps to live), and
        those that move off the ends and are not wrapped get sacked.
        Particles can stay between _end and up to but not including _end+1
        No particles can exitst before start without wrapping.
        """
        moved_particles = []
        for vel, pos, stl, color, bright in self.particles:

            stl -= 1    # steps to live
            if stl > 0:

                pos = pos + vel
                if vel > 0:
                    if pos >= (self._end + 1):
                        if self.wrap:
                            pos = pos - (self._end + 1) + self._start
                        else:
                            continue  # Sacked
                else:
                    if pos < self._start:
                        if self.wrap:
                            pos = pos + self._end + 1 + self._start
                        else:
                            continue  # Sacked

                if random.random() < self.step_flare_prob:
                    bright = 255
                else:
                    bright = bright + random.choice(self.bd)
                    if bright > 255:
                        bright = 255
                    # Zombie particles with bright<=0 walk, don't -overflow
                    if bright < -10000:
                        bright = -10000

                moved_particles.append((vel, pos, stl, color, bright))

        self.particles = moved_particles

    def move_emitters(self):
        """
        Move each emitter by it's velocity. Emmitters that move off the ends
        and are not wrapped get sacked.
        """
        moved_emitters = []
        for e_pos, e_dir, e_vel, e_range, e_color, e_pal in self.emitters:

            e_pos = e_pos + e_vel
            if e_vel > 0:
                if e_pos >= (self._end + 1):
                    if self.wrap:
                        e_pos = e_pos - (self._end + 1) + self._start
                    else:
                        continue  # Sacked
            else:
                if e_pos < self._start:
                    if self.wrap:
                        e_pos = e_pos + self._end + 1 + self._start
                    else:
                        continue  # Sacked

            moved_emitters.append(
                (e_pos, e_dir, e_vel, e_range, e_color, e_pal))

        self.emitters = moved_emitters

    def start_new_particles(self):
        """
        Start some new particles from the emitters. We roll the dice
        starts_at_once times, seeing if we can start each particle based
        on starts_prob. If we start, the particle gets a color form
        the palette and a velocity from the vel list.
        """
        for e_pos, e_dir, e_vel, e_range, e_color, e_pal in self.emitters:
            for roll in range(self.starts_at_once):
                if random.random() < self.starts_prob:  # Start one?
                    p_vel = self.vel[random.choice(len(self.vel))]
                    if e_dir < 0 or e_dir == 0 and random.random() > 0.5:
                        p_vel = -p_vel
                    self.particles.append((
                        p_vel,  # Velocity
                        e_pos,  # Position
                        int(e_range // abs(p_vel)),  # steps to live
                        e_pal[
                            random.choice(len(e_pal))],  # Color
                        255))  # Brightness

    def visibility(self, strip_pos, particle_pos):
        """
        Compute particle visibility based on distance between current
        strip position being rendered and particle position. A value
        of 0.0 is returned if they are >= one aperture away, values
        between 0.0 and 1.0 are returned if they are less than one
        aperature apart.
        """
        dist = abs(particle_pos - strip_pos)
        if dist > self.half_size:
            dist = self._size - dist
        if dist < self.aperture:
            return (self.aperture - dist) / self.aperture
        else:
            return 0

    def render_particles(self):
        """
        Render visible particles at each strip position, by modifying
        the strip's color list.
        """
        for strip_pos in range(self._start, self._end + 1):

            blended = COLORS.black

            # Render visible emitters
            if self.has_e_colors:
                for (e_pos, e_dir, e_vel, e_range,
                     e_color, e_pal) in self.emitters:
                    if e_color is not None:
                        vis = self.visibility(strip_pos, e_pos)
                        if vis > 0:
                            blended = color_blend(
                                blended,
                                color_scale(e_color, int(vis * 255)))

            # Render visible particles
            for vel, pos, stl, color, bright in self.particles:
                vis = self.visibility(strip_pos, pos)
                if vis > 0 and bright > 0:
                    blended = color_blend(
                        blended,
                        color_scale(color, int(vis * bright)))

            # Add background if showing
            if (blended == COLORS.black):
                blended = self.bgcolor

            self.color_list[strip_pos] = blended

    def step(self, amt=1):
        "Make a frame of the animation"
        self.move_particles()
        if self.has_moving_emitters:
            self.move_emitters()
        self.start_new_particles()
        self.render_particles()
        if self.emitters == [] and self.particles == []:
            self.completed = True
