0 */4		* * *		root	/usr/bin/rsnapshot hourly
30 3  	* * *		root	/usr/bin/rsnapshot daily
0  3  	* * 1		root	/usr/bin/rsnapshot weekly
30 2  	1 * *		root	/usr/bin/rsnapshot monthly
