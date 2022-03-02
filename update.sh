if [[ $1 != "setup" ]]; then
 	echo "polling alphavantage api" $(date -u)
	python src/poll.py
 	tar cvf daily.tar storage/daily/
else
 	echo "setting up storage/daily/ tarball"
	tar xvf daily.tar
fi
