var wv = {
    x_offset: 0,
    y_offset: 50,
    nw: 80,
    nh: 40,
    pr: 5,
    handleMouseEvent: null
};

wv.draw_node = function (stage, workflow, nodes, node) {
    var nf = nodes[node['id']];
    var container = new createjs.Container();
    container.x = wv.x_offset + node['x'];
    container.y = wv.y_offset + node['y'];

    // background
    var item = new createjs.Shape();
    var g = item.graphics;
    if (nf == null) {
        g.beginFill("#ff8cff").beginStroke("#ff8080");
    } else {
        g.beginFill("#c88cff").beginStroke("#808080");
    }
    g.drawRoundRect(-wv.nw / 2., -wv.nh / 2., wv.nw, wv.nh, 5, 5, 5, 5);
    item.name = node['id'];
        item.on("click", handleMouseEvent);
        item.on("dblclick", handleMouseEvent);
        item.on("mouseover", handleMouseEvent);
    container.addChild(item);

    if (nf != null) {
        // ports
        var nb = nf.inputs.length;
        for (i in nf.inputs){
            var input = nf.inputs[i];
            var item = new createjs.Shape();
            var g = item.graphics.beginFill("#3333ff").beginStroke("#000000");
            g.drawCircle(0, 0, wv.pr);
            item.x = -(nb - 1) * 2 * wv.pr + i * wv.pr * 4;
            item.y = -wv.nh / 2.;
            item.name = node['id'] + "/in:" + input['name'];
                item.on("mouseover", handleMouseEvent);
            container.addChild(item);
        }

        nb = nf.outputs.length;
        for (i in nf.outputs){
            var output = nf.outputs[i];
            var item = new createjs.Shape();
            var g = item.graphics.beginFill("#ff3333").beginStroke("#000000");
            g.drawCircle(0, 0, wv.pr);
            item.x = -(nb - 1) * 2 * wv.pr + i * wv.pr * 4;
            item.y = wv.nh / 2.;
            item.name = node['id'] + "/out:" + output['name'];
                item.on("mouseover", handleMouseEvent);
            container.addChild(item);
        }
    }
    stage.addChild(container);

    // label
    var label_txt = node['label'];
    if (label_txt == null) {
        label_txt = nf['name'];
    }
    var label = new createjs.Text(label_txt, "14px Arial");
    var bounds = label.getBounds();
    label.x = container.x - bounds.width / 2;
    label.y = container.y - bounds.height / 2;
    stage.addChild(label);
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

wv.draw_link = function (stage, workflow, nodes, link) {
    var item = new createjs.Shape();
    var g = item.graphics.setStrokeStyle(1).beginStroke("#000000");
    var src = workflow['nodes'][link[0]];
    var nf = nodes[src['id']];
    if (nf == null) {
        g.moveTo(wv.x_offset + src['x'], wv.y_offset + src['y']);
    }
    else {
        var i = wv.out_port_index(nf, link[1]);
        if (i == -1) {
            //g.setStrokeDash([2, 1], 0);
            g.moveTo(wv.x_offset + src['x'], wv.y_offset + src['y']);
        } else {
            var nb = nf.outputs.length;
            g.moveTo(wv.x_offset + src['x'] - (nb - 1) * 2 * wv.pr + i * wv.pr * 4, wv.y_offset + src['y'] + wv.nh / 2.);
        }
    }
    var tgt = workflow['nodes'][link[2]];
    nf = nodes[tgt['id']];
    if (nf == null) {
        g.lineTo(wv.x_offset + tgt['x'], wv.y_offset + tgt['y']);
    }
    else {
        var i = wv.in_port_index(nf, link[3]);
        if (i == -1) {
            //g.setStrokeDash([2, 1], 0);
            g.lineTo(wv.x_offset + tgt['x'], wv.y_offset + tgt['y']);
        } else {
            var nb = nf.inputs.length;
            g.lineTo(wv.x_offset + tgt['x'] - (nb - 1) * 2 * wv.pr + i * wv.pr * 4, wv.y_offset + tgt['y'] - wv.nh / 2.);
        }
    }
    stage.addChild(item);
};

wv.draw_workflow = function(stage, workflow, nodes) {
    for (i in workflow['connections']) {
        wv.draw_link(stage, workflow, nodes, workflow['connections'][i]);
    }

    for (i in workflow['nodes']) {
        wv.draw_node(stage, workflow, nodes, workflow['nodes'][i]);
    }
};