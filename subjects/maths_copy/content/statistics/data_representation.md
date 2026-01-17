# Data Representation

## Data Fundamentals Revision

### Theory

Data representation builds upon understanding different types of data and the importance of organizing information effectively for analysis. Data can be classified as qualitative (categorical) or quantitative (numerical), with quantitative data further divided into discrete (countable) or continuous (measurable).

$$\text{Relative Frequency} = \frac{\text{Frequency}}{\text{Total Number of Observations}}$$

$$\text{Percentage Frequency} = \text{Relative Frequency} \times 100\%$$

### Application

#### Examples

##### Example 1: Basic Data Classification
Survey data collected from 30 students about favorite subjects: Math (8), Science (7), English (6), History (5), Art (4)

**Method 1: Frequency Analysis**

$\text{Total responses} = 8 + 7 + 6 + 5 + 4 = 30 \quad \text{(sum all frequencies)}$

$\text{Relative frequency for Math} = \frac{8}{30} = 0.267 \quad \text{(approximately 26.7\%)}$

$\text{Modal category} = \text{Math} \quad \text{(highest frequency of 8)}$

#### Interactive Visualization: Data Types Explorer

<div id="data-fundamentals-container" class="visualization-container" style="height: 500px; display: flex; align-items: center; justify-content: center; background-color: #f8f9fa; border: 2px dashed #dee2e6; border-radius: 8px;">
    <div style="text-align: center; color: #6c757d; font-size: 18px; font-weight: 500;">
        Interactive Graph
        <div style="font-size: 14px; margin-top: 8px; font-weight: normal;">
            Data types and frequency distribution visualization will be implemented here
        </div>
    </div>
</div>

#### Multiple Choice Questions

<div id="data-fundamentals-mcq" class="quiz-container"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const quizData = {
        title: "Data Fundamentals Practice Questions",
        questions: [
            {
                text: "Which type of data would the number of students in a class be classified as?",
                options: ["Qualitative", "Quantitative Continuous", "Quantitative Discrete", "Categorical"],
                correctIndex: 2,
                explanation: "The number of students is quantitative discrete data because it consists of countable whole numbers.",
                difficulty: "Basic"
            },
            {
                text: "If a survey of 50 people shows 15 prefer coffee, what is the relative frequency?",
                options: ["\\(0.15\\)", "\\(0.30\\)", "\\(0.50\\)", "\\(15\\)"],
                correctIndex: 1,
                explanation: "Relative frequency = \\(\\frac{15}{50} = 0.30\\)",
                difficulty: "Basic"
            }
        ]
    };
    MCQQuiz.create('data-fundamentals-mcq', quizData);
});
</script>

## Data Representation

### Theory

**Foundational Definitions:** Data representation involves organizing and displaying information to reveal patterns, trends, and insights. It transforms raw data into visual or tabular formats that facilitate understanding and analysis.

**Key Visualization Methods and Their Properties:**

**Frequency Tables:** Organize data into categories with their corresponding counts

• Structure: Categories/Values | Frequency | Relative Frequency | Percentage
• Purpose: Summarize data distribution and calculate proportions
• Formula: $\text{Cumulative Frequency}_i = \sum_{j=1}^{i} f_j$

**Bar Charts:** Display categorical data using rectangular bars

• Properties: Bars are separated (not touching), height represents frequency
• Orientation: Can be vertical (column chart) or horizontal
• Special case: Grouped bar charts for comparing multiple datasets
• Formula for bar height: $h_i = k \cdot f_i$ where $k$ is a scaling constant

**Histograms:** Show distribution of continuous data using connected bars

• Key distinction: Bars touch (no gaps) representing continuous intervals
• Equal-width intervals: $\text{Width} = \frac{\text{Range}}{\text{Number of intervals}}$
• Unequal-width intervals: Use frequency density = $\frac{\text{Frequency}}{\text{Interval width}}$
• Area principle: Area of bar ∝ frequency

**Pie Charts:** Display parts of a whole using circular sectors

$\text{Central Angle} = \frac{\text{Category Frequency}}{\text{Total Frequency}} \times 360°$

$\text{Sector Area} = \frac{\text{Central Angle}}{360°} \times \pi r^2$

**Line Graphs:** Show changes over time or relationships between continuous variables

• Properties: Points connected by line segments
• Multiple series: Different lines for comparison
• Time series: X-axis represents time periods
• Interpolation: Estimating values between data points

**Stem-and-Leaf Plots:** Display data while preserving individual values

• Structure: Stem (leading digits) | Leaf (trailing digits)
• Advantage: Shows distribution and retains actual data values
• Back-to-back: Compare two datasets
• Key: Always specify the unit represented by stem|leaf

**Cumulative Frequency Curves (Ogives):** Show running totals of frequencies

$$F(x) = \sum_{x_i \leq x} f_i$$

• Less than ogive: Plots cumulative frequency against upper class boundaries
• Greater than ogive: Plots cumulative frequency against lower class boundaries
• Median location: At $\frac{n}{2}$ on the cumulative frequency axis
• Quartile locations: $Q_1$ at $\frac{n}{4}$, $Q_3$ at $\frac{3n}{4}$

#### Interactive Visualization: Data Representation Methods

<div id="data-representation-container" class="visualization-container" style="height: 500px; display: flex; align-items: center; justify-content: center; background-color: #f8f9fa; border: 2px dashed #dee2e6; border-radius: 8px;">
    <div style="text-align: center; color: #6c757d; font-size: 18px; font-weight: 500;">
        Interactive Graph
        <div style="font-size: 14px; margin-top: 8px; font-weight: normal;">
            Multiple data representation methods comparison will be implemented here
        </div>
    </div>
</div>

### Application

#### Examples

##### Example 1: Creating a Frequency Table
Solve: Organize the following test scores into a frequency table with class intervals of width 10: 
45, 67, 72, 89, 56, 91, 78, 83, 62, 75, 88, 93, 71, 85, 79

**Method 1: Systematic Organization**

$\text{Range} = 93 - 45 = 48 \quad \text{(find data spread)}$

$\text{Number of intervals} = \lceil \frac{48}{10} \rceil = 5 \quad \text{(round up to cover all data)}$

$\text{Class intervals: } 40-49, 50-59, 60-69, 70-79, 80-89, 90-99 \quad \text{(establish boundaries)}$

$\text{Frequency count: } f_1=1, f_2=1, f_3=2, f_4=5, f_5=4, f_6=2 \quad \text{(tally each interval)}$

##### Example 2: Constructing a Histogram
Solve: Create a histogram for grouped data representing monthly rainfall (mm): 0-20 (3 months), 20-40 (4 months), 40-80 (2 months), 80-120 (3 months)

**Method 1: Equal Area Principle**

$\text{Frequency density}_1 = \frac{3}{20} = 0.15 \quad \text{(for interval 0-20)}$

$\text{Frequency density}_2 = \frac{4}{20} = 0.20 \quad \text{(for interval 20-40)}$

$\text{Frequency density}_3 = \frac{2}{40} = 0.05 \quad \text{(for interval 40-80)}$

$\text{Frequency density}_4 = \frac{3}{40} = 0.075 \quad \text{(for interval 80-120)}$

##### Example 3: Calculating Pie Chart Angles
Solve: A survey of 120 students' transport methods shows: Bus (45), Walk (30), Car (25), Bicycle (20). Calculate the central angles for a pie chart.

**Method 1: Proportional Angle Calculation**

$\text{Angle for Bus} = \frac{45}{120} \times 360° = 135° \quad \text{(largest sector)}$

$\text{Angle for Walk} = \frac{30}{120} \times 360° = 90° \quad \text{(quarter circle)}$

$\text{Angle for Car} = \frac{25}{120} \times 360° = 75° \quad \text{(calculate proportion)}$

$\text{Angle for Bicycle} = \frac{20}{120} \times 360° = 60° \quad \text{(smallest sector)}$

#### Multiple Choice Questions

<div id="data-representation-mcq" class="quiz-container"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const quizData = {
        title: "Data Representation Practice Questions",
        questions: [
            {
                text: "In a histogram with unequal class widths, what should be plotted on the vertical axis?",
                options: ["Frequency", "Frequency density", "Cumulative frequency", "Relative frequency"],
                correctIndex: 1,
                explanation: "Frequency density must be used for unequal class widths to ensure the area of each bar represents the frequency correctly.",
                difficulty: "Intermediate"
            },
            {
                text: "A stem-and-leaf plot shows: 3|2 5 7. If the key states 3|2 = 32, what are the data values?",
                options: ["3.2, 3.5, 3.7", "32, 35, 37", "23, 53, 73", "320, 350, 370"],
                correctIndex: 1,
                explanation: "Using the key 3|2 = 32, the stem 3 with leaves 2, 5, 7 gives us 32, 35, 37.",
                difficulty: "Basic"
            },
            {
                text: "For the dataset {2, 5, 5, 7, 8, 10, 12}, at what cumulative frequency value would you find the median on an ogive?",
                options: ["\\(3\\)", "\\(3.5\\)", "\\(4\\)", "\\(7\\)"],
                correctIndex: 1,
                explanation: "With n = 7, the median is at position \\(\\frac{7}{2} = 3.5\\) on the cumulative frequency scale.",
                difficulty: "Intermediate"
            }
        ]
    };
    MCQQuiz.create('data-representation-mcq', quizData);
});
</script>

#### Sector Specific Questions: Data Representation Applications

<div id="data-representation-identity-container"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const dataRepresentationContent = {
        "title": "Data Representation: Applications",
        "intro_content": `<p>Data representation techniques are essential across all sectors for communicating information effectively. Whether analyzing experimental results, monitoring production processes, tracking financial trends, or visualizing creative projects, choosing the appropriate representation method is crucial for clarity and insight.</p>`,
        "questions": [
            {
                "category": "scientific",
                "title": "Biology: Population Growth Study",
                "content": `A biologist studying bacterial growth recorded the following population counts (in thousands) at hourly intervals: 2, 3, 5, 8, 13, 21, 34, 55. Create a line graph representation and explain why this is the most appropriate method for this data.`,
                "answer": `<p><strong>Solution:</strong></p>
                <p>Line graph is most appropriate because:</p>
                <p>1. Time series data: X-axis represents continuous time (hours)</p>
                <p>2. Shows growth trend: Exponential pattern clearly visible</p>
                <p>3. Allows interpolation: Can estimate population between measurements</p>
                <p>4. Key features:</p>
                <p>• Plot points: (0,2), (1,3), (2,5), (3,8), (4,13), (5,21), (6,34), (7,55)</p>
                <p>• Connect with smooth curve (not straight lines) for biological growth</p>
                <p>• Label axes: Time (hours) vs Population (thousands)</p>
                <p>• Include title: "Bacterial Population Growth Over Time"</p>
                <p>The Fibonacci-like pattern suggests exponential growth with ratio ≈ 1.618</p>`
            },
            {
                "category": "engineering",
                "title": "Manufacturing: Quality Control Analysis",
                "content": `A factory produces electronic components with the following defect distribution over 1000 units: Electrical faults (45), Physical damage (30), Calibration errors (15), Other (10). Create both a Pareto chart and calculate pie chart angles to help prioritize quality improvements.`,
                "answer": `<p><strong>Solution:</strong></p>
                <p>Pareto Chart Construction:</p>
                <p>1. Order by frequency: Electrical (45), Physical (30), Calibration (15), Other (10)</p>
                <p>2. Calculate cumulative percentages:</p>
                <p>• Electrical: \\(\\frac{45}{100} = 45\\%\\) (cumulative: 45%)</p>
                <p>• Physical: \\(\\frac{30}{100} = 30\\%\\) (cumulative: 75%)</p>
                <p>• Calibration: \\(\\frac{15}{100} = 15\\%\\) (cumulative: 90%)</p>
                <p>• Other: \\(\\frac{10}{100} = 10\\%\\) (cumulative: 100%)</p>
                <p>Pie Chart Angles:</p>
                <p>• Electrical: \\(0.45 \\times 360° = 162°\\)</p>
                <p>• Physical: \\(0.30 \\times 360° = 108°\\)</p>
                <p>• Calibration: \\(0.15 \\times 360° = 54°\\)</p>
                <p>• Other: \\(0.10 \\times 360° = 36°\\)</p>
                <p>The Pareto principle suggests focusing on electrical and physical defects (75% of problems)</p>`
            },
            {
                "category": "financial",
                "title": "Investment: Portfolio Distribution Analysis",
                "content": `An investment fund needs to visualize asset allocation: Stocks €2.5M, Bonds €1.8M, Real Estate €1.2M, Commodities €0.5M. Create a pie chart representation and calculate what percentage each sector represents.`,
                "answer": `<p><strong>Solution:</strong></p>
                <p>Total portfolio value: €2.5M + €1.8M + €1.2M + €0.5M = €6.0M</p>
                <p>Percentage calculations:</p>
                <p>• Stocks: \\(\\frac{2.5}{6.0} \\times 100\\% = 41.67\\%\\)</p>
                <p>• Bonds: \\(\\frac{1.8}{6.0} \\times 100\\% = 30.00\\%\\)</p>
                <p>• Real Estate: \\(\\frac{1.2}{6.0} \\times 100\\% = 20.00\\%\\)</p>
                <p>• Commodities: \\(\\frac{0.5}{6.0} \\times 100\\% = 8.33\\%\\)</p>
                <p>Central angles for pie chart:</p>
                <p>• Stocks: \\(0.4167 \\times 360° = 150°\\)</p>
                <p>• Bonds: \\(0.3000 \\times 360° = 108°\\)</p>
                <p>• Real Estate: \\(0.2000 \\times 360° = 72°\\)</p>
                <p>• Commodities: \\(0.0833 \\times 360° = 30°\\)</p>
                <p>This visualization clearly shows stocks dominate the portfolio at over 40%</p>`
            },
            {
                "category": "creative",
                "title": "Film Production: Scene Duration Analysis",
                "content": `A film editor analyzing a 120-minute movie categorized scenes by duration: 0-2 min (45 scenes), 2-5 min (30 scenes), 5-10 min (15 scenes), 10-20 min (5 scenes). Construct a histogram with frequency density to visualize the distribution.`,
                "answer": `<p><strong>Solution:</strong></p>
                <p>Calculate frequency density for each interval:</p>
                <p>• 0-2 min: \\(\\frac{45}{2} = 22.5\\) scenes/min</p>
                <p>• 2-5 min: \\(\\frac{30}{3} = 10\\) scenes/min</p>
                <p>• 5-10 min: \\(\\frac{15}{5} = 3\\) scenes/min</p>
                <p>• 10-20 min: \\(\\frac{5}{10} = 0.5\\) scenes/min</p>
                <p>Histogram construction:</p>
                <p>1. X-axis: Scene duration (minutes)</p>
                <p>2. Y-axis: Frequency density (scenes per minute)</p>
                <p>3. Draw connected bars with heights 22.5, 10, 3, 0.5</p>
                <p>4. No gaps between bars (continuous data)</p>
                <p>Analysis: Most scenes are short (under 2 minutes), typical of modern fast-paced editing. Longer scenes (10-20 min) are rare, likely key dramatic moments.</p>`
            }
        ]
    };
    MathQuestionModule.render(dataRepresentationContent, 'data-representation-identity-container');
});
</script>

### Key Takeaways

```{important}
1. **Choose appropriate representations**: Match the visualization method to your data type and purpose
2. **Frequency density for histograms**: When class widths are unequal, use frequency density = frequency/width
3. **Cumulative frequency curves**: Useful for finding medians, quartiles, and percentiles
4. **Pie charts show proportions**: Calculate angles using (frequency/total) × 360°
5. **Stem-and-leaf plots**: Preserve individual data values while showing distribution
6. **Bar charts vs histograms**: Bars separated for categorical data, touching for continuous data
7. **Always label clearly**: Include titles, axis labels, units, and keys for interpretation
```