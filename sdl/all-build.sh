#!/bin/sh

TARGET=${1:-m68k-atari-mint}

fails=
for i in \
	2048 \
	afternoonstalker \
	airball \
	airstrike \
	alienblaster \
	amphetamine \
	batrachians \
	blobwars \
	breaker \
	cavestory \
	ceferino \
	circuslinux \
	deathris \
	digger \
	fanwor \
	fillets-ng \
	freecraft \
	gemdropx \
	gnuboy \
	gnurobbo \
	grafx2 \
	griffon \
	hcl \
	hocoslamfy \
	jetpac \
	kobo-deluxe \
	lbreakout2 \
	lgeneral \
	lmarbles \
	ltris \
	megamario \
	metrocross \
	minislug \
	openjazz \
	opentyrian \
	pegs \
	sdlbomber \
	starfighter \
	stargun \
	symphyla \
	tetris \
	vanilla-conquer \
	xgalaga \
	xpired \
	zelda3t \
	zeldansq \
	zeldaolb_fr \
	zeldaolb_us \
	zeldapicross \
	zeldaroth \
	;
do
	echo "build $i"
	if time ./${i}-build.sh ${TARGET} > /dev/null 2>&1; then 
		echo "ok"
	else
		echo "failed"
		fails="$fails $i"
	fi
	echo "";
done
if test "$fails" != ""; then
	echo "failed:$fails"
else
	echo "all ok"
fi
