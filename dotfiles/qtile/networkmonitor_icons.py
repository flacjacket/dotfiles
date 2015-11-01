import cairocffi
from math import sin, cos, atan2, pi


def usb_icon(ctx):
    ctx.set_source_rgb(1, 1, 1)
    _strike_usb(ctx)


def wired_icon(ctx):
    ctx.set_source_rgb(1, 1, 1)
    _strike_wired(ctx)


def wifi_icon(ctx, quality):
    ctx.set_source_rgb(1, 1, 1)
    if quality >= 1:
        _strike_wifi1(ctx)
    if quality >= 2:
        _strike_wifi2(ctx)
    if quality >= 3:
        _strike_wifi3(ctx)
    if quality >= 4:
        _strike_wifi4(ctx)


def noconn_icon(ctx):
    ctx.set_source_rgb(1, 1, 1)
    ctx.set_line_width(100)
    _strike_nowifi(ctx)


def vpn_icon(ctx):
    ctx.set_source_rgb(1, 1, 1)
    _strike_shield(ctx)


def _rotate(x, y, angle):
    """Rotate a point of an angle around the origin point."""
    return x * cos(angle) - y * sin(angle), y * cos(angle) + x * sin(angle)


def _point_angle(cx, cy, px, py):
    """Return angle between x axis and point knowing given center."""
    return atan2(py - cy, px - cx)


def _quadratic_points(x1, y1, x2, y2, x3, y3):
    """Return the quadratic points to create quadratic curves."""
    xq1 = x2 * 2 / 3 + x1 / 3
    yq1 = y2 * 2 / 3 + y1 / 3
    xq2 = x2 * 2 / 3 + x3 / 3
    yq2 = y2 * 2 / 3 + y3 / 3
    return xq1, yq1, xq2, yq2, x3, y3


def _elliptic_curve(ctx, rx, ry, rotation, large, sweep, x3, y3):
    x1, y1 = ctx.get_current_point()
    radii_ratio = ry / rx

    # Cancel the rotation of the second point
    xe, ye = _rotate(x3, y3, -rotation)
    ye /= radii_ratio

    # Find the angle between the second point and the x axis
    angle = _point_angle(0, 0, xe, ye)

    # Put the second point onto the x axis
    xe = (xe ** 2 + ye ** 2) ** .5
    ye = 0

    # Update the x radius if it is too small
    rx = max(rx, xe / 2)

    # Find one circle centre
    xc = xe / 2
    yc = (rx ** 2 - xc ** 2) ** .5

    # Choose between the two circles according to flags
    if not (large ^ sweep):
        yc = -yc

    # Define the arc sweep
    arc = (ctx.arc if sweep else ctx.arc_negative)

    # Put the second point and the center back to their positions
    xe, ye = _rotate(xe, 0, angle)
    xc, yc = _rotate(xc, yc, angle)

    # Find the drawing angles
    angle1 = _point_angle(xc, yc, 0, 0)
    angle2 = _point_angle(xc, yc, xe, ye)

    # Draw the arc
    ctx.save()
    ctx.translate(x1, y1)
    ctx.rotate(rotation)
    ctx.scale(1, radii_ratio)
    arc(xc, yc, rx, angle1, angle2)
    ctx.restore()


def _strike_wired(ctx):
    ctx.arc(321, 129, 4, 3*pi/2, 2*pi)
    ctx.arc(321, 271, 4, 0, pi/2)
    ctx.arc_negative(279, 279, 4, 3*pi/2, pi)
    ctx.arc(271, 288, 4, 0, pi/2)
    ctx.arc_negative(249, 296, 4, 3*pi/2, pi)
    ctx.arc(241, 301, 4, 0, pi/2)
    ctx.arc(159, 301, 4, pi/2, pi)
    ctx.arc_negative(151, 296, 4, 2*pi, 3*pi/2)
    ctx.arc(129, 288, 4, pi/2, pi)
    ctx.arc_negative(121, 279, 4, 2*pi, 3*pi/2)
    ctx.arc(79, 271, 4, pi/2, pi)
    ctx.arc(79, 129, 4, pi, 3*pi/2)

    rad = 12.5
    skip = 30
    ctx.rel_line_to(skip, 0)
    ctx.rel_line_to(0, 60)
    x, y = ctx.get_current_point()
    ctx.arc_negative(x+rad, y, rad, pi, 0)
    ctx.rel_line_to(0, -60)
    ctx.rel_line_to(skip, 0)
    ctx.rel_line_to(0, 60)
    x, y = ctx.get_current_point()
    ctx.arc_negative(x+rad, y, rad, pi, 0)
    ctx.rel_line_to(0, -60)
    ctx.rel_line_to(skip, 0)
    ctx.rel_line_to(0, 60)
    x, y = ctx.get_current_point()
    ctx.arc_negative(x+rad, y, rad, pi, 0)
    ctx.rel_line_to(0, -60)
    ctx.rel_line_to(skip, 0)
    ctx.rel_line_to(0, 60)
    x, y = ctx.get_current_point()
    ctx.arc_negative(x+rad, y, rad, pi, 0)
    ctx.rel_line_to(0, -60)
    ctx.close_path()
    ctx.fill_preserve()


def _strike_usb(ctx):
    #matrix = cairocffi.Matrix(0, -1, 1, 0, 8.5712985, 353.92249)
    #ctx.transform(matrix)

    # rectangle
    ctx.rectangle(226.23077, 198.17175, 34.054432, 33.971706)
    ctx.fill()

    matrix = cairocffi.Matrix(1.027502, 0, 0, 1.027502, 3.164391, 82.27125)
    ctx.transform(matrix)
    # m 92.57172,87.795685
    ctx.move_to(92.57172, 87.795685)
    # a 24.204533,24.204533 0 1 1 -48.409065,0 24.204533,24.204533 0 1 1 48.409065,0
    _elliptic_curve(ctx, 24.204533, 24.204533, 0, True, True, -48.409065, 0)
    _elliptic_curve(ctx, 24.204533, 24.204533, 0, True, True, 48.409065, 0)
    # z
    ctx.close_path()
    matrix.invert()
    ctx.transform(matrix)

    matrix = cairocffi.Matrix(0.683726,0,0,0.683726,157.7966,69.64945)
    ctx.transform(matrix)
    # m 92.57172,87.795685
    ctx.move_to(92.57172, 87.795685)
    # a 24.204533,24.204533 0 1 1 -48.409065,0 24.204533,24.204533 0 1 1 48.409065,0
    _elliptic_curve(ctx, 24.204533, 24.204533, 0, True, True, -48.409065, 0)
    _elliptic_curve(ctx, 24.204533, 24.204533, 0, True, True, 48.409065, 0)
    # z
    ctx.close_path()
    matrix.invert()
    ctx.transform(matrix)

    # m 280.71527,156.68252
    ctx.move_to(280.71527, 156.68252)
    # c 0,0 33.7386,15.4741 33.23125,15.85461
    ctx.rel_line_to(33.23125, 15.85461)
    # c -0.50734,0.38051 -33.23125,15.34727 -33.23125,15.34727
    ctx.rel_line_to(-33.23125, 15.34727)
    # l 0,-31.20188
    ctx.rel_line_to(0, -31.20188)
    # z
    ctx.close_path()

    # FILL
    ctx.fill()

    # m 105.26052,171.85683
    ctx.move_to(105.26052, 171.85683)
    # c 29.11504,-2.74237 43.80379,-42.36574 60.69526,-42.36574
    ctx.rel_curve_to(29.11504, -2.74237, 43.80379, -42.36574, 60.69526, -42.36574)
    # c 11.42079,0 16.41714,0.52924 30.94969,0.52924
    ctx.rel_curve_to(11.42079, 0, 16.41714, 0.52924, 30.94969, 0.52924)

    # m 139.78853,172.06998
    ctx.move_to(139.78853, 172.06998)
    # c 30.07966,0 37.16402,28.45664 59.41407,42.56265
    ctx.rel_curve_to(30.07966, 0, 37.16402, 28.45664, 59.41407, 42.56265)
    # c 3.77011,2.15435 37.77275,0.75371 39.94619,0.75371
    ctx.rel_curve_to(3.77011, 2.15435, 37.77275, 0.75371, 39.94619, 0.75371)

    # m 74.032648,171.98191 215.131262,0
    ctx.move_to(74.032648, 171.98191)
    ctx.rel_line_to(215.131262, 0)

    # STROKE
    ctx.set_line_width(9.56692886)
    ctx.stroke()

    # m 139.78853,172.06998 c 30.07966,0 37.16402,28.45664 59.41407,42.56265 3.77011,2.15435 37.77275,0.75371 39.94619,0.75371

    # m 74.032648,171.98191 215.131262,0



def _strike_wifi1(ctx):
    # M1024 1651
    ctx.move_to(1024, 1851)
    # q-20 0-93-73.5
    x1, y1 = 0, 0
    x2, y2 = -20, 0
    x3, y3 = -93, -73.5
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    # t-73-93.5
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = -73, -93.5
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    # q0-32 62.5-54
    x1, y1 = 0, 0
    x2, y2 = 0, -32
    x3, y3 = 62.5, -54
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    # t103.5-22 103.5 22 62.5 54
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = 103.5, -22
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = 103.5, 22
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = 62.5, 54
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    # q0 20-73 93.5
    x1, y1 = 0, 0
    x2, y2 = 0, 20
    x3, y3 = -73, 93.5
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    ctx.close_path()
    ctx.fill_preserve()


def _strike_wifi2(ctx):
    # m270-271
    ctx.rel_move_to(270, -271)
    # q-2 0-40-25
    x1, y1 = 0, 0
    x2, y2 = -2, 0
    x3, y3 = -40, -25
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    # t-101.5-50-128.5-25-128.5 25-101 50-40.5 25
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = -101.5, -50
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = -128.5, -25
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = -128.5, 25
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = -101, 50
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = -40.5, 25
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    # q-18 0-93.5-75
    x1, y1 = 0, 0
    x2, y2 = -18, 0
    x3, y3 = -93.5, -75
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    # t-75.5-93
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = -75.5, -93
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    # q0-13 10-23 78-77 196-121
    x1, y1 = 0, 0
    x2, y2 = 0, -13
    x3, y3 = 10, -23
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    x1, y1 = 0, 0
    x2, y2 = 78, -77
    x3, y3 = 196, -121
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    # t233-44 233 44 196 121
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = 223, -44
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = 233, 44
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = 196, 121
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    # q10 10 10 23 0 18-75.5 93
    x1, y1 = 0, 0
    x2, y2 = 10, 10
    x3, y3 = 10, 23
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    x1, y1 = 0, 0
    x2, y2 = 0, 18
    x3, y3 = -75.5, 93
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    # t-93.5 75
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = -93.5, 75
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    ctx.close_path()
    ctx.fill_preserve()


def _strike_wifi3(ctx):
    # m273-272
    ctx.rel_move_to(273, -272)
    # q-11 0-23-8-136-105-252-154.5
    x1, y1 = 0, 0
    x2, y2 = -11, 0
    x3, y3 = -23, -8
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    x1, y1 = 0, 0
    x2, y2 = -136, -105
    x3, y3 = -252, -154.5
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    # t-268-49.5
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = -268, -49.5
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    # q-85 0-170.5 22
    x1, y1 = 0, 0
    x2, y2 = -85, 0
    x3, y3 = -170.5, 22
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    # t-149 53-113.5 62-79 53-31 22
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = -149, 53
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = -113.5, 62
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = -79, 53
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = -31, 22
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    # q-17 0-92-75
    x1, y1 = 0, 0
    x2, y2 = -17, 0
    x3, y3 = -92, -75
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    # t-75-93
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = -75, -93
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    # q0-12 10-22 132-132 320-205
    x1, y1 = 0, 0
    x2, y2 = 0, -12
    x3, y3 = 10, -22
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    x1, y1 = 0, 0
    x2, y2 = 132, -132
    x3, y3 = 320, -205
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    # t380-73 380 73 320 205
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = 380, -73
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = 380, 73
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = 320, 205
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    # q10 10 10 22 0 18-75 93
    x1, y1 = 0, 0
    x2, y2 = 10, 10
    x3, y3 = 10, 22
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    x1, y1 = 0, 0
    x2, y2 = 0, 18
    x3, y3 = -75, 93
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    # t-92 75
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = -92, 75
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    ctx.close_path()
    ctx.fill_preserve()


def _strike_wifi4(ctx):
    # m271-271
    ctx.rel_move_to(271, -271)
    # q-11 0-22-9-179-157-371.5-236.5
    x1, y1 = 0, 0
    x2, y2 = -11, 0
    x3, y3 = -22, -9
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    x1, y1 = 0, 0
    x2, y2 = -179, -157
    x3, y3 = -371.5, -236.5
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    # t-420.5-79.5-420.5 79.5-371.5 236.5
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = -420.5, -79.5
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = -420.5, 79.5
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = -371.5, 236.5
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    # q-11 9-22 9-17 0-92.5-75
    x1, y1 = 0, 0
    x2, y2 = -11, 9
    x3, y3 = -22, 9
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    x1, y1 = 0, 0
    x2, y2 = -17, 0
    x3, y3 = -92.5, -75
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    # t-75.5-93
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = -75.5, -93
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    # q0-13 10-23 187-186 445-288
    x1, y1 = 0, 0
    x2, y2 = 0, -13
    x3, y3 = 10, -23
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    x1, y1 = 0, 0
    x2, y2 = 187, -186
    x3, y3 = 445, -288
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    # t527-102 527 102 445 288
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = 527, -102
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = 527, 102
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = 445, 288
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    # q10 10 10 23 0 18-75.5 93
    x1, y1 = 0, 0
    x2, y2 = 10, 10
    x3, y3 = 10, 23
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    x1, y1 = 0, 0
    x2, y2 = 0, 18
    x3, y3 = -75.5, 93
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    # t-92.5 75
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = -92.5, 75
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    ctx.close_path()
    ctx.fill()


def _strike_nowifi(ctx):
    ctx.move_to(117, 812)
    # q0-13 10-23 187-186 445-288
    x1, y1 = 0, 0
    x2, y2 = 0, -13
    x3, y3 = 10, -23
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    x1, y1 = 0, 0
    x2, y2 = 187, -186
    x3, y3 = 445, -288
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    # t527-102 527 102 445 288
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = 527, -102
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = 527, 102
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = 445, 288
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    # q10 10 10 23 0 18-75.5 93
    x1, y1 = 0, 0
    x2, y2 = 10, 10
    x3, y3 = 10, 23
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    # x1, y1 = 0, 0
    # x2, y2 = 0, 18
    # x3, y3 = -75.5, 93
    # ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    # line to the bottom
    ctx.line_to(1024, 1900)
    ctx.close_path()
    ctx.stroke()


def _strike_shield(ctx):
    # M1472 1088
    ctx.move_to(1472, 1088)
    # v-640
    ctx.rel_line_to(0, -640)
    # h-448
    ctx.rel_line_to(-448, 0)
    # v1137
    ctx.rel_line_to(0, 1137)
    # q119-63 213-137 235-184 235-360
    ctx.rel_curve_to(0, 0, 119, -63, 213, -137)
    ctx.rel_curve_to(0, 0, 235, -184, 235, -360)
    # z
    ctx.close_path()
    # m192-768
    ctx.rel_move_to(192, -768)
    # v768
    ctx.rel_line_to(0, 768)
    # q0 86-33.5 170.5
    x1, y1 = 0, 0
    x2, y2 = 0, 86
    x3, y3 = -33.5, 170.5
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    # t-83 150-118 127.5-126.5 103-121 77.5-89.5 49.5-42.5 20
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = -83, 150
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = -118, 127.5
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = -126.5, 103
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = -121, 77.5
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = -89.5, 49.5
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = -42.5, 20
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    # q-12 6-26 6
    x1, y1 = 0, 0
    x2, y2 = -12, 6
    x3, y3 = -26, 6
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    # t-26-6
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = -26, -6
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    # q-16-7-42.5-20
    x1, y1 = 0, 0
    x2, y2 = -16, -7
    x3, y3 = -42.5, -20
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    # t-89.5-49.5-121-77.5-126.5-103-118-127.5-83-150-33.5-170.5
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = -89.5, -49.5
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = -121, -77.5
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = -126.5, -103
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = -118, -127.5
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = -83, -150
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = -33.5, -170.5
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    # v-768
    ctx.rel_line_to(0, -768)
    # q0-26 19-45
    x1, y1 = 0, 0
    x2, y2, 0, -26
    x3, y3 = 19, -45
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    # t45-19
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = 45, -19
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    # h1152
    ctx.rel_line_to(1152, 0)
    # q26 0 45 19
    x1, y1 = 0, 0
    x2, y2, 26, 0
    x3, y3 = 45, 19
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    # t19 45
    x1, y1 = 0, 0
    x2 = x3 - x2
    y2 = y3 - y2
    x3, y3 = 19, 45
    ctx.rel_curve_to(*_quadratic_points(x1, y1, x2, y2, x3, y3))
    # z
    ctx.close_path()
    ctx.fill()
    return
