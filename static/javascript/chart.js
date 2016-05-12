function xticFormat(timePeroid) {
    timeUnit = timePeroid.slice(-1);
    if (timeUnit === 'h' || timeUnit === 'd') {
	return '%_I:%M%p';
    }
    else if (timeUnit === 'w') {
	return '%a %_I:%M%p';
    }
    else if (timeUnit === 'm' || timeUnit === 'y') {
	return '%b %_d';
    }
    else {
	return '%x'
    }
}

function addChart(data, svgid, timeFormat) {
    var colors = d3.scale.category20();
    var chart;

    nv.addGraph(function() {
        chart = nv.models.stackedAreaChart()
            .useInteractiveGuideline(true)
            .x(function(d) { return d[0] })
            .y(function(d) { return d[1] })
            .controlLabels({stacked: "Stacked"})
            .duration(300);

        chart.xAxis.tickFormat(function(d) { return d3.time.format(timeFormat)(new Date(d)) });
        chart.yAxis.tickFormat(d3.format(',.4f'));

        chart.legend.vers('furious');

        d3.select(svgid)
            .datum(data)
            .transition().duration(1000)
            .call(chart)
            .each('start', function() {
                setTimeout(function() {
                    d3.selectAll(svgid + ' *').each(function() {
                        if(this.__transition__)
                            this.__transition__.duration = 1;
                    })
                }, 0)
            });

        nv.utils.windowResize(chart.update);
        return chart;
    });
}
