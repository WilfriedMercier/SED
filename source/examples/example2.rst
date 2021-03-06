Example 2: Resolved SFR map with LePhare from an output file
============================================================

We assume the SED fitting has already been performed and there is an output file named :file:`example/1/{1.out}`.

Since we need the mean map, scale factor and exposure time to scale back the output properties, we start by building the FilterList oject as in :doc:`example 1 </examples/example1>`

.. code:: python

    import os.path           as     opath
    from   astropy.io        import fits
    import SED

    galName    = '1'
    zeropoints = [25.68, 26.51, 25.69, 25.94, 24.87, 26.27, 26.23, 26.45, 25.94]
    redshift   = 0.622
    bands      = ['435', '606', '775', '814', '850', '105', '125', '140', '160']
    
    dataFiles  = []
    data2Files = [] # flux maps convolved by the square of the PSF
    varFiles   = []
    
    for band in bands:
    
       file    = opath.abspath(opath.join('data', f'{galName}_{band}.fits'))
       dataFiles.append(file)
       
       file2   = opath.abspath(opath.join('data', f'{galName}_{band}_PSF2.fits'))
       data2Files.append(file2)
    
       vfile   = opath.abspath(opath.join('data', f'{galName}_{band}_var.fits'))
       varFiles.append(vfile)
       
    mfile      = opath.abspath(opath.join('data', f'{galName}_mask.fits'))
    with fits.open(mfile) as hdul:
       mask    = hdul[0].data == 0
          
    filts      = []
    for band, data, data2, var, zpt in zip(bands, dataFiles, data2Files, varFiles, zeropoints):
       filts.append(sed.Filter(band, file, file2, var, zpt))
    
    flist      = SED.FilterList(filts, mask, code=SED.SEDcode.LEPHARE, redshift=redshift)
    flist.genTable(cleanMethod=SED.CleanMethod.ZERO, scaleFactor=100, texpFac=4)
    
Now we just have to build an output object and link the filter list to it

.. code:: python

    output = sed.LePhareOutput('1/1.out')
    output.link(flist)
    
As in :doc:`example 1 </examples/example1>`, we can now generate a resolved map for the median SFR

.. code:: python

    from   matplotlib        import rc
    import matplotlib        as     mpl
    import matplotlib.pyplot as     plt
        
    rc('font', **{'family': 'serif', 'serif': ['Times']})
    rc('text', usetex=True)
    mpl.rcParams['text.latex.preamble'] = r'\usepackage{newtxmath}'
    rc('figure', figsize=(5, 4.5))

    sfr = output.toImage('sfr_med')
    
    plt.imshow(sfr.data, origin='lower', cmap='rainbow')
    plt.xlabel('X [pixel]', size=13)
    plt.ylabel('Y [pixel]', size=13)
    
    cbar = plt.colorbar(ret, orientation='vertical', shrink=0.9)
    cbar.set_label(r'SFR [M$_{\odot}$ yr$^{-1}$]', size=13)
    plt.show()
    
.. plot::
    
    import os.path           as     opath
    from   astropy.io        import fits
    import SED
    
    from   matplotlib        import rc
    import matplotlib        as     mpl
    import matplotlib.pyplot as     plt
    
    # Define data file names
    galName    = '1'                                                             # Galaxy number
    zeropoints = [25.68, 26.51, 25.69, 25.94, 24.87, 26.27, 26.23, 26.45, 25.94] # HST zeropoints
    redshift   = 0.622                                                           # Redshift of the galaxy
    bands      = ['435', '606', '775', '814', '850', '105', '125', '140', '160'] # Bands
    band_names = ['ACS_WFC.F435W', 'ACS_WFC.F606W', 'ACS_WFC.F775W',             # Names of the band for LePhare
                  'ACS_WFC.F814W', 'ACS_WFC.F850LP', 'WFC3_IR.F105W',
                  'WFC3_IR.F125W', 'WFC3_IR.F140W', 'WFC3_IR.F160W']
    
    dataFiles  = [] # Flux maps
    data2Files = [] # Flux maps convolved by the PSF squared
    varFiles   = [] # Variance maps
    
    for band in bands:
    
       file    = opath.abspath(opath.join('..', '..', 'example', 'data', f'{galName}_{band}.fits'))
       dataFiles.append(file)
    
       file2   = opath.abspath(opath.join('..', '..', 'example', 'data', f'{galName}_{band}_PSF2.fits'))
       data2Files.append(file2)
    
       vfile   = opath.abspath(opath.join('..', '..', 'example', 'data', f'{galName}_{band}_var.fits'))
       varFiles.append(vfile)
    
    # Get mask file
    mfile      = opath.abspath(opath.join('..', '..', 'example', 'data', f'{galName}_mask.fits'))
    with fits.open(mfile) as hdul:
       mask    = hdul[0].data == 0
    
    ###   1. Generate a FilterList object   ###
    filts      = []
    for band, data, data2, var, zpt in zip(bands, dataFiles, data2Files, varFiles, zeropoints):
       filts.append(SED.Filter(band, data, data2, var, zpt))
    
    flist      = SED.FilterList(filts, mask, code=SED.SEDcode.LEPHARE, redshift=redshift)
    
    ###   2. Update data table and add Poisson noise (texpFac != 0)   ###
    flist.genTable(cleanMethod=SED.CleanMethod.ZERO, scaleFactor=100, texpFac=4)
    
    ###   6. Generate a resolved stellar mass map   ###
    output = SED.LePhareOutput(opath.join('..', '..', 'example', galName, f'{galName}.out'))
    output.link(flist)
    mass_star  = output.toImage('sfr_med')
    
    ###   7. Plot   ###
    from   matplotlib        import rc
    import matplotlib        as     mpl
    import matplotlib.pyplot as     plt
        
    rc('font', **{'family': 'serif', 'serif': ['Times']})
    rc('text', usetex=True)
    mpl.rcParams['text.latex.preamble'] = r'\usepackage{newtxmath}'
    rc('figure', figsize=(5, 4.5))

    sfr = output.toImage('sfr_med')
    
    ret = plt.imshow(sfr.data, origin='lower', cmap='rainbow')
    plt.xlabel('X [pixel]', size=13)
    plt.ylabel('Y [pixel]', size=13)
    
    cbar = plt.colorbar(ret, orientation='vertical', shrink=0.9)
    cbar.set_label(r'SFR [M$_{\odot}$ yr$^{-1}$]', size=13)
    plt.show()