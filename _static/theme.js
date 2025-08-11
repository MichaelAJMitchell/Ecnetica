// dark mode and light mode theme toggle
// with a listener for system theme changes

document.addEventListener('DOMContentLoaded', function() {
    createEnhancedThemeToggle();
    createCourseNavigator();
});

function createEnhancedThemeToggle() {
    // Find the navbar end section
    const navbarEnd = document.querySelector('.navbar-nav.navbar-end') || 
                     document.querySelector('.navbar-header-items__end') ||
                     document.querySelector('nav .navbar-nav:last-child');
    
    if (!navbarEnd) {
        console.log('Could not find navbar end section');
        return;
    }
    
    // Detect browser's preferred theme
    const getPreferredTheme = () => {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            return savedTheme;
        }
        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    };
    
    // Set initial theme
    const initialTheme = getPreferredTheme();
    document.documentElement.setAttribute('data-theme', initialTheme);
    
    // Create toggle button
    const themeToggle = document.createElement('button');
    themeToggle.className = 'btn theme-toggle-custom';
    themeToggle.setAttribute('aria-label', 'Toggle theme');
    themeToggle.setAttribute('title', 'Toggle light/dark theme');
    
    // Icon functions using navbar-icon class
    const getSunIcon = () => `<svg class="navbar-icon" viewBox="0 0 24 24">
        <path d="M12 3v2.25m6.364.386-1.591 1.591M21 12h-2.25m-.386 6.364-1.591-1.591M12 18.75V21m-4.773-4.227-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0Z" />
    </svg>`;
    
    const getMoonIcon = () => `<svg class="navbar-icon" viewBox="0 0 24 24">
        <path d="M21.752 15.002A9.72 9.72 0 0 1 18 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 0 0 3 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 0 0 9.002-5.998Z" />
    </svg>`;
    
    // Set initial icon (sun for dark theme, moon for light theme)
    themeToggle.innerHTML = initialTheme === 'dark' ? getSunIcon() : getMoonIcon();
    
    // Add to navbar
    navbarEnd.appendChild(themeToggle);
    
    // Toggle functionality with icon update
    themeToggle.addEventListener('click', function() {
        const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        
        // Update icon with smooth transition
        themeToggle.style.transform = 'scale(0.8)';
        setTimeout(() => {
            themeToggle.innerHTML = newTheme === 'dark' ? getSunIcon() : getMoonIcon();
            themeToggle.style.transform = 'scale(1)';
        }, 100);
    });
    
    // Listen for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
        if (!localStorage.getItem('theme')) {
            const newTheme = e.matches ? 'dark' : 'light';
            document.documentElement.setAttribute('data-theme', newTheme);
            themeToggle.innerHTML = newTheme === 'dark' ? getSunIcon() : getMoonIcon();
        }
    });
}

// course navigator creation
// This function creates a course navigator panel with a structured course outline
// It includes a toggle button, collapsible sections, and search functionality.

function createCourseNavigator() {
    // Course structure - matches _toc.yml might be better to use a JSON file
    const courseStructure = {
        'Introduction': {
            'Course Overview': '/content/introduction/course_overview.html',
            'Mathematical Thinking': {
                'Problem Solving': '/content/introduction/problem_solving.html',
                'Proof Techniques': '/content/introduction/proof_techniques.html'
            },
            'Knowledge Graph': '/content/knowledge-graph.html'
        },
        'Interactive Tools': {
            'Python Playground': '/content/interactive/python_playground.html',
            'BKT Simple Demo': '/content/interactive/BKT_Simple_Demo.html'
        },
        'Number Systems': {
            'Overview': {
                'Natural Numbers and Integers': '/content/number_systems/natural_integers.html',
                'Rational Numbers': '/content/number_systems/rational_numbers.html',
                'Irrational Numbers': '/content/number_systems/irrational_numbers.html',
                'Proof Irrationality Root2': '/content/number_systems/proof_irrationality_root2.html',
                'Operations Properties': '/content/number_systems/operations_properties.html'
            },
            'Practical Considerations': {
                'Scientific Notation': '/content/number_systems/scientific_notation.html',
                'Estimation Approximation': '/content/number_systems/estimation_approximation.html',
                'Percentage Error Tolerance': '/content/number_systems/percentage_error_tolerance.html',
                'Accumulated Error': '/content/number_systems/accumulated_error.html'
            }
        },
        'Algebra': {
            'Expressions Manipulation': {
                'Algebraic Notation': '/content/algebra/algebraic_notation.html',
                'Substitution Simplification': '/content/algebra/substitution_simplification.html',
                'Important Products': '/content/algebra/important_products.html',
                'Binomial Expansion': '/content/algebra/binomial_expansion.html',
                'Pascals Triangle': '/content/algebra/pascals_triangle.html'
            },
            'Factorization': {
                'Factoring Techniques': '/content/algebra/factoring_techniques.html',
                'Sum Difference Cubes': '/content/algebra/sum_difference_cubes.html',
                'Long Division Polynomials': '/content/algebra/long_division_polynomials.html',
                'Polynomial Division': '/content/algebra/polynomial_division.html'
            },
            'Algebraic Fractions': {
                'Addition Subtraction Fractions': '/content/algebra/addition_subtraction_fractions.html',
                'Multiplication Division Fractions': '/content/algebra/multiplication_division_fractions.html',
                'Complex Fractions': '/content/algebra/complex_fractions.html'
            },
            'Equations': {
                'Linear Equations': '/content/algebra/linear_equations.html',
                'Simultaneous Linear 2var': '/content/algebra/simultaneous_linear_2var.html',
                'Simultaneous Linear 3var': '/content/algebra/simultaneous_linear_3var.html',
                'Quadratic Equations': '/content/algebra/quadratic_equations.html',
                'Quadratic Formula': '/content/algebra/quadratic_formula.html',
                'Simultaneous Mixed': '/content/algebra/simultaneous_mixed.html',
                'Rearranging Formulae': '/content/algebra/rearranging_formulae.html'
            },
            'Inequalities': {
                'Linear Inequalities': '/content/algebra/linear_inequalities.html',
                'Quadratic Inequalities': '/content/algebra/quadratic_inequalities.html',
                'Rational Inequalities': '/content/algebra/rational_inequalities.html',
                'Absolute Value': '/content/algebra/absolute_value.html',
                'Inequality Proofs': '/content/algebra/inequality_proofs.html'
            },
            'Advanced Topics': {
                'Factor Theorem': '/content/algebra/factor_theorem.html',
                'Polynomial Roots': '/content/algebra/polynomial_roots.html',
                'Surd Equations': '/content/algebra/surd_equations.html',
                'Discriminants': '/content/algebra/discriminants.html'
            }
        },
        'Functions': {
            'Fundamentals': {
                'Definition Mappings': '/content/functions/definition_mappings.html',
                'Domain Codomain Range': '/content/functions/domain_codomain_range.html',
                'Representation Methods': '/content/functions/representation_methods.html'
            },
            'Properties': {
                'Injective Surjective Bijective': '/content/functions/injective_surjective_bijective.html',
                'Composite Functions': '/content/functions/composite_functions.html',
                'Inverse Functions': '/content/functions/inverse_functions.html',
                'Graphs Inverses': '/content/functions/graphs_inverses.html'
            },
            'Types and Graphs': {
                'Linear Functions': '/content/functions/linear_functions.html',
                'Quadratic Functions': '/content/functions/quadratic_functions_gen.html',
                'Completed Square Form': '/content/functions/completed_square_form.html',
                'Cubic Polynomial': '/content/functions/cubic_polynomial.html',
                'Exponential Functions': '/content/functions/exponential_functions.html',
                'Logarithmic Functions': '/content/functions/logarithmic_functions.html'
            },
            'Transformations': {
                'Translations': '/content/functions/translations.html',
                'Reflections': '/content/functions/reflections.html',
                'Scaling': '/content/functions/scaling.html'
            }
        },
        'Sequences and Series': {
            'Introduction': {
                'Patterns Recognition': '/content/sequences/patterns_recognition.html',
                'Term Formulas': '/content/sequences/term_formulas.html'
            },
            'Arithmetic': {
                'Arithmetic Sequences': '/content/sequences/arithmetic_sequences.html',
                'Arithmetic Series': '/content/sequences/arithmetic_series.html',
                'Applications Arithmetic': '/content/sequences/applications_arithmetic.html'
            },
            'Geometric': {
                'Geometric Sequences': '/content/sequences/geometric_sequences.html',
                'Geometric Series': '/content/sequences/geometric_series.html',
                'Infinite Geometric Series': '/content/sequences/infinite_geometric_series.html',
                'Applications Geometric': '/content/sequences/applications_geometric.html'
            },
            'Advanced': {
                'Quadratic Sequences': '/content/sequences/quadratic_sequences.html',
                'Limits Sequences': '/content/sequences/limits_sequences.html',
                'Convergence Divergence': '/content/sequences/convergence_divergence.html'
            }
        },
        'Indices and Logarithms': {
            'Indices': {
                'Laws Indices': '/content/indices_logarithms/laws_indices.html',
                'Rational Indices': '/content/indices_logarithms/rational_indices.html',
                'Equations Indices': '/content/indices_logarithms/equations_indices.html',
                'Surds Rationalization': '/content/indices_logarithms/surds_rationalization.html'
            },
            'Logarithms': {
                'Logarithmic Definition': '/content/indices_logarithms/logarithmic_definition.html',
                'Laws Logarithms': '/content/indices_logarithms/laws_logarithms.html',
                'Logarithmic Equations': '/content/indices_logarithms/logarithmic_equations.html',
                'Applications Logarithms': '/content/indices_logarithms/applications_logarithms.html'
            }
        },
        'Complex Numbers': {
            'Introduction': {
                'Imagination Definition': '/content/complex/imagination_definition.html',
                'Argand Diagram': '/content/complex/argand_diagram.html',
                'Modulus Complex Number': '/content/complex/modulus_complex_number.html',
                'Conjugate Complex Number': '/content/complex/conjugate_complex_number.html'
            },
            'Operations': {
                'Addition Subtraction': '/content/complex/addition_subtraction.html',
                'Multiplication': '/content/complex/multiplication.html',
                'Division': '/content/complex/division.html',
                'Conjugate Rules': '/content/complex/conjugate_rules.html'
            },
            'Advanced': {
                'Polar Form': '/content/complex/polar_form.html',
                'De Moivre Theorem': '/content/complex/de_moivre_theorem.html',
                'Roots Unity Applications': '/content/complex/roots_unity_applications.html',
                'Polynomial Complex Roots': '/content/complex/polynomial_complex_roots.html',
                'Conjugate Root Theorem': '/content/complex/conjugate_root_theorem.html'
            }
        },
        'Differential Calculus': {
            'Foundations': {
                'Limits': '/content/differential_calculus/limits.html',
                'Continuity': '/content/differential_calculus/continuity.html',
                'Differentiation Principles': '/content/differential_calculus/differentiation_principles.html',
                'Differentiation First Principles': '/content/differential_calculus/differentiation_first_principles.html'
            },
            'Techniques': {
                'Polynomial Functions': '/content/differential_calculus/polynomial_functions.html',
                'Chain Rule': '/content/differential_calculus/chain_rule.html',
                'Product Quotient Rules': '/content/differential_calculus/product_quotient_rules.html',
                'Trigonometric Functions': '/content/differential_calculus/trigonometric_functions.html',
                'Exponential Logarithmic': '/content/differential_calculus/exponential_logarithmic.html',
                'Inverse Trigonometric': '/content/differential_calculus/inverse_trigonometric.html',
                'Implicit Differentiation': '/content/differential_calculus/implicit_differentiation.html'
            },
            'Applications': {
                'Tangents Normals': '/content/differential_calculus/tangents_normals.html',
                'Increasing Decreasing': '/content/differential_calculus/increasing_decreasing.html',
                'Turning Points': '/content/differential_calculus/turning_points.html',
                'Points Inflection': '/content/differential_calculus/points_inflection.html',
                'Optimization': '/content/differential_calculus/optimization.html',
                'Rates Change': '/content/differential_calculus/rates_change.html',
                'Differential Equations': '/content/differential_calculus/differential_equations.html'
            }
        },
        'Integral Calculus': {
            'Foundations': {
                'Antiderivatives': '/content/integral_calculus/antiderivatives.html',
                'Indefinite Integrals': '/content/integral_calculus/indefinite_integrals.html'
            },
            'Techniques': {
                'Basic Integration': '/content/integral_calculus/basic_integration.html',
                'Exponential Trigonometric': '/content/integral_calculus/exponential_trigonometric.html',
                'Integration Substitution': '/content/integral_calculus/integration_substitution.html'
            },
            'Applications': {
                'Definite Integrals': '/content/integral_calculus/definite_integrals.html',
                'Area Under Curve': '/content/integral_calculus/area_under_curve.html',
                'Area Between Curves': '/content/integral_calculus/area_between_curves.html',
                'Trapezoidal Rule': '/content/integral_calculus/trapezoidal_rule.html',
                'Average Value': '/content/integral_calculus/average_value.html'
            }
        },
        'Length, Area, and Volume': {
            '2D Shapes': {
                'Perimeter Area Triangle': '/content/measurement/perimeter_area_triangle.html',
                'Perimeter Area Quadrilaterals': '/content/measurement/perimeter_area_quadrilaterals.html',
                'Perimeter Area Circles': '/content/measurement/perimeter_area_circles.html',
                'Arc Length Sector Area': '/content/measurement/arc_length_sector_area.html'
            },
            '3D Shapes': {
                'Rectangular Solids': '/content/measurement/rectangular_solids.html',
                'Cylinders': '/content/measurement/cylinders.html',
                'Cones': '/content/measurement/cones.html',
                'Spheres Hemispheres': '/content/measurement/spheres_hemispheres.html',
                'Nets Surface Area': '/content/measurement/nets_surface_area.html'
            }
        },
        'Coordinate Geometry': {
            'Line': {
                'Equations Line': '/content/coordinate/equations_line.html',
                'Slope': '/content/coordinate/slope.html',
                'Parallel Perpendicular': '/content/coordinate/parallel_perpendicular.html',
                'Distance Point Line': '/content/coordinate/distance_point_line.html',
                'Angle Between Lines': '/content/coordinate/angle_between_lines.html',
                'Area Triangle': '/content/coordinate/area_triangle.html',
                'Division Line Segment': '/content/coordinate/division_line_segment.html'
            },
            'Circle': {
                'Standard Form': '/content/coordinate/standard_form.html',
                'General Form': '/content/coordinate/general_form.html',
                'Tangents Circles': '/content/coordinate/tangents_circles.html',
                'Intersection Line Circle': '/content/coordinate/intersection_line_circle.html',
                'GF Problems': '/content/coordinate/gf_problems.html'
            }
        },
        'Synthetic Geometry': {
            'Fundamentals': {
                'Basic Concepts': '/content/geometry/basic_concepts.html',
                'Axioms': '/content/geometry/axioms.html',
                'Angles Lines': '/content/geometry/angles_lines.html'
            },
            'Triangles Quadrilaterals': {
                'Triangle Properties': '/content/geometry/triangle_properties.html',
                'Congruent Triangles': '/content/geometry/congruent_triangles.html',
                'Similar Triangles': '/content/geometry/similar_triangles.html',
                'Pythagoras Theorem': '/content/geometry/pythagoras_theorem.html',
                'Quadrilateral Properties': '/content/geometry/quadrilateral_properties.html'
            },
            'Circles': {
                'Circle Properties': '/content/geometry/circle_properties.html',
                'Angles Circle': '/content/geometry/angles_circle.html',
                'Cyclic Quadrilaterals': '/content/geometry/cyclic_quadrilaterals.html',
                'Tangents': '/content/geometry/tangents.html'
            },
            'Proofs Constructions': {
                'Proof Techniques': '/content/geometry/proof_techniques.html',
                'Formal Proofs': '/content/geometry/formal_proofs.html',
                'Constructions 16 to 22': '/content/geometry/constructions_16_to_22.html'
            }
        },
        'Trigonometry': {
            'Right Triangles': {
                'Trigonometric Ratios': '/content/trigonometry/trigonometric_ratios.html',
                'Practical Applications': '/content/trigonometry/practical_applications.html'
            },
            'Angle Measure': {
                'Degrees Radians': '/content/trigonometry/degrees_radians.html',
                'Unit Circle': '/content/trigonometry/unit_circle.html'
            },
            'Trigonometric Functions': {
                'Sine Cosine Tangent': '/content/trigonometry/sine_cosine_tangent.html',
                'Graphs Functions': '/content/trigonometry/graphs_functions.html',
                'Transformations': '/content/trigonometry/transformations.html',
                'Special Angles': '/content/trigonometry/special_angles.html'
            },
            'Advanced': {
                'Trigonometric Equations': '/content/trigonometry/trigonometric_equations.html',
                'Sine Cosine Rules': '/content/trigonometry/sine_cosine_rules.html',
                'Area Formulas': '/content/trigonometry/area_formulas.html',
                'Trigonometric Identities': '/content/trigonometry/trigonometric_identities.html',
                'Derive Trig Formulae': '/content/trigonometry/derive_trig_formulae.html',
                '3D Problems': '/content/trigonometry/3D_problems.html'
            }
        },
        'Financial Mathematics': {
            'Fundamentals': {
                'Percentages': '/content/financial/percentages.html',
                'Profit Loss': '/content/financial/profit_loss.html',
                'Mark Up Margin': '/content/financial/mark_up_margin.html',
                'Compound Interest': '/content/financial/compound_interest.html',
                'Present Value': '/content/financial/present_value.html'
            },
            'Applications': {
                'Depreciation': '/content/financial/depreciation.html',
                'Costing Materials Labour': '/content/financial/costing_materials_labour.html',
                'Loans Mortgages': '/content/financial/loans_mortgages.html',
                'Income Tax Deductions': '/content/financial/income_tax_deductions.html',
                'Value Added Tax': '/content/financial/value_added_tax.html',
                'Geometric Series Applications': '/content/financial/geometric_series_applications.html'
            }
        },
        'Proof by Induction': {
            'Principles': {
                'Mathematical Induction': '/content/induction/mathematical_induction.html',
                'Summation Formulas': '/content/induction/summation_formulas.html'
            },
            'Applications': {
                'Divisibility Proofs': '/content/induction/divisibility_proofs.html',
                'Inequalities Proofs': '/content/induction/inequalities_proofs.html',
                'Geometric Series Proofs': '/content/induction/geometric_series_proofs.html'
            }
        },
        'Statistics': {
            'Data Fundamentals': {
                'Types Data': '/content/statistics/types_data.html',
                'Data Collection': '/content/statistics/data_collection.html',
                'Population Samples': '/content/statistics/population_samples.html',
                'Sampling Methods': '/content/statistics/sampling_methods.html',
                'Experimental Design': '/content/statistics/experimental_design.html'
            },
            'Data Representation': {
                'Tables Graphs': '/content/statistics/tables_graphs.html',
                'Frequency Distributions': '/content/statistics/frequency_distributions.html',
                'Scatter Plots': '/content/statistics/scatter_plots.html',
                'Distribution Patterns': '/content/statistics/distribution_patterns.html'
            },
            'Descriptive': {
                'Measures Center': '/content/statistics/measures_center.html',
                'Measures Spread': '/content/statistics/measures_spread.html',
                'Quartiles Percentiles': '/content/statistics/quartiles_percentiles.html',
                'Correlation Coefficient': '/content/statistics/correlation_coefficient.html',
                'Linear Regression': '/content/statistics/linear_regression.html'
            },
            'Inferential': {
                'Sampling Distributions': '/content/statistics/sampling_distributions.html',
                'Sampling Variability': '/content/statistics/sampling_variability.html',
                'Central Limit Theorem': '/content/statistics/central_limit_theorem.html',
                'Confidence Intervals': '/content/statistics/confidence_intervals.html',
                'Hypothesis Testing': '/content/statistics/hypothesis_testing.html',
                'P Values': '/content/statistics/p_values.html'
            }
        },
        'Probability': {
            'Fundamentals': {
                'Concepts': '/content/probability/concepts.html',
                'Experimental Theoretical': '/content/probability/experimental_theoretical.html',
                'Set Theory': '/content/probability/set_theory.html',
                'Equally Likely Outcomes': '/content/probability/equally_likely_outcomes.html'
            },
            'Counting': {
                'Counting Principle': '/content/probability/counting_principle.html',
                'Permutations': '/content/probability/permutations.html',
                'Combinations': '/content/probability/combinations.html',
                'Factorial Notation': '/content/probability/factorial_notation.html'
            },
            'Rules': {
                'Addition Rule': '/content/probability/addition_rule.html',
                'Multiplication Rule': '/content/probability/multiplication_rule.html',
                'Conditional Probability': '/content/probability/conditional_probability.html',
                'Independence': '/content/probability/independence.html',
                'Sampling With Without Replacement': '/content/probability/sampling_with_without_replacement.html'
            },
            'Distributions': {
                'Expected Value': '/content/probability/expected_value.html',
                'Fair Games': '/content/probability/fair_games.html',
                'Bernoulli Trials': '/content/probability/bernoulli_trials.html',
                'Binomial Distribution': '/content/probability/binomial_distribution.html',
                'Normal Distribution': '/content/probability/normal_distribution.html',
                'Reading Normal Tables': '/content/probability/reading_normal_tables.html'
            }
        },
        'Exam Preparation': {
            'Study Strategies': '/content/exam_prep/study_strategies.html',
            'Problem Solving': {
                'Exam Techniques': '/content/exam_prep/exam_techniques.html',
                'Common Question Types': '/content/exam_prep/common_question_types.html'
            },
            'Practice Papers': '/content/exam_prep/practice_papers.html'
        }
    };

    // Create the toggle button
    createNavigatorButton();
    
    // Create the navigator panel
    createNavigatorPanel(courseStructure);
}

function createNavigatorButton() {
    // Find the navbar end section
    const navbarEnd = document.querySelector('.navbar-nav.navbar-end') || 
                     document.querySelector('.navbar-header-items__end') ||
                     document.querySelector('nav .navbar-nav:last-child');
    
    if (!navbarEnd) return;
    
    // Create course navigator button
    const navButton = document.createElement('button');
    navButton.id = 'course-nav-toggle';
    navButton.className = 'btn course-nav-toggle';
    
    navButton.innerHTML = `<svg class="navbar-icon" viewBox="0 0 24 24">
        <path d="M12 6.042A8.967 8.967 0 0 0 6 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 0 1 6 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 0 1 6-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0 0 18 18a8.967 8.967 0 0 0-6 2.292m0-14.25v14.25" />
    </svg>`;
    
    navButton.setAttribute('aria-label', 'Open Course Navigator');
    navButton.setAttribute('title', 'Course Navigator (Ctrl+M)');
    
    // Add click handler
    navButton.addEventListener('click', toggleNavigator);
    
    // Add to navbar
    navbarEnd.appendChild(navButton);
    
    // Add keyboard shortcut (Ctrl+M)
    document.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'm') {
            e.preventDefault();
            toggleNavigator();
        }
    });
}

function createNavigatorPanel(courseStructure) {
    // Create overlay
    const overlay = document.createElement('div');
    overlay.id = 'course-nav-overlay';
    
    // Create panel
    const panel = document.createElement('div');
    panel.id = 'course-nav-panel';
    
    // Create panel header
    const header = document.createElement('div');
    header.className = 'nav-panel-header';
    
    header.innerHTML = `
        <div class="nav-panel-title-row">
            <h3 class="nav-panel-title">Course Navigator</h3>
            <button id="close-nav-panel" class="nav-panel-close" title="Close (Esc)">×</button>
        </div>
        <input type="text" id="nav-search" class="nav-search-input" placeholder="Search topics...">
    `;
    
    // Create navigation content
    const content = document.createElement('div');
    content.id = 'nav-content';
    content.className = 'nav-content';
    
    // Build navigation tree
    content.appendChild(buildNavigationTree(courseStructure));
    
    // Assemble panel
    panel.appendChild(header);
    panel.appendChild(content);
    
    // Add to page
    document.body.appendChild(overlay);
    document.body.appendChild(panel);
    
    // Add event handlers
    setupNavigatorHandlers(overlay, panel);
    
    // Add search functionality
    setupNavigatorSearch();
}



// Replace ALL the duplicate buildNavigationTree functions in your theme.js with this SINGLE correct version:

function buildNavigationTree(structure, level = 0) {
    const container = document.createElement('div');
    
    // Arrow icon functions
    const getExpandedArrow = () => `<svg class="nav-arrow-icon" viewBox="0 0 24 24">
        <path d="m19.5 8.25-7.5 7.5-7.5-7.5" />
    </svg>`;
    
    const getCollapsedArrow = () => `<svg class="nav-arrow-icon" viewBox="0 0 24 24">
        <path d="m8.25 4.5 7.5 7.5-7.5 7.5" />
    </svg>`;
    
    for (const [key, value] of Object.entries(structure)) {
        const item = document.createElement('div');
        item.style.marginLeft = `${level * 15}px`;
        
        if (typeof value === 'string') {
            // It's a link
            const link = document.createElement('a');
            link.href = value;
            link.textContent = key;
            link.className = 'nav-item-link';
            
            // Highlight current page
            if (window.location.pathname.includes(value)) {
                link.classList.add('current-page');
            }
            
            item.appendChild(link);
        } else {
            // It's a section with subsections
            const toggle = document.createElement('div');
            toggle.className = 'nav-section-toggle';
            
            // Check if this section contains the current page
            const containsCurrentPage = checkIfSectionContainsCurrentPage(value);
            const isExpanded = containsCurrentPage; // Expand if contains current page
            
            // Use SVG arrows instead of emoji
            toggle.innerHTML = `${isExpanded ? getExpandedArrow() : getCollapsedArrow()}${key}`;
            
            const subsection = buildNavigationTree(value, level + 1);
            subsection.style.display = isExpanded ? 'block' : 'none';
            
            toggle.addEventListener('click', () => {
                const isVisible = subsection.style.display !== 'none';
                subsection.style.display = isVisible ? 'none' : 'block';
                // Update arrow icon with SVG
                toggle.innerHTML = `${isVisible ? getCollapsedArrow() : getExpandedArrow()}${key}`;
            });
            
            item.appendChild(toggle);
            item.appendChild(subsection);
        }
        
        container.appendChild(item);
    }
    
    return container;
}

// Keep only ONE copy of this helper function:
function checkIfSectionContainsCurrentPage(sectionData) {
    const currentPath = window.location.pathname;
    
    // Recursively check all values in the section
    function searchSection(data) {
        if (typeof data === 'string') {
            // It's a URL - check if it matches current page
            return currentPath.includes(data);
        } else if (typeof data === 'object') {
            // It's a nested section - check all its children
            for (const value of Object.values(data)) {
                if (searchSection(value)) {
                    return true;
                }
            }
        }
        return false;
    }
    
    return searchSection(sectionData);
}

// Helper function to check if a section contains the current page
function checkIfSectionContainsCurrentPage(sectionData) {
    const currentPath = window.location.pathname;
    
    // Recursively check all values in the section
    function searchSection(data) {
        if (typeof data === 'string') {
            // It's a URL - check if it matches current page
            return currentPath.includes(data);
        } else if (typeof data === 'object') {
            // It's a nested section - check all its children
            for (const value of Object.values(data)) {
                if (searchSection(value)) {
                    return true;
                }
            }
        }
        return false;
    }
    
    return searchSection(sectionData);
}

function setupNavigatorHandlers(overlay, panel) {
    const closeBtn = document.getElementById('close-nav-panel');
    
    // Close handlers
    closeBtn.addEventListener('click', closeNavigator);
    overlay.addEventListener('click', closeNavigator);
    
    // Escape key to close
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && panel.style.right === '0px') {
            closeNavigator();
        }
    });
}

function setupNavigatorSearch() {
    const searchInput = document.getElementById('nav-search');
    const navContent = document.getElementById('nav-content');
    
    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase();
        const links = navContent.querySelectorAll('.nav-item-link');
        
        links.forEach(link => {
            const text = link.textContent.toLowerCase();
            const matches = text.includes(query);
            
            // Show/hide the link
            link.style.display = matches || query === '' ? 'block' : 'none';
            
            // Show parent sections if child matches
            if (matches && query !== '') {
                let parent = link.closest('.nav-section-toggle')?.nextElementSibling;
                while (parent) {
                    parent.style.display = 'block';
                    parent = parent.parentElement?.closest('.nav-section-toggle')?.nextElementSibling;
                }
            }
        });
    });
}

function toggleNavigator() {
    const panel = document.getElementById('course-nav-panel');
    const overlay = document.getElementById('course-nav-overlay');
    
    if (panel.style.right === '0px') {
        closeNavigator();
    } else {
        openNavigator();
    }
}

function openNavigator() {
    const panel = document.getElementById('course-nav-panel');
    const overlay = document.getElementById('course-nav-overlay');
    
    overlay.style.display = 'block';
    setTimeout(() => {
        overlay.style.opacity = '1';
        panel.style.right = '0px';
    }, 10);
    
    // Focus search input
    setTimeout(() => {
        document.getElementById('nav-search')?.focus();
    }, 300);
}

function closeNavigator() {
    const panel = document.getElementById('course-nav-panel');
    const overlay = document.getElementById('course-nav-overlay');
    
    panel.style.right = '-400px';
    overlay.style.opacity = '0';
    
    setTimeout(() => {
        overlay.style.display = 'none';
    }, 300);
}