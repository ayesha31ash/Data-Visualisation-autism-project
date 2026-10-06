d3.csv("Autism-Merged-Dataset.csv").then(function(data) {
    const rootData = { name: "root", children: [] };

    const ageGroups = d3.group(data, d => d.age_group);
    ageGroups.forEach((ageValues, ageKey) => {
        const ageNode = { name: ageKey, children: [] };


        const genderGroups = d3.group(ageValues, d => d.gender);
        genderGroups.forEach((genderValues, genderKey) => {
            const genderNode = { name: genderKey, children: [] };

            const autismGroups = d3.group(genderValues, d => d["class/asd"]);
            autismGroups.forEach((autismValues, autismKey) => {
                genderNode.children.push({
                    name: autismKey === "yes" ? "Diagnosed" : "N Diagnosed",
                    value: autismValues.length,
                    ethnicity: autismValues[0].ethnicity
                });
            });

            // Normalize the data within each gender group by dividing each value by the total number of entries
            const genderTotal = genderNode.children.reduce((sum, d) => sum + d.value, 0);
            genderNode.children.forEach(d => d.value /= genderTotal); // Normalizing each child value

            ageNode.children.push(genderNode);
        });

        // Normalize the data within each age group
        const ageTotal = ageNode.children.reduce((sum, d) => sum + d.value, 0);
        ageNode.children.forEach(d => d.value /= ageTotal); // Normalizing each child value

        rootData.children.push(ageNode);
    });

    const root = d3.hierarchy(rootData).sum(d => d.value);

    const width = 900;
    const height = 900;
    const radius = Math.min(width, height) / 3;

    const partition = d3.partition().size([2 * Math.PI, radius]);
    partition(root);

    const arc = d3.arc()
        .startAngle(d => d.x0)
        .endAngle(d => d.x1)
        .innerRadius(d => d.y0)
        .outerRadius(d => d.y1);

    // Age Group Color Scale 
    const ageGroupColor = d3.scaleOrdinal()
        .domain(["Child", "Adult", "Adolescent"])
        .range(["#800080", "#0000FF", "#FFB6C1"]); 

    const genderColor = d3.scaleOrdinal()
        .domain(["Male", "Female"])
        .range(["#008000", "#D8BFD8"]); 

    const color = d3.scaleOrdinal()
        .domain(["Diagnosed", "N Diagnosed"])
        .range(["#E63946", "#457B9D"]);

    const svg = d3.select("#sunburst-chart")
        .append("svg")
        .attr("viewBox", `0 0 ${width} ${height}`)
        .attr("preserveAspectRatio", "xMidYMid meet")
        .append("g")
        .attr("transform", `translate(${width / 2}, ${height / 2})`);

    let selectedNode = null;

    // Tooltip Setup
    const tooltip = d3.select("body")
        .append("div")
        .attr("class", "tooltip")
        .style("position", "absolute")
        .style("background", "#fff")
        .style("border", "1px solid #ccc")
        .style("padding", "8px")
        .style("border-radius", "5px")
        .style("box-shadow", "0px 2px 5px rgba(0,0,0,0.2)")
        .style("visibility", "hidden")
        .style("font-size", "14px");

    // Summary Box Setup
    const summaryBox = d3.select("body")
        .append("div")
        .attr("id", "summary-box")
        .style("border", "1px solid #ccc")
        .style("padding", "10px")
        .style("margin-top", "20px")
        .style("background", "#f9f9f9")
        .style("border-radius", "5px")
        .style("width", "300px")
        .style("position", "absolute")  // Make it absolute for hovering
        .style("visibility", "hidden");  // Initially hidden

    // Draw Sunburst Paths
    const paths = svg.selectAll("path")
        .data(root.descendants().filter(d => d.depth))
        .enter().append("path")
        .attr("d", arc)
        .style("fill", d => {
            if (d.depth === 3) return color(d.data.name); // Diagnosed vs N Diagnosed
            if (d.depth === 2) return ageGroupColor(d.data.name); // Age Group
            if (d.depth === 1) return genderColor(d.data.name); // Gender
            return "#ccc";
        })
        .style("stroke", "#fff")
        .style("stroke-width", 1)
        .on("mouseover", function(event, d) {
            const total = d3.sum(d.parent.children, (child) => child.value);
            const percentage = ((d.value / total) * 100).toFixed(2);

            let tooltipContent = `<strong>${d.data.name}</strong><br>Count: ${d.value}<br>Percentage: ${percentage}%`;
            if (d.depth === 3) {
                tooltipContent += `<br>Ethnicity: ${d.data.ethnicity}`;
            }

            tooltip.style("visibility", "visible")
                .html(tooltipContent)
                .style("top", `${event.pageY - 10}px`)
                .style("left", `${event.pageX + 10}px`);

            d3.select(this).style("fill", " #FFFFFF");
        })
        .on("mousemove", function(event) {
            tooltip.style("top", `${event.pageY - 10}px`)
                .style("left", `${event.pageX + 10}px`);
        })
        .on("mouseout", function() {
            tooltip.style("visibility", "hidden");
            d3.select(this).style("fill", function(d) {
                if (d.depth === 3) return color(d.data.name); // Diagnosed vs N Diagnosed
                if (d.depth === 2) return ageGroupColor(d.data.name); // Age Group
                if (d.depth === 1) return genderColor(d.data.name); // Gender
                return "#ccc";
            });
        })
        .on("click", function(event, d) {
            if (selectedNode === d) {
                resetView();
                selectedNode = null;
                summaryBox.style("visibility", "hidden"); // Hide summary when resetting
            } else {
                selectedNode = d;
                filterView(d);
                updateSummary(d, event); // Pass event to updateSummary function
                summaryBox.style("visibility", "visible"); // Show summary box
            }
        });

    // Add Labels Inside Arcs
    svg.selectAll("text")
        .data(root.descendants().filter(d => d.depth))
        .enter().append("text")
        .attr("transform", d => {
            const x = (arc.innerRadius()(d) + arc.outerRadius()(d)) / 2;
            const angle = ((d.x0 + d.x1) / 2) * 180 / Math.PI - 90;
            return `translate(${arc.centroid(d)}) rotate(${angle})`;
        })
        .attr("dy", "0.35em")
        .style("text-anchor", "middle")
        .style("fill", "#000")
        .style("font-size", "12px")
        .style("pointer-events", "none")
        .style("user-select", "none")
        .text(d => d.data.name);

    function filterView(d) {
        svg.selectAll("path")
            .transition().duration(500)
            .style("opacity", path => (path === d || path.parent === d || path.parent?.parent === d ? 1 : 0.1))
            .attr("d", path => (path === d || path.parent === d || path.parent?.parent === d ? arc(path) : ""));

        svg.selectAll("text")
            .transition().duration(500)
            .style("opacity", text => (text === d || text.parent === d || text.parent?.parent === d ? 1 : 0.1));
    }

    function resetView() {
        svg.selectAll("path")
            .transition().duration(500)
            .style("opacity", 1)
            .attr("d", arc);

        svg.selectAll("text")
            .transition().duration(500)
            .style("opacity", 1);
    }

    function updateSummary(d, event) {
        const total = d3.sum(d.parent.children, (child) => child.value);
        const percentage = ((d.value / total) * 100).toFixed(2);

        let summaryContent = `<strong>Selected Node:</strong> ${d.data.name}<br>`;
        summaryContent += `<strong>Percentage:</strong> ${percentage}%<br>`;
        if (d.depth === 3) {
            summaryContent += `<strong>Ethnicity:</strong> ${d.data.ethnicity}<br>`;
        }
        summaryBox.html(summaryContent)
            .style("top", `${event.pageY + 10}px`)  // Position below the mouse
            .style("left", `${event.pageX + 10}px`); // Position to the right of the mouse
    }
});
