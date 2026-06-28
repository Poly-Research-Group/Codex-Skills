# ISR-Style Summary Statistics Table Guidelines

The main summary statistics table should be compact, manuscript-facing, and theory-aligned. It should not simply dump every numeric variable.

## Main key-variable table

Recommended columns:

```text
Variable | Description | Mean | Standard deviation | Minimum | Maximum
```

Recommended final row when all variables use the same analysis sample:

```text
Number of observations | N
```

## Grouped or decomposed table

When the study has decomposed outcomes, mechanisms, directional flows, or construct families, use a grouped table:

```text
Direction/Group | Variable | Description | Mean | Standard deviation | Minimum | Maximum
```

## Variable selection

Include variables central to the hypotheses:

1. Dependent variables.
2. Key independent variables or treatments.
3. Moderators.
4. Mechanism variables if central to the empirical design.
5. Main controls.
6. Fixed-effect dimensions only if they are meaningful variables rather than high-cardinality identifiers.

Do not include every raw source variable.

## Descriptions

Descriptions should be short but substantively meaningful. For binary variables, describe the condition coded as 1. For categorical factors, include the coding scheme or refer to a note.

## Numeric formatting

- Use thousands separators for large values.
- Use a consistent decimal rule, usually three decimals, but strip trailing zeros for readability if appropriate.
- Preserve negative signs for variables that can be negative.
- For proportions and dummies, 0/1 min/max and a mean between 0 and 1 are acceptable.

## Common-N rule

If all variables are summarized over the same analysis sample, report a single Number of observations row. If variable-specific N differs, either summarize over the common complete-case sample or add an `N` column and note the reason.
