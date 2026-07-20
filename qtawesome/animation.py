import math
from qtpy.QtCore import QTimer
from qtpy.QtGui import QColor


# ---- Utility functions for common animation patterns
# ----------------------------------------------------------------------------
def _sine_wave_value(elapsed, period, min_val, max_val):
    """Map elapsed time to sine wave value between min and max.

    Parameters
    ----------
    elapsed: int
        Elapsed time in milliseconds
    period: int
        Period of one complete sine wave cycle in milliseconds
    min_val: float
        Minimum value (at sine wave minimum)
    max_val: float
        Maximum value (at sine wave maximum)

    Returns
    -------
    return_value: float
        Value between min_val and max_val based on sine wave
    """
    angle = (elapsed % period) / period * 2 * math.pi
    sine = math.sin(angle)
    value_range = max_val - min_val
    return min_val + (sine + 1) / 2 * value_range


def _cosine_wave_value(elapsed, period, min_val, max_val):
    """Map elapsed time to cosine wave value between min and max.

    Similar to sine but starts at maximum value.

    Parameters
    ----------
    elapsed: int
        Elapsed time in milliseconds
    period: int
        Period of one complete cosine wave cycle in milliseconds
    min_val: float
        Minimum value (at cosine wave minimum)
    max_val: float
        Maximum value (at cosine wave maximum)

    Returns
    -------
    return_value: float
        Value between min_val and max_val based on cosine wave
    """
    angle = (elapsed % period) / period * 2 * math.pi
    cosine = math.cos(angle)
    value_range = max_val - min_val
    return min_val + (cosine + 1) / 2 * value_range


def _get_cycle_position(elapsed, period):
    """Get normalized position in current cycle.

    Parameters
    ----------
    elapsed: int
        Elapsed time in milliseconds
    period: int
        Period of one complete cycle in milliseconds

    Returns
    -------
    return_value: float
        Float between 0.0 and 1.0 representing position in cycle
    """
    return (elapsed % period) / period


def _elastic_ease_out(t, amplitude=1.0, period_factor=0.3):
    """Elastic ease-out easing function.

    Creates overshoot and bounce effect.

    Parameters
    ----------
    t: float
        Progress value from 0.0 to 1.0
    amplitude: Optional(float)
        Amplitude of the elastic effect (default: 1.0)
    period_factor: Optional(float)
        Period factor for oscillation (default: 0.3)

    Returns
    -------
    return_value: float
        Eased value with elastic overshoot
    """
    if t == 0 or t == 1:
        return t

    p = period_factor
    s = p / 4
    return amplitude * math.pow(2, -10 * t) * math.sin((t - s) * (2 * math.pi) / p) + 1


# ---- Utility functions for common transformations
# ----------------------------------------------------------------------------
def _apply_centered_transform(painter, rect, scale=1.0, angle=0.0):
    """Apply centered transformation to painter.

    Parameters
    ----------
    painter: QPainter
        Painter object
    rect: QRect
        Rectangle containing the icon
    scale: Optional(float)
        Scale factor
    angle: Optional(float)
        Rotation angle in degrees
    """
    x_center = rect.width() * 0.5
    y_center = rect.height() * 0.5
    painter.translate(x_center, y_center)
    if angle != 0:
        painter.rotate(angle)
    if scale != 1.0:
        painter.scale(scale, scale)
    painter.translate(-x_center, -y_center)


# ---- Animations
# ----------------------------------------------------------------------------
class BaseAnimation:
    """Base class for all icon animations.

    Provide common functionality like timing, duration, and lifecycle
    management.

    Subclasses should override _update_animation_state() and _apply_transform().

    Parameters
    ----------
    parent_widget: QWidget
        The widget containing the animated icon
    interval: Optional(int)
        Update interval in milliseconds (default: 10)
    duration: Optional(int | None)
        Total animation duration in milliseconds, None for infinite (default:
        None)
    autostart: Optional(boolean)
        Whether to start the animation automatically (default: True)
    """

    def __init__(self, parent_widget, interval=10, duration=None, autostart=True):
        self.parent_widget = parent_widget
        self.interval = interval
        self.duration = duration
        self.autostart = autostart

        # Store animation state per widget: [timer, elapsed_time, state_dict]
        self.info = {}

    def _update(self):
        """Internal update method called by timer."""
        if self.parent_widget in self.info:
            timer, elapsed, state = self.info[self.parent_widget]

            # Update elapsed time
            elapsed += self.interval

            # Check if duration has been reached
            if self.duration is not None and elapsed >= self.duration:
                self.stop()
                return

            # Update animation-specific state
            self._update_animation_state(elapsed, state)

            self.info[self.parent_widget] = timer, elapsed, state
            self.parent_widget.update()

    def _update_animation_state(self, elapsed, state):
        """Override this method to update animation-specific state.

        Parameters
        ----------
        elapsed: int
            Elapsed time in milliseconds
        state: dict
            Dictionary containing animation state
        """
        raise NotImplementedError("Subclasses must implement _update_animation_state")

    def _apply_transform(self, icon_painter, painter, rect, state):
        """Override this method to apply painter transformations.

        Parameters
        ----------
        icon_painter:
            The icon painter instance
        painter: QPainter
            Painter object
        rect: QRect
            Rect object defining the icon area
        state: dict
            Dictionary containing animation state
        """
        raise NotImplementedError("Subclasses must implement _apply_transform")

    def _get_initial_state(self):
        """Override this method to provide initial animation state.

        Returns:
            Dictionary containing initial animation state
        """
        return {}

    def setup(self, icon_painter, painter, rect):
        """Called during paint event to set up and apply animation."""
        if self.parent_widget not in self.info:
            # First setup - create timer
            timer = QTimer(self.parent_widget)
            timer.timeout.connect(self._update)
            self.info[self.parent_widget] = [timer, 0, self._get_initial_state()]
            if self.autostart:
                timer.start(self.interval)
        else:
            # Apply transformation based on current state
            timer, elapsed, state = self.info[self.parent_widget]
            self._apply_transform(icon_painter, painter, rect, state)

    def start(self):
        """Start the animation."""
        if self.parent_widget in self.info:
            timer = self.info[self.parent_widget][0]
            timer.start(self.interval)

    def stop(self):
        """Stop the animation."""
        if self.parent_widget in self.info:
            timer = self.info[self.parent_widget][0]
            timer.stop()

    def reset(self):
        """Reset animation to initial state."""
        if self.parent_widget in self.info:
            timer = self.info[self.parent_widget][0]
            self.info[self.parent_widget] = [timer, 0, self._get_initial_state()]


class Spin(BaseAnimation):
    """Continuous rotation animation.

    Parameters
    ----------
    parent_widget: QWidget
        The widget containing the animated icon
    interval: int
        Update interval in milliseconds (default: 10)
    step: int
        Rotation increment per update in degrees (default: 1)
    duration: Optional(int | None)
        Total animation duration in milliseconds, None for infinite (default:
        None)
    autostart: Optional(boolean)
        Whether to start the animation automatically (default: True)
    """

    def __init__(
        self, parent_widget, interval=10, step=1, duration=None, autostart=True
    ):
        super().__init__(parent_widget, interval, duration, autostart)
        self.step = step

    def _get_initial_state(self):
        return {"angle": 0}

    def _update_animation_state(self, elapsed, state):
        state["angle"] += self.step
        if state["angle"] >= 360:
            state["angle"] = 0

    def _apply_transform(self, icon_painter, painter, rect, state):
        _apply_centered_transform(painter, rect, angle=state["angle"])


class Pulse(Spin):
    """Stepped rotation animation (45-degree increments).

    Parameters
    ----------
    parent_widget: QWidget
        The widget containing the animated icon
    duration: Optional(int | None)
        Total animation duration in milliseconds, None for infinite (default:
        None)
    autostart: Optional(boolean)
        Whether to start the animation automatically (default: True)
    """

    def __init__(self, parent_widget, duration=None, autostart=True):
        super().__init__(
            parent_widget,
            interval=300,
            step=45,
            duration=duration,
            autostart=autostart,
        )


class Breathe(BaseAnimation):
    """Breathing/scaling animation (icon grows and shrinks).

    Parameters
    ----------
    parent_widget: QWidget
        The widget containing the animated icon
    interval: Optional(int)
        Update interval in milliseconds (default: 20)
    min_scale: Optional(float)
        Minimum scale factor (default: 0.8)
    max_scale: Optional(float)
        Maximum scale factor (default: 1.2)
    period: Optional(int)
        Period in milliseconds for one complete breath cycle (default: 2000)
    duration: Optional(int | None)
        Total animation duration in milliseconds, None for infinite (default:
        None)
    autostart: Optional(boolean)
        Whether to start the animation automatically (default: True)
    """

    def __init__(
        self,
        parent_widget,
        interval=20,
        min_scale=0.8,
        max_scale=1.2,
        period=2000,
        duration=None,
        autostart=True,
    ):
        super().__init__(parent_widget, interval, duration, autostart)
        self.min_scale = min_scale
        self.max_scale = max_scale
        self.period = period

    def _get_initial_state(self):
        return {"scale": 1.0}

    def _update_animation_state(self, elapsed, state):
        # Use sine wave for smooth breathing effect
        state["scale"] = _sine_wave_value(
            elapsed, self.period, self.min_scale, self.max_scale
        )

    def _apply_transform(self, icon_painter, painter, rect, state):
        _apply_centered_transform(painter, rect, scale=state["scale"])


class Fade(BaseAnimation):
    """Fade/opacity pulsating animation (icon fades in and out).

    Parameters
    ----------
    parent_widget: QWidget
        The widget containing the animated icon
    interval: Optional(int)
        Update interval in milliseconds (default: 20)
    min_opacity: Optional(float)
        Minimum opacity (0.0 to 1.0, default: 0.2)
    max_opacity: Optional(float)
        Maximum opacity (0.0 to 1.0, default: 1.0)
    period: Optional(int)
        Period in milliseconds for one complete fade cycle (default: 2000)
    duration: Optional(int | None)
        Total animation duration in milliseconds, None for infinite (default:
        None)
    autostart: Optional(boolean)
        Whether to start the animation automatically (default: True)

    Notes
    -----
    * This animation modifies the icon_painter to inject the animated opacity.
      The opacity animation is applied by storing it per-widget in the
      icon_painter instance, which will be read during the paint process.
    """

    def __init__(
        self,
        parent_widget,
        interval=20,
        min_opacity=0.2,
        max_opacity=1.0,
        period=2000,
        duration=None,
        autostart=True,
    ):
        super().__init__(parent_widget, interval, duration, autostart)
        self.min_opacity = max(0.0, min(1.0, min_opacity))
        self.max_opacity = max(0.0, min(1.0, max_opacity))
        self.period = period

    def _get_initial_state(self):
        return {"opacity": 1.0}

    def _update_animation_state(self, elapsed, state):
        # Use sine wave for smooth fading effect
        state["opacity"] = _sine_wave_value(
            elapsed, self.period, self.min_opacity, self.max_opacity
        )

    def _apply_transform(self, icon_painter, painter, rect, state):
        # Store the animation opacity per-widget in the icon_painter so it can
        # be used when the opacity is set later in the paint process
        if not hasattr(icon_painter, "_fade_animation_opacities"):
            icon_painter._fade_animation_opacities = {}
        icon_painter._fade_animation_opacities[id(self.parent_widget)] = state[
            "opacity"
        ]


class Shake(BaseAnimation):
    """Shake/bounce animation (icon vibrates horizontally and vertically).

    Parameters
    ----------
    parent_widget: QWidget
        The widget containing the animated icon
    interval: Optional(int)
        Update interval in milliseconds (default: 20)
    amplitude_x: Optional(int)
        Horizontal shake amplitude in pixels (default: 3)
    amplitude_y: Optional(int)
        Vertical shake amplitude in pixels (default: 3)
    period: Optional(int)
        Period in milliseconds for one complete shake cycle (default: 200)
    duration: Optional(int | None)
        Total animation duration in milliseconds, None for infinite (default:}
        None)
    autostart: Optional(boolean)
        Whether to start the animation automatically (default: True)
    """

    def __init__(
        self,
        parent_widget,
        interval=20,
        amplitude_x=3,
        amplitude_y=3,
        period=200,
        duration=None,
        autostart=True,
    ):
        super().__init__(parent_widget, interval, duration, autostart)
        self.amplitude_x = amplitude_x
        self.amplitude_y = amplitude_y
        self.period = period

    def _get_initial_state(self):
        return {"offset_x": 0, "offset_y": 0}

    def _update_animation_state(self, elapsed, state):
        # Use different frequencies for x and y to create more natural shake
        angle_x = (elapsed % self.period) / self.period * 2 * math.pi
        angle_y = (elapsed % (self.period * 1.3)) / (self.period * 1.3) * 2 * math.pi

        state["offset_x"] = math.sin(angle_x) * self.amplitude_x
        state["offset_y"] = math.sin(angle_y) * self.amplitude_y

    def _apply_transform(self, icon_painter, painter, rect, state):
        painter.translate(state["offset_x"], state["offset_y"])


class ColorCycle(BaseAnimation):
    """Color cycling animation (icon cycles through specified colors).

    Parameters
    ----------
    parent_widget: QWidget
        The widget containing the animated icon
    interval: Optional(int)
        Update interval in milliseconds (default: 50)
    colors: Optional(list[str] | None)
        List of color strings to cycle through (default: None that fallbacks to
        rainbow colors)
    color_duration: Optional(int)
        Time to spend on each color in milliseconds (default: 500)
    duration: Optional(int | None)
        Total animation duration in milliseconds, None for infinite (default:
        None)
    autostart: Optional(boolean)
        Whether to start the animation automatically (default: True)
    """

    def __init__(
        self,
        parent_widget,
        interval=50,
        colors=None,
        color_duration=500,
        duration=None,
        autostart=True,
    ):
        super().__init__(parent_widget, interval, duration, autostart)
        if colors is None:
            # Default rainbow colors
            self.colors = [
                "red",
                "orange",
                "yellow",
                "green",
                "blue",
                "indigo",
                "violet",
            ]
        else:
            self.colors = colors

        self.color_duration = color_duration

    def _get_initial_state(self):
        return {"current_color": QColor(self.colors[0]), "color_index": 0}

    def _update_animation_state(self, elapsed, state):
        # Calculate which color we should be at
        total_cycle_time = len(self.colors) * self.color_duration
        cycle_position = elapsed % total_cycle_time
        color_index = int(cycle_position / self.color_duration)

        if color_index != state["color_index"]:
            state["color_index"] = color_index
            state["current_color"] = QColor(self.colors[color_index])

    def _apply_transform(self, icon_painter, painter, rect, state):
        # Store the color in icon_painter's options for the paint operation
        # This is a bit of a hack - we're modifying the painter's pen color
        current_color = state["current_color"]
        painter.setPen(current_color)
        painter.setBrush(current_color)


class HeartBeat(BaseAnimation):
    """HeartBeat animation (double pulse with pause, like a heartbeat).

    Parameters
    ----------
    parent_widget: QWidget
        The widget containing the animated icon
    interval: Optional(int)
        Update interval in milliseconds (default: 20)
    min_scale: Optional(float)
        Minimum scale factor (default: 1.0)
    max_scale: Optional(float)
        Maximum scale factor during pulse (default: 1.3)
    period: Optional(int)
        Period in milliseconds for one complete heartbeat cycle (default: 1000)
    duration: Optional(int | None)
        Total animation duration in milliseconds, None for infinite (default:
        None)
    autostart: Whether to start the animation automatically (default: True)
    """

    def __init__(
        self,
        parent_widget,
        interval=20,
        min_scale=1.0,
        max_scale=1.3,
        period=1000,
        duration=None,
        autostart=True,
    ):
        super().__init__(parent_widget, interval, duration, autostart)
        self.min_scale = min_scale
        self.max_scale = max_scale
        self.period = period
        # Calculate timing proportions based on period
        # Pattern: beat1 (15%) + gap (10%) + beat2 (15%) + pause (60%)
        self.beat1_end = self.period * 0.15
        self.gap_end = self.period * 0.25
        self.beat2_end = self.period * 0.40

    def _get_initial_state(self):
        return {"scale": 1.0}

    def _update_animation_state(self, elapsed, state):
        # Calculate position in current cycle
        cycle_pos = elapsed % self.period

        if cycle_pos < self.beat1_end:
            # First beat: scale up then down
            progress = cycle_pos / self.beat1_end
            # Use sin for smooth pulse
            scale_factor = math.sin(progress * math.pi)
            state["scale"] = (
                self.min_scale + (self.max_scale - self.min_scale) * scale_factor
            )
        elif cycle_pos < self.gap_end:
            # Gap between beats
            state["scale"] = self.min_scale
        elif cycle_pos < self.beat2_end:
            # Second beat: scale up then down
            progress = (cycle_pos - self.gap_end) / (self.beat2_end - self.gap_end)
            scale_factor = math.sin(progress * math.pi)
            state["scale"] = (
                self.min_scale + (self.max_scale - self.min_scale) * scale_factor
            )
        else:
            # Pause
            state["scale"] = self.min_scale

    def _apply_transform(self, icon_painter, painter, rect, state):
        _apply_centered_transform(painter, rect, scale=state["scale"])


class Swing(BaseAnimation):
    """Swing animation (pendulum-like rotation back and forth).

    Parameters
    ----------
    parent_widget: QWidget
        The widget containing the animated icon
    interval: Optional(int)
        Update interval in milliseconds (default: 20)
    angle: Optional(int)
        Maximum swing angle in degrees (±angle, default: 15)
    period: Optional(int)
        Period in milliseconds for one complete swing cycle (default: 1000)
    duration: Optional(int | None)
        Total animation duration in milliseconds, None for infinite (default:
        None)
    autostart: Optional(boolean)
        Whether to start the animation automatically (default: True)
    """

    def __init__(
        self,
        parent_widget,
        interval=20,
        angle=15,
        period=1000,
        duration=None,
        autostart=True,
    ):
        super().__init__(parent_widget, interval, duration, autostart)
        self.max_angle = angle
        self.period = period

    def _get_initial_state(self):
        return {"angle": 0}

    def _update_animation_state(self, elapsed, state):
        # Use sine wave for smooth pendulum motion
        state["angle"] = _sine_wave_value(
            elapsed, self.period, -self.max_angle, self.max_angle
        )

    def _apply_transform(self, icon_painter, painter, rect, state):
        _apply_centered_transform(painter, rect, angle=state["angle"])


class Elastic(BaseAnimation):
    """Elastic/bounce animation (scale with overshoot and settle).

    The icon scales up, overshoots, bounces back, and settles at the target
    scale. This creates a spring-like elastic effect.

    Parameters
    ----------
    parent_widget: QWidget
        The widget containing the animated icon
    interval: Optional(int)
        Update interval in milliseconds (default: 20)
    min_scale: Optional(float)
        Starting scale factor (default: 0.5)
    max_scale: Optional(float)
        Target scale factor (default: 1.0)
    period: Optional(int)
        Period in milliseconds for one complete elastic bounce cycle (default:
        1500)
    duration: Optional(int | None)
        Total animation duration in milliseconds, None for infinite (default:
        None)
    autostart: Optional(boolean)
        Whether to start the animation automatically (default: True)
    """

    def __init__(
        self,
        parent_widget,
        interval=20,
        min_scale=0.5,
        max_scale=1.0,
        period=1500,
        duration=None,
        autostart=True,
    ):
        super().__init__(parent_widget, interval, duration, autostart)
        self.min_scale = min_scale
        self.max_scale = max_scale
        self.period = period

    def _get_initial_state(self):
        return {"scale": self.min_scale}

    def _update_animation_state(self, elapsed, state):
        # Elastic easing function with overshoot
        cycle_pos = _get_cycle_position(elapsed, self.period)
        scale_progress = _elastic_ease_out(cycle_pos)
        state["scale"] = (
            self.min_scale + (self.max_scale - self.min_scale) * scale_progress
        )

    def _apply_transform(self, icon_painter, painter, rect, state):
        _apply_centered_transform(painter, rect, scale=state["scale"])


class CompositeAnimation(BaseAnimation):
    """Composite animation that combines multiple animations.

    This allows you to layer multiple animation effects on a single icon.
    For example, you could combine Spin + Breathe, or Swing + Fade.

    Parameters
    ----------
    parent_widget: QWidget
        The widget containing the animated icon
    animations: list
        List of animation instances to combine
    interval: Optional(int)
        Update interval in milliseconds (default: 10)
    duration: Optional(int | None)
        Total animation duration in milliseconds, None for infinite (default:
        None)
    autostart: Optional(boolean)
        Whether to start the animation automatically (default: True)

    Examples
    --------
    Combine spinning and breathing animations

    .. code-block:: python

       anim1 = qta.Spin(button, step=2, autostart=False)
       anim2 = qta.Breathe(button, autostart=False)
       composite = qta.CompositeAnimation(button, [anim1, anim2])
       icon = qta.icon('fa5s.star', animation=composite)
    """

    def __init__(
        self,
        parent_widget,
        animations,
        interval=10,
        duration=None,
        autostart=True,
    ):
        super().__init__(parent_widget, interval, duration, autostart)
        self.animations = animations

        # Set all child animations to not autostart since we'll manage them
        for anim in self.animations:
            anim.autostart = False
            anim.parent_widget = parent_widget

    def _get_initial_state(self):
        return {"initialized": False}

    def _update_animation_state(self, elapsed, state):
        # Update all child animations' states
        for anim in self.animations:
            if anim.parent_widget in anim.info:
                timer, anim_elapsed, anim_state = anim.info[anim.parent_widget]
                anim_elapsed += self.interval
                anim._update_animation_state(anim_elapsed, anim_state)
                anim.info[anim.parent_widget] = timer, anim_elapsed, anim_state

    def _apply_transform(self, icon_painter, painter, rect, state):
        # Initialize child animations on first call
        if not state["initialized"]:
            for anim in self.animations:
                if anim.parent_widget not in anim.info:
                    # Create a dummy timer (won't be used)
                    timer = QTimer(anim.parent_widget)
                    anim.info[anim.parent_widget] = [
                        timer,
                        0,
                        anim._get_initial_state(),
                    ]
            state["initialized"] = True

        # Apply all child animation transforms
        for anim in self.animations:
            if anim.parent_widget in anim.info:
                timer, anim_elapsed, anim_state = anim.info[anim.parent_widget]
                anim._apply_transform(icon_painter, painter, rect, anim_state)

    def start(self):
        """Start the composite animation and all child animations."""
        super().start()
        for anim in self.animations:
            if anim.parent_widget in anim.info:
                # Child animations don't have active timers, managed by parent
                pass

    def stop(self):
        """Stop the composite animation and all child animations."""
        super().stop()
        for anim in self.animations:
            if anim.parent_widget in anim.info:
                pass
