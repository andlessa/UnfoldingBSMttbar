#!/bin/sh

homeDIR="$( pwd )"

echo "Installation will take place in $homeDIR"


cd $homeDIR


#madgraph="MG5_aMC_v3.8.0.tar.gz"
#URL=https://launchpad.net/mg5amcnlo/3.0/3.8.x/+download/$madgraph
# MadGraph 3.6.3 (version used in this project). Launchpad only keeps the latest
# 3.6.x release, so the official GitHub tag is used instead.
madgraph="v3.6.3.tar.gz"
URL=https://github.com/mg5amcnlo/mg5amcnlo/archive/refs/tags/$madgraph
# Use github version with fix for printing intermediate particles
#madgraph="mg5amcnlo-3.6.3.zip"
echo -n "Install MadGraph (y/n)? "
read answer
if echo "$answer" | grep -iq "^y" ;then
        if [ -d "MG5" ]; then
           rm -rf MG5
        fi
	mkdir MG5;
	echo "[installer] getting MadGraph5"; wget -O $madgraph $URL 2>/dev/null || curl -L -o $madgraph $URL; tar -zxf $madgraph -C MG5 --strip-components 1;
	#cp $madgraph $madgraph"_bak"
	#unzip $madgraph;
	#mv mg5amcnlo-3.6.3 MG5;
	#mv $madgraph"_bak" $madgraph
	cd $homeDIR
	cd ./MG5;
	echo "[installer] installing LHAPDF6, HepMC and Collier"
        echo -e "install hepmc\ninstall lhapdf6\ninstall pythia8\ninstall collier\nexit\n" > mad_install.txt;
	./bin/mg5_aMC -f mad_install.txt
	cd $homeDIR
	sed  "s|homeDIR|$homeDIR|g" mg5_configuration.txt > ./MG5/input/mg5_configuration.txt;
fi
cd $homeDIR

