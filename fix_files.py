import re

# 1. Fix volume-calculator.astro
with open('src/pages/sites/siliconbased/volume-calculator.astro', 'r') as f:
    content = f.read()

# Update meta description
content = content.replace(
    'description: "Stop guessing 3D volumes. Calculate the exact volume of cubes, spheres, cylinders, and cones instantly with our interactive calculator. See the formulas in action."',
    'description: "Calculate exact 3D volume instantly. Are you underestimating the true capacity of standard shapes? Discover the mathematical secrets that change how you measure empty space."'
)

# Add error message div in HTML
html_to_replace = '''      <div class="result-card">
        <span class="calc-result-label">Calculated Volume</span>'''
html_replacement = '''      <div id="error-message" class="error-message" style="display: none;"></div>
      <div class="result-card">
        <span class="calc-result-label">Calculated Volume</span>'''
content = content.replace(html_to_replace, html_replacement)

# Update Javascript
js_to_replace = '''      function updateCalculation() {
        const config = shapeConfigs[shapeSelect.value];
        const values = config.inputs.map(inputConfig => {
          const el = document.getElementById(inputConfig.id);
          const val = parseFloat(el.value);
          return isNaN(val) || val < 0 ? 0 : val;
        });

        const result = config.calculate(values);
        resultVolume.textContent = formatNumber(result);
      }'''
js_replacement = '''      function updateCalculation() {
        const config = shapeConfigs[shapeSelect.value];
        let hasError = false;
        const errorMessage = document.getElementById("error-message");
        const values = config.inputs.map(inputConfig => {
          const el = document.getElementById(inputConfig.id);
          if (el.value === "") return 0;
          const val = parseFloat(el.value);
          if (isNaN(val) || val < 0) {
            hasError = true;
            return 0;
          }
          return val;
        });

        if (hasError) {
          errorMessage.textContent = "⚠️ Invalid input: Please enter positive numbers only. Dimensions cannot be negative.";
          errorMessage.style.display = "block";
          resultVolume.textContent = "0.00";
        } else {
          errorMessage.style.display = "none";
          const result = config.calculate(values);
          resultVolume.textContent = formatNumber(result);
        }
      }'''
content = content.replace(js_to_replace, js_replacement)

# Add error style
style_to_replace = '''.result-card { background: color-mix(in srgb, var(--accent-color) 10%, transparent);'''
style_replacement = '''.error-message { background: #fee2e2; color: #b91c1c; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border: 1px solid #f87171; font-weight: 500; }
    .result-card { background: color-mix(in srgb, var(--accent-color) 10%, transparent);'''
content = content.replace(style_to_replace, style_replacement)

# Expand explainer
explainer_to_replace = '''<p>Calculating the volume of three-dimensional objects is a fundamental concept in geometry, physics, and everyday engineering. Volume represents the amount of three-dimensional space enclosed by a closed boundary—or, more simply, how much "stuff" can fit inside an object. Our interactive 3D Volume Calculator allows you to instantly determine the capacity of the five most common geometric solids: cubes, spheres, cylinders, cones, and rectangular prisms.</p>'''
explainer_replacement = '''<p>Calculating the volume of three-dimensional objects is a fundamental concept in geometry, physics, and everyday engineering. Volume represents the amount of three-dimensional space enclosed by a closed boundary—or, more simply, how much "stuff" can fit inside an object. Whether you are filling a swimming pool, packaging products for shipment, designing a fuel tank, or studying advanced mathematics, understanding how to accurately compute volume is an indispensable skill. Our interactive 3D Volume Calculator allows you to instantly determine the capacity of the five most common geometric solids: cubes, spheres, cylinders, cones, and rectangular prisms.</p>

      <p>The concept of volume dates back to ancient civilizations. The ancient Egyptians and Babylonians developed empirical formulas to calculate the volume of granaries and pyramids to manage food storage and architectural projects. Later, Greek mathematicians like Archimedes revolutionized the field by using the method of exhaustion to rigorously prove the volume of spheres and cylinders. Today, these ancient principles form the bedrock of modern calculus, engineering design, and computer-aided modeling. When you use our calculator, you are applying centuries of mathematical refinement with a single click.</p>

      <p>Why is volume so critical? Consider the logistics industry. Shipping companies must calculate the exact volumetric weight of packages to optimize cargo space on airplanes and ships. An error in calculating the volume of a rectangular prism (a standard cardboard box) can lead to wasted space and massive financial losses. Similarly, in the medical field, the volume of spheres and cylinders dictates the precise dosage of liquid medications administered through syringes and intravenous drips. Every calculation carries real-world consequences, making precision absolutely vital.</p>'''

content = content.replace(explainer_to_replace, explainer_replacement)

explainer_to_replace2 = '''<p>By providing a seamless, instant way to solve these geometric equations, our Volume Calculator serves as a valuable utility for students learning spatial geometry, professionals requiring quick on-the-job estimations, and anyone needing to calculate the capacity of a 3D object.</p>'''
explainer_replacement2 = '''<p>By providing a seamless, instant way to solve these geometric equations, our Volume Calculator serves as a valuable utility for students learning spatial geometry, professionals requiring quick on-the-job estimations, and anyone needing to calculate the capacity of a 3D object.</p>

      <h3>Advanced Applications and Considerations</h3>
      <p>While standard geometric shapes cover many everyday scenarios, real-world objects are often complex composites of multiple shapes. For instance, a typical silo is not just a cylinder; it is a cylinder topped with a hemisphere or a cone. To find the total volume of such composite objects, engineers break the complex shape down into its fundamental geometric components, calculate the volume of each part using the formulas provided in this tool, and sum the results. This method of decomposition is exactly how modern 3D rendering software and physics engines calculate the properties of complex digital models.</p>

      <p>Furthermore, when discussing volume in the context of fluids, the conversation inevitably turns to density and mass. Volume tells you how much space an object occupies, but it does not tell you how heavy it is. To determine the mass of the contents, you must multiply the calculated volume by the density of the material filling it. For example, a cubic meter of water has a mass of exactly 1,000 kilograms, but a cubic meter of gold has a mass of 19,300 kilograms. This relationship between volume, density, and mass highlights why precise volume calculations are the crucial first step in any structural or material engineering project.</p>

      <p>Finally, it is essential to consider the impact of environmental variables on physical volume. In thermodynamics, the volume of gases and even liquids can expand or contract based on temperature and pressure—a principle described by the Ideal Gas Law and thermal expansion coefficients. While our calculator provides the pure geometric capacity based on static dimensions, real-world applications (like designing pressure vessels or deep-sea submersibles) require incorporating these dynamic physical variables to ensure structural integrity and safety.</p>

      <p>Ultimately, the ability to rapidly and accurately model spatial capacity is a cornerstone of human innovation. We designed this tool to remove the friction of manual computation, allowing you to focus on the higher-level problem-solving and creative design aspects of your projects. We encourage you to experiment with different dimensions and shapes, observing how non-linear changes—like doubling the radius of a sphere—exponentially impact the total volume. Mathematics is not just about numbers; it is about understanding the invisible rules that govern the physical universe.</p>'''
content = content.replace(explainer_to_replace2, explainer_replacement2)

with open('src/pages/sites/siliconbased/volume-calculator.astro', 'w') as f:
    f.write(content)


# 2. Fix hurricane-melissa-tracker-live.astro
with open('src/pages/sites/siliconbased/hurricane-melissa-tracker-live.astro', 'r') as f:
    content2 = f.read()

# Update meta description
content2 = content2.replace(
    'description: "Track Hurricane Melissa\'s exact projected path, wind speeds, and potential impact. Calculate expected storm surge and category based on live meteorological data."',
    'description: "Track Hurricane Melissa\'s projected path and intensity. Will it hit Cat 5? Discover the terrifying math behind storm surge volumes and see how the worst-case scenario unfolds."'
)

# Add error message and change slider to number input + slider
html_to_replace2 = '''        <input type="range" id="projection-time" min="0" max="120" step="1" value="48">
        <span id="time-display" class="time-display">Projected: +48 Hours</span>'''
html_replacement2 = '''        <div id="error-message" class="error-message" style="display: none;"></div>
        <div style="display: flex; gap: 1rem; align-items: center; justify-content: center; margin-bottom: 1rem;">
          <input type="number" id="projection-time-num" min="0" max="168" value="48" style="width: 100px; text-align: center;">
          <input type="range" id="projection-time" min="0" max="168" step="1" value="48" style="flex: 1;">
        </div>
        <span id="time-display" class="time-display">Projected: +48 Hours</span>'''
content2 = content2.replace(html_to_replace2, html_replacement2)

# Update Javascript
js_to_replace2 = '''      function calculateMetrics() {
        const hours = parseInt(timeInput.value, 10);

        timeDisplay.textContent = hours === 0 ? "Current Status (+0 Hours)" : `Projected: +${hours} Hours`;'''
js_replacement2 = '''      const timeInputNum = document.getElementById("projection-time-num");
      const errorMessage = document.getElementById("error-message");

      function syncInputs(e) {
        if (e.target.id === 'projection-time') {
          timeInputNum.value = e.target.value;
        } else {
          timeInput.value = e.target.value;
        }
        calculateMetrics();
      }

      timeInput.addEventListener("input", syncInputs);
      timeInputNum.addEventListener("input", syncInputs);

      function calculateMetrics() {
        const val = parseInt(timeInputNum.value, 10);

        if (isNaN(val) || val < 0 || val > 168) {
          errorMessage.textContent = "⚠️ Invalid projection time. Please enter a value between 0 and 168 hours.";
          errorMessage.style.display = "block";
          return;
        }

        errorMessage.style.display = "none";
        const hours = val;

        timeDisplay.textContent = hours === 0 ? "Current Status (+0 Hours)" : `Projected: +${hours} Hours`;'''
content2 = content2.replace(js_to_replace2, js_replacement2)
content2 = content2.replace('timeInput.addEventListener("input", calculateMetrics);', '')

# Update CSS for error message
style_to_replace2 = '''.input-group label { display: block; margin-bottom: 1rem; font-size: 1.1rem; font-weight: 600; color: var(--text-primary); }'''
style_replacement2 = '''.input-group label { display: block; margin-bottom: 1rem; font-size: 1.1rem; font-weight: 600; color: var(--text-primary); }
    .error-message { background: #fee2e2; color: #b91c1c; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border: 1px solid #f87171; font-weight: 500; text-align: left; }'''
content2 = content2.replace(style_to_replace2, style_replacement2)

# Expand explainer
explainer_to_replace3 = '''<p>Tracking tropical cyclones like Hurricane Melissa requires complex meteorological models that analyze thousands of atmospheric and oceanic data points. Our interactive <strong>Hurricane Melissa Live Tracker</strong> simplifies this data, providing a forward-looking projection of the storm's path, wind intensity, barometric pressure, and potential storm surge volume over the next 120 hours (5 days). By utilizing the slider, users can visually step through time to see how the storm is expected to behave as it interacts with ocean currents, wind shear, and landmasses.</p>'''
explainer_replacement3 = '''<p>Tracking tropical cyclones like Hurricane Melissa requires complex meteorological models that analyze thousands of atmospheric and oceanic data points. Every hour, satellites, ocean buoys, and hurricane hunter aircraft feed massive streams of data into supercomputers, generating highly sophisticated ensemble models. Our interactive <strong>Hurricane Melissa Live Tracker</strong> simplifies this overwhelming influx of data, translating complex meteorological physics into an accessible, forward-looking projection of the storm's path, wind intensity, barometric pressure, and potential storm surge volume over the next 168 hours (7 days). By utilizing the interactive slider, users can visually step through time to see exactly how the storm is expected to behave as it interacts with ocean currents, atmospheric ridges, wind shear, and vulnerable landmasses.</p>

      <p>Tropical cyclones are among the most powerful and destructive natural forces on the planet, capable of unleashing energy equivalent to a 10-megaton nuclear bomb every 20 minutes. Understanding the mechanics behind these atmospheric behemoths is critical for coastal residents, emergency management agencies, and urban planners. When a storm like Melissa threatens a populated coastline, the difference between a minor disruption and a historic catastrophe often comes down to just a few degrees of track shift or a sudden fluctuation in wind intensity. This tracker is designed to bridge the gap between raw scientific data and public awareness, demystifying the variables that determine a hurricane's ultimate destructive potential.</p>'''
content2 = content2.replace(explainer_to_replace3, explainer_replacement3)

explainer_to_replace4 = '''<p>Use this tracker as an educational resource to understand how these massive weather systems evolve over time. Always prioritize safety, prepare evacuation kits early, and follow the guidance of local authorities when a storm threatens your area.</p>'''
explainer_replacement4 = '''<p>Use this tracker as an educational resource to understand how these massive weather systems evolve over time. Always prioritize safety, prepare evacuation kits early, and follow the guidance of local authorities when a storm threatens your area.</p>

      <h3>The Role of Climate Change in Hurricane Intensity</h3>
      <p>As we observe the projected path and intensification of hypothetical storms like Melissa, it is impossible to ignore the growing consensus among climatologists regarding the impact of global warming on tropical cyclone behavior. While climate change may not necessarily increase the total frequency of hurricanes, overwhelming evidence suggests that it is increasing the proportion of storms that reach Category 4 and 5 status. The mechanism behind this is relatively straightforward: rising global temperatures lead to warmer ocean surfaces, which act as high-octane rocket fuel for developing storm systems.</p>

      <p>Furthermore, warmer atmospheric air can hold significantly more moisture. This physical reality means that modern hurricanes are capable of producing much heavier rainfall rates than storms of previous decades, leading to unprecedented inland flooding. We saw this devastating effect in recent historical storms, where the primary cause of damage and loss of life was not the wind, but the catastrophic, slow-moving deluges that submerged entire cities. Additionally, rising global sea levels provide a higher baseline for storm surges, meaning that even a weak Category 1 storm can push a dangerous amount of water into coastal communities that were previously considered safe.</p>

      <p>Meteorologists are also observing a worrying trend known as "rapid intensification." Rapid intensification occurs when a storm's maximum sustained winds increase by at least 35 mph in a 24-hour period. Because of abnormally warm sea surface temperatures, storms are undergoing this dangerous transformation closer to landfall, giving coastal residents far less time to prepare or evacuate. As you use our tracker to model Melissa's timeline, keep in mind that these timeline projections are becoming increasingly difficult for forecasters to lock down when ocean conditions are primed for explosive storm growth.</p>

      <h3>Preparedness and Risk Mitigation</h3>
      <p>The data presented by predictive tools should serve as a catalyst for action, not just a source of anxiety. Coastal vulnerability is a complex equation involving physical geography, urban infrastructure, and community preparedness. When a major hurricane approaches, relying solely on the Saffir-Simpson category can be dangerously misleading. A sprawling, slow-moving Category 2 storm can push a far more devastating storm surge into a shallow bay than a compact, fast-moving Category 4 storm. This is why we have integrated the Estimated Storm Surge Volume metric into our tracker—to highlight the immense, physical weight of the water being displaced.</p>

      <p>Preparedness must be a year-round mindset. Homeowners should understand their exact elevation above sea level, their specific evacuation zone, and the structural integrity of their roofs and windows. We strongly encourage users of this tool to complement their understanding of storm mechanics with actionable emergency plans. Build a resilient disaster supply kit, establish clear communication protocols with family members, and understand the specific insurance policies that protect your property. The science of meteorology allows us to see the danger coming; it is up to us to act on that knowledge.</p>'''
content2 = content2.replace(explainer_to_replace4, explainer_replacement4)

with open('src/pages/sites/siliconbased/hurricane-melissa-tracker-live.astro', 'w') as f:
    f.write(content2)
