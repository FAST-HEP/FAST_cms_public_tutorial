function Chip_set_cvmfs_vars(){
    Chip_cvmfs_PythonDir=/cvmfs/sft.cern.ch/lcg/releases/Python/2.7.13-597a5/x86_64-slc6-gcc62-opt/
    Chip_cvmfs_PipDir=/cvmfs/sft.cern.ch/lcg/releases/pip/8.1.2-c9f5a/x86_64-slc6-gcc62-opt/
    Chip_cvmfs_GCCSetup=/cvmfs/sft.cern.ch/lcg/contrib/gcc/6.2/x86_64-slc6/setup.sh
    Chip_cvmfs_Libs=/cvmfs/sft.cern.ch/lcg/views/LCG_88/x86_64-slc6-gcc62-opt/
    Chip_cvmfs_LzmaDir=/cvmfs/cms.cern.ch/slc6_amd64_gcc620/external/xz/5.2.2/
    Chip_cvmfs_Xrootd=/cvmfs/sft.cern.ch/lcg/releases/LCG_88/xrootd_python/0.3.0/x86_64-slc6-gcc62-opt/
}
export -f Chip_set_cvmfs_vars
Chip_set_cvmfs_vars

CHIP_top_dir(){
  local Canonicalize="readlink -f"
  $Canonicalize asdf &> /dev/null || Canonicalize=realpath
  dirname "$($Canonicalize "${BASH_SOURCE[0]}")"
}

CHIP_build_some_path(){
  local NewPath="$1" ;shift
  for dir in "$@";do
    if ! $( echo "$NewPath" | grep -q '\(.*:\|^\)'"$dir"'\(:.*\|$\)' ); then
      NewPath="${dir}${NewPath:+:${NewPath}}"
    fi
  done
  echo "$NewPath"
}

CHIP_build_path(){
  local Dirs=( {"$Chip_cvmfs_PythonDir","$Chip_cvmfs_PipDir"}/bin)
  CHIP_build_some_path "$PATH" "${Dirs[@]}"
}

CHIP_build_python_path(){
  local Dirs=( {"$Chip_cvmfs_PythonDir","$Chip_cvmfs_PipDir","$Chip_cvmfs_Xrootd"}/lib/python2.7/site-packages/)

  CHIP_build_some_path "$PYTHONPATH" "${Dirs[@]}"
}

export PYTHONPATH="$(CHIP_build_python_path)"
export PATH="$(CHIP_build_path)"
export LD_LIBRARY_PATH="$(CHIP_build_some_path "$LD_LIBRARY_PATH" "${Chip_cvmfs_Libs}"{lib,lib64} "${Chip_cvmfs_LzmaDir}"/lib )"
source "$Chip_cvmfs_GCCSetup"

unset CHIP_build_some_path
unset CHIP_build_path
unset CHIP_build_python_path
unset ${!Chip_cvmfs_*}
