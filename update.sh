if [[ $# -eq 0 ]] ; then
    echo "please enter valid option {setup, push}"
    echo "./update.sh {option}"
    exit 0
fi

if [[ $1 == "setup" ]]; then
        echo "archiving current data"
        tar -cvf previous.tar storage/
	mv previous.tar previous/
	echo "archived files in previous/"
 	echo "polling alphavantage api" $(date -u)
	python src/poll.py
 	tar cvf daily.tar storage/daily/tickers/
 	tar cvf features.tar storage/daily/features/
 	tar cvf cryptocurrencies.tar storage/daily/cryptocurrencies
	split -b 25M daily.tar "daily.tar.part"
	split -b 25M features.tar "features.tar.part"
	rm daily.tar
	rm features.tar
	mv *.tar* gitdata

elif [[ $1 == "push" ]]; then
 	echo "setting up tarballs for storage/daily/*"
	echo "creating daily.tar"
	echo "creating features.tar"
	echo "creating cryptocurrencies.tar"
 	tar cvf daily.tar storage/daily/tickers/
 	tar cvf features.tar storage/daily/features/
 	tar cvf cryptocurrencies.tar storage/daily/cryptocurrencies
	split -b 25M daily.tar "daily.tar.part"
	split -b 25M features.tar "features.tar.part"
	rm daily.tar
	rm features.tar
	mv *.tar* gitdata

else
    echo "please enter valid option {setup, push}"
    echo "./update.sh {option}"
    exit 0
fi
