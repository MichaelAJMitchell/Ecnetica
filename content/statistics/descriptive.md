# Descriptive Statistics

## Data Representation Revision

### Theory

Descriptive statistics builds upon data representation concepts, using organized data displays to calculate summary measures that describe the main features of a dataset. Understanding data organization is essential for accurate statistical calculations.

$$\text{Frequency Distribution} = \{(x_i, f_i) : i = 1, 2, ..., k\}$$

where $x_i$ represents values/categories and $f_i$ represents their frequencies.

$$\text{Total Frequency} = n = \sum_{i=1}^{k} f_i$$

### Application

#### Examples

##### Example 1: Calculating Statistics from Frequency Tables
Let's calculate basic summary statistics from grouped data.

Data: Test scores with frequencies: 60-69 (3), 70-79 (7), 80-89 (12), 90-99 (8)

**Method 1: Find Modal Class and Total**

$\text{Total students} = 3 + 7 + 12 + 8 = 30 \quad \text{(sum all frequencies)}$

$\text{Modal class} = 80-89 \quad \text{(highest frequency of 12)}$

$\text{Relative frequency of modal class} = \frac{12}{30} = 0.4 \quad \text{(40\% of data)}$

#### Interactive Visualization: Frequency Distribution Explorer

<div id="data-summary-container" class="visualization-container" style="height: 500px; display: flex; align-items: center; justify-content: center; background-color: #f8f9fa; border: 2px dashed #dee2e6; border-radius: 8px;">
    <div style="text-align: center; color: #6c757d; font-size: 18px; font-weight: 500;">
        Interactive Graph
        <div style="font-size: 14px; margin-top: 8px; font-weight: normal;">
            Frequency distribution and statistical measures visualization will be implemented here
        </div>
    </div>
</div>

#### Multiple Choice Questions

<div id="data-summary-mcq" class="quiz-container"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const quizData = {
        title: "Data Representation Review Questions",
        questions: [
            {
                text: "Which measure of central tendency is most affected by extreme values?",
                options: ["Mode", "Median", "Mean", "Range"],
                correctIndex: 2,
                explanation: "The mean is most affected by extreme values because it uses all data values in its calculation.",
                difficulty: "Basic"
            },
            {
                text: "In a frequency table with classes 0-10, 10-20, 20-30, what is the class midpoint of 10-20?",
                options: ["\\(10\\)", "\\(15\\)", "\\(20\\)", "\\(14.5\\)"],
                correctIndex: 1,
                explanation: "Class midpoint = \\(\\frac{10 + 20}{2} = 15\\)",
                difficulty: "Basic"
            }
        ]
    };
    MCQQuiz.create('data-summary-mcq', quizData);
});
</script>

## Descriptive Statistics

### Theory

**Foundational Definitions:** Descriptive statistics summarize and describe the main features of a dataset through numerical measures and graphical representations. These statistics provide insight into the center, spread, and shape of data distributions.

**Measures of Central Tendency:**

**Mean (Arithmetic Average):** The sum of all values divided by the number of values

$$\bar{x} = \frac{\sum_{i=1}^{n} x_i}{n} = \frac{x_1 + x_2 + ... + x_n}{n}$$

• Properties: Affected by extreme values (outliers)
• Uses all data values in calculation
• For grouped data: $\bar{x} = \frac{\sum f_i x_i}{\sum f_i}$ where $x_i$ is class midpoint
• Weighted mean: $\bar{x}_w = \frac{\sum w_i x_i}{\sum w_i}$ where $w_i$ are weights

**Median:** The middle value when data is arranged in order

• For odd n: Median = value at position $\frac{n+1}{2}$
• For even n: Median = average of values at positions $\frac{n}{2}$ and $\frac{n}{2} + 1$
• Properties: Not affected by extreme values
• For grouped data: $\text{Median} = L + \frac{\frac{n}{2} - F}{f} \times h$
  where L = lower boundary of median class, F = cumulative frequency before median class, f = frequency of median class, h = class width

**Mode:** The most frequently occurring value(s)

• Can have no mode, one mode (unimodal), or multiple modes (bimodal, multimodal)
• For grouped data: Modal class has highest frequency
• Estimated mode: $\text{Mode} = L + \frac{d_1}{d_1 + d_2} \times h$
  where $d_1$ = difference with previous class frequency, $d_2$ = difference with next class frequency

**Measures of Spread (Dispersion):**

**Range:** The difference between maximum and minimum values

$$\text{Range} = x_{max} - x_{min}$$

• Simple but affected by extreme values
• Interquartile range (IQR): $IQR = Q_3 - Q_1$ (more robust)

**Variance:** Average squared deviation from the mean

Population variance: $$\sigma^2 = \frac{\sum_{i=1}^{n} (x_i - \mu)^2}{n}$$

Sample variance: $$s^2 = \frac{\sum_{i=1}^{n} (x_i - \bar{x})^2}{n-1}$$

• Alternative formula: $\sigma^2 = \frac{\sum x_i^2}{n} - \mu^2$
• For grouped data: $\sigma^2 = \frac{\sum f_i(x_i - \bar{x})^2}{\sum f_i}$

**Standard Deviation:** Square root of variance

$$\sigma = \sqrt{\sigma^2} \quad \text{(population)}$$
$$s = \sqrt{s^2} \quad \text{(sample)}$$

• Properties: Same units as original data
• Approximately 68% of data within 1 standard deviation of mean (normal distribution)
• Approximately 95% within 2 standard deviations
• Approximately 99.7% within 3 standard deviations

**Measures of Position:**

**Quartiles:** Divide ordered data into four equal parts

• $Q_1$ (First quartile): 25th percentile
• $Q_2$ (Second quartile): 50th percentile (median)
• $Q_3$ (Third quartile): 75th percentile
• Position formula: $Q_k$ position = $\frac{k(n+1)}{4}$

**Percentiles:** Divide data into 100 equal parts

$$P_k \text{ position} = \frac{k(n+1)}{100}$$

**Box Plots (Box-and-Whisker Plots):** Visual summary of five-number summary

• Minimum, $Q_1$, Median, $Q_3$, Maximum
• Shows outliers: values beyond $Q_1 - 1.5 \times IQR$ or $Q_3 + 1.5 \times IQR$
• Indicates skewness through asymmetry

**Coefficient of Variation:** Relative measure of variability

$$CV = \frac{s}{\bar{x}} \times 100\%$$

• Useful for comparing variability between datasets with different units or scales
• Dimensionless measure

#### Interactive Visualization: Descriptive Statistics Explorer

<div id="descriptive-statistics-container" class="visualization-container" style="height: 500px; display: flex; align-items: center; justify-content: center; background-color: #f8f9fa; border: 2px dashed #dee2e6; border-radius: 8px;">
    <div style="text-align: center; color: #6c757d; font-size: 18px; font-weight: 500;">
        Interactive Graph
        <div style="font-size: 14px; margin-top: 8px; font-weight: normal;">
            Interactive descriptive statistics calculator and visualization will be implemented here
        </div>
    </div>
</div>

### Application

#### Examples

##### Example 1: Calculating Mean, Median, and Mode
Solve: Find the mean, median, and mode for the dataset: 12, 15, 18, 15, 22, 15, 19, 20, 18, 25

**Method 1: Direct Calculation**

$\text{Ordered data: } 12, 15, 15, 15, 18, 18, 19, 20, 22, 25 \quad \text{(arrange in order)}$

$\bar{x} = \frac{12 + 15 + 15 + 15 + 18 + 18 + 19 + 20 + 22 + 25}{10} = \frac{179}{10} = 17.9 \quad \text{(mean)}$

$\text{Median} = \frac{18 + 18}{2} = 18 \quad \text{(average of 5th and 6th values)}$

$\text{Mode} = 15 \quad \text{(appears 3 times, most frequent)}$

##### Example 2: Computing Standard Deviation
Solve: Calculate the population standard deviation for: 4, 7, 9, 10, 14

**Method 1: Definition Formula**

$\mu = \frac{4 + 7 + 9 + 10 + 14}{5} = \frac{44}{5} = 8.8 \quad \text{(calculate mean first)}$

$\sum(x_i - \mu)^2 = (4-8.8)^2 + (7-8.8)^2 + (9-8.8)^2 + (10-8.8)^2 + (14-8.8)^2$

$= 23.04 + 3.24 + 0.04 + 1.44 + 27.04 = 54.8 \quad \text{(sum of squared deviations)}$

$\sigma = \sqrt{\frac{54.8}{5}} = \sqrt{10.96} = 3.31 \quad \text{(population standard deviation)}$

**Method 2: Alternative Formula**

$\sum x_i^2 = 16 + 49 + 81 + 100 + 196 = 442 \quad \text{(sum of squares)}$

$\sigma^2 = \frac{442}{5} - (8.8)^2 = 88.4 - 77.44 = 10.96 \quad \text{(variance)}$

$\sigma = \sqrt{10.96} = 3.31 \quad \text{(confirms our result)}$

##### Example 3: Finding Quartiles and Creating Box Plot
Solve: Find the five-number summary for: 23, 25, 28, 30, 32, 35, 38, 40, 42, 45, 48, 52, 55

**Method 1: Position Formula**

$n = 13 \quad \text{(count data points)}$

$Q_1 \text{ position} = \frac{1(13+1)}{4} = 3.5 \quad \text{(between 3rd and 4th values)}$

$Q_1 = \frac{28 + 30}{2} = 29 \quad \text{(interpolate)}$

$Q_2 \text{ (median) position} = \frac{2(13+1)}{4} = 7 \quad \text{(7th value)}$

$Q_2 = 38 \quad \text{(middle value)}$

$Q_3 \text{ position} = \frac{3(13+1)}{4} = 10.5 \quad \text{(between 10th and 11th values)}$

$Q_3 = \frac{45 + 48}{2} = 46.5 \quad \text{(interpolate)}$

$\text{Five-number summary: Min}=23, Q_1=29, \text{Median}=38, Q_3=46.5, \text{Max}=55$

#### Multiple Choice Questions

<div id="descriptive-statistics-mcq" class="quiz-container"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const quizData = {
        title: "Descriptive Statistics Practice Questions",
        questions: [
            {
                text: "For the dataset {2, 4, 4, 4, 5, 5, 7, 9}, what is the relationship between mean, median, and mode?",
                options: ["Mean < Median < Mode", "Mode < Median < Mean", "Mode = Median < Mean", "Mean = Median = Mode"],
                correctIndex: 1,
                explanation: "Mode = 4 (most frequent), Median = 4.5 (average of 4 and 5), Mean = 5 (40/8). So Mode < Median < Mean, indicating positive skew.",
                difficulty: "Intermediate"
            },
            {
                text: "If a dataset has variance \\(\\sigma^2 = 16\\), what is the standard deviation?",
                options: ["\\(2\\)", "\\(4\\)", "\\(8\\)", "\\(256\\)"],
                correctIndex: 1,
                explanation: "Standard deviation = \\(\\sqrt{\\text{variance}} = \\sqrt{16} = 4\\)",
                difficulty: "Basic"
            },
            {
                text: "In a box plot, what percentage of data typically lies between Q1 and Q3?",
                options: ["25%", "50%", "75%", "100%"],
                correctIndex: 1,
                explanation: "The interquartile range (Q1 to Q3) contains the middle 50% of the data.",
                difficulty: "Basic"
            },
            {
                text: "Which measure of spread is most appropriate for comparing variability between heights (cm) and weights (kg)?",
                options: ["Range", "Standard deviation", "Coefficient of variation", "Variance"],
                correctIndex: 2,
                explanation: "Coefficient of variation (CV) is dimensionless and allows comparison between datasets with different units.",
                difficulty: "Intermediate"
            }
        ]
    };
    MCQQuiz.create('descriptive-statistics-mcq', quizData);
});
</script>

#### Sector Specific Questions: Descriptive Statistics Applications

<div id="descriptive-statistics-identity-container"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const descriptiveStatisticsContent = {
        "title": "Descriptive Statistics: Applications",
        "intro_content": `<p>Descriptive statistics are fundamental tools used across all sectors to summarize data, identify patterns, and make informed decisions. From analyzing experimental results to monitoring financial performance, these measures provide essential insights for problem-solving and optimization.</p>`,
        "questions": [
            {
                "category": "scientific",
                "title": "Chemistry: Reaction Rate Analysis",
                "content": `A chemist measures reaction completion times (minutes) in 10 trials: 12.3, 11.8, 12.5, 13.1, 12.2, 11.9, 12.7, 12.4, 12.8, 12.6. Calculate the mean, standard deviation, and coefficient of variation. Determine if any measurements should be considered outliers using the 1.5×IQR rule.`,
                "answer": `<p><strong>Solution:</strong></p>
                <p>Step 1: Calculate mean</p>
                <p>\\(\\bar{x} = \\frac{12.3 + 11.8 + 12.5 + 13.1 + 12.2 + 11.9 + 12.7 + 12.4 + 12.8 + 12.6}{10}\\)</p>
                <p>\\(\\bar{x} = \\frac{124.3}{10} = 12.43\\) minutes</p>
                <p>Step 2: Calculate standard deviation</p>
                <p>\\(\\sum(x_i - \\bar{x})^2 = 0.0169 + 0.3969 + 0.0049 + 0.4489 + 0.0529 + 0.2809 + 0.0729 + 0.0009 + 0.1369 + 0.0289\\)</p>
                <p>\\(= 1.441\\)</p>
                <p>\\(s = \\sqrt{\\frac{1.441}{9}} = \\sqrt{0.1601} = 0.400\\) minutes</p>
                <p>Step 3: Coefficient of variation</p>
                <p>\\(CV = \\frac{0.400}{12.43} \\times 100\\% = 3.22\\%\\)</p>
                <p>Step 4: Check for outliers</p>
                <p>Ordered data: 11.8, 11.9, 12.2, 12.3, 12.4, 12.5, 12.6, 12.7, 12.8, 13.1</p>
                <p>\\(Q_1 = 12.2\\), \\(Q_3 = 12.7\\), \\(IQR = 0.5\\)</p>
                <p>Lower fence: \\(12.2 - 1.5(0.5) = 11.45\\)</p>
                <p>Upper fence: \\(12.7 + 1.5(0.5) = 13.45\\)</p>
                <p>All values fall within fences, so no outliers. Low CV (3.22%) indicates consistent reaction times.</p>`
            },
            {
                "category": "engineering",
                "title": "Mechanical Engineering: Tensile Strength Testing",
                "content": `Steel cable samples show breaking strengths (kN): 85-90 (8 samples), 90-95 (15 samples), 95-100 (22 samples), 100-105 (12 samples), 105-110 (3 samples). Calculate the mean and standard deviation for this grouped data. What percentage of cables meet a 92 kN minimum specification?`,
                "answer": `<p><strong>Solution:</strong></p>
                <p>Step 1: Find class midpoints and calculate mean</p>
                <p>Midpoints: 87.5, 92.5, 97.5, 102.5, 107.5</p>
                <p>\\(\\bar{x} = \\frac{8(87.5) + 15(92.5) + 22(97.5) + 12(102.5) + 3(107.5)}{60}\\)</p>
                <p>\\(= \\frac{700 + 1387.5 + 2145 + 1230 + 322.5}{60} = \\frac{5785}{60} = 96.42\\) kN</p>
                <p>Step 2: Calculate standard deviation</p>
                <p>\\(\\sum f_i(x_i - \\bar{x})^2 = 8(87.5-96.42)^2 + 15(92.5-96.42)^2 + 22(97.5-96.42)^2 + 12(102.5-96.42)^2 + 3(107.5-96.42)^2\\)</p>
                <p>\\(= 8(79.57) + 15(15.37) + 22(1.17) + 12(36.97) + 3(122.77)\\)</p>
                <p>\\(= 636.56 + 230.55 + 25.74 + 443.64 + 368.31 = 1704.8\\)</p>
                <p>\\(\\sigma = \\sqrt{\\frac{1704.8}{60}} = \\sqrt{28.41} = 5.33\\) kN</p>
                <p>Step 3: Percentage meeting 92 kN specification</p>
                <p>Classes 85-90: Approximately 5 of 8 samples > 92 kN (using linear interpolation)</p>
                <p>Classes 90-95 and above: All samples > 92 kN</p>
                <p>Total meeting spec: \\(5 + 15 + 22 + 12 + 3 = 57\\)</p>
                <p>Percentage: \\(\\frac{57}{60} \\times 100\\% = 95\\%\\)</p>`
            },
            {
                "category": "financial",
                "title": "Banking: Customer Transaction Analysis",
                "content": `A bank analyzes daily ATM withdrawals (€): 20, 50, 50, 100, 20, 200, 50, 100, 50, 20, 150, 100, 50, 300, 50. Calculate measures of central tendency and create a five-number summary. Identify the most common withdrawal amount and explain what the IQR tells us about customer behavior.`,
                "answer": `<p><strong>Solution:</strong></p>
                <p>Step 1: Order the data</p>
                <p>20, 20, 20, 50, 50, 50, 50, 50, 50, 100, 100, 100, 150, 200, 300</p>
                <p>Step 2: Measures of central tendency</p>
                <p>Mean: \\(\\bar{x} = \\frac{1410}{15} = 94\\) €</p>
                <p>Median: 8th value = 50 €</p>
                <p>Mode: 50 € (appears 6 times)</p>
                <p>Step 3: Five-number summary</p>
                <p>Min = 20 €</p>
                <p>\\(Q_1\\) position = \\(\\frac{15+1}{4} = 4\\), so \\(Q_1 = 50\\) €</p>
                <p>Median = 50 €</p>
                <p>\\(Q_3\\) position = \\(\\frac{3(15+1)}{4} = 12\\), so \\(Q_3 = 100\\) €</p>
                <p>Max = 300 €</p>
                <p>Step 4: Analysis</p>
                <p>IQR = 100 - 50 = 50 €</p>
                <p>The IQR of 50 € shows that the middle 50% of withdrawals range from 50 € to 100 €, indicating most customers withdraw moderate amounts. The mode of 50 € suggests this is a standard ATM denomination. The mean (94 €) exceeds the median (50 €), showing positive skew due to occasional large withdrawals.</p>`
            },
            {
                "category": "creative",
                "title": "Music Production: Audio Level Analysis",
                "content": `A sound engineer measures peak decibel levels across 12 song sections: 68, 72, 85, 78, 82, 90, 75, 88, 92, 86, 80, 84. Calculate the mean, standard deviation, and determine the dynamic range (max - min). If industry standards recommend keeping 95% of peaks within ±2 standard deviations of the mean, what dB range should be targeted?`,
                "answer": `<p><strong>Solution:</strong></p>
                <p>Step 1: Calculate mean</p>
                <p>\\(\\bar{x} = \\frac{68 + 72 + 85 + 78 + 82 + 90 + 75 + 88 + 92 + 86 + 80 + 84}{12}\\)</p>
                <p>\\(= \\frac{980}{12} = 81.67\\) dB</p>
                <p>Step 2: Calculate standard deviation</p>
                <p>\\(\\sum(x_i - 81.67)^2 = 183.11 + 93.44 + 11.11 + 13.44 + 0.11 + 69.44 + 44.44 + 40.11 + 106.78 + 18.78 + 2.78 + 5.44\\)</p>
                <p>\\(= 589.0\\)</p>
                <p>\\(s = \\sqrt{\\frac{589.0}{11}} = \\sqrt{53.55} = 7.32\\) dB</p>
                <p>Step 3: Dynamic range</p>
                <p>Dynamic range = 92 - 68 = 24 dB</p>
                <p>Step 4: Target range for 95% of peaks</p>
                <p>Lower limit: \\(81.67 - 2(7.32) = 67.03\\) dB</p>
                <p>Upper limit: \\(81.67 + 2(7.32) = 96.31\\) dB</p>
                <p>Target range: 67-96 dB</p>
                <p>This range accommodates natural dynamic variation while maintaining consistent listening levels. Current measurements show good control with all peaks within the recommended range.</p>`
            }
        ]
    };
    MathQuestionModule.render(descriptiveStatisticsContent, 'descriptive-statistics-identity-container');
});
</script>

### Key Takeaways

```{important}
1. **Mean, median, and mode**: Each measures center differently - choose based on data distribution and outliers
2. **Standard deviation**: Measures typical distance from the mean; use with mean for symmetric data
3. **Quartiles and IQR**: Robust measures unaffected by outliers; use with median for skewed data
4. **Variance uses squared units**: Always take square root for standard deviation to match data units
5. **Coefficient of variation**: Enables comparison of variability across different scales or units
6. **Box plots**: Visualize five-number summary and identify outliers using 1.5×IQR rule
7. **Sample vs population**: Use n-1 for sample variance/standard deviation, n for population
8. **Grouped data formulas**: Use class midpoints and frequencies when raw data unavailable
```