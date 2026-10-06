// Mirrored Bar Chart - ASD Diagnosis by Gender & Ethnicity
d3.csv("Autism-Merged-Dataset.csv").then(function(data) {
    console.log("CSV Loaded Successfully:", data); 

    // Convert 'class/asd' to numeric (if necessary)
    data.forEach(d => {
        d["class/asd"] = d["class/asd"] === "yes" ? 1 : d["class/asd"] === "no" ? 0 : +d["class/asd"];
    });

    // Aggregate diagnosis counts by ethnicity
    let groupedData = d3.rollup(data, 
        v => ({
            diagnosed: d3.sum(v, d => d["class/asd"] === 1 ? 1 : 0),
            nonDiagnosed: d3.sum(v, d => d["class/asd"] === 0 ? 1 : 0),
            total: v.length
        }), 
        d => d.ethnicity
    );

    // Convert to array and normalize data (percentage)
    let processedData = Array.from(groupedData, ([key, value]) => ({
        ethnicity: key,
        diagnosed: (value.diagnosed / value.total) * 100, // Normalized percentage
        nonDiagnosed: (value.nonDiagnosed / value.total) * 100 
    }));

    console.log("Processed Data for Mirrored Bar Chart:", processedData); // ✅ Check exact values

    // Set dimensions
    const margin = {top: 50, right: 50, bottom: 50, left: 150};
    const width = 900 - margin.left - margin.right;
    const height = processedData.length * 45; 

    // Create SVG
    const svg = d3.select("#mirrored-bar-chart .viz-container")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left}, ${margin.top})`);

    // Update X-axis domain dynamically
    const maxValue = d3.max(processedData, d => Math.max(d.diagnosed, d.nonDiagnosed));
    const xScale = d3.scaleLinear()
        .domain([-maxValue, maxValue])
        .range([0, width]);

    // Create Y scale
    const yScale = d3.scaleBand()
        .domain(processedData.map(d => d.ethnicity))
        .range([0, height])
        .padding(0.3); // Increased padding for better spacing

    // Add X-axis gridlines
    svg.append("g")
        .attr("class", "grid")
        .call(d3.axisBottom(xScale)
            .tickSize(-height)
            .tickFormat("")
        )
        .attr("transform", `translate(0, ${height})`);

    // Add X-axis
    svg.append("g")
        .attr("transform", `translate(0, ${height})`)
        .call(d3.axisBottom(xScale).ticks(5).tickFormat(d => Math.abs(d) + "%"));

    // Add Y-axis
    svg.append("g")
        .call(d3.axisLeft(yScale));

    // Create Tooltip
    const tooltip = d3.select("body").append("div") 
        .attr("class", "tooltip")       
        .style("position", "absolute")
        .style("background", "rgba(0, 0, 0, 0.8)")
        .style("color", "white")
        .style("border-radius", "5px")
        .style("padding", "8px")
        .style("display", "none")
        .style("pointer-events", "none");

    // Define color palette
    const diagnosedColor = "#E63946";  // Softer red
    const nonDiagnosedColor = "#457B9D";  // Softer blue

    // Bars for Diagnosed (left)
    svg.selectAll(".bar-diagnosed")
        .data(processedData)
        .enter()
        .append("rect")
        .attr("class", "bar-diagnosed")
        .attr("x", d => xScale(-d.diagnosed))
        .attr("y", d => yScale(d.ethnicity))
        .attr("width", d => Math.abs(xScale(d.diagnosed) - xScale(0)))
        .attr("height", yScale.bandwidth())
        .attr("fill", diagnosedColor)
        .on("mouseover", function(event, d) {
            tooltip.style("display", "block")
                .html(`<b>${d.ethnicity}</b><br>Diagnosed: ${d.diagnosed.toFixed(2)}%`)
                .style("left", (event.pageX + 10) + "px") 
                .style("top", (event.pageY - 20) + "px");
        })
        .on("mouseout", () => tooltip.style("display", "none"))
        .on("click", function(event, d) {
            alert(`Ethnicity: ${d.ethnicity}\nDiagnosed: ${d.diagnosed.toFixed(2)}%`);
        });

    // Bars for Non-Diagnosed (right)
    svg.selectAll(".bar-non-diagnosed")
        .data(processedData)
        .enter()
        .append("rect")
        .attr("class", "bar-non-diagnosed")
        .attr("x", xScale(0))
        .attr("y", d => yScale(d.ethnicity))
        .attr("width", d => Math.abs(xScale(d.nonDiagnosed) - xScale(0)))
        .attr("height", yScale.bandwidth())
        .attr("fill", nonDiagnosedColor)
        .on("mouseover", function(event, d) {
            tooltip.style("display", "block")
                .html(`<b>${d.ethnicity}</b><br>Non-Diagnosed: ${d.nonDiagnosed.toFixed(2)}%`)
                .style("left", (event.pageX + 10) + "px") 
                .style("top", (event.pageY - 20) + "px");
        })
        .on("mouseout", () => tooltip.style("display", "none"))
        .on("click", function(event, d) {
            alert(`Ethnicity: ${d.ethnicity}\nNon-Diagnosed: ${d.nonDiagnosed.toFixed(2)}%`);
        });

    // Add legend
    svg.append("text").attr("x", xScale(-50)).attr("y", -20).text("Diagnosed (%)").style("fill", diagnosedColor);
    svg.append("text").attr("x", xScale(50)).attr("y", -20).text("Non-Diagnosed (%)").style("fill", nonDiagnosedColor);

    // Add chart title
    svg.append("text")
        .attr("x", width / 2)
        .attr("y", -30)
        .attr("text-anchor", "middle")
        .style("font-size", "16px")
        .style("font-weight", "bold")
        .text("ASD Diagnosis Rates by Ethnicity");

});