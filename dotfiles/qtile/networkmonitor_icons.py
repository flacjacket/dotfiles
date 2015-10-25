from math import pi


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


def _quadratic_points(x1, y1, x2, y2, x3, y3):
    """Return the quadratic points to create quadratic curves."""
    xq1 = x2 * 2 / 3 + x1 / 3
    yq1 = y2 * 2 / 3 + y1 / 3
    xq2 = x2 * 2 / 3 + x3 / 3
    yq2 = y2 * 2 / 3 + y3 / 3
    return xq1, yq1, xq2, yq2, x3, y3


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
