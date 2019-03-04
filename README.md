# FAST for the CMS HEP Tutorial
This project demonstrates how to use the FAST approach to implement the [CMS HEP analysis tutorial from 2012](http://ippog.org/resources/2012/cms-hep-tutorial)
### Quick-start
Install things:
```bash
# Step 1: Clone this repository
git clone https://gitlab.cern.ch/fast-hep/public/fast_cms_public_tutorial.git
cd fast_cms_public_tutorial

# Step 2: Check you have the pre-requisites (see following section)
# source setup_lcg.sh

# Step 3: install the python requirements (possibly add --user)
pip install -r requirements.txt

# Step 4: add this package to your PYTHONPATH:
export PYTHONPATH="$PWD:$PYTHONPATH"
```

### Run things
A simple demo of the commands needed to run this analysis can be found in the pipeline directory.
```bash
cd pipeline
make input_files
make curator
make carpenter
make plotter
```

## Slow-start:
### Installing
```
# Step 1: Clone this repository
git clone https://gitlab.cern.ch/fast-hep/public/fast_cms_public_tutorial.git
cd fast_cms_public_tutorial

# Step 2: Check you have the pre-requisites (see following section)
# source setup_lcg.sh

# Step 3: install the python requirements
pip install -r requirements.txt

# Step 4: add this package to your PYTHONPATH:
export PYTHONPATH="$PWD:$PYTHONPATH"
```

#### On Lxplus or other HEP clusters:
You need a relatively recent version of python and pip to use this project, ie.
around python > 2.7.13 and pip > 8.  On most laptops that might already be the case,
but on CERN's lxplus, and likely other Centos 7 machines (at least on those I've tried), you might want to use the script contained in this repository to set these up:
```
source setup_lcg.sh
```
This will create the main dependencies (like python, xrootd, etc) using versions which have been compiled and posted to CVMFS.
You'll have to run that every time you log in since it sets up the python version.

If you work on a laptop or any system where the default python and pip versions are recent, then you shouldnt need to do this, just skip to the next section.


#### Subsequent running (working from a clean shell)
Some of the above steps will need to be run each time you log in, in particular step 2 (if it was needed when you first installed things), and step 4.
If you also have to follow troubleshooting point 2 below, then you'll want to run that each time you log in (unless you do this in your .bashrc file, as recommended).

#### Updating things
To update this code, use git pull:
```
git pull origin master
```
To update the python package dependencies, just add the `--upgrade` option to the pip install command you ran above:
```
pip install --user --upgrade -r requirements.txt
```

## Getting the data:
The dataset file, `file_list.yml` expects you to put the data inside the directory where you cloned this repository, so do:
```
cd fast_cms_public_tutorial
wget ippog.org/sites/ippog.web.cern.ch/files/HEPTutorial_0.tar
tar -xf HEPTutorial_0.tar HEPTutorial/files/
```

## Running
Some explanation of how to use `fast_carpenter` is given in the [README of the package](https://gitlab.cern.ch/fast-hep/public/fast-carpenter/blob/master/README.md).

In essence, to run the first stages of the analysis and produce some dataframes:
1. Make sure you have a dataset file to specify the input root trees, eg. [file_list.yml](https://gitlab.cern.ch/fast-hep/public/fast_cms_public_tutorial.git/tree/master/file_list.yml).
2. Create the config file describing what you want to do with the data, eg.[sequence_cfg.yml](https://gitlab.cern.ch/fast-hep/public/fast_cms_public_tutorial.git/tree/master/sequence_cfg.yml). 
3. Run these through the fast_carpenter command.  Since fast-carpenter is installed using pip, the main executable should be accessible from anywhere, and you can just do:
```
fast_carpenter --outdir output/ file_list.yml sequence_cfg.yml
```
(If you cannot see the `fast_carpenter` command, you might need to follow the trouble-shooting point 2 below)
Note that (currently) `file_list.yml` contains relative paths to the data, so you need to run the command from the directory where you untarred the dataset.

Use the built-in help option for `fast_carpenter` to see other available options, eg. using multiprocessing, running on the batch, etc.

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
