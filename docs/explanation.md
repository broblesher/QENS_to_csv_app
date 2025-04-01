# Background
QENS to csv App arises from the neccesity to parse data recorded in different instruments from several facilities, reduced using a variety of scientific software. All the input files are text files with a different number of header lines, some of them containing metadata, followed by the measured quantities at different scattering vector ($Q$) values in three columns (Energy, Scattered Intensity, error). The goal was to have only one application to sort the data recorded in all the intruments in a matrix with the measured quantities at different $Q$-values along the columns.

# Input data files
## IN5
The data obtained in [IN5](https://www.ill.eu/for-ill-users/instruments/instruments-list/in5/description/instrument-layout) at [ILL](https://www.ill.eu/) (Granoble, France) was reduced using [Lamp](https://www.ill.eu/for-ill-users/support-labs-infrastructure/software-scientific-tools/lamp). The input file is a *.inx file. There are 4 header lines followed by the recorded data in three space-separated columns. This block repeats for each $Q$-value:

```text
 653    1    2    0    0    0    0  650

0.0980  81.799  6.2832    0.000   1.0 0
                 0.0000  4.2959  0.0000
      -4.99500  0.00000e+00 -1.0000e+00
      -4.98500  0.00000e+00 -1.0000e+00
      -4.97500  0.00000e+00 -1.0000e+00
.......................................
       1.49500  0.00000e+00 -1.0000e+00
 653    1    2    0    0    0    0  650

0.1960  81.799  6.2832    0.000   1.0 0
                 0.0000  4.2959  0.0000
      -4.99500  0.00000e+00 -1.0000e+00
      -4.98500  0.00000e+00 -1.0000e+00
      -4.97500  0.00000e+00 -1.0000e+00
      -4.96500  0.00000e+00 -1.0000e+00
.......................................
```

The $Q$-value is the first value of the third row for each block.

## IN16B
The data recorded in [IN16B](https://www.ill.eu/for-ill-users/instruments/instruments-list/in16b/description/instrument-layout) at [ILL](https://www.ill.eu/) (Grenoble, France) was reduced using [DAVE](https://www.ncnr.nist.gov/dave/index.html). The input file is a *.dat file. There are 26 main hearder lines (begining with the \# symbol) contining the metadata. Next, there are 4 subheader lines followed by the measurement at each $Q$-value, consisting in 3 tab separated columns with the recorded quantities:

```text
# instrument.name = IN16b 
# user.proposal = 6-02-637 
.............................................
# Spectrum No. 0
# q(Angstrom^-1) = 0.29
# Scattering Angle(Degrees) = 16.80
# Energy transfer(meV), Intensity, Error
-1.426190e-01	-9.629884e-02	 9.415056e-02
.............................................
# Spectrum No. 2
# q(Angstrom^-1) = 0.59
# Scattering Angle(Degrees) = 34.42
# Energy transfer(meV), Intensity, Error
-1.426190e-01	 0.000000e+00	 0.000000e+00
.............................................
```

## FOCUS
The data measured at [FOCUS](https://www.psi.ch/en/sinq/focus) at [PSI](https://www.psi.ch/en/cnm) (Villigen, Switzerland) was reduced using [DAVE](https://www.ncnr.nist.gov/dave/index.html). The input data file is a *.txt file. There are 58 main header lines (begining with the \# symbol) containing the metadata, followed by the measurements at each $Q$-value: 3 subheader lines followed by three space-separated columns with the recorded quantities:

```text
#DAVE ASCII OUTPUT
#Instrument: FOCUS
...................................
#Group Number: 1
#Group Value: 0.35000000
#X Value    Intensity dIntensity
-1.0000000  -1.6424588  0.18596862
..................................
#Group Number: 2
#Group Value: 0.45000000
#X Value    Intensity dIntensity
-1.0000000  0.34624067  0.42417713
...................................
```

The $Q$-value is in the **\#Group Value:** line.

## LET
The data recorded in [LET](https://www.isis.stfc.ac.uk/Pages/let.aspx) at [ISIS](https://www.isis.stfc.ac.uk/Pages/home.aspx) (Oxfordshire, UK) was reduce using [Mantid](https://www.mantidproject.org/) and [MSlice](http://mslice.isis.rl.ac.uk). In this case, there is a *.txt file for each $Q$. The files have 4 header lines (begining with the \# symbol) followed by the measured data in three space separated columns:

```text
# MSlice Cut of workspace "LET77597_1.05meV_rings"
# Cut axis: DeltaE,-3.0,0.699999988079071,0.004999999888241291
# Integration axis: |Q|,0.7999999999999999,0.8999999999999999, 0.0
# (Energy Transfer (meV)) (Signal) (Error)
-3.000000000e+00          nan          nan
...................................................................
```

The $Q$ is the mean value of the quantities in the third row (**# Integration axis:**).

# Output data files

## Scattered Intensity: $S(Q, E)$
The output file containing the scattered intensity data contains $3*n_Q$ (with $n_Q$ the number of $Q$-values) columns:

| E (meV) | D1_Butanol_250K_0.098A-1 | err | E (meV) | D1_Butanol_250K_0.196A-1 | err | ... |
|:-------:|:------------------------:|:---:|:-------:|:------------------------:|:---:|:---:|
| -4.995  | 0.0                      | 0.0 | -4.995  | 0.0                      | 0.0 | ... |
| ...     | ...                      | ... | ...     | ...                      | ... | ... |

The name of the scattered intensity columns contains the name of the input file and the corresponding $Q$-value.

## Susceptibility: $\chi (Q, E)$
QENS to csv App gives the option to calculate and export the susceptibility $\chi(Q, E)$ corresponding to each measurement, calculated as:[^1]

$\chi''(Q, E) = \pi [\textrm{e}^{|E|/k_B  T} - 1] S(Q, E)$,      $~~~~~~~~~~~~~~~E < 0$
$\chi''(Q, E) = \pi [1 - \textrm{e}^{-E/k_B T} - 1] S(Q, E)$,    $~~~~~~~E > 0$

The corresponding output file contains $4*n_Q$ (with $n_Q$ the number of $Q$-values) columns:

| E- (meV) | D1_Butanol_250K_0.098A-1 | E+ (meV) | D1_Butanol_250K_0.098A-1 | ... |
|:--------:|:------------------------:|:--------:|:------------------------:|:---:|
|   0.005  |   0.0004907819456634216  |   0.005  |   0.0005436917706691087  | ... |
|    ...   |            ...           |    ...   |            ...           | ... |

The energy columns contain the $|E|$ values, and the subscript indicates if the value corresponds to the negative ($-$) or the positive ($+$) energy. The name of the $\chi (Q, E)$ columns contain the name of the input file and the corresponding $Q$ value. The data is sorted in ascending order for the absolute value of energy.

[^1]: Arbe, A., Nilsen, G. J., Stewart, J. R., Alvarez, F., Sakai, V. G., & Colmenero, J. (2020). Coherent structural relaxation of water from meso- To intermolecular scales measured using neutron spectroscopy with polarization analysis. Physical Review Research, 2(2), 022015. [DOI: 10.1103/PhysRevResearch.2.022015](https://doi.org/10.1103/PhysRevResearch.2.022015)