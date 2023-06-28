# Changing the Timing Requirements of the Green500 Run Rules / Power measurement methodology

Discussion lead: Thomas Ilsche

Status: internal consensus reached in the Power Measurement Methodology team meeting 2023-06-27. 

https://sites.google.com/lbl.gov/power-measurement/home

## Current rule

The current Level 1 rule states

- 1a: Granularity: One power sample per second 
- 1b: Timing: At equal intervals across the core phase of the run, which must be at least one minute
- 1c: Measurements: Core phase average

While this is primarily about Level 1, noteworthy the Level 2 rules for 1c: Measurement include "10 average power measurements in the core phase".

## Context and Problem Statement

The community feedback we received included this exemplary statement:

> The granularity of the measurements was 1 second.
> Such granularity is required because the system uses GPUs – significant computing power and not so much memory.
> In this case, linpack runs last for only a few minutes, so to comply with requirements, we need to measure power in very short intervals.
> In contrast, standard dc power equipment is usually designed to gather power information over longer periods of time.
> I think that this is our main feedback, that taking measurements of GPU-powered machines became a bit challenging without specialized power meters.

Furthermore, from our feedback we understand that many sites do in fact not have the capability to measure power consumption at 1s intervals.
This is especially true for sites that do not use sophisticated measurement devices just for the Green500 submission.
Out of 20 sites that reported their measurement interval, 11 sites had 1s or better, 6 sites 10s-12s, and 3 sites 60s.

We further acknowledged that the description of the timing requirement is not very clear.
While the _Granularity_ requires 1 Sa/s, only a single average measurement value is required.
For many sites, it is not clear how they arrive at the average value - whether it originates from sufficient measurement rates.

Documentation about vendor-provided measurement is often not clear on how measurement samples are processed and therefore whether the measurement is compliant with the Green500 rules.

## Decision Drivers

- **Easy measurements** to ensure that many sites can make a Green500 submission without the need for specialized measurement devices; Level 1 measurement should be accessible to the vast majority of sites.
- Ensure a **good accuracy**; The potential impact from suboptimal sampling should not be less than 5%.
- Keep the rule and their description **clear and simple**; The methodology document should be easy to understand and implement.
- Avoid accidentally invalid submissions.

## Detailed Analysis

On the one hand, our survey data clearly shows that many sites do not have the capability to measure power consumption at 1s intervals.
To avoid excluding these sites from the Green500, we need to specifically allow measurement intervals of 60s or at the very least 12s.

On the other hand, the impact of low measurement rates on accuracy was not well understood.
Hence, the analysis in [this repository](https://github.com/tilsche/hpl-phases) was conducted.
We included high resolution HPL power traces from actual Green500 subission from 3 sites and one vendor totalling 7 different systems.
Note that one of the data sets is currently not public, but was included in the evaluation.

### Effect on short runs

The analysis shows, that the impact of 60s measurement intervals is most significant for short runtimes.
Our data included several GPU systems with runtimes around 5 minutes or less.
Runtimes around 5 minutes are typical for smaller GPU systems (see the runtime [analysis](runtimes/runtimes.ipynb)).
Of the 185 accelerator systems in the 2023/06 Top500 list, 56 systems have a runtime of 10 minutes or less, and 18 systems have a runtime of 5 minutes or less.

### Effect on longer runs

The longer runs of our data set have higher variability, in particular the TUD/Barnard run has extreme noise within the power data.
However, due to the long runtimes, none of the runs were substantially affected by reducing the measurement interval (less than 1% introduced worst-case-error). 

### Different shapes

We observed that the power trace of different runs has vastly different shapes, even for our set of several smaller GPU systems.
Nevertheless, the most influential factor was the runtime, not the shape of the power trace.

### Technical side note about trace data 

Our analysis for worst accuracy are based on high resolution power traces (typically 1s, 15s for ORNL).
It is not clear for all systems whether each data point is an average over the full interval to the previous data point, or whether it is an _instantaneous_ measurement.
By _instantaneous_ we mean that the measurement represents an average over a smaller period of time than between two data points.
This is an effect of reading measurement data through various interfaces where intermediate samples will be lost.
Instantaneous in this context does not allow to measure only parts of an AC wave form - this is covered by the accuracy requirement for measurement devices.
For example, for the current TUD/Barnard power trace, we know that the data points are averages over 200ms intervals, but only every fourth data point is stored.
For the ORNL system, each measurement is an average over 15 seconds.
We consider this to reflect the diversity of measurements across sites.

### Technical side note about worst-case-error analysis

To determine the worst-case error, we assume the following that A lower-capability measurement uses fewer of the data points of the high-resolution trace.
From that high-resolution trace, we take samples using given fixed practical measurement interval.
I.e., data inbetween samples is lost and only instantaneous measurement samples are available.
To determine the worst-case, we apply any offset, i.e., for shift 0, we take samples 0, 60, 120, ... for shift 1, we take samples 1, 61, 121, ... and so on.
This gives the worst-case error for a given measurement interval for one particular power trace.

The worst-case error does not consider deliberate manipulation, e.g.:
- tuning the sampling interval achieve aliasing with the power trace
- tuning the HPL to achieve aliasing with the sampling interval
- changing the temporal pattern of HPL introducing a different dynamic power trace that leads to worse errors

## Considered Options

### Option 1: minimum measurement interval of 60s and at least 5 samples

The initial suggestion was based on the 60s interval and the typical low-end runtime of 5 minutes.
This option was designed to allow the majority of runs to be measured with 60s intervals.
Only runs of less than 5 minutes would need higher sampling rates.
Our exemplary analysis suggests, that for short runs around 5 minutes or less, the worst-case-error is around 5%-9%.

### Option 2: minimum measurement interval of 60s and at least 10 samples

This option would still allow the majority of runs to be measured with 60s intervals.
Short runs of 5 minutes or less would require measurement rates of 30s/20s or better.
Our exemplary analysis suggests, that for short runs around 5 minutes or less, the worst-case-error is around 2.0%-3.3%.

### Option 3: minimum measurement interval of 15s or 12s

While not explicitly calculated, this option would lead to higher accuracy for short runs.
However, it would exclude sites with only 60s measurement intervals (3 sites in our survey), even if they have long runs that are not affected.

## Decision Outcome

Chosen option: "Option 2: minimum measurement interval of 60s and at least 10 samples" as a compromise of accuracy and accessibility.

### Consequences

#### Accessibility

Following the specific feedback, the new rule makes it easier for sites to make a Green500 submission for short runs.
Still, some sites may not have the capability, particularly those with only 60s measurement intervals and runs shorter than 10 minutes.

#### Accuracy

There is a possibility of introducing additional sampling errors error compared to the strict interpretation of the current rule. 
However, the impact should practically be limited to less than 5%, even in worst-case scenarios.
Our survey suggests, this error may have already been in current suggestions, due to ambiguity of the current methodology document.

#### Documentation

The methodology document needs to be updated to reflect the new rule, both in the summary table and the text.
Further clarification of the document is necessary to avoid ambiguity.
This discussion assumes instantaneous measurements are allowed for Level 1.
Therefore, this is the baseline for simplification and clarification of the requirements in the methodology document.