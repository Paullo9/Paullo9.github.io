# Introduction
- This introductory chapter gives a brief overview/key concepts
- why is this research important and interesting? Not to technical here
- from electron/matter interaction to TEM to STEM to 4D-STEM

## Imaging with fast electrons
**Why is this research interesting? Why should we do it? Why are we able to do it now? Why is now the best time?**
- catchy introductory sentences here! 
- EM came a long way from photographic film to high-end cameras/direct electron detectors, alongside with increasingly large datasets, giving insides to/helps gain information on the structure/composition etc. of materials
- maybe contrast the developments in EM, higher and higher resolution/ data intensive measurments etc. with the development of computing power/its increase over time, especially in the age of AI, everyone has access to powerfull computational methods/cluster/hardware, complete industries and research interests shifted because of new technologie
- materials research gets accelerated by the advances in hardware and software

**Why image with electrons in the first place?** 
maybe put the graph in section experimental in somethoing like this: [[messaufbau2.png]]
- electrons show a strong interactions with matter, due to their mass + velocity in the TEM, stronger interactions than light
- different interactions with matter; different detectors/information can be observed
- elastic vs. inelastic scattering


![[electronww.svg]]
>  *Fig 1: Schematic representation of different electron interactions with a thin specimen, BSE and SE like in SEM + transmitted electrons can be used for EELS etc.*


**Properties of electrons?**
- Resolution? 
- Relativistic wavelength/mass? Higher acceleration = shorter wavelength = higher resolution, but at a cost...

$$
\lambda = \frac{h}{\sqrt{2 m_0 eV (1+ \frac{eV}{2 m_0 c^2})}}
$$

- by this metric we expect a resolution of ... for a acceleration voltage of 200keV...

## Modes of Transmission electron microscopy
[[@tsuda1999]]

**How do we use these fast electrons for microscopy?**
- directing a beam of electrons trough a thin sample (usually smaller 100nm), electrons interact with the sample in various ways which can be detected, e.g scattering etc.
- basic components of a TEM? Electrongun, Focussing with electromagnetic lenses, imaging with detectors etc.

**Which TEM modi are there?**
- shortly describe different modi: TEM-BF, TEM-DF, STEM-BF, STEM-ADF/HAADF
- In TEM the imaging modes can be selected by the objective aperture, is the aperture centered on the direct beam, usually the brightest spot, a bright-field image is formed
- dark-field images are formed when the aperture is centered around a diffracted spot or the beam is tiled in a way so that a diffracted spot is on axis, probably best as it minimizes abberations?
- Imaging contrast is inverted for BF- and DF-TEM, specimen/parts of the specimen that scatters strongly appear dark in a BF image as they deviate a significant amount of electrons from their trajectory. In DF-TEM on the other hand they would up show as bright regions
- STEM: convergent beam instead of a parallel beam, rastered over the sample, and interaction/transmission in each position is detected
- Similarly to the TEM mode there are BF and DF in the STEM mode, the signal collected is determined by the chosen detector and the camera length 
- schematic representation of these four modi can be seen in Figrue 123

![[TEM_modes.svg]]
> *Fig 2: Schematic representation of BF and DF imaging in TEM and STEM mode. a)  BF imaging in the TEM mode by selecting the unscattered beam through the objective aperture. b) DF imaging is obtained by tilting the beam such that a diffracted beam is on-axis c) The on-axis  beam is collected by a BF detector in STEM mode, adjusted to a long camera length compared to DF-STEM d) The ADF and HAADF are annular detectors that collect the scattered beam at shorter camera lengths*

**Contrast? which information do i get from which mode?**
- SAD easier to interpret than CBED?
- TEM: defects, crystal structure by diffracrion spots, easy to interpret
- STEM DF: defects, dislocations, z-contrast

## From STEM to 4D-STEM
[[@pennycook2016]]
**Why is it called 4D-STEM? How does it work?**
- operation principle, scanning 2D area in real space, collect a 2D CBED diffraction pattern for each real space probe position
- generates large datasets,  what is in the dataset? which information can i get?

![[4DSTEM_Overview.svg]] 
> *Fig 3*

**What is the challenge?**
- why are the datasets so large? show simple calculation
- commercial software and open source software available to process data -> different options such as py4dastem, hyperspy, libertem, etc.
- py4DSTEM chosen because...
- computational methods needed but require large system memory -> computing on a cluster
- teaser for next chapter most relevant parameters, detectors + datamanagement and processing will be described in chapter theory

## Aim of this work
**What exactly did we do? what will be shown on the following pages? where to find the code etc.?**
- measuring 4DSTEM on the TEM at hand, FEI...
- processing the datasets we generated using the OMNI Cluster of university of siegen
- great challenge of processing large datasets, we try to face using py4DSTEM, a package provided by C. ophus et all [[@ophusRecordingUsing4DSTEM2014]]
- try to establish a workflow for 4DSTEM measurments and datamangement/analysis
- code for 4DSTEM can be found at *link github*, code written for this thesis can be found at *my github*

![[amorph_crystalline.svg]]
> *Fig 4: maybe exclude this figure, too trivial...*
