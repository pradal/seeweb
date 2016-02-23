var wv = {
    x_offset: 0,
    y_offset: 50,
    nw: 80,
    nh: 40,
    pr: 5
};

wv.draw_node = function (paper, workflow, nodes, node) {
    var nf = nodes[node['id']];
    var loc_x = wv.x_offset + node['x'];
    var loc_y = wv.y_offset + node['y'];

    // background
    var bg = paper.rect(loc_x + -wv.nw / 2., loc_y + -wv.nh / 2., wv.nw, wv.nh, 5);
    bg.attr({'stroke-width': 1,
             'stroke-linejoin': 'round'});
    if (nf == null) {
        bg.attr({'gradient': '90-#ff8cff-#c8c8c8',
                 'stroke': '#ff8080'});
    } else {
        bg.attr({'gradient': '90-#8c8cff-#c8c8c8',
                 'stroke': '#808080',
                 'href': nf['url']});
    }

    if (nf != null) {
        // ports
        var nb = nf.inputs.length;
        for (i in nf.inputs){
            var input = nf.inputs[i];
            var port = paper.circle(loc_x + -(nb - 1) * 2 * wv.pr + i * wv.pr * 4,
                                    loc_y + -wv.nh / 2.,
                                    wv.pr);
            port.attr({'gradient': '180-#3333ff-#2222ff',
                       'stroke': '#000000',
                       'stroke-width': 1});
        }

        nb = nf.outputs.length;
        for (i in nf.outputs){
            var output = nf.outputs[i];
            var port = paper.circle(loc_x + -(nb - 1) * 2 * wv.pr + i * wv.pr * 4,
                                    loc_y + wv.nh / 2.,
                                    wv.pr);
            port.attr({'gradient': '180-#ffff33-#9a9a00',
                       'stroke': '#000000',
                       'stroke-width': 1});
        }
    }

    // label
    var label_txt = node['label'];
    if (label_txt == null) {
        label_txt = nf['name'];
    }
    var label = paper.text(loc_x, loc_y, label_txt);
    label.attr({'fill': '#000000'});
};

wv.in_port_index = function (nf, port_name) {
    for (i in nf.inputs) {
        if (nf.inputs[i]['name'] == port_name) {
            return i;
        }
    }
    return -1;
};

wv.out_port_index = function (nf, port_name) {
    for (i in nf.outputs) {
        if (nf.outputs[i]['name'] == port_name) {
            return i;
        }
    }
    return -1;
};

wv.draw_link = function (paper, workflow, nodes, link) {
    var src = workflow['nodes'][link[0]];
    var src_x = wv.x_offset + src['x'];
    var src_y = wv.y_offset + src['y'];

    var nf = nodes[src['id']];
    if (nf != null) {
        var i = wv.out_port_index(nf, link[1]);
        if (i != -1) {
            var nb = nf.outputs.length;
            src_x += i * wv.pr * 4 - (nb - 1) * 2 * wv.pr;
            src_y += wv.nh / 2.;
        }
    }
    var tgt = workflow['nodes'][link[2]];
    var tgt_x = wv.x_offset + tgt['x'];
    var tgt_y = wv.y_offset + tgt['y'];

    nf = nodes[tgt['id']];
    if (nf != null) {
        var i = wv.in_port_index(nf, link[3]);
        if (i != -1) {
            var nb = nf.inputs.length;
            tgt_x += i * wv.pr * 4 - (nb - 1) * 2 * wv.pr;
            tgt_y -= wv.nh / 2.;
        }
    }

    pth = paper.path("M" + src_x + " " + src_y + "L" + tgt_x + " " + tgt_y);
    pth.attr({'stroke': '#000000',
              'stroke-width': 1});
};

wv.draw_workflow = function(paper, workflow, nodes) {
    for (i in workflow['links']) {
        wv.draw_link(paper, workflow, nodes, workflow['links'][i]);
    }

    for (i in workflow['nodes']) {
        wv.draw_node(paper, workflow, nodes, workflow['nodes'][i]);
    }
};