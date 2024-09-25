---
title: Theoretical introduction to 4D-STEM

---

## Ewald sphere and Laue zones
Electron diffraction patterns arise from the interaction of incident electrons with the periodic crystal structure of a sample, following the principles of elastic scattering. A key concept for understanding the position of diffraction spots in these patterns is the **Ewald sphere** construction, introduced by Paul Peter Ewald. It provides a geometric framework to describe the relationship between the incident wave vector ($\vec{k_0}$), the scattered wave vector ($\vec{k}$), and the crystal's reciprocal lattice. {cite}`ewald1921` The Ewald sphere is constructed in reciprocal space and represents all possible directions where diffraction can occur, governed by **Bragg’s law**:

 $$
n \lambda = 2 d sin(\theta)
$$

where:

- $n$ is an integer/the order of diffraction,
- $\lambda$ is the wavelength of the incident electrons,
- $d$ is the interplanar spacing of the crystal,
- and $\theta$ is the angle of incidence that satisfies the diffraction condition.

The radius of the sphere is inversely proportional to the wavelength $\lambda$. Given the short wavelength of electrons, typically in the order of picometers for high-energy electron beams, the radius of the Ewald sphere becomes very large. [[@delille2001a]] This leads to highly localized region of reciprocal space being intersected by the sphere, the resulting diffraction spots are often concentrated in relatively narrow rings, known as **Laue zones**. [[@maiwald2018]] [[@zuo2005]] These zones represent higher-order reflections as electrons diffract at higher angles, in contrast to the central disk of zero-order Laue zone (ZOLZ). [[@zuo2005]][[@nakazawa2023]] As shown in **Figure 1**, these zones can be visualized as circles in a 2D plane, representing the intersections of the reciprocal lattice with the Ewald sphere. The symmetry and spacing of these rings correspond to the underlying symmetry of the crystal lattice being studied.


```{figure} ./figures/laue_zones.svg
:name: ewaldandlaue

a) **Ewald Sphere**:  reciprocal lattice points which intersect with the sphere are diffraction points, marking the positions where Bragg conditions are fulfilled and constructive interference occurs. b) **Laue Circles**: In-plane view shows concentric rings which illustrate the Laue zones, with the innermost circle being the *zero order laue zone* (ZOLZ), and outer circles representing higher orders
```

Due to the small wavelength and the resulting small curvature of the Ewalds sphere, most of the scattered electrons are present in the ZOLZ.

## Electron diffraction from convergent incident beam

[[@lebeauPositionaveragedconvergent2010]][[@chuvilin2005]][[@morniroli2006]][[@delille2001]][[@bird1992]][[@williams2009]][[@bustillo4DSTEMBeamSensitiveMaterials2021]][[@zuo2011]]

In scanning transmission electron microscopy (STEM), unlike in transmission electron microscopy (TEM) where a nearly parallel electron beam is used, the electron beam is focused to a small point on the sample. 
This so called convergent beam has a range of incident angles, each corresponding to a slightly different position on the Ewald sphere.
Since the Ewald sphere is curved, the Bragg condition is met over a range of angles, broadening the diffraction spots into a disks which are called **convergent beam electron diffraction (CBED)** patterns.
Figure 2 shows the resulting diffraction patterns of a parallel incident beam, often referred to as selected area diffraction (SAD) pattern and of a convergent incident beam, highlighting the difference in the formation of spots versus disks.

![[CBED_vs_SAD.svg]]
> *Fig 2: Comparison of diffraction patterns obtained using Selected Area Diffraction (SAD) and Convergent Beam Electron Diffraction (CBED). The SAD pattern, produced with a parallel incident beam, features sharp diffraction spots, characteristic of long-range order in the sample. In contrast, the CBED pattern, generated with a convergent beam, displays diffraction disks, providing detailed local crystallographic information and allowing for finer spatial resolution.*

The CBED patterns contain rich crystallographic information, with the type and quality of data obtained being highly dependent on the convergence angle $\alpha$. However, there is a trade-off between achieving high resolution in real space and in diffraction space, as noted by ...[[@ophusFourDimensionalScanningTransmission2019a]] [[@zuo2011]].

At smaller convergence angles, the electron probe has lower resolution in real space but provides higher resolution in reciprocal space. For very small angles, the disks closely resemble those in selected area diffraction (SAD), where the diffraction spots are sharp and well-defined.
As the convergence angle increases, the real-space resolution improves, but the diffraction resolution decreases due to the overlapping of the disks. This overlap occurs because the increased range of incident beam directions causes the disks to spread out and merge.
Figure 3 illustrates the effect of the convergence angle $\alpha$ on disk position and size, as well as simulated CBED patterns for both small and large convergence angle $\alpha$.

![[CBED_alpha.svg|300]] ![[CBED_sim.svg|200]] 
> Fig 3: a) Two different convergence semiangles α resulting in dif-  
ferent CBED patterns; small angles (red cone) result in non-overlapping disks, increased angles (blue cone) results in broader and overlapping disks b) Simulated CBED patterns of silicium (111)  
choosing the zone axis as the propagation direction for two different convergence semiangles using abTEM, a python package for TEM simulation [[@madsen_abtem_2021]]



## Possible detector configuration
[[@levin2021]][[@nord2020]][[@yang2015]][[@tate2016]]

There is a variety of possible detector configurations available to detect CBED patterns, each with unique advantages and disadvantages. 
**Charge-Coupled Devices (CCDs)** were first introduced in electron microscopy in the 1980s. These detectors are coupled with a scintillator, such as single crystal Yttrium aluminium garnet (YAG), to convert incident electrons into photons, protecting the sensitive sensor from direct electron bombardment. The photons are transmitted to the CCD sensor through fiber optics, allowing the device to remain undamaged by high-energy electrons. In many cases, Peltier elements are used to cool the detector and reduce thermal noise, thereby improving image quality. CCDs operate by reading out the charge sequentially, line by line and pixel by pixel, making the process relatively slow compared to newer technologies such as complementary metal oxide semiconductor (CMOS) electronics.

(Despite their historical importance, CCDs have certain limitations. Their Detective Quantum Efficiency (DQE) is lower compared to other systems, as the conversion of electrons to photons inherently results in some signal loss. In addition, radiation damage over time can degrade the performance, especially in terms of CTE, which governs how efficiently charge is transferred across the detector.)


**CMOS** detectors offer several key advantages over CCDs. One of the main benefits is their faster readout speed, thanks to their ability to read out charge from each pixel simultaneously, rather than sequentially. Additionally, CMOS detectors suffer from less blooming, a phenomenon where charge spreads across adjacent pixels and blurs the image. This makes CMOS detectors better suited for high-speed imaging applications where clarity is critical.

However, like CCDs, CMOS detectors are typically coupled with a scintillator to prevent damage from direct electron impacts. This intermediate photon conversion process lowers their DQE when compared to direct electron detectors. Nonetheless, the faster readout speed and reduced blooming make CMOS detectors a preferred choice in applications where these factors are more important than absolute sensitivity.


**Direct electron detectors** are a significant improvement in terms of DQE because they do not require an intermediate step to convert electrons into photons. By detecting electrons directly, these detectors can achieve much higher sensitivity, making them ideal for high-resolution and low-dose imaging. Hybrid Pixel Detector (Pixel Array Detector - PAD) and Monolithic Active Pixel Sensor (MAPS) are the two main types of direct electron detectors.

A hybrid pixel detector, also known as a **pixel array detector (PAD)**, is an advanced type of direct electron detector. In this design, each pixel is read out in parallel, greatly enhancing data acquisition speed. The pixels are typically large and thick (e.g., 150 μm x 150 μm x 500 μm), which allows them to fully absorb high-energy electrons. This leads to a high dynamic range, making PADs well-suited for applications where precise electron energy measurements are crucial. However, the larger pixel size comes with the disadvantage of a lower total pixel count, which limits spatial resolution. An example of this type of detector is the Electron Microscopy Pixel Array Detector (EMPAD), described in detail by Tate et al. [[@tate2016]]

Monolithic Active Pixel Sensors (MAPS) are another form of direct electron detector, designed with much smaller pixel sizes (e.g., 6.5 μm x 6.5 μm x 8 μm). This smaller pixel size allows for a much higher spatial resolution, which is important for applications requiring detailed imaging at the nanoscale. However, the reduced pixel size also results in a lower dynamic range compared to hybrid pixel detectors, as smaller pixels absorb fewer electrons. MAPS detectors are typically radiation-hardened, making them more resilient in environments with high radiation exposure, such as in TEMs used for 4D-STEM experiments.



![[detectors.svg]]
> *Fig 0: a) Indirect electron detector: Schematic of a Scintillator-coupled detector; electrons are converted to photons which reach the detector via fiber optic coupling b) Direct electron detector: electrons directly land on a radiation hardened sensor; MAPS vs EMPAD c) readout architecture: CCD; accumulated charge from each pixel is shifted in parallel, pixel by pixel and row by row, and sequencially converted to voltage, CTE must be high but is degredated by radiation demage? CMOS; charge is chonverted to voltage in each pixel and read out simultanouisly, much faster/advantagous speed*

For the experiments in this thesis, we will be using a Gatan Continuum Camera. 

It has a pixel format of 2048 x 2048 with 18-micron pixels
The camera operates at 200kV 
DQE at half Nyquist of 0.128 and a dynamic range of 76 dB, 

The camera’s readout noise of 4.93 ADC counts and its frame rate of 94.2 fps 




## Scan strategy and measurment
[[@velazco2020]] [[@vanrompay2019]][[@lifshin2013]][[@kovarik2016]][[@sang2016]][[@stevens2018]][[@liuAdvancesApplicationsAtomicResolution2021]][[@ortega2021]][[@lifshin2013]]

Undersampling occurs at low magnifications when the probe size is smaller than the step size, meaning the beam covers only a portion of each pixel. As a result, the measured value at a given location represents only a fraction of the entire pixel, leading to less accurate measurements at lower magnifications .

Oversampling, on the other hand, happens at high magnifications when the probe size exceeds the step size. In this case, the signal becomes a summation from multiple pixels, resulting in blurred images. To address this, deconvolution methods paired with knowledge of the point spread function (PSF) can help maintain image resolution .


![[sampling.svg|500]]
> *Fig x. Oversampling: probe size is larger than the step size, the signal measured is a summation of signals from multiple pixels, Undersampling:  beam is smaller than a pixel, meaning the measured value at a given location only represents a portion of the entire pixel*


Sparse sampling is a technique used to reduce electron dose and acquisition time by scanning only a subset of pixels. Missing pixels are then filled in using reconstruction algorithms like inpainting, which rely on spatial frequencies to restore the image .

A variant of this is random undersampling (R-US), where only a random fraction of pixels is scanned. However, the effectiveness of R-US can be limited by noise, particularly Poisson noise. Other methods, like tilt-undersampling (T-US), which involves fewer images with larger tilt increments, can be more advantageous in reducing dose .

Different scan strategies can also be used in place of traditional raster scans. Spiral scans, like Archimedean or Fermat spirals, allow for faster scanning speeds and a more uniform electron dose distribution, though they may cause distortions and uneven sampling densities at higher speeds. Serpentine scans, which follow a back-and-forth path, improve dose uniformity but can introduce distortions due to hysteresis effects in the scanning coils. Hilbert scans provide a more isotropic path and distribute distortions more evenly from sample drift, making them useful for strain mapping, although short dwell times can lead to issues with scan system settling time  .

Choosing the step size appropriately is critical for achieving the desired data. Undersampling results in a loss of information in at least one dimension but saves time, while oversampling introduces blur without adding valuable information .

  

It’s also essential to consider whether atomic resolution is necessary for your measurements. High resolution might not always be required, and reducing the electron dose per pixel can preserve sample integrity without compromising the data quality  .