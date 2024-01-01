#!/bin/sh
fails=
for i in \
	2048 \
	airball \
	airstrike \
	alienblaster \
	amphetamine \
	blobwars \
	breaker \
	cavestory \
	circuslinux \
	deathris \
	digger \
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
	xgalaga \
	xpired \
	zelda3t \
	zeldansq \
	zeldaolb_fr \
	zeldaolb_us \
	zeldapicross_fr \
	zeldapicross_us \
	zeldaroth_fr \
	zeldaroth_us \
	;
do
	echo "build $i"
	if time ./${i}-build.sh > /dev/null 2>&1; then 
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
