from svgwrite import Drawing


def draw_node(paper, workflow, nodes, interfaces, node):
    """Draw a single node of a workflow definition

    Args:
        paper:
        workflow:
        nodes:
        interfaces:
        node:

    Returns:

    """
    nw = 80
    nh = 40
    pr = 5

    nf = nodes.get(node['id'], None)

    g = paper.add(paper.g())
    g.translate(node['x'], node['y'])
    if nf is None:
        link = g
    else:
        link = g.add(paper.a(href=nf['url'], target='_top'))

    # background
    bg = paper.rect((-nw / 2, -nh / 2), (nw, nh), rx=5, ry=5, stroke_width=1)
    link.add(bg)
    if nf is None:
        bg.stroke('#ff8080')
        bg.fill("url(#bg_failed)")
    else:
        bg.stroke('#808080')
        bg.fill("url(#bg_loaded)")

    # label
    label_txt = node['label']
    if label_txt is None and nf is not None:
        label_txt = nf['name']

    style = 'font-size: 18px; font-family: verdana; text-anchor: middle'
    frag = paper.tspan(label_txt, dy=[5])
    label = paper.text("", style=style, fill='#000000')
    label.add(frag)
    link.add(label)

    # ports
    if nf is not None:
        nb = len(nf['inputs'])
        py = -nh / 2
        for i, pdef in enumerate(nf['inputs']):
            px = i * pr * 4 - (nb - 1) * 2 * pr
            port = paper.circle((px, py), pr, stroke='#000000', stroke_width=1)
            port.fill("url(#in_port)")
            g.add(port)

        nb = len(nf['outputs'])
        py = nh / 2
        for i, pdef in enumerate(nf['outputs']):
            px = i * pr * 4 - (nb - 1) * 2 * pr
            port = paper.circle((px, py), pr, stroke='#000000', stroke_width=1)
            port.fill("url(#out_port)")
            g.add(port)


def port_index(ports, port_name):
    """

    Args:
        ports:
        port_name:

    Returns:

    """
    for i, port in enumerate(ports):
        if port['name'] == port_name:
            return i

    return None


def draw_link(paper, workflow, nodes, interfaces, link):
    """Draw a single node of a workflow definition

    Args:
        paper:
        workflow:
        nodes:
        interfaces:
        link:

    Returns:

    """
    nh = 40
    pr = 5

    src = workflow['nodes'][link[0]]
    src_x = src['x']
    src_y = src['y']
    nf = nodes.get(src['id'], None)
    if nf is not None:
        i = port_index(nf['outputs'], link[1])
        if i is not None:
            nb = len(nf['outputs'])
            src_x += i * pr * 4 - (nb - 1) * 2 * pr
            src_y += nh / 2.

    tgt = workflow['nodes'][link[2]]
    tgt_x = tgt['x']
    tgt_y = tgt['y']

    nf = nodes.get(tgt['id'], None)
    if nf is not None:
        i = port_index(nf['inputs'], link[3])
        if i is not None:
            nb = len(nf['inputs'])
            tgt_x += i * pr * 4 - (nb - 1) * 2 * pr
            tgt_y -= nh / 2.

    pth = paper.polyline([(src_x, src_y), (tgt_x, tgt_y)],
                         stroke='#000000',
                         stroke_width=1)
    paper.add(pth)


def draw_workflow(workflow, nodes, interfaces, size):
    """Draw the svg representation of a workflow

    Args:
        workflow:
        nodes:
        interfaces:

    Returns:
        (str) SVG encoded string
    """
    nw = 80
    nh = 40
    pr = 5
    padding = 20

    paper = Drawing("workflow.svg", size, id="repr")

    lg = paper.linearGradient((0.5, 0), (0.5, 1.), id="bg_loaded")
    lg.add_stop_color(0, color='#8c8cff')
    lg.add_stop_color(1, color='#c8c8c8')
    paper.defs.add(lg)

    lg = paper.linearGradient((0.5, 0), (0.5, 1.), id="bg_failed")
    lg.add_stop_color(0, color='#ff8cff')
    lg.add_stop_color(1, color='#c8c8c8')
    paper.defs.add(lg)

    lg = paper.linearGradient((0.5, 0), (0.5, 1.), id="in_port")
    lg.add_stop_color(0, color='#3333ff')
    lg.add_stop_color(1, color='#2222ff')
    paper.defs.add(lg)

    lg = paper.linearGradient((0.5, 0), (0.5, 1.), id="out_port")
    lg.add_stop_color(0, color='#ffff33')
    lg.add_stop_color(1, color='#9a9a00')
    paper.defs.add(lg)

    for link in workflow['links']:
        draw_link(paper, workflow, nodes, {}, link)

    for node in workflow['nodes']:
        draw_node(paper, workflow, nodes, {}, node)

    xmin = min(node['x'] for node in workflow['nodes']) - nw / 2 - padding
    xmax = max(node['x'] for node in workflow['nodes']) + nw / 2 + padding
    ymin = min(node['y'] for node in workflow['nodes']) - nh / 2 - pr - padding
    ymax = max(node['y'] for node in workflow['nodes']) + nh / 2 + pr + padding

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
