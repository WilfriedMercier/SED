#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
.. codeauthor:: Wilfried Mercier - IRAP <wilfried.mercier@irap.omp.eu>

Modules which can be used in Cigale.
"""

from   abc           import ABC, abstractmethod
from   .properties   import BoolProperty, PathProperty, StrProperty, ListIntProperty, ListFloatProperty
from   typing        import List

##########################################
#        Star Formation Histories        #
##########################################

class SFHmodule(ABC):
    r'''
    .. codeauthor:: Wilfried Mercier - IRAP <wilfried.mercier@irap.omp.eu>
    
    Class implementing a module to deal with SFH models.
    
    :param bool normalise: (**Optional**) whether to normalise the SFH to produce one solar mass
    '''
    
    def __init__(self, normalise: bool = True) -> None:
        r'''Init method.'''
        
        self.normalise = BoolProperty(normalise)
        
    @abstractmethod
    def __str__(self, *args, **kwargs) -> str:
        r'''
        .. codeauthor:: Wilfried Mercier - IRAP <wilfried.mercier@irap.omp.eu>
        
        Implement a string representation of the class used to make Cigale parameter files.
        '''
        
        return
    
class SFH2EXPmodule(SFHmodule):
    r'''
    .. codeauthor:: Wilfried Mercier - IRAP <wilfried.mercier@irap.omp.eu>
    
    Class implementing a module for an exponential SFH with two stellar populations.
    
    :param list tau_main: (**Optional**) e-folding time of the main stellar population model in Myr
    :param list tau_burst: (**Optional**) e-folding time of the late starburst population model in Myr.
    :param list f_burst: (**Optional**) mass fraction of the late burst population
    :param list age: (**Optional**) age of the main stellar population in the galaxy in Myr
    :param list burst_age: (**Optional**) age of the late burst in Myr
    :param list sfr_0: (**Optional**) Value of SFR at t = 0 in M_sun/yr
    :param bool normalise: (**Optional**) whether to normalise the SFH to produce one solar mass
    '''
    
    def __init__(self, tau_main: List[float] = [6000.0], 
                 tau_burst: List[float] = [50.0],
                 f_burst: List[float] = [0.01], 
                 age: List[int] = [5000], 
                 burst_age: List[int] = [20], 
                 sfr_0: List[float] = [1.0],
                 normalise: bool = True) -> None:
        
        r'''Init method.'''
        
        super().__init__(normalise=normalise)
        
        self.tau_main  = ListFloatProperty(tau_main,  minBound=0.0)
        self.tau_burst = ListFloatProperty(tau_burst, minBound=0.0)
        self.f_burst   = ListFloatProperty(f_burst,   minBound=0.0, maxBound=0.9999)
        self.age       = ListIntProperty(  age,       minBound=0)
        self.burst_age = ListIntProperty(  burst_age, minBound=0)
        self.sfr_0     = ListFloatProperty(sfr_0,     minBound=0.0)
        
    def __str__(self, *args, **kwargs) -> str:
        r'''
        .. codeauthor:: Wilfried Mercier - IRAP <wilfried.mercier@irap.omp.eu>
        
        Implement a string representation of the class used to make Cigale parameter files.
        '''
        
        text = f'''\
        [[sfh2exp]]
          # e-folding time of the main stellar population model in Myr.
          tau_main = {self.tau_main}
          # e-folding time of the late starburst population model in Myr.
          tau_burst = {self.tau_burst}
          # Mass fraction of the late burst population.
          f_burst = {self.f_burst}
          # Age of the main stellar population in the galaxy in Myr. The precision
          # is 1 Myr.
          age = {self.age}
          # Age of the late burst in Myr. The precision is 1 Myr.
          burst_age = {self.burst_age}
          # Value of SFR at t = 0 in M_sun/yr.
          sfr_0 = {self.sfr_0}
          # Normalise the SFH to produce one solar mass.
          normalise = {self.normalise}
        '''
        
        return text
    
    
class SFHDELAYEDmodule(SFHmodule):
    r'''
    .. codeauthor:: Wilfried Mercier - IRAP <wilfried.mercier@irap.omp.eu>
    
    Class implementing a module for a delayed exponential SFH.
    
    :param list tau_main: (**Optional**) e-folding time of the main stellar population model in Myr
    :param list age_main: (**Optional**) age of the main stellar population in the galaxy in Myr
    :param list tau_burst: (**Optional**) e-folding time of the late starburst population model in Myr
    :param list age_burst: (**Optional**) age of the late burst in Myr
    :param list f_burst: (**Optional**) mass fraction of the late burst population
    :param list sfr_A: (**Optional**) multiplicative factor controlling the SFR if **normalise** is False. For instance without any burst: SFR(t)=sfr_A×t×exp(-t/τ)/τ²
    :param bool normalise: (**Optional**) whether to normalise the SFH to produce one solar mass
    '''
    
    def __init__(self, tau_main: List[float] = [2000.0], 
                 age_main: List[int] = [5000],
                 tau_burst: List[float] = [50.0],
                 age_burst: List[int] = [20], 
                 f_burst: List[float] = [0.0],  
                 sfr_A: List[float] = [1.0],
                 normalise: bool = True) -> None:
        r'''Init method.'''
        
        super().__init__(normalise=normalise)
        
        self.tau_main  = ListFloatProperty(tau_main,  minBound=0.0)
        self.age_main  = ListIntProperty(  age_main,  minBound=0)
        self.tau_burst = ListFloatProperty(tau_burst, minBound=0.0)
        self.age_burst = ListIntProperty(  age_burst, minBound=0)
        self.f_burst   = ListFloatProperty(f_burst,   minBound=0.0, maxBound=0.9999)
        self.sfr_A     = ListFloatProperty(sfr_A,     minBound=0.0)
        
    def __str__(self, *args, **kwargs) -> str:
        r'''
        .. codeauthor:: Wilfried Mercier - IRAP <wilfried.mercier@irap.omp.eu>
        
        Implement a string representation of the class used to make Cigale parameter files.
        '''
        
        text = f'''\
        [[sfhdelayed]]
          # e-folding time of the main stellar population model in Myr.
          tau_main = {self.tau_main}
          # Age of the main stellar population in the galaxy in Myr. The precision
          # is 1 Myr.
          age_main = {self.age_main}
          # e-folding time of the late starburst population model in Myr.
          tau_burst = {self.tau_burst}
          # Age of the late burst in Myr. The precision is 1 Myr.
          age_burst = {self.age_burst}
          # Mass fraction of the late burst population.
          f_burst = {self.f_burst}
          # Multiplicative factor controlling the SFR if normalise is False. For
          # instance without any burst: SFR(t)=sfr_A×t×exp(-t/τ)/τ²
          sfr_A = {self.sfr_A}
          # Normalise the SFH to produce one solar mass.
          normalise = {self.normalise}
        '''
        
        return text
    
    
class SFHDELAYEDBQmodule(SFHmodule):
    r'''
    .. codeauthor:: Wilfried Mercier - IRAP <wilfried.mercier@irap.omp.eu>
    
    Class implementing a module for an exponential SFH with a burst/quench scenario.
    
    :param list tau_main: (**Optional**) e-folding time of the main stellar population model in Myr
    :param list age_main: (**Optional**) age of the main stellar population in the galaxy in Myr
    :param list age_bq: (**Optional**) age of the burst/quench episode in Myr
    :param list r_sfr: (**Optional**) ratio of the SFR after/before age_bq
    :param list sfr_A: (**Optional**) multiplicative factor controlling the SFR if **normalise** is False. For instance without any burst: SFR(t)=sfr_A×t×exp(-t/τ)/τ²
    :param bool normalise: (**Optional**) whether to normalise the SFH to produce one solar mass
    '''
    
    def __init__(self, tau_main: List[float] = [2000.0], 
                 age_main: List[int] = [5000],
                 age_bq: List[int] = [500],
                 r_sfr: List[float] = [0.1], 
                 sfr_A: List[float] = [1.0],
                 normalise: bool = True) -> None:
        
        r'''Init method.'''
        
        super().__init__(normalise=normalise)
        
        self.tau_main  = ListFloatProperty(tau_main,  minBound=0.0)
        self.age_main  = ListIntProperty(  age_main,  minBound=0)
        self.age_bq    = ListIntProperty(  age_bq,    minBound=0)
        self.r_sfr     = ListFloatProperty(r_sfr,     minBound=0.0)
        self.sfr_A     = ListFloatProperty(sfr_A,     minBound=0.0)
        
    def __str__(self, *args, **kwargs) -> str:
        r'''
        .. codeauthor:: Wilfried Mercier - IRAP <wilfried.mercier@irap.omp.eu>
        
        Implement a string representation of the class used to make Cigale parameter files.
        '''
        
        text = f'''\
        [[sfhdelayedbq]]
          # e-folding time of the main stellar population model in Myr.
          tau_main = {self.tau_main}
          # Age of the main stellar population in the galaxy in Myr. The precision
          # is 1 Myr.
          age_main = {self.age_main}
          # Age of the burst/quench episode. The precision is 1 Myr.
          age_bq = {self.age_bq}
          # Ratio of the SFR after/before age_bq.
          r_sfr = {self.r_sfr}
          # Multiplicative factor controlling the SFR if normalise is False. For
          # instance without any burst/quench: SFR(t)=sfr_A×t×exp(-t/τ)/τ²
          sfr_A = {self.sfr_A}
          # Normalise the SFH to produce one solar mass.
          normalise = {self.normalise}    
        '''
        
        return text
    
    
class SFHFROMFILEmodule(SFHmodule):
    r'''
    .. codeauthor:: Wilfried Mercier - IRAP <wilfried.mercier@irap.omp.eu>
    
    Class implementing a module for a SFH from a file.
    
    :param str filename: (**Optional**) name of the file containing the SFH. The first column must be the time in Myr, starting from 0 with a step of 1 Myr. The other columns must contain the SFR in Msun/yr.
    :param list sfr_column: (**Optional**) list of column indices of the SFR. The first SFR column has the index 1.
    :param list age: (**Optional**) age in Myr at which the SFH will be looked at
    :param bool normalise: (**Optional**) whether to normalise the SFH to produce one solar mass
    '''
    
    def __init__(self, filename: str = '',
                 sfr_column: List[int] = [1],
                 age: List[int] = [1000],
                 normalise: bool = True) -> None:
        
        r'''Init method.'''
        
        super().__init__(normalise=normalise)
        
        self.filename   = PathProperty(filename)
        self.sfr_column = ListIntProperty(sfr_column)
        self.age        = ListIntProperty(age, minBound=0)
        
    def __str__(self, *args, **kwargs) -> str:
        r'''
        .. codeauthor:: Wilfried Mercier - IRAP <wilfried.mercier@irap.omp.eu>
        
        Implement a string representation of the class used to make Cigale parameter files.
        '''
        
        text = f'''\
        [[sfhfromfile]]
          # Name of the file containing the SFH. The first column must be the time
          # in Myr, starting from 0 with a step of 1 Myr. The other columns must
          # contain the SFR in Msun/yr.[Msun/yr].
          filename = {self.filename}
          # List of column indices of the SFR. The first SFR column has the index
          # 1.
          sfr_column = {self.sfr_column}
          # Age in Myr at which the SFH will be looked at.
          age = {self.age}
          # Normalise the SFH to one solar mass produced at the given age.
          normalise = {self.normalise}
        '''
        
        return text
    
    
class SFHPERIODICmodule(SFHmodule):
    r'''
    .. codeauthor:: Wilfried Mercier - IRAP <wilfried.mercier@irap.omp.eu>
    
    Class implementing a module for a SFH with periodic bursts.
    
    :param list type_bursts: (**Optional**) type of the individual star formation episodes. 0: exponential, 1: delayed, 2: rectangle
    :param list delta_bursts: (**Optional**) elapsed time between the beginning of each burst in Myr
    :param list age: (**Optional**) age of the main stellar population in the galaxy in Myr
    :param list sfr_A: (**Optional**) multiplicative factor controlling the amplitude of SFR (valid for each event)
    :param bool normalise: (**Optional**) whether to normalise the SFH to produce one solar mass
    '''
    
    def __init__(self, type_bursts: List[int] = [0],
                 delta_bursts: List[int] = [50],
                 tau_bursts: List[float] = [20.0],
                 age: List[int] = [1000],
                 sfr_A: List[float] = [1.0],
                 normalise: bool = True) -> None:
        
        r'''Init method.'''
        
        super().__init__(normalise=normalise)
        
        self.type_bursts  = ListIntProperty(  type_bursts,  minBound=0, maxBound=2)
        self.delta_bursts = ListIntProperty(  delta_bursts, minBound=0)
        self.tau_bursts   = ListFloatProperty(tau_bursts,   minBound=0)
        self.age          = ListIntProperty(  age,          minBound=0)
        self.sfr_A        = ListFloatProperty(sfr_A,        minBound=0.0)
        
    def __str__(self, *args, **kwargs) -> str:
        r'''
        .. codeauthor:: Wilfried Mercier - IRAP <wilfried.mercier@irap.omp.eu>
        
        Implement a string representation of the class used to make Cigale parameter files.
        '''
        
        text = f'''\
        [[sfhperiodic]]
          # Type of the individual star formation episodes. 0: exponential, 1:
          # delayed, 2: rectangle.
          type_bursts = {self.type_bursts}
          # Elapsed time between the beginning of each burst in Myr. The precision
          # is 1 Myr.
          delta_bursts = {self.delta_bursts}
          # Duration (rectangle) or e-folding time of all short events in Myr. The
          # precision is 1 Myr.
          tau_bursts = {self.tau_bursts}
          # Age of the main stellar population in the galaxy in Myr. The precision
          # is 1 Myr.
          age = {self.age}
          # Multiplicative factor controlling the amplitude of SFR (valid for each
          # event).
          sfr_A = {self.sfr_A}
          # Normalise the SFH to produce one solar mass.
          normalise = {self.normalise}
        '''
        
        return text
    
############################################
#        Single Stellar Populations        #
############################################

class SSPmodule(ABC):
    r'''
    .. codeauthor:: Wilfried Mercier - IRAP <wilfried.mercier@irap.omp.eu>
    
    Class implementing a module to deal with SSP models.
    
    :param list imf: (**Optional**) initial mass function. See specific SSP module for the meaning of the values 0 and 1.
    :param list separation_age: (**Optional**) age [Myr] of the separation between the young and the old star populations. The default value in 10^7 years (10 Myr). Set to 0 not to differentiate ages (only an old population).
    '''
    
    def __init__(self, imf: List[int] = [0],
                 separation_age: List[int] = [10]) -> None:
        
        r'''Init method.'''
        
        self.imf            = ListIntProperty(imf,            minBound=0, maxBound=1)
        self.separation_age = ListIntProperty(separation_age, minBound=0)
        
    @abstractmethod
    def __str__(self, *args, **kwargs) -> str:
        r'''
        .. codeauthor:: Wilfried Mercier - IRAP <wilfried.mercier@irap.omp.eu>
        
        Implement a string representation of the class used to make Cigale parameter files.
        '''
        
        return
    
class BC03module(SSPmodule):
    r'''
    .. codeauthor:: Wilfried Mercier - IRAP <wilfried.mercier@irap.omp.eu>
    
    Class implementing a Bruzual et Charlot (2003) SSP module.
    
    :param list imf: (**Optional**) initial mass function: 0 (Salpeter) or 1 (Chabrier)
    :param list separation_age: (**Optional**) age [Myr] of the separation between the young and the old star populations. The default value in 10^7 years (10 Myr). Set to 0 not to differentiate ages (only an old population).
    :param list metallicity: (**Optional**) metallicity. Possible values are: 0.0001, 0.0004, 0.004, 0.008, 0.02, 0.05
    '''
    
    def __init__(self, imf: List[int] = [0],
                 separation_age: List[int] = [10],
                 metallicity: List[float] = [0.02]) -> None:
        
        r'''Init method.'''
        
        super().__init__(imf=imf, separation_age=separation_age)
        
        self.metallicity = ListFloatProperty(metallicity, minBound=0.0001, maxBound=0.05, 
                                             testFunc=lambda value: any((i not in [0.0001, 0.0004, 0.004, 0.008, 0.02, 0.05] for i in value)),
                                             testMsg='Metallicity for bc03 module must be one of 0.0001, 0.0004, 0.004, 0.008, 0.02, 0.05.')
        
    def __str__(self, *args, **kwargs) -> str:
        r'''
        .. codeauthor:: Wilfried Mercier - IRAP <wilfried.mercier@irap.omp.eu>
        
        Implement a string representation of the class used to make Cigale parameter files.
        '''
        
        text = f'''
        [[bc03]]
          # Initial mass function: 0 (Salpeter) or 1 (Chabrier).
          imf = {self.imf}
          # Metalicity. Possible values are: 0.0001, 0.0004, 0.004, 0.008, 0.02,
          # 0.05.
          metallicity = {self.metallicity}
          # Age [Myr] of the separation between the young and the old star
          # populations. The default value in 10^7 years (10 Myr). Set to 0 not to
          # differentiate ages (only an old population).
          separation_age = {self.separation_age}
        '''
        
        return text
    
class M2005module(SSPmodule):
    r'''
    .. codeauthor:: Wilfried Mercier - IRAP <wilfried.mercier@irap.omp.eu>
    
    Class implementing a Maraston (2005) SSP module.
    
    .. warning:
        
        This module cannot be combined with :class:`NEBULARmodule`.
    
    :param list imf: (**Optional**) initial mass function: 0 (Salpeter) or 1 (Kroupa)
    :param list separation_age: (**Optional**) age [Myr] of the separation between the young and the old star populations. The default value in 10^7 years (10 Myr). Set to 0 not to differentiate ages (only an old population).
    :param list metallicity: (**Optional**) metallicity. Possible values are: 0.001, 0.01, 0.02, 0.04
    '''
    
    def __init__(self, imf: List[int] = [0],
                 separation_age: List[int] = [10],
                 metallicity: List[float] = [0.02]) -> None:
        
        r'''Init method.'''
        
        super().__init__(imf=imf, separation_age=separation_age)
        
        self.metallicity = ListFloatProperty(metallicity, minBound=0.001, maxBound=0.04, 
                                             testFunc=lambda value: any((i not in [0.001, 0.01, 0.02, 0.04] for i in value)),
                                             testMsg='Metallicity for bc03 module must be one of 0.001, 0.01, 0.02, 0.04.')
        
    def __str__(self, *args, **kwargs) -> str:
        r'''
        .. codeauthor:: Wilfried Mercier - IRAP <wilfried.mercier@irap.omp.eu>
        
        Implement a string representation of the class used to make Cigale parameter files.
        '''
        
        text = f'''
        [[m2005]]
          # Initial mass function: 0 (Salpeter) or 1 (Kroupa)
          imf = {self.imf}
          # Metallicity. Possible values are: 0.001, 0.01, 0.02, 0.04.
          metallicity = {self.metallicity}
          # Age [Myr] of the separation between the young and the old star
          # populations. The default value in 10^7 years (10 Myr). Set to 0 not to
          # differentiate ages (only an old population).
          separation_age = {self.separation_age}
        '''
        
        return text
    
##################################
#        Nebular emission        #
##################################

class NEBULARmodule:
    r'''
    .. codeauthor:: Wilfried Mercier - IRAP <wilfried.mercier@irap.omp.eu>
    
    Class implementing a module to deal with nebular emission.
    
    .. warning:
        
        This module cannot be combined with :class:`M2005module`.
    
    :param list logU: (**Optional**) ionisation parameter. Minimum value is -4.0, maximum is -1.0 and steps of 0.1 only are accepted (i.e. -1.5 is ok but not -1.53).
    :param list f_esc: (**Optional**) fraction of Lyman continuum photons escaping the galaxy
    :param list f_dust: (**Optional**) fraction of Lyman continuum photons absorbed by dust
    :param list lines_width: (**Optional**) Line width in km/s
    :param bool include_emission: (**Optional**) whether to include the nebular emission or not
    '''
    
    def __init__(self, logU: List[float] = [-2.0],
                 f_esc: List[float] = [0.0],
                 f_dust: List[float] = [0.0],
                 lines_width: List[float] = [300.0],
                 include_emission: bool = True) -> None:
        
        r'''Init method.'''
        
        logURange = [i/10 for i in range(-40, -9, 1)]
        
        self.logU = ListFloatProperty(logU, minBound=-4.0, maxBound=-1.0,
                                      testFunc=lambda value: any((i not in logURange for i in value)),
                                      testMsg='One on the logU values is not accepted. Accepted values are between -4.0 and -1.0 by steps of 0.1.')
        
        self.f_esc       = ListFloatProperty(f_esc,       minBound=0, maxBound=1)
        self.f_dust      = ListFloatProperty(f_dust,      minBound=0, maxBound=1)
        self.lines_width = ListFloatProperty(lines_width, minBound=0)
        self.emission    = BoolProperty(include_emission)
        
    def __str__(self, *args, **kwargs) -> str:
        r'''
        .. codeauthor:: Wilfried Mercier - IRAP <wilfried.mercier@irap.omp.eu>
        
        Implement a string representation of the class used to make Cigale parameter files.
        '''
        
        text = f'''
        [[nebular]]
          # Ionisation parameter
          logU = {self.logU}
          # Fraction of Lyman continuum photons escaping the galaxy
          f_esc = {self.f_esc}
          # Fraction of Lyman continuum photons absorbed by dust
          f_dust = {self.f_dust}
          # Line width in km/s
          lines_width = {self.lines_width}
          # Include nebular emission.
          emission = {self.emission}
        '''
        
        return text
    
##################################
#        Dust attenuation        #
##################################

class ATTENUATIONmodule(ABC):
    r'''
    .. codeauthor:: Wilfried Mercier - IRAP <wilfried.mercier@irap.omp.eu>
    
    Class implementing a module to deal with dust attenuation.
    
    :param str filters: (**Optional**) filters for which the attenuation will be computed and added to the SED information dictionary. You can give several filter names separated by a & (don't use commas).
    '''
    
    def __init__(self, filters: str = 'V_B90 & FUV') -> None:
        
        r'''Init method.'''
        
        self.filters = StrProperty(filters)
        
    @abstractmethod
    def __str__(self, *args, **kwargs) -> str:
        r'''
        .. codeauthor:: Wilfried Mercier - IRAP <wilfried.mercier@irap.omp.eu>
        
        Implement a string representation of the class used to make Cigale parameter files.
        '''
        
        return
    
class DUSTATT_MODIFIED_CF00module(ATTENUATIONmodule):
    r'''
    .. codeauthor:: Wilfried Mercier - IRAP <wilfried.mercier@irap.omp.eu>
    
    Class implementing a modified Charlot & Fall 2000 attenuation law module.
    
    :param str filters: (**Optional**) filters for which the attenuation will be computed and added to the SED information dictionary. You can give several filter names separated by a & (don't use commas).
    :param list Av_ISM: (**Optional**) V-band attenuation in the interstellar medium
    :param list mu: (**Optional**) Av_ISM / (Av_BC+Av_ISM)
    :param list slope_ISM: (**Optional**) power law slope of the attenuation in the ISM
    :param list slope_BC: (**Optional**) power law slope of the attenuation in the birth clouds
    '''
    
    def __init__(self, filters: str = 'V_B90 & FUV',
                 Av_ISM: List[float] = [1.0],
                 mu: List[float] = [0.44],
                 slope_ISM: List[float] = [-0.7],
                 slope_BC: List[float] = [-1.3]) -> None:
        
        r'''Init method.'''
        
        super().__init__(filters=filters)
        
        self.filters   = StrProperty(filters)
        self.Av_ISM    = ListFloatProperty(Av_ISM, minBound=0.0)
        self.mu        = ListFloatProperty(mu,     minBound=0.0001, maxBound=1.0)
        self.slope_ISM = ListFloatProperty(slope_ISM)
        self.slope_ISM = ListFloatProperty(slope_BC)
        
    def __str__(self, *args, **kwargs) -> str:
        r'''
        .. codeauthor:: Wilfried Mercier - IRAP <wilfried.mercier@irap.omp.eu>
        
        Implement a string representation of the class used to make Cigale parameter files.
        '''
        
        text = f'''
        [[dustatt_modified_CF00]]
          # V-band attenuation in the interstellar medium.
          Av_ISM = {self.Av_ISM}
          # Av_ISM / (Av_BC+Av_ISM)
          mu = {self.mu}
          # Power law slope of the attenuation in the ISM.
          slope_ISM = {self.slope_ISM}
          # Power law slope of the attenuation in the birth clouds.
          slope_BC = {self.slope_BC}
          # Filters for which the attenuation will be computed and added to the
          # SED information dictionary. You can give several filter names
          # separated by a & (don't use commas).
          filters = {self.filters}
        '''
        
        return text
    
class DUSTATT_MODIFIED_STARBUSTmodule(ATTENUATIONmodule):
    r'''
    .. codeauthor:: Wilfried Mercier - IRAP <wilfried.mercier@irap.omp.eu>
    
    Class implementing a modified Calzetti 2000 attenuation law module.
    
    :param str filters: (**Optional**) filters for which the attenuation will be computed and added to the SED information dictionary. You can give several filter names separated by a & (don't use commas).
    :param list E_BV_lines: (**Optional**) E(B-V)l, the colour excess of the nebular lines light for both the young and old population
    :param list E_BV_factor: (**Optional**) reduction factor to apply on E_BV_lines to compute E(B-V)s the stellar continuum attenuation. Both young and old population are attenuated with E(B-V)s.
    :param list uv_bump_wavelength: (**Optional**) central wavelength of the UV bump in nm
    :param list uv_bump_width: (**Optional**) width (FWHM) of the UV bump in nm
    :param list uv_bump_amplitude: (**Optional**) amplitude of the UV bump. For the Milky Way: 3.
    :param list powerlaw_slope: (**Optional**) slope delta of the power law modifying the attenuation curve
    :param list Ext_law_emission_lines: (**Optional**) extinction law to use for attenuating the emission lines flux. Possible values are: 1, 2, 3. 1: MW, 2: LMC, 3: SMC. MW is modelled using CCM89, SMC and LMC using Pei92.
    :param list Rv: (**Optional**) ratio of total to selective extinction, A_V / E(B-V), for the extinction curve applied to emission lines. Standard value is 3.1 for MW using CCM89, but can be changed.F or SMC and LMC using Pei92 the value is automatically set to 2.93 and 3.16 respectively, no matter the value you write.
    '''
    
    def __init__(self, filters: str = 'B_B90 & V_B90 & FUV',
                 E_BV_lines: List[float] = [0.3],
                 E_BV_factor: List[float] = [0.44],
                 uv_bump_wavelength: List[float] = [217.5],
                 uv_bump_width: List[float] = [35.0],
                 uv_bump_amplitude: List[float] = [0.0],
                 powerlaw_slope: List[float] = [0.0],
                 Ext_law_emission_lines: List[int] = 1,
                 Rv: List[float] = 3.1) -> None:
        
        r'''Init method.'''
        
        super().__init__(filters=filters)
        
        self.filters                = StrProperty(filters)
        self.E_BV_lines             = ListFloatProperty(E_BV_lines,           minBound=0.0)
        self.E_BV_factor            = ListFloatProperty(E_BV_factor,          minBound=0.0, maxBound=0.0)
        self.uv_bump_wavelength     = ListFloatProperty(uv_bump_wavelength,   minBound=0.0)
        self.uv_bump_width          = ListFloatProperty(uv_bump_width,        minBound=0.0)
        self.uv_bump_amplitude      = ListFloatProperty(uv_bump_amplitude,    minBound=0.0)
        self.powerlaw_slope         = ListFloatProperty(powerlaw_slope)
        self.Ext_law_emission_lines = ListIntProperty(Ext_law_emission_lines, minBound=1, maxBound=3)
        self.Rv                     = ListFloatProperty(Rv)
        
    def __str__(self, *args, **kwargs) -> str:
        r'''
        .. codeauthor:: Wilfried Mercier - IRAP <wilfried.mercier@irap.omp.eu>
        
        Implement a string representation of the class used to make Cigale parameter files.
        '''
        
        text = f'''
        [[dustatt_modified_starburst]]
          # E(B-V)l, the colour excess of the nebular lines light for both the
          # young and old population.
          E_BV_lines = {self.E_BV_lines}
          # Reduction factor to apply on E_BV_lines to compute E(B-V)s the stellar
          # continuum attenuation. Both young and old population are attenuated
          # with E(B-V)s.
          E_BV_factor = {self.E_BV_factor}
          # Central wavelength of the UV bump in nm.
          uv_bump_wavelength = {self.uv_bump_wavelength}
          # Width (FWHM) of the UV bump in nm.
          uv_bump_width = {self.uv_bump_width}
          # Amplitude of the UV bump. For the Milky Way: 3.
          uv_bump_amplitude = {self.uv_bump_amplitude}
          # Slope delta of the power law modifying the attenuation curve.
          powerlaw_slope = {self.powerlaw_slope}
          # Extinction law to use for attenuating the emissio  n lines flux.
          # Possible values are: 1, 2, 3. 1: MW, 2: LMC, 3: SMC. MW is modelled
          # using CCM89, SMC and LMC using Pei92.
          Ext_law_emission_lines = {self.Ext_law_emission_lines}
          # Ratio of total to selective extinction, A_V / E(B-V), for the
          # extinction curve applied to emission lines.Standard value is 3.1 for
          # MW using CCM89, but can be changed.For SMC and LMC using Pei92 the
          # value is automatically set to 2.93 and 3.16 respectively, no matter
          # the value you write.
          Rv = {self.Rv}
          # Filters for which the attenuation will be computed and added to the
          # SED information dictionary. You can give several filter names
          # separated by a & (don't use commas).
          filters = {self.filters}
        '''
        
        return text
    
###############################
#        Dust emission        #
###############################