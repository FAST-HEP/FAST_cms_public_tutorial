# CHIP
Instructions, configs, and dedicated scribblers of the CHIP analysis

## Instructions to set things up:
### Pre-requisites:
You need a relatively recent version of python and pip to use this project, ie.
python > 2.7.13 and pip > 8.  On most laptops that might already be the case,
but on CERN's lxplus, Bristol's Soolin, and Imperial lx machines, you should use the script contained in this repository to set these up:
```
source CHIP/analysis/setup_lcg.sh
```
You'll have to run that every time you log in to lxplus since it sets up the python version.
Unlike previous codes however it doesn't do anything with code specific to FAST.

### Installing
```
# Step 1: Make a directory for this work:
mkdir -p CHIP && cd CHIP

# Step 2: Clone this repository
git clone ssh://git@gitlab.cern.ch:7999/cms-chip/chip.git analysis

# Step 3: Check you have the pre-requisites (see above section)
# source analysis/setup_lcg.sh

# Step 4: install the requirements
pip install --user --src . -r analysis/requirements_dev.txt

# Step 5: add the chip package to your PYTHONPATH:
export PYTHONPATH="$PWD/analysis:$PYTHONPATH"
```

If you're not likely to want to edit fast-carpenter then instead of step 4 you can do:
```
pip install --user -r analysis/requirements.txt
```

#### Subsequent running (working from a clean shell)
Some of the above steps will need to be run each time you log in, in particular step 3 (if it was needed when you first installed things), and step 5.
If you also have to follow troubleshooting point 2 below, then you'll want to run that each time you log in (unless you do this in your .bashrc file, as recommended).

#### Updating things
You will from time-to-time want to update things.  To update this code, use git pull:
```
cd CHIP/analysis
git pull origin master
```
To update the python package dependencies, just add the `--upgrade` option to the pip install command you ran above:
```
cd CHIP
pip install --user --upgrade --src . -r analysis/requirements_dev.txt
```

### Running
Some explanation of how to use `fast_carpenter` is given in the [README of the package](https://gitlab.cern.ch/fast-hep/public/fast-carpenter/blob/master/README.md).

In essence, to run the first stages of the analysis and produce some dataframes:
1. Make sure you have a dataset file to specify the input root trees, eg. the one(s) under the [samples](https://gitlab.cern.ch/cms-chip/chip/tree/master/samples) directory.
2. Create the config file describing what you want to do with the data, eg. the one(s) under the [configs](https://gitlab.cern.ch/cms-chip/chip/tree/master/configs) directory.
3. Run these through the fast_carpenter command.  Since fast-carpenter is installed using pip, the main executable should be accessible from anywhere, and you can just do:
```
fast_carpenter --outdir output/ samples/WH.yaml configs/explore.yaml
```

### Other sources of help:
The README's of the dependency packages should contain more guidance:
 * [fast-carpenter](https://gitlab.cern.ch/fast-hep/public/fast-carpenter/blob/master/README.md)
 * [fast-curator](https://gitlab.cern.ch/fast-hep/public/fast-curator/blob/master/README.md)
 * [fast-flow](https://gitlab.cern.ch/fast-hep/public/fast-flow/blob/master/README.md)
 * [alphatwirl](https://github.com/alphatwirl/alphatwirl)

###  Troubleshooting:
1. If you have problems with pip installing things the first time you run on lxplus, try doing:
```
source /cvmfs/sft.cern.ch/lcg/views/LCG_94/x86_64-slc6-gcc7-opt/setup.sh
pip install --user setuptools
```
2. All `pip` commands in this guidance install python packages and executables in your user area by using the `--user` option, ie. executables end up in `$HOME/.local/bin`  and python packages (assuming python 2.7) end up under `$HOME/.local/lib/python2.7/site-package`.  Whilst python will check under `$HOME/.local` by default, to make sure you see the `fast_curator` and `fast_carpenter` executables you need to add `$HOME/.local/bin` to your `PATH` variable.  Ideally do this in your bashrc file:
```
export PATH="$HOME/.local/bin:$PATH"
```
3. When using a batch mode (eg `htcondor` or `sge`) if your files are all accessed using xrootd you'll probably need to
  make sure the proxy you have can be seen by the batch system.  To ensure this, make sure the variable
  `X509_USER_PROXY` to point to a place visible in batch jobs and in interactive sessions.
   - On lxplus, a good value is: `export X509_USER_PROXY=/afs/cern.ch/work/${USER:0:1}/$USER/x509up_u$UID`
   - At Imperial, a decent value is probably: `export X509_USER_PROXY=/home/hep/${USER}/.x509up_u$UID`
  Once that's done, you should set up the voms proxy as normal: `voms-proxy-init --voms cms`
4. Problems with missing lzma library.  If when you try running the fast_carpenter command you see the error:
```
ImportError: 

Install lzma package with:

    pip install backports.lzma --user
or
    conda install -c conda-forge backports.lzma
```
then the first thing to do is try the recommended `pip install` command.  If that fails for some reason, then try doing:`

```
cvmfs_LzmaDir=/cvmfs/cms.cern.ch/slc6_amd64_gcc620/external/xz/5.2.2/
pip install backports.lzma --ignore-installed --global-option=build_ext --global-option="-L${cvmfs_LzmaDir}/lib/" --global-option="-I${cvmfs_LzmaDir}/include/" --user
```
