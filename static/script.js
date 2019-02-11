d3.json("/api/temp", function(error, json) {
	if (error) return console.warn(error);
	json = json.map( function(d) {
		return {
			datetime: new Date(d.datetime),
			temp: d.temp
		}
	});
	var chart = d3_timeseries()
				  .addSerie(json, {x:'datetime',y:'temp'},{interpolate:'monotone',color:"#333"})
	chart('#chart')
});


function kpi(data) {
	var upd8 = d3.select('#kpi').selectAll('span').data(data)
	upd8.enter()
		.append('span')
	.merge(upd8)
		.text( function(d) { return d.temp.toString() + "°C"} )
}

d3.interval(function() {
	d3.json("/api/lasttemp", function(error, json) {
		kpi(json);
	});
}, 1000);

//(function() {
	var	n = 20, 
		data = d3.range(n).map(function(d) { return {datetime:new Date(Date.now() - 20e3 + (d * 1e3)), temp:d}});
	var svg = d3.select("#livedata"),
		margin = {top: 20, right: 20, bottom: 20, left: 40},
		width = +svg.attr("width") - margin.left - margin.right,
		height = +svg.attr("height") - margin.top - margin.bottom,
		g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");
	var x = d3.scaleTime()
		.domain(d3.extent(data))
		.range([0, width]);
	var y = d3.scaleLinear()
		.domain([0, 80])
		.range([height, 0]);
	var line = d3.line()
		.x(function(d) { return x(d.datetime); })
		.y(function(d) { return y(d.temp); });
		//.curve(d3.curveBasis);
	g.append("defs").append("clipPath")
		.attr("id", "clip-temp-1")
	  .append("rect")
		.attr("width", width)
		.attr("height", height);
	/*
	g.append("g")
		.attr("class", "axis axis--x")
		.attr("transform", "translate(0," + y(0) + ")")
		.call(d3.axisBottom(x));
		*/
	g.append("g")
		.attr("class", "axis axis--y")
		.call(d3.axisLeft(y));
	g.append("g")
		.attr("clip-path", "url(#clip-temp-1)")
	  .append("path")
		.datum(data)
		.attr("class", "line")
	  .transition()
		.duration(1000)
		.ease(d3.easeLinear)
		.on("start", tick);

function tick() {
	var self = this;
	d3.json("/api/lasttemp", function(error, json) {
		// Push a new data point onto the back.
		data.push({temp:json[0].temp, datetime: new Date()});
		console.log(json);
		// Redifine time domain to the interval [10s in the past, now]
		x.domain([new Date(Date.now() - 20e3), new Date()]);
		// Pop the old data point off the front.
		data.shift();
	});
	// Redraw the line.
	d3.select(self)
		.attr("d", line)
		.attr("transform", null);
	// Slide it to the left by 1 s.
	d3.active(self)
		.attr("transform", "translate(" + x(new Date(Date.now() - 21e3)) + ",0)")
		.transition()
		.on("start", tick);
}
//})();
