# Analyzing HPL power traces

This repository contains analyses of the dynamic power consumption of HPL runs typically of TOP500/Green500 submissions.
The goal is to determine the influence of low-granularity power measurements (i.e. 60 second intervals) on resulting accuracy.

# TUD Systems 

## Alpha
- [34-node GPU system ](https://top500.org/system/179942/)
- short 7-minute run
- 1s-interval power measurement
- "smooth" power consumption with strong drop during the end of the run

## Barnard

- [630-node CPU system](https://top500.org/system/180137/)
- long > 9h run
- 1s-interval power measurement
- large power variation in very short patterns
- energy measurements available, but problamtic due to timestamp accuracy

## Author

Thomas Ilsche <thomas.ilsche@tu-dresden.de>

# ORNL System

## Frontier

### Description

- [Large GPU system (#1 TOP500)](https://top500.org/system/180047/)
- Averaged power data in 15s bins
- 2 hour run
- Some drops in power due to synchronization
- Switching algorithms between high sustained performance and better convergence causes jump in power consumption during the run
- Drop in power in end phase

### Data source

The Frontier dataset is available at
https://doi.ccs.ornl.gov/ui/doi/437

It is available as per
[Creative Commons - Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)
- Author Information
  1. Primary Contact Information
    - Name: Scott Atchley
    - Institution: Oak Ridge National Laboratory
    - Address: 1 Bethel Valley Road, Oak Ridge, Tennessee, 37830
    - Email: atchleyes@ornl.gov
  2. Co-Investigator Data Processing Contact Information
    - Name: Dr. Matthias Maiterth
    - Institution: Oak Ridge National Laboratory
    - Address: 1 Bethel Valley Road, Oak Ridge, Tennessee, 37830
    - Email: maiterthm@ornl.gov