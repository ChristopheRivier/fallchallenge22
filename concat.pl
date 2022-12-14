use strict;
use warnings;


my $out = './';
my $source = 'src/';

open( my $prog, ">", 'perlCodeGen.py');

open( my $main, "<" , $source.'main.py');

  while ( ! eof($main) ) {
    my $line = readline $main;
	if( $line =~/from ([a-z]*) .*/ and not($line=~/.*#exclude/)){
	print $prog "#--------------------- BEGIN $1\n";

	open( my $tmp, "<", $source.$1.".py");

	while ( ! eof($tmp) ) {
         my $linetmp = readline $tmp;
		 if( $linetmp=~/.* #exclude/){}
		 else{
		 print $prog $linetmp;
		 }
	}
	close $tmp;
	print $prog "#--------------------- END $1\n";
	}else{
	print $prog $line;
	}

}
close $main;
close $prog;
