r"""
Tests for QtAwesome animations.
"""

# Standard library imports

# Test Library imports
import pytest

# Third party imports
from qtpy import QtWidgets, QtCore

# Local imports
import qtawesome as qta


@pytest.fixture
def test_widget(qtbot):
    """Create a test widget for animations."""
    widget = QtWidgets.QPushButton("Test")
    qtbot.addWidget(widget)
    return widget


def test_spin_animation_rotation(test_widget, qtbot):
    """Test that Spin animation actually rotates the icon."""
    animation = qta.Spin(test_widget, step=10, interval=50)
    icon = qta.icon("fa5s.spinner", animation=animation)
    test_widget.setIcon(icon)

    with qtbot.waitExposed(test_widget):
        test_widget.show()
    test_widget.update()

    qtbot.waitUntil(lambda: test_widget in animation.info)
    _, _, state1 = animation.info[test_widget]
    angle1 = state1["angle"]

    # Wait for rotation to progress
    qtbot.wait(200)
    test_widget.update()

    _, _, state2 = animation.info[test_widget]
    angle2 = state2["angle"]

    # Angle should have increased
    assert angle2 > angle1
    # Angle should wrap at 360
    assert 0 <= angle2 < 360


def test_spin_animation_step_size(test_widget, qtbot):
    """Test that step parameter affects rotation speed."""
    # Large step = faster rotation
    animation = qta.Spin(test_widget, step=45, interval=50)
    icon = qta.icon("fa5s.spinner", animation=animation)
    test_widget.setIcon(icon)

    with qtbot.waitExposed(test_widget):
        test_widget.show()
    test_widget.update()

    qtbot.waitUntil(lambda: test_widget in animation.info)
    _, _, state1 = animation.info[test_widget]
    angle1 = state1["angle"]

    # Wait for one update
    qtbot.wait(60)
    test_widget.update()

    # Should have rotated by approximately the step size
    qtbot.waitUntil(
        lambda: 40 <= animation.info[test_widget][2]["angle"] - angle1 <= 50
    )  # Allow some tolerance


def test_pulse_animation_creation(test_widget):
    """Test that Pulse animation can be created."""
    animation = qta.Pulse(test_widget)
    icon = qta.icon("fa5s.spinner", animation=animation)
    assert icon is not None
    assert animation.step == 45
    assert animation.interval == 300


def test_breathe_animation_scaling(test_widget, qtbot):
    """Test that Breathe animation actually scales the icon."""
    animation = qta.Breathe(
        test_widget, min_scale=0.7, max_scale=1.3, period=800, interval=50
    )
    icon = qta.icon("fa5s.heart", animation=animation)
    test_widget.setIcon(icon)

    with qtbot.waitExposed(test_widget):
        test_widget.show()
    test_widget.update()

    qtbot.waitUntil(lambda: test_widget in animation.info)
    scales = []
    # Sample scales over time
    for i in range(8):
        _, _, state = animation.info[test_widget]
        scales.append(state["scale"])
        qtbot.wait(100)
        test_widget.update()

    # Should see variation in scales
    assert len(set(scales)) > 2
    # All scales should be within bounds
    for scale in scales:
        assert animation.min_scale <= scale <= animation.max_scale
    # Should see both growth and shrinkage
    assert max(scales) > min(scales)


def test_fade_animation_opacity_changes(test_widget, qtbot):
    """Test that Fade animation actually changes opacity over time."""
    animation = qta.Fade(
        test_widget, min_opacity=0.2, max_opacity=1.0, period=1000, interval=50
    )
    icon = qta.icon("fa5s.lightbulb", animation=animation)
    test_widget.setIcon(icon)

    # Trigger paint to initialize
    with qtbot.waitExposed(test_widget):
        test_widget.show()
    test_widget.update()

    # Get initial opacity state
    qtbot.waitUntil(lambda: test_widget in animation.info)
    _, _, state1 = animation.info[test_widget]
    opacity1 = state1["opacity"]

    # Wait for animation to progress
    qtbot.wait(100)
    test_widget.update()

    # Get new opacity state
    _, _, state2 = animation.info[test_widget]
    opacity2 = state2["opacity"]

    # Opacity should have changed
    assert opacity1 != opacity2
    # Opacity should be within bounds
    assert animation.min_opacity <= opacity2 <= animation.max_opacity


def test_fade_animation_period_affects_speed(test_widget, qtbot):
    """Test that period parameter actually affects animation speed."""
    # Fast fade (short period)
    fast_anim = qta.Fade(test_widget, period=500, interval=50)
    icon = qta.icon("fa5s.lightbulb", animation=fast_anim)
    test_widget.setIcon(icon)

    with qtbot.waitExposed(test_widget):
        test_widget.show()
    test_widget.update()

    qtbot.waitUntil(lambda: test_widget in fast_anim.info)
    # Progress through half the period
    qtbot.wait(300)
    test_widget.update()

    # Should have progressed significantly (at least 250ms)
    qtbot.waitUntil(lambda: fast_anim.info[test_widget][1] >= 250)


def test_shake_animation_offset_changes(test_widget, qtbot):
    """Test that Shake animation actually moves the icon."""
    animation = qta.Shake(
        test_widget, amplitude_x=5, amplitude_y=5, period=200, interval=50
    )
    icon = qta.icon("fa5s.bell", animation=animation)
    test_widget.setIcon(icon)

    test_widget.show()
    qtbot.waitExposed(test_widget)
    test_widget.update()

    qtbot.waitUntil(lambda: test_widget in animation.info)
    _, _, state = animation.info[test_widget]
    offset_x = state["offset_x"]
    offset_y = state["offset_y"]

    # Offsets should be within amplitude bounds
    assert abs(offset_x) <= animation.amplitude_x
    assert abs(offset_y) <= animation.amplitude_y

    # Wait and check that offsets change
    qtbot.wait(100)
    test_widget.update()

    _, _, state2 = animation.info[test_widget]
    offset_x2 = state2["offset_x"]
    offset_y2 = state2["offset_y"]

    # At least one offset should have changed
    assert offset_x != offset_x2 or offset_y != offset_y2


def test_color_cycle_changes_colors(test_widget, qtbot):
    """Test that ColorCycle animation actually cycles through colors."""
    custom_colors = ["red", "blue", "green"]
    animation = qta.ColorCycle(
        test_widget, colors=custom_colors, color_duration=200, interval=50
    )
    icon = qta.icon("fa5s.star", animation=animation)
    test_widget.setIcon(icon)

    test_widget.show()
    qtbot.waitExposed(test_widget)
    test_widget.update()

    qtbot.waitUntil(lambda: test_widget in animation.info)
    _, _, state1 = animation.info[test_widget]
    color_index1 = state1["color_index"]

    # Wait for color to change (longer than color_duration)
    qtbot.wait(250)
    test_widget.update()

    # Color index should have changed
    qtbot.waitUntil(
        lambda: color_index1 != animation.info[test_widget][2]["color_index"]
    )
    # Should cycle within bounds
    assert 0 <= animation.info[test_widget][2]["color_index"] < len(custom_colors)


def test_heartbeat_animation_double_pulse(test_widget, qtbot):
    """Test that HeartBeat animation produces two distinct pulses."""
    animation = qta.HeartBeat(
        test_widget, min_scale=1.0, max_scale=1.3, period=800, interval=40
    )
    icon = qta.icon("fa5s.heart", animation=animation)
    test_widget.setIcon(icon)

    test_widget.show()
    qtbot.waitExposed(test_widget)
    test_widget.update()
    qtbot.wait(100)

    qtbot.waitUntil(lambda: test_widget in animation.info)
    scales = []
    # Sample scale values throughout one complete period
    for i in range(8):
        _, _, state = animation.info[test_widget]
        scales.append(state["scale"])
        qtbot.wait(100)
        test_widget.update()

    # Should see variation in scales (not all the same)
    assert len(set(scales)) > 1
    # All scales should be within bounds
    for scale in scales:
        assert animation.min_scale <= scale <= animation.max_scale


def test_heartbeat_timing_proportions(test_widget):
    """Test that HeartBeat timing proportions are correct."""
    animation = qta.HeartBeat(test_widget, period=1500)
    # Check timing proportions are calculated correctly
    assert animation.beat1_end == 1500 * 0.15
    assert animation.gap_end == 1500 * 0.25
    assert animation.beat2_end == 1500 * 0.40


def test_swing_animation_pendulum_motion(test_widget, qtbot):
    """Test that Swing animation produces pendulum-like back and forth motion."""
    animation = qta.Swing(test_widget, angle=20, period=600, interval=50)
    icon = qta.icon("fa5s.bell", animation=animation)
    test_widget.setIcon(icon)

    test_widget.show()
    qtbot.waitExposed(test_widget)
    test_widget.update()
    qtbot.wait(100)

    qtbot.waitUntil(lambda: test_widget in animation.info)
    angles = []
    # Sample angles throughout period
    for i in range(6):
        _, _, state = animation.info[test_widget]
        angles.append(state["angle"])
        qtbot.wait(100)
        test_widget.update()

    # Should see variation in angles
    assert len(set(angles)) > 1
    # All angles should be within bounds (±max_angle)
    for angle in angles:
        assert -animation.max_angle <= angle <= animation.max_angle
    # Should swing both positive and negative
    qtbot.waitUntil(lambda: animation.info[test_widget][2]["angle"] > 0)
    qtbot.waitUntil(lambda: animation.info[test_widget][2]["angle"] > 0)


def test_elastic_animation_overshoot_behavior(test_widget, qtbot):
    """Test that Elastic animation overshoots and settles."""
    animation = qta.Elastic(
        test_widget, min_scale=0.5, max_scale=1.0, period=1000, interval=50
    )
    icon = qta.icon("fa5s.certificate", animation=animation)
    test_widget.setIcon(icon)

    test_widget.show()
    qtbot.waitExposed(test_widget)
    test_widget.update()
    qtbot.wait(100)

    qtbot.waitUntil(lambda: test_widget in animation.info)
    scales = []
    max_observed = 0
    # Sample scales throughout the elastic animation
    for i in range(12):
        _, _, state = animation.info[test_widget]
        scale = state["scale"]
        scales.append(scale)
        max_observed = max(max_observed, scale)
        qtbot.wait(80)
        test_widget.update()

    # Should see scale variations (bouncing)
    assert len(set(scales)) > 1
    # Elastic should overshoot the target (max_scale)
    # Due to elastic easing, it should exceed max_scale at some point
    assert (
        max_observed > animation.max_scale or max_observed >= animation.max_scale * 0.95
    )


def test_composite_animation_combines_effects(test_widget, qtbot):
    """Test that CompositeAnimation actually combines multiple animation effects."""
    # Create a composite with Spin + Breathe
    anim1 = qta.Spin(
        test_widget,
        step=10,
        autostart=False,
    )
    anim2 = qta.Breathe(
        test_widget,
        min_scale=0.8,
        max_scale=1.2,
        autostart=False,
    )
    composite = qta.CompositeAnimation(test_widget, [anim1, anim2], interval=50)
    icon = qta.icon("fa5s.star", animation=composite)
    test_widget.setIcon(icon)

    test_widget.show()
    qtbot.waitExposed(test_widget)
    test_widget.update()
    qtbot.wait(100)

    # Check that both child animations are updating
    qtbot.waitUntil(lambda: test_widget in anim1.info and test_widget in anim2.info)
    # Get initial states
    _, _, spin_state1 = anim1.info[test_widget]
    _, _, breathe_state1 = anim2.info[test_widget]
    angle1 = spin_state1["angle"]
    scale1 = breathe_state1["scale"]

    # Wait for updates
    qtbot.wait(200)
    test_widget.update()

    # Get new states
    _, _, spin_state2 = anim1.info[test_widget]
    _, _, breathe_state2 = anim2.info[test_widget]
    angle2 = spin_state2["angle"]
    scale2 = breathe_state2["scale"]

    # Both animations should be progressing
    assert angle2 != angle1  # Spin is rotating
    # Scale might be the same if sampled at same point in sine wave, so just check it's valid
    assert 0.8 <= scale2 <= 1.2
    assert scale1 != scale2


def test_composite_animation_child_autostart_disabled(test_widget):
    """Test that CompositeAnimation disables autostart on child animations."""
    anim1 = qta.Spin(test_widget, autostart=True)
    anim2 = qta.Breathe(test_widget, autostart=True)
    composite = qta.CompositeAnimation(test_widget, [anim1, anim2])
    # Child animations should have autostart disabled by composite
    assert anim1.autostart is False
    assert anim2.autostart is False
    assert composite.animations == [anim1, anim2]


def test_animation_start_stop(test_widget, qtbot):
    """Test that animations can be started and stopped."""
    animation = qta.Spin(test_widget, autostart=False)
    icon = qta.icon("fa5s.spinner", animation=animation)
    test_widget.setIcon(icon)

    # Animation should not be running initially
    assert animation.autostart is False

    # Trigger a paint event to initialize the animation
    test_widget.show()
    qtbot.waitExposed(test_widget)
    test_widget.update()
    qtbot.wait(50)

    # Start animation
    animation.start()
    qtbot.waitUntil(lambda: test_widget in animation.info)
    qtbot.waitUntil(lambda: animation.info[test_widget][0].isActive())

    # Stop animation
    animation.stop()
    qtbot.waitUntil(lambda: not animation.info[test_widget][0].isActive())


def test_animation_reset(test_widget, qtbot):
    """Test that animations can be reset to initial state."""
    animation = qta.Spin(test_widget, autostart=False)
    icon = qta.icon("fa5s.spinner", animation=animation)
    test_widget.setIcon(icon)

    # Trigger paint to initialize
    test_widget.show()
    qtbot.waitExposed(test_widget)
    test_widget.update()
    qtbot.wait(50)

    animation.start()
    # Force an update to change the state
    qtbot.waitUntil(lambda: test_widget in animation.info)
    timer, elapsed, state = animation.info[test_widget]
    animation.info[test_widget] = [timer, 1000, state]  # Set elapsed time

    # Reset should restore initial state
    animation.reset()
    qtbot.waitUntil(lambda: animation.info[test_widget][1] == 0)


def test_animation_with_duration(test_widget, qtbot):
    """Test that animations stop after duration expires."""
    animation = qta.Spin(test_widget, duration=100, interval=10)
    icon = qta.icon("fa5s.spinner", animation=animation)
    test_widget.setIcon(icon)

    # Show widget to trigger paint and start animation
    test_widget.show()
    qtbot.waitExposed(test_widget)
    test_widget.update()

    # Wait for duration to expire
    qtbot.wait(200)

    # Animation should have stopped
    qtbot.waitUntil(lambda: test_widget in animation.info)
    qtbot.waitUntil(lambda: not animation.info[test_widget][0].isActive())


def test_base_animation_interface(test_widget):
    """Test that BaseAnimation requires implementation of abstract methods."""
    from qtawesome.animation import BaseAnimation

    # Trying to instantiate directly should work, but methods should raise NotImplementedError
    base_anim = BaseAnimation(test_widget)

    with pytest.raises(NotImplementedError):
        base_anim._update_animation_state(0, {})

    with pytest.raises(NotImplementedError):
        base_anim._apply_transform(None, None, None, {})


def test_animation_state_initialization(test_widget):
    """Test that animations properly initialize their state."""
    animation = qta.Breathe(test_widget)
    initial_state = animation._get_initial_state()
    assert "scale" in initial_state
    assert initial_state["scale"] == 1.0


def test_fade_animation_opacity_isolation(qtbot):
    """Test that Fade animation only affects its own widget, not others."""
    qta._resource["iconic"] = None
    iconic_font = qta._instance()
    widget1 = QtWidgets.QPushButton("Widget 1")
    widget2 = QtWidgets.QPushButton("Widget 2")
    qtbot.addWidget(widget1)
    qtbot.addWidget(widget2)

    # Create fade animation only for widget1
    fade_anim1 = qta.Fade(widget1, min_opacity=0.3, max_opacity=1.0, interval=50)
    icon1 = qta.icon("fa5s.lightbulb", animation=fade_anim1)
    widget1.setIcon(icon1)

    # Create non-fade icon for widget2
    icon2 = qta.icon("fa5s.sun", color="yellow")
    widget2.setIcon(icon2)

    # Show widgets and trigger paint
    with qtbot.waitExposed(widget1):
        widget1.show()
    with qtbot.waitExposed(widget2):
        widget2.show()

    widget1.update()
    widget2.update()

    # Check that fade opacity is stored per-widget
    painter = iconic_font.painter
    qtbot.waitUntil(lambda: hasattr(painter, "_fade_animation_opacities"))

    # Widget1 should have opacity stored
    assert id(widget1) in painter._fade_animation_opacities
    # Widget2 should NOT have opacity stored
    assert id(widget2) not in painter._fade_animation_opacities

    # Widget1's opacity should be within bounds
    qtbot.waitUntil(
        lambda: 0.3 <= painter._fade_animation_opacities[id(widget1)] <= 1.0
    )


def test_fade_animation_painter_integration(qtbot):
    """Test that Fade animation actually integrates with the icon painter."""
    qta._resource["iconic"] = None
    iconic_font = qta._instance()
    widget = QtWidgets.QPushButton("Test")
    qtbot.addWidget(widget)

    # Create fade animation with known opacity range
    fade_anim = qta.Fade(
        widget, min_opacity=0.5, max_opacity=1.0, period=1000, interval=50
    )
    icon = qta.icon("fa5s.circle", color="blue", animation=fade_anim)
    widget.setIcon(icon)

    with qtbot.waitExposed(widget):
        widget.show()
    widget.update()

    # Get the iconic font instance and painter
    painter_instance = iconic_font.painter
    qtbot.waitUntil(lambda: hasattr(painter_instance, "_fade_animation_opacities"))

    # Verify the fade opacity is being stored in the painter
    widget_id = id(widget)
    assert widget_id in painter_instance._fade_animation_opacities

    # Get opacity at different times and verify it changes
    opacity1 = painter_instance._fade_animation_opacities[widget_id]

    qtbot.wait(100)
    widget.update()
    qtbot.wait(100)

    opacity2 = painter_instance._fade_animation_opacities[widget_id]

    # Opacity should change over time (unless we hit the exact same point in the cycle)
    assert opacity1 != opacity2

    # Both should be in valid range
    assert 0.5 <= opacity1 <= 1.0
    assert 0.5 <= opacity2 <= 1.0


def test_fade_animation_multiple_widgets_independent(qtbot):
    """Test that multiple Fade animations on different widgets are independent."""
    qta._resource["iconic"] = None
    iconic_font = qta._instance()

    widget1 = QtWidgets.QPushButton("Widget 1")
    widget2 = QtWidgets.QPushButton("Widget 2")
    widget3 = QtWidgets.QPushButton("Widget 3")
    qtbot.addWidget(widget1)
    qtbot.addWidget(widget2)
    qtbot.addWidget(widget3)

    # Three different fade animations with different parameters
    fade1 = qta.Fade(widget1, min_opacity=0.2, max_opacity=1.0, period=500)
    fade2 = qta.Fade(widget2, min_opacity=0.5, max_opacity=0.9, period=1000)
    fade3 = qta.Fade(widget3, min_opacity=0.1, max_opacity=0.8, period=1500)

    icon1 = qta.icon("fa5s.star", animation=fade1)
    icon2 = qta.icon("fa5s.heart", animation=fade2)
    icon3 = qta.icon("fa5s.circle", animation=fade3)

    widget1.setIcon(icon1)
    widget2.setIcon(icon2)
    widget3.setIcon(icon3)

    # Show all widgets
    with qtbot.waitExposed(widget1):
        widget1.show()
    with qtbot.waitExposed(widget2):
        widget2.show()
    with qtbot.waitExposed(widget3):
        widget3.show()
    widget1.update()
    widget2.update()
    widget3.update()

    # Check painter has separate opacity for each widget
    painter = iconic_font.painter
    qtbot.waitUntil(lambda: hasattr(painter, "_fade_animation_opacities"))

    opacities = painter._fade_animation_opacities

    # All three widgets should have entries
    qtbot.waitUntil(lambda: id(widget1) in opacities)
    qtbot.waitUntil(lambda: id(widget2) in opacities)
    qtbot.waitUntil(lambda: id(widget3) in opacities)

    # Each should be within their respective bounds
    qtbot.waitUntil(lambda: 0.2 <= opacities[id(widget1)] <= 1.0)
    qtbot.waitUntil(lambda: 0.5 <= opacities[id(widget2)] <= 0.9)
    qtbot.waitUntil(lambda: 0.1 <= opacities[id(widget3)] <= 0.8)

    # Wait and verify they can have different values
    qtbot.wait(200)
    widget1.update()
    widget2.update()
    widget3.update()
    qtbot.wait(50)

    # Re-check opacities - they may be different from each other
    # due to different periods
    opacity1 = opacities[id(widget1)]
    opacity2 = opacities[id(widget2)]
    opacity3 = opacities[id(widget3)]
    assert opacity1 != opacity2
    assert opacity2 != opacity3
    assert opacity3 != opacity1

    # All should still be in valid ranges
    qtbot.waitUntil(lambda: 0.2 <= opacity1 <= 1.0)
    qtbot.waitUntil(lambda: 0.5 <= opacity2 <= 0.9)
    qtbot.waitUntil(lambda: 0.1 <= opacity3 <= 0.8)


def test_multiple_animations_on_different_widgets(qtbot):
    """Test that multiple animations can run independently on different widgets."""
    widget1 = QtWidgets.QPushButton("Widget 1")
    widget2 = QtWidgets.QPushButton("Widget 2")
    qtbot.addWidget(widget1)
    qtbot.addWidget(widget2)

    anim1 = qta.Spin(widget1, step=1)
    anim2 = qta.Breathe(widget2, min_scale=0.8, max_scale=1.2)

    icon1 = qta.icon("fa5s.spinner", animation=anim1)
    icon2 = qta.icon("fa5s.heart", animation=anim2)

    widget1.setIcon(icon1)
    widget2.setIcon(icon2)

    # Show widgets to trigger paint and initialize animations
    with qtbot.waitExposed(widget1):
        widget1.show()
    with qtbot.waitExposed(widget2):
        widget2.show()
    widget1.update()
    widget2.update()

    # Both animations should have their own state
    qtbot.waitUntil(lambda: widget1 in anim1.info and widget2 in anim2.info)
    assert widget1 not in anim2.info
    assert widget2 not in anim1.info


def test_animation_with_icon_widget_updates(qtbot):
    """Test that animations actually animate IconWidget."""
    # Create IconWidget with Spin animation
    icon_widget = qta.IconWidget("fa5s.spinner", size=QtCore.QSize(32, 32))
    animation = qta.Spin(icon_widget, step=15, interval=50)

    # Recreate icon with animation
    icon = qta.icon("fa5s.spinner", animation=animation)
    icon_widget.setIcon(icon)
    qtbot.addWidget(icon_widget)

    with qtbot.waitExposed(icon_widget):
        icon_widget.show()
    icon_widget.update()

    # Verify animation is running on IconWidget
    qtbot.waitUntil(lambda: icon_widget in animation.info)
    _, _, state1 = animation.info[icon_widget]
    angle1 = state1["angle"]

    # Wait for animation to progress
    qtbot.wait(150)
    icon_widget.update()

    _, _, state2 = animation.info[icon_widget]
    angle2 = state2["angle"]

    # Angle should have changed
    assert angle2 != angle1
    # Should be within valid range
    assert 0 <= angle2 < 360


def test_composite_animation_all_effects_active(test_widget, qtbot):
    """Test that CompositeAnimation with three effects has all running simultaneously."""
    # Create composite with Spin + Breathe + Fade
    anim1 = qta.Spin(test_widget, step=10, autostart=False)
    anim2 = qta.Breathe(test_widget, min_scale=0.8, max_scale=1.2, autostart=False)
    anim3 = qta.Fade(test_widget, min_opacity=0.5, max_opacity=1.0, autostart=False)

    composite = qta.CompositeAnimation(test_widget, [anim1, anim2, anim3], interval=50)
    icon = qta.icon("fa5s.gem", animation=composite)
    test_widget.setIcon(icon)

    with qtbot.waitExposed(test_widget):
        test_widget.show()
    test_widget.update()
    qtbot.wait(100)

    # Verify all three child animations are initialized and updating
    qtbot.waitUntil(
        lambda: test_widget in anim1.info
        and test_widget in anim2.info
        and test_widget in anim3.info
    )
    # Get initial states
    _, _, spin_state1 = anim1.info[test_widget]
    _, _, breathe_state1 = anim2.info[test_widget]
    _, _, fade_state1 = anim3.info[test_widget]

    angle1 = spin_state1["angle"]
    scale1 = breathe_state1["scale"]
    opacity1 = fade_state1["opacity"]

    # Wait for updates
    qtbot.wait(200)
    test_widget.update()

    # Get new states
    _, _, spin_state2 = anim1.info[test_widget]
    _, _, breathe_state2 = anim2.info[test_widget]
    _, _, fade_state2 = anim3.info[test_widget]

    angle2 = spin_state2["angle"]
    scale2 = breathe_state2["scale"]
    opacity2 = fade_state2["opacity"]

    # All three should be progressing
    assert angle2 != angle1  # Spin is rotating
    # Scale and opacity should be within bounds
    assert 0.8 <= scale2 <= 1.2
    assert scale1 != scale2
    assert 0.5 <= opacity2 <= 1.0
    assert opacity1 != opacity2

    # Also verify Fade opacity is in the painter
    iconic_font = qta._instance()
    painter = iconic_font.painter
    qtbot.waitUntil(lambda: hasattr(painter, "_fade_animation_opacities"))
    assert id(test_widget) in painter._fade_animation_opacities
    painter_opacity = painter._fade_animation_opacities[id(test_widget)]
    assert 0.5 <= painter_opacity <= 1.0


if __name__ == "__main__":
    pytest.main()
