from svgwrite import Drawing


def draw_node(node, interfaces, size):
    """Draw a single node of a workflow definition

    Args:
        node:
        interfaces:

    Returns:

    """
    pr = 15
    padding = 20

    paper = Drawing("workflow_node.svg", size, id="repr")

    lg = paper.linearGradient((0.5, 0), (0.5, 1.), id="in_port")
    lg.add_stop_color(0, color='#3333ff')
    lg.add_stop_color(1, color='#2222ff')
    paper.defs.add(lg)

    lg = paper.linearGradient((0.5, 0), (0.5, 1.), id="out_port")
    lg.add_stop_color(0, color='#ffff33')
    lg.add_stop_color(1, color='#9a9a00')
    paper.defs.add(lg)

    # body
    nb = max(len(node['inputs']), len(node['outputs']))
    nw = max(300, pr * (nb * 6 + 4))
    nh = 150

    g = paper.add(paper.g())

    # background
    lg = paper.linearGradient((0.5, 0), (0.5, 1.))
    lg.add_stop_color(0, color='#8c8cff')
    lg.add_stop_color(1, color='#c8c8c8')
    paper.defs.add(lg)

    bg = paper.rect((-nw / 2, -nh / 2), (nw, nh), rx=15, ry=15, stroke_width=1)
    bg.stroke('#808080')
    bg.fill(lg)
    g.add(bg)

    # label
    style = 'font-size: 22px; font-family: verdana; text-anchor: middle'
    frag = paper.tspan(node['name'], dy=[7])
    label = paper.text("", style=style, fill='#000000')
    label.add(frag)
    g.add(label)

    # ports
    onstyle = 'font-size: 18px; font-family: verdana; text-anchor: end'
    instyle = 'font-size: 18px; font-family: verdana; text-anchor: start'
    istyle = 'font-size: 10px; font-family: verdana; text-anchor: middle'
    nb = len(node['inputs'])
    py = -nh / 2
    for i, pdef in enumerate(node['inputs']):
        px = i * pr * 6 - (nb - 1) * 3 * pr
        pg = g.add(paper.g())
        pg.translate(px, py)
        idef = interfaces.get(pdef['interface'], None)
        if idef is None:
            link = pg
        else:
            link = pg.add(paper.a(href=idef['url'], target='_top'))

        port = paper.circle((0, 0), pr, stroke='#000000', stroke_width=1)
        port.fill("url(#in_port)")
        link.add(port)
        # port name
        frag = paper.tspan(pdef['name'], dy=[-2 * pr + 5])
        label = paper.text("", style=instyle, fill='#000000')
        label.rotate(-45)
        label.add(frag)
        pg.add(label)
        # port interface
        itxt = pdef['interface']
        if len(itxt) > 10:
            itxt = itxt[:7] + "..."
        frag = paper.tspan(itxt, dy=[2 * pr + 3])
        label = paper.text("", style=istyle, fill='#000000')
        label.add(frag)
        link.add(label)

    nb = len(node['outputs'])
    py = nh / 2
    for i, pdef in enumerate(node['outputs']):
        px = i * pr * 6 - (nb - 1) * 3 * pr
        pg = g.add(paper.g())
        pg.translate(px, py)
        idef = interfaces.get(pdef['interface'], None)
        if idef is None:
            link = pg
        else:
            link = pg.add(paper.a(href=idef['url'], target='_top'))

        port = paper.circle((0, 0), pr, stroke='#000000', stroke_width=1)
        port.fill("url(#out_port)")
        link.add(port)
        # port name
        frag = paper.tspan(pdef['name'], dy=[2 * pr + 5])
        label = paper.text("", style=onstyle, fill='#000000')
        label.rotate(-45)
        label.add(frag)
        pg.add(label)
        # port interface
        itxt = pdef['interface']
        if len(itxt) > 10:
            itxt = itxt[:7] + "..."
        frag = paper.tspan(itxt, dy=[-2 * pr + 3])
        label = paper.text("", style=istyle, fill='#000000')
        label.add(frag)
        link.add(label)

    xmin = - nw / 2 - padding
    xmax = + nw / 2 + padding
    ymin = - nh / 2 - pr * 3 - padding
    ymax = + nh / 2 + pr * 3 + padding

    w = float(size[0])
    h = float(size[1])
    xratio = (xmax - xmin) / w
    yratio = (ymax - ymin) / h
    if xratio > yratio:
        xsize = int(xratio * w)
        ysize = int(xratio * h)
        ymin -= (ysize - (ymax - ymin)) / 2
    else:
        xsize = int(yratio * w)
        ysize = int(yratio * h)
        xmin -= (xsize - (xmax - xmin)) / 2

    paper.viewbox(xmin, ymin, xsize, ysize)

    return paper.tostring(), (xmin, ymin, xsize, ysize)
