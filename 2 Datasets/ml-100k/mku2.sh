#!/bin/sh

trap `rm -f tmp.$$; exit 1` 1 2 15

for i in 1 2 3 4 5
do
	head -`expr $i \* 20000` u.data | tail -20000 > tmp.$$
	sort -t"	" -k 1,1n -k 2,2n tmp.$$ > u$i.test
	head -`expr \( $i - 1 \) \* 20000` u.data > tmp.$$
	tail -`expr \( 5 - $i \) \* 20000` u.data >> tmp.$$
	sort -t"	" -k 1,1n -k 2,2n tmp.$$ > u$i.base
done

allbut.pl wr 1 10 100000 u.data
sort -t"	" -k 1,1n -k 2,2n wr.base > tmp.$$
mv tmp.$$ wr.base
sort -t"	" -k 1,1n -k 2,2n wr.test > tmp.$$
mv tmp.$$ wr.test
